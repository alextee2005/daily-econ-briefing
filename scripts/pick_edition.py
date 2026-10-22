"""Choose which edition PDF a delivery run should send.

On 22 October 2026 every subscriber was sent the **7 September** edition.
Three independent defects had to line up for that, and two of them were here:

1. `deliver.yml`'s push trigger was not restricted to `main`, so a push to a
   feature branch that happened to carry main's edition commits matched the
   `editions/**.pdf` path filter and started a delivery. (Fixed in the
   workflow, not here.)
2. The selection fell back to `ls editions/*.pdf | sort | tail -1` with the
   comment "filenames are ISO-dated, so sort works". They are not all
   ISO-dated: 16 early files are `..._20260907.pdf` and the rest are
   `..._2026-10-22.pdf`. In ASCII `-` (0x2D) sorts below every digit, so
   *every* dashed name sorts before *every* compact one and `tail -1` returns
   the newest file of the older naming convention — 7 September, forever.
3. Nothing checked that the chosen file was plausibly current, so a
   forty-five-day-old edition went out without a murmur.

So: parse the date out of the name rather than trusting a byte sort, and
refuse to send a stale edition unless a human named the file explicitly.
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Both conventions this repository has used. Kept as one regex with optional
# separators rather than two patterns, so a third variant (underscores, say)
# is one character away instead of a new branch.
STEM_RE = re.compile(r"(\d{4})-?(\d{2})-?(\d{2})$")

# How old an automatically-chosen edition may be before the run refuses it.
# Four days clears a Friday edition picked up on the following Tuesday after a
# Monday holiday, which is the longest legitimate gap the schedule produces.
# An explicitly named file bypasses this entirely — that is a person choosing.
MAX_AGE_DAYS = 4


class NoEdition(Exception):
    """No file could be chosen, with a reason fit for a workflow log."""


def edition_date(path) -> date | None:
    """The date in an edition's filename, or None if it carries no usable one."""
    m = STEM_RE.search(Path(path).stem)
    if not m:
        return None
    try:
        return date(*(int(g) for g in m.groups()))
    except ValueError:
        return None  # e.g. a 13th month — a typo, not an edition


def newest(paths) -> str | None:
    """The latest edition by its parsed date, ignoring files without one.

    Never by filename sort. That is the bug this module exists for.
    """
    dated = [(d, p) for p in paths if (d := edition_date(p)) is not None]
    if not dated:
        return None
    # max() on the pair breaks a same-date tie by name, deterministically.
    return max(dated, key=lambda dp: (dp[0], str(dp[1])))[1]


def pick(manual: str, changed: str, available, today: date) -> tuple[str, str]:
    """Return (path, how_it_was_chosen), or raise NoEdition.

    Precedence: an explicitly named file, then a PDF this push actually added,
    then the newest available. Only the last of those is second-guessed on
    age — the first two are evidence about *this* run, not a guess.
    """
    if manual:
        return manual, "named explicitly on the workflow run"

    if changed:
        return changed, "added or modified by this push"

    chosen = newest(available)
    if chosen is None:
        raise NoEdition("No edition PDF found with a date in its filename.")

    age = (today - edition_date(chosen)).days
    if age > MAX_AGE_DAYS:
        raise NoEdition(
            f"The newest edition on disk is {edition_date(chosen)}, {age} days "
            f"old, and nothing in this push added a PDF. Refusing to send it: "
            f"an automatic run sending a {age}-day-old briefing is the 22 "
            f"October 2026 misdelivery. Use the 'file' input to send it "
            f"deliberately."
        )
    return chosen, f"newest on disk ({edition_date(chosen)}, {age} day(s) old)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manual", default="")
    ap.add_argument("--changed", default="")
    ap.add_argument("--today", default="")
    args = ap.parse_args()

    today = date.fromisoformat(args.today) if args.today else date.today()
    # Repo-relative, because the path is echoed into $GITHUB_OUTPUT and used
    # verbatim by later steps and in the delivery caption.
    available = sorted(
        str(p.relative_to(REPO)) for p in (REPO / "editions").glob("*.pdf")
    )

    try:
        chosen, why = pick(args.manual.strip(), args.changed.strip(), available, today)
    except NoEdition as exc:
        print(f"::error::{exc}", file=sys.stderr)
        return 1

    if not (REPO / chosen).is_file():
        print(f"::error::{chosen} was selected but does not exist.", file=sys.stderr)
        return 1

    print(f"pdf={chosen}")
    print(f"why={why}")
    print(f"edition_date={edition_date(chosen) or 'unknown'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
