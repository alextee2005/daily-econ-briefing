"""Pin the stage reporter against the run shapes this pipeline actually hit.

Run: python3 scripts/test_run_report.py

Each case is a real failure we spent a full 18-minute run diagnosing. The
point of the reporter is that the next one costs a glance instead.
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_report import OK, MISSING, PARTIAL, build_stages, load_log  # noqa: E402


def log_file(tmp: Path, calls, result=None):
    entries = [{"type": "system", "subtype": "init"}]
    for name, payload in calls:
        entries.append({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": name, "input": payload}]}})
    entries.append({"type": "result", **(result or {"subtype": "success", "is_error": False})})
    p = tmp / "log.json"
    p.write_text(json.dumps(entries))
    return p


def stages_for(tmp: Path, calls, made):
    """made: which output files exist on disk."""
    build = tmp / "build"
    build.mkdir(exist_ok=True)
    pdf, html, spec = tmp / "out.pdf", build / "briefing.html", tmp / "next-spec.md"
    if "charts" in made:
        (build / "chart1.png").write_bytes(b"\x89PNG")
    if "html" in made:
        html.write_text("<html></html>")
    if "pdf" in made:
        pdf.write_bytes(b"%PDF-1.4" + b"0" * 50_000)
    if "spec" in made:
        spec.write_text("# spec" + "x" * 9000)
    calls_parsed, _, _ = load_log(log_file(tmp, calls))
    return {n: s for n, s, _ in build_stages(calls_parsed, pdf, html, spec, build)}


failures = 0


def expect(label, got, want):
    global failures
    ok = got == want
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        print(f"      want {want}, got {got}")


# The real failure: research spawned in the background, turn ended, nothing built.
with tempfile.TemporaryDirectory() as td:
    s = stages_for(Path(td),
                   [("Read", "spec"), ("Agent", "equities"), ("Agent", "macro"),
                    ("WebSearch", "fomc"), ("ScheduleWakeup", "{}")],
                   made=[])
    expect("backgrounded research: spec read", s["1. Read the standing spec"], OK)
    expect("backgrounded research: research started but produced nothing",
           s["2. Research passes"], PARTIAL)
    expect("backgrounded research: PDF never rendered", s["6. PDF rendered"], MISSING)
    expect("backgrounded research: spec never written", s["8. Next spec written"], MISSING)

# A clean, complete run.
with tempfile.TemporaryDirectory() as td:
    s = stages_for(Path(td),
                   [("Read", "spec"), ("Agent", "equities"), ("WebFetch", "reuters"),
                    ("Bash", "python3 scripts/make_charts.py"),
                    ("Write", "build/briefing.html"),
                    ("Bash", "python3 check_refs.py build/briefing.html"),
                    ("Bash", "node render_pdf.js"), ("Bash", "pdftoppm -png -r 72"),
                    ("Write", "spec/daily-economic-briefing-spec-2026-09-18T0000Z.md")],
                   made=["charts", "html", "pdf", "spec"])
    expect("complete run: every stage ok", set(s.values()), {OK})

# Rendered but the spec rewrite never happened — the exit-code-2 shape.
with tempfile.TemporaryDirectory() as td:
    s = stages_for(Path(td),
                   [("Read", "spec"), ("Agent", "x"), ("Bash", "make_charts"),
                    ("Write", "build/briefing.html"), ("Bash", "render_pdf")],
                   made=["charts", "html", "pdf"])
    expect("spec skipped: PDF ok", s["6. PDF rendered"], OK)
    expect("spec skipped: spec missing", s["8. Next spec written"], MISSING)

# Nothing ran at all — the auth-failure shape.
with tempfile.TemporaryDirectory() as td:
    s = stages_for(Path(td), [], made=[])
    expect("auth failure: nothing reached", set(s.values()), {MISSING})

print(f"\n{failures} failure(s)")
sys.exit(1 if failures else 0)
