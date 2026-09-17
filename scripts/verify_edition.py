"""Validate what Claude produced, before any of it is committed.

Exit codes are meaningful — the workflow branches on them:

    0   PDF and spec both good; commit everything.
    2   PDF good, spec update rejected; commit the PDF only and keep the
        previous spec as current. A bad spec would otherwise become the
        instructions for every future run, so a rejected one must not land —
        but that is no reason to withhold a briefing that is fine.
    1   PDF bad; commit nothing.

The spec checks are deliberately structural, not editorial. Claude has free
rein over the spec's content; what it may not do is ship a truncated or
half-written file, or one whose edition log the next run cannot pick up.
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

EXPECTED_PAGES = 4
MIN_PDF_BYTES = 40_000
MIN_SPEC_BYTES = 8_000
MAX_SPEC_BYTES = 120_000
# A rewrite that loses more than this much of the previous spec is treated as a
# truncation rather than a deliberate edit.
MIN_SPEC_RATIO = 0.60

ok, problems = [], []


summary_rows = []


def check(label: str, passed: bool, detail: str = "") -> bool:
    (ok if passed else problems).append(f"{label}{f' — {detail}' if detail else ''}")
    print(f"  {'PASS' if passed else 'FAIL'}  {label}{f' — {detail}' if detail else ''}")
    summary_rows.append((label, passed, detail))
    return passed


def write_summary(verdict: str) -> None:
    """Append the checks to the job summary, beside the stage table."""
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not path:
        return
    lines = ["## Edition verification", "", f"**{verdict}**", "",
             "| check | result | detail |", "|---|---|---|"]
    lines += [f"| {lbl} | {'pass' if ok_ else 'FAIL'} | {det or ''} |"
              for lbl, ok_, det in summary_rows]
    with open(path, "a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def page_count(pdf: Path) -> int | None:
    try:
        out = subprocess.run(
            ["pdfinfo", str(pdf)], capture_output=True, text=True, check=True
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"  WARN  pdfinfo unavailable or failed: {exc}")
        return None
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else None


def verify_pdf(pdf: Path, html: Path, repo: Path) -> bool:
    print(f"\nPDF — {pdf}")
    if not check("file exists", pdf.is_file()):
        return False

    size = pdf.stat().st_size
    good = check("size is plausible", size >= MIN_PDF_BYTES, f"{size:,} bytes")

    pages = page_count(pdf)
    if pages is not None:
        # A 5-page PDF is almost always a stray forced page break, not genuine
        # overflow — see the production notes in the spec.
        good &= check("page count", pages == EXPECTED_PAGES, f"got {pages}, want {EXPECTED_PAGES}")

    if not html.is_file():
        # The prompt asks for build/briefing.html, but a run that put it
        # somewhere reasonable shouldn't lose an otherwise-good briefing.
        for candidate in (repo / "briefing.html", *sorted(repo.glob("**/briefing.html"))):
            if candidate.is_file():
                print(f"  NOTE  using {candidate.relative_to(repo)} for the citation check")
                html = candidate
                break

    if html.is_file():
        script = repo / ".claude/skills/daily-economic-briefing/scripts/check_refs.py"
        r = subprocess.run([sys.executable, str(script), str(html)], capture_output=True, text=True)
        print("    " + r.stdout.strip().replace("\n", "\n    "))
        good &= check("citations and stray tildes", r.returncode == 0)
    else:
        check("briefing.html present for citation check", False, f"{html} missing")
        good = False

    return good


def verify_spec(new: Path, prev: Path, edition_date: str) -> bool:
    print(f"\nSpec — {new}")
    if not check("file exists", new.is_file()):
        return False

    text = new.read_text(encoding="utf-8")
    size = len(text.encode("utf-8"))
    prev_size = len(prev.read_text(encoding="utf-8").encode("utf-8")) if prev.is_file() else 0

    good = check("size within bounds", MIN_SPEC_BYTES <= size <= MAX_SPEC_BYTES, f"{size:,} bytes")

    if prev_size:
        ratio = size / prev_size
        good &= check(
            "not truncated vs previous",
            ratio >= MIN_SPEC_RATIO,
            f"{ratio:.0%} of {prev_size:,} bytes",
        )

    # The edition log is how the next run learns where its window starts and
    # what not to repeat. It is the one piece of structure the pipeline itself
    # depends on, so it is the one piece that is not Claude's to drop.
    good &= check("edition log present", re.search(r"^##\s+Edition log", text, re.M) is not None)

    logged, detail = edition_was_logged(text, prev.read_text(encoding="utf-8") if prev.is_file() else "",
                                        edition_date)
    good &= check("new edition recorded in the log", logged, detail)

    return good


def edition_was_logged(new_text: str, prev_text: str, edition_date: str) -> tuple[bool, str]:
    """Did this run actually append an edition to the log?

    The log numbers its entries and writes dates in prose ("Wed 16 Sept 2026"),
    never ISO — so matching on the ISO edition date never fires. Prefer the
    edition number, which is unambiguous and survives any date style, and fall
    back to recognising the date in the shapes the log actually uses.
    """
    def highest(text):
        # Only bold headings that *begin* with "Edition", so prose references
        # such as "**Open threads for edition 22:**" — which name an edition
        # before it exists — are not mistaken for entries.
        log = text.split("## Edition log", 1)[-1]
        nums = [int(n) for n in re.findall(r"\*\*Editions?\s+(\d{1,4})", log)]
        return max(nums) if nums else None

    before, after = highest(prev_text), highest(new_text)
    if before is not None and after is not None:
        return after > before, f"highest edition {before} -> {after}"

    d = date.fromisoformat(edition_date)
    # The log abbreviates September as "Sept", which %b never produces, so
    # include the four-letter truncation alongside the usual renderings.
    months = {d.strftime("%b"), d.strftime("%B"), d.strftime("%B")[:4]}
    forms = {edition_date}
    for m in months:
        forms |= {f"{d.day} {m} {d.year}", f"{d:%d} {m} {d.year}",
                  f"{m} {d.day}", f"{m} {d.day}, {d.year}"}
    hit = next((f for f in forms if f in new_text), None)
    return bool(hit), f"matched {hit!r}" if hit else "no edition number or recognisable date"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--html", default="build/briefing.html")
    ap.add_argument("--new-spec", required=True)
    ap.add_argument("--prev-spec", required=True)
    ap.add_argument("--edition-date", required=True)
    ap.add_argument("--repo", default=str(REPO))
    args = ap.parse_args()

    repo = Path(args.repo)
    pdf_ok = verify_pdf(repo / args.pdf, repo / args.html, repo)
    spec_ok = verify_spec(repo / args.new_spec, repo / args.prev_spec, args.edition_date)

    print(f"\n{len(ok)} passed, {len(problems)} failed")
    if not pdf_ok:
        write_summary("Briefing rejected — nothing committed.")
        print("::error::Briefing failed verification — committing nothing.")
        return 1
    if not spec_ok:
        write_summary("PDF accepted; spec update rejected — previous spec stays current.")
        print("::warning::Spec update rejected — shipping the PDF and keeping the previous spec.")
        return 2
    write_summary("PDF and spec both accepted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
