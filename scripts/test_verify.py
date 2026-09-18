"""Pin the spec-validation logic. Run: python3 scripts/test_verify.py

The edition-log check shipped broken: it looked for the ISO edition date in a
log that writes dates only in prose ("Wed 16 Sept 2026"). It could never pass,
so every run would have returned exit code 2 and the spec would have stayed
frozen at the seed forever — silently disabling the continuity the whole
pipeline depends on. These cases exist so that cannot recur.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_edition import REQUIRED_SECTIONS, edition_was_logged  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
SEED = sorted((REPO / "spec").glob("daily-economic-briefing-spec-*.md"))[0].read_text()

CASES = [
    # label, new spec text, expected
    ("new entry in the log's own prose style",
     SEED + "\n\n**Edition 22 (most recent — full detail)** — Thu 17 Sept 2026, window Wed 16 Sept.\n",
     True),
    ("new entry written with an ISO date instead",
     SEED + "\n\n**Edition 22** — 2026-09-17, covering 2026-09-16.\n",
     True),
    ("spec carried forward with no new entry",
     SEED,
     False),
    # The seed's own "**Open threads for edition 22:**" line names an edition
    # before it exists; counting prose mentions would read it as an entry.
    ("prose mention of a future edition, no entry",
     SEED + "\n\nStill thinking about edition 22 and edition 23.\n",
     False),
    ("condensed-range heading still parses",
     SEED + "\n\n**Editions 22–24 (condensed):** three quiet sessions.\n",
     True),
]

failures = 0
for label, text, want in CASES:
    got, detail = edition_was_logged(text, SEED, "2026-09-17")
    passed = got == want
    failures += not passed
    print(f"{'PASS' if passed else 'FAIL'}  {label}")
    if not passed:
        print(f"      want {want}, got {got} ({detail})")

# With no log in either file, fall back to recognising the date itself.
got, _ = edition_was_logged("## Edition log\nThu 17 Sept 2026 — first edition.\n", "", "2026-09-17")
failures += not got
print(f"{'PASS' if got else 'FAIL'}  cold start falls back to a prose date match")

# --- the structure check must match sections, not the spec's labels ----------
# A first version matched the literal string "Method note" and reported it
# missing from all nine committed editions, including ones produced before this
# pipeline existed — every edition renders it as a paragraph opening "Method:".
import re  # noqa: E402

REAL_FOOTERS = [
    "Method: every figure traces to a named source in Annex B",
    "Method note: produced by an automated recurring research process",
    "Method:  produced by an automated recurring research/drafting process",
]
pattern = dict(REQUIRED_SECTIONS)["Method note"]
for footer in REAL_FOOTERS:
    hit = re.search(pattern, footer, re.I) is not None
    failures += not hit
    print(f"{'PASS' if hit else 'FAIL'}  method footer recognised: {footer[:46]}...")

# And it must still notice a document that genuinely has no method section.
absent = re.search(pattern, "Annex B — Sources\n[1] AP wire\n[2] Federal Reserve", re.I) is None
failures += not absent
print(f"{'PASS' if absent else 'FAIL'}  a document with no method section is still flagged")

print(f"\n{failures} failure(s)")
sys.exit(1 if failures else 0)
