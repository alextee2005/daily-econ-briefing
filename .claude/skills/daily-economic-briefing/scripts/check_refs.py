"""Cross-check inline [n] citations against the source annex, both directions.

Eyeballing this stops working past ~30 sources. Two failure modes it catches:
a source cited in the body but missing from the annex (a dangling reference),
and an annex entry never cited inline — usually a source that was genuinely
used but lost its <sup> tag, so add the citation rather than deleting the
entry.

Sources moved from Annex B to Annex C at edition 49. Nothing here needed
changing: entries are found by the `<li>[n]` shape, not by which annex they
sit under. One consequence worth knowing — an Annex A correction written as
"<li>[32] was wrong" would be counted as a source entry. Write such a line as
"<li>Reference [32] was wrong" and it is ignored.

Usage: python3 check_refs.py briefing.html
"""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "briefing.html"
html = open(path, encoding="utf-8").read()

inline = {int(n) for n in re.findall(r'sup class="ref">\[(\d+)\]</sup>', html)}
sources = {int(n) for n in re.findall(r"<li>\[(\d+)\]", html)}

missing = sorted(inline - sources)
unused = sorted(sources - inline)
tildes = html.count("~")

print(f"inline citations: {len(inline)}   source entries: {len(sources)}")
print(f"cited inline but absent from the annex: {missing or 'none'}")
print(f"listed in the annex but never cited:    {unused or 'none'}")
print(f"stray '~' characters (want 0):        {tildes}")

sys.exit(1 if (missing or unused or tildes) else 0)
