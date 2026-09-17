"""Cross-check inline [n] citations against Annex B, both directions.

Eyeballing this stops working past ~30 sources. Two failure modes it catches:
a source cited in the body but missing from Annex B (a dangling reference), and
an Annex B entry never cited inline — usually a source that was genuinely used
but lost its <sup> tag, so add the citation rather than deleting the entry.

Usage: python3 check_refs.py briefing.html
"""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "briefing.html"
html = open(path, encoding="utf-8").read()

inline = {int(n) for n in re.findall(r'sup class="ref">\[(\d+)\]</sup>', html)}
annexb = {int(n) for n in re.findall(r"<li>\[(\d+)\]", html)}

missing = sorted(inline - annexb)
unused = sorted(annexb - inline)
tildes = html.count("~")

print(f"inline citations: {len(inline)}   Annex B entries: {len(annexb)}")
print(f"cited inline but absent from Annex B: {missing or 'none'}")
print(f"listed in Annex B but never cited:    {unused or 'none'}")
print(f"stray '~' characters (want 0):        {tildes}")

sys.exit(1 if (missing or unused or tildes) else 0)
