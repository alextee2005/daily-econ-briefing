"""Decide whether today's briefing should run, and compute its window.

The workflow fires two cron entries every weekday (00:00 and 01:00 UTC) so that
one of them always lands at 20:00 America/New_York — roughly four hours after
the US close — on both sides of the US daylight-saving switch. This script is
what lets exactly one of them through.

Three independent reasons to skip:

  too-early    the ET clock says we are less than four hours past the close.
               In winter the 00:00 UTC fire is 19:00 EST and must not run; the
               01:00 UTC fire is 20:00 EST and must.
  already-run  an edition for this UTC date is already committed. This is what
               stops the second cron entry duplicating the first, and makes a
               manual re-run idempotent.
  no-session   no NYSE session has closed since the previous edition's cutoff
               (the morning after a market holiday). Note this is deliberately
               *not* "was yesterday a trading day" — a Monday run sits at 20:00
               ET Sunday and must still produce the Friday-plus-weekend edition.

Usage:
    python3 scripts/gate.py [--now ISO8601] [--force] [--edition-date DATE]

Writes `key=value` lines to stdout and, when set, to $GITHUB_OUTPUT.
"""

import argparse
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
REPO = Path(__file__).resolve().parent.parent

# Hours past midnight ET at which a run is considered late enough to cover the
# session that just closed. 16:00 close + 4h = 20:00.
CUTOFF_HOUR_ET = 20

EDITION_RE = re.compile(r"^Daily_Economic_Briefing_(\d{4}-\d{2}-\d{2}|\d{8})(?:_.*)?\.pdf$")
SPEC_RE = re.compile(r"^daily-economic-briefing-spec-(\d{4}-\d{2}-\d{2}T\d{4}Z)\.md$")


def nyse_sessions(start: date, end: date) -> list[date]:
    """NYSE trading sessions in [start, end], inclusive.

    Imported lazily and allowed to raise: a run that cannot determine the real
    market calendar must fail loudly rather than guess at holidays.
    """
    if end < start:
        return []
    import pandas_market_calendars as mcal

    sched = mcal.get_calendar("NYSE").schedule(
        start_date=start.isoformat(), end_date=end.isoformat()
    )
    return [d.date() for d in sched.index]


def latest_edition_date(repo: Path) -> date | None:
    """Date of the most recent committed edition, across both naming eras."""
    found = []
    for pdf in (repo / "editions").glob("*.pdf"):
        m = EDITION_RE.match(pdf.name)
        if not m:
            continue
        raw = m.group(1)
        fmt = "%Y-%m-%d" if "-" in raw else "%Y%m%d"
        found.append(datetime.strptime(raw, fmt).date())
    return max(found) if found else None


def latest_spec(repo: Path) -> Path:
    """Newest spec by its embedded timestamp.

    Matching strictly on the timestamp pattern means a stray or hand-renamed
    file in spec/ cannot silently become the instructions for the next run.
    """
    specs = []
    for p in (repo / "spec").glob("*.md"):
        m = SPEC_RE.match(p.name)
        if m:
            specs.append((m.group(1), p))
    if not specs:
        raise SystemExit(
            "no spec matching daily-economic-briefing-spec-<ISO>.md found in spec/"
        )
    return max(specs)[1]


def decide(now_utc: datetime, repo: Path, force: bool, edition_date: date | None):
    now_et = now_utc.astimezone(ET)
    ed_date = edition_date or now_utc.date()
    prev_ed = latest_edition_date(repo)

    def skip(reason):
        return {"should_run": "false", "skip_reason": reason, "edition_date": ed_date.isoformat()}

    if not force:
        if now_et.hour < CUTOFF_HOUR_ET:
            return skip(f"too early — {now_et:%H:%M} ET is before the {CUTOFF_HOUR_ET}:00 ET cutoff")
        if prev_ed == ed_date:
            return skip(f"edition {ed_date} already published")

    # The window ends with the session that has actually closed. On the normal
    # schedule now_et.hour is always >= 20, so this is today and the branch is a
    # no-op — but --force can land at any hour, and a window running to
    # now_et.date() at 00:30 ET would include a session that has not yet opened.
    window_end = (
        now_et.date() if now_et.hour >= CUTOFF_HOUR_ET else now_et.date() - timedelta(days=1)
    )

    # The previous edition covered the session(s) up to 20:00 ET on the day
    # before its own date, so that is where this window starts.
    prev_cutoff = (prev_ed - timedelta(days=1)) if prev_ed else (window_end - timedelta(days=1))
    covered = nyse_sessions(prev_cutoff + timedelta(days=1), window_end)

    if not covered and not force:
        return skip(f"no NYSE session has closed since {prev_cutoff}")

    spec = latest_spec(repo)
    next_spec = repo / "spec" / f"daily-economic-briefing-spec-{now_utc:%Y-%m-%dT%H%M}Z.md"
    if next_spec.name <= spec.name:
        # Only reachable if the clock moved backwards or a spec was stamped in
        # the future; nudge forward so ordering — and therefore resolution of
        # "latest" — stays monotonic.
        next_spec = repo / "spec" / f"daily-economic-briefing-spec-{now_utc + timedelta(minutes=1):%Y-%m-%dT%H%M}Z.md"

    return {
        "should_run": "true",
        "skip_reason": "",
        "edition_date": ed_date.isoformat(),
        # Report the real cutoff on a normal run; on a forced off-hours run,
        # report the close of the last session in the window, so the stated
        # cutoff never sits after data the run is not supposed to have.
        "cutoff_et": (
            now_et.strftime("%Y-%m-%d %H:%M ET")
            if now_et.hour >= CUTOFF_HOUR_ET
            else f"{window_end} {CUTOFF_HOUR_ET}:00 ET"
        ),
        "window_start_et": f"{prev_cutoff} 20:00 ET",
        "sessions_covered": ",".join(d.isoformat() for d in covered) or "none",
        "prev_edition_date": prev_ed.isoformat() if prev_ed else "none",
        "spec_path": str(spec.relative_to(repo)),
        "next_spec_path": str(next_spec.relative_to(repo)),
        "pdf_path": f"editions/Daily_Economic_Briefing_{ed_date}.pdf",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--now", help="ISO-8601 UTC instant; defaults to the real clock")
    ap.add_argument("--force", action="store_true", help="bypass all three skip checks")
    ap.add_argument("--edition-date", help="override the edition date (YYYY-MM-DD)")
    ap.add_argument("--repo", default=str(REPO))
    args = ap.parse_args()

    now = (
        datetime.fromisoformat(args.now.replace("Z", "+00:00")).astimezone(timezone.utc)
        if args.now
        else datetime.now(timezone.utc)
    )
    ed = date.fromisoformat(args.edition_date) if args.edition_date else None

    out = decide(now, Path(args.repo), args.force, ed)

    lines = [f"{k}={v}" for k, v in out.items()]
    print("\n".join(lines))
    if gh := os.environ.get("GITHUB_OUTPUT"):
        with open(gh, "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

    if out["should_run"] == "true":
        print(f"\n::notice::Generating edition {out['edition_date']} "
              f"covering {out['sessions_covered']} (cutoff {out['cutoff_et']})", file=sys.stderr)
    else:
        print(f"\n::notice::Skipping: {out['skip_reason']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
