"""Pin the gate's schedule logic. Run: python3 scripts/test_gate.py

These cases are the reason the retry-cron arrangement is safe. Anyone changing
gate.py should be able to break exactly one of them at a time and see why.
"""

import re
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gate import decide  # noqa: E402


def fake_repo(tmp: Path, editions: list[str], specs: list[str]) -> Path:
    (tmp / "editions").mkdir(parents=True, exist_ok=True)
    (tmp / "spec").mkdir(parents=True, exist_ok=True)
    for d in editions:
        (tmp / "editions" / f"Daily_Economic_Briefing_{d}.pdf").write_bytes(b"%PDF-1.4\n")
    for s in specs:
        (tmp / "spec" / f"daily-economic-briefing-spec-{s}.md").write_text("# spec\n")
    return tmp


SPEC = ["2026-09-17T0000Z"]
CASES = [
    # label, UTC instant, committed editions, expect should_run, expect substring
    ("EDT 00:00Z — first cron runs",
     "2026-09-22T00:00", ["2026-09-18"], True, "2026-09-21"),
    ("EDT 01:00Z — second cron self-skips",
     "2026-09-22T01:00", ["2026-09-18", "2026-09-22"], False, "already published"),
    ("Monday covers Friday plus the weekend",
     "2026-09-21T00:00", ["2026-09-18"], True, "2026-09-18"),
    ("EST 00:00Z — 19:00 ET is too early",
     "2026-12-02T00:00", ["2026-12-01"], False, "too early"),
    ("EST 01:00Z — 20:00 ET runs",
     "2026-12-02T01:00", ["2026-12-01"], True, "2026-12-01"),
    ("morning after Thanksgiving — no session to cover",
     "2026-11-27T01:00", ["2026-11-26"], False, "no NYSE session"),
    ("Monday after Thanksgiving — covers the half-day",
     "2026-11-30T01:00", ["2026-11-26"], True, "2026-11-27"),
    ("a delayed cron still runs",
     "2026-09-22T01:12", ["2026-09-18"], True, "2026-09-21"),
    ("multi-day gap widens the window",
     "2026-09-22T00:00", ["2026-09-16"], True, "2026-09-16,2026-09-17,2026-09-18,2026-09-21"),
    ("cold start with no prior edition",
     "2026-09-18T00:00", [], True, "2026-09-17"),
    ("legacy YYYYMMDD filenames still parse",
     "2026-09-09T00:00", ["20260908"], True, "2026-09-08"),
    # The crons fire at :17, not :00 — the top of the hour is contended and the
    # first scheduled run came 2h43m late from "0 0 * * 1-5". These pin the
    # times actually in the workflow.
    ("EDT 00:17Z — the real first cron runs",
     "2026-09-22T00:17", ["2026-09-18"], True, "2026-09-21"),
    ("EST 00:17Z — 19:17 ET is still too early",
     "2026-12-02T00:17", ["2026-12-01"], False, "too early"),
    ("EST 01:17Z — 20:17 ET runs",
     "2026-12-02T01:17", ["2026-12-01"], True, "2026-12-01"),
    # A badly delayed fire still has to produce the right edition: this is the
    # 2h43m delay that actually happened, reproduced.
    ("a 2h43m delayed fire still runs and covers the right session",
     "2026-09-18T02:43", ["2026-09-17"], True, "2026-09-17"),
]

failures = 0
for label, now, editions, want_run, want_sub in CASES:
    with tempfile.TemporaryDirectory() as td:
        repo = fake_repo(Path(td), editions, SPEC)
        got = decide(
            datetime.fromisoformat(now).replace(tzinfo=timezone.utc), repo, False, None
        )
    ran = got["should_run"] == "true"
    haystack = got.get("sessions_covered", "") + " " + got.get("skip_reason", "")
    passed = ran == want_run and want_sub in haystack
    failures += not passed
    print(f"{'PASS' if passed else 'FAIL'}  {label}")
    if not passed:
        print(f"      want run={want_run} containing {want_sub!r}")
        print(f"      got  run={ran} from {haystack.strip()!r}")

# A forced run at an arbitrary hour must not claim a session that has not closed.
# 04:36Z on Thu 17 Sept is 00:36 ET Thursday: the window ends Wednesday.
with tempfile.TemporaryDirectory() as td:
    repo = fake_repo(Path(td), ["2026-09-16"], SPEC)
    odd = decide(
        datetime.fromisoformat("2026-09-17T04:36").replace(tzinfo=timezone.utc), repo, True, None
    )
passed = odd["sessions_covered"] == "2026-09-16" and odd["cutoff_et"] == "2026-09-16 20:00 ET"
failures += not passed
print(f"{'PASS' if passed else 'FAIL'}  forced off-hours run stops at the last closed session "
      f"(covers {odd['sessions_covered']}, cutoff {odd['cutoff_et']})")

# --force must override every skip reason, so a manual re-run is always possible.
with tempfile.TemporaryDirectory() as td:
    repo = fake_repo(Path(td), ["2026-11-26"], SPEC)
    forced = decide(
        datetime.fromisoformat("2026-11-27T01:00").replace(tzinfo=timezone.utc), repo, True, None
    )
passed = forced["should_run"] == "true"
failures += not passed
print(f"{'PASS' if passed else 'FAIL'}  --force overrides a skip")

# The next spec filename must sort after the current one, or "latest" breaks.
with tempfile.TemporaryDirectory() as td:
    repo = fake_repo(Path(td), ["2026-09-18"], SPEC)
    out = decide(
        datetime.fromisoformat("2026-09-22T00:00").replace(tzinfo=timezone.utc), repo, False, None
    )
passed = Path(out["next_spec_path"]).name > Path(out["spec_path"]).name
failures += not passed
print(f"{'PASS' if passed else 'FAIL'}  next spec sorts after current "
      f"({Path(out['spec_path']).name} -> {Path(out['next_spec_path']).name})")

# --- the retry slots, read from the workflow itself ---------------------------
# The crons are retries: GitHub drops scheduled events, so the morning needs
# more than one chance. What makes that safe is that the gate lets exactly one
# fire through and stops the rest on "already published" — so these cases
# assert both halves, against the cron list actually in briefing.yml rather
# than a copy that can drift out of step with it.
#
# The winter count is the one that matters. Two entries looked like redundancy
# but gave only ONE usable fire in EST, because 00:17 UTC is 19:17 there and
# always too early: half the year had no second chance at all.
WORKFLOW = Path(__file__).resolve().parent.parent / ".github/workflows/briefing.yml"
slots = sorted(
    (int(h), int(m))
    for m, h in re.findall(r'^\s*- cron:\s*"(\d+)\s+(\d+) \* \* 1-5"', WORKFLOW.read_text(), re.M)
)

MIN_CHANCES = 4
for label, fire_day, prior in [
    ("EDT", date(2026, 7, 14), "2026-07-13"),
    ("EST", date(2026, 12, 15), "2026-12-14"),
]:
    with tempfile.TemporaryDirectory() as td:
        repo = fake_repo(Path(td), [prior], SPEC)
        ran, early, published = [], [], []
        for hour, minute in slots:
            now = datetime(fire_day.year, fire_day.month, fire_day.day, hour, minute,
                           tzinfo=timezone.utc)
            got = decide(now, repo, False, None)
            if got["should_run"] == "true":
                ran.append(hour)
                # Stand in for the run committing its edition, so the fires
                # that follow see what they would really see.
                (repo / "editions" /
                 f"Daily_Economic_Briefing_{got['edition_date']}.pdf").write_bytes(b"%PDF-1.4\n")
            elif "too early" in got["skip_reason"]:
                early.append(hour)
            else:
                published.append(hour)

    chances = len(slots) - len(early)
    for desc, passed in [
        (f"{label}: exactly one fire produces the edition (at {ran[0]:02d}:{slots[0][1]:02d}Z)"
         if ran else f"{label}: exactly one fire produces the edition",
         len(ran) == 1),
        (f"{label}: every later fire stops on 'already published' "
         f"({len(published)} of them)", len(published) == chances - 1),
        (f"{label}: at least {MIN_CHANCES} usable chances (got {chances})",
         chances >= MIN_CHANCES),
    ]:
        failures += not passed
        print(f"{'PASS' if passed else 'FAIL'}  {desc}")

print(f"\n{failures} failure(s)")
sys.exit(1 if failures else 0)
