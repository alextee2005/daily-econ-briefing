"""Pin edition selection. Run: python3 scripts/test_pick_edition.py

The case that matters most is the first one: a byte sort over this
repository's two filename conventions returns the 7 September 2026 edition
and keeps returning it forever, which is what every subscriber received on
22 October.
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pick_edition import NoEdition, edition_date, newest, pick  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
failures = 0


def check(label, passed, detail=""):
    global failures
    failures += not passed
    print(f"{'PASS' if passed else 'FAIL'}  {label}{f' — {detail}' if detail else ''}")


# --- the actual misdelivery, reproduced from the real filenames -------------
REAL = sorted(str(p.relative_to(REPO)) for p in (REPO / "editions").glob("*.pdf"))
check("the repository really does mix both naming conventions",
      any("-" in Path(p).stem.split("_")[-1] for p in REAL)
      and any("-" not in Path(p).stem.split("_")[-1] for p in REAL))

byte_sorted = sorted(REAL)[-1]
check("a byte sort still picks the old-convention file (the bug)",
      "20260907" in byte_sorted, Path(byte_sorted).name)
check("newest() picks the genuinely latest edition instead",
      edition_date(newest(REAL)) == max(d for p in REAL if (d := edition_date(p))),
      Path(newest(REAL)).name)

# --- date parsing across both conventions -----------------------------------
PARSE = [
    ("editions/Daily_Economic_Briefing_20260907.pdf", date(2026, 9, 7)),
    ("editions/Daily_Economic_Briefing_2026-10-22.pdf", date(2026, 10, 22)),
    ("editions/Daily_Economic_Briefing_2026-01-02.pdf", date(2026, 1, 2)),
    ("editions/no_date_at_all.pdf", None),
    ("editions/Daily_Economic_Briefing_2026-13-01.pdf", None),  # 13th month
]
for name, want in PARSE:
    check(f"parse {Path(name).name}", edition_date(name) == want, str(edition_date(name)))

# A file with no parsable date must never be chosen, not even as a last resort.
check("undated files are ignored by newest()",
      newest(["editions/garbage.pdf", "editions/x_2026-10-20.pdf"])
      == "editions/x_2026-10-20.pdf")
check("newest() of nothing usable is None", newest(["editions/garbage.pdf"]) is None)

# --- precedence --------------------------------------------------------------
AVAIL = ["editions/b_20260907.pdf", "editions/a_2026-10-22.pdf"]
TODAY = date(2026, 10, 22)

got, why = pick("editions/chosen.pdf", "editions/pushed.pdf", AVAIL, TODAY)
check("an explicitly named file wins over everything", got == "editions/chosen.pdf", why)

got, why = pick("", "editions/pushed.pdf", AVAIL, TODAY)
check("a PDF added by the push wins over the newest on disk",
      got == "editions/pushed.pdf", why)

got, why = pick("", "", AVAIL, TODAY)
check("with neither, the newest by date is used", got == "editions/a_2026-10-22.pdf", why)

# --- the staleness guard -----------------------------------------------------
# This is the backstop: even if selection goes wrong again in some way nobody
# has thought of yet, a month-old edition does not reach a subscriber.
try:
    pick("", "", ["editions/x_20260907.pdf"], TODAY)
    check("a 45-day-old edition is refused", False, "it was sent")
except NoEdition as exc:
    check("a 45-day-old edition is refused", "45 days old" in str(exc))

try:
    got, _ = pick("", "", ["editions/x_2026-10-16.pdf"], TODAY)  # Fri -> Thu, 6 days
    check("a 6-day-old edition is refused too", False, got)
except NoEdition:
    check("a 6-day-old edition is refused too", True)

got, why = pick("", "", ["editions/x_2026-10-19.pdf"], TODAY)  # a long weekend
check("a 3-day gap (holiday weekend) still delivers", got == "editions/x_2026-10-19.pdf", why)

# A person naming the file is never second-guessed on age — that is the
# documented way to re-send an old edition on purpose.
got, _ = pick("editions/x_20260907.pdf", "", ["editions/x_20260907.pdf"], TODAY)
check("naming an old file explicitly bypasses the age guard",
      got == "editions/x_20260907.pdf")

# Likewise a push that genuinely added an old-looking file: that is evidence
# about this run rather than a guess, so it is honoured.
got, _ = pick("", "editions/x_20260907.pdf", AVAIL, TODAY)
check("a pushed file is honoured regardless of its date", got == "editions/x_20260907.pdf")

try:
    pick("", "", [], TODAY)
    check("no editions at all is an error, not a silent skip", False)
except NoEdition:
    check("no editions at all is an error, not a silent skip", True)

print(f"\n{failures} failure(s)")
sys.exit(1 if failures else 0)
