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
from run_report import (  # noqa: E402
    OK, MISSING, PARTIAL, build_stages, cost_line, denial_section, error_section, load_log,
)


def log_file(tmp: Path, calls, result=None, results_for=None):
    """results_for: {tool_name: (content, is_error)} replies to emit per call."""
    entries = [{"type": "system", "subtype": "init"}]
    for i, (name, payload) in enumerate(calls):
        tid = f"tu_{i}"
        entries.append({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": tid, "name": name, "input": payload}]}})
        if results_for and name in results_for:
            content, is_err = results_for[name]
            entries.append({"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": tid,
                 "content": content, "is_error": is_err}]}})
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
    run = load_log(log_file(tmp, calls))
    return {n: s for n, s, _ in build_stages(run.calls, pdf, html, spec, build)}


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

# --- denials must name the tool, not just count it ----------------------------
with tempfile.TemporaryDirectory() as td:
    tmp = Path(td)
    run = load_log(log_file(
        tmp,
        [("Read", "spec"), ("NotebookEdit", "x"), ("Bash", "ls")],
        result={"subtype": "success", "is_error": False, "permission_denials_count": 1},
        results_for={"NotebookEdit": ("Claude requested permissions to use "
                                      "NotebookEdit, but you haven't granted it.", True)},
    ))
expect("denial captured", [t for t, _ in run.denials], ["NotebookEdit"])
section = "\n".join(denial_section(run, "Read,Bash,Write"))
expect("denied tool is named in the report", "`NotebookEdit`" in section, True)
expect("report flags it as absent from allowedTools", "**no**" in section, True)

# A denial of a tool that IS declared is a different problem, and must read so.
section2 = "\n".join(denial_section(run, "Read,Bash,NotebookEdit"))
expect("declared-but-denied reads differently", "| yes |" in section2, True)

# Count with no message: say the tool is unidentifiable rather than stay silent.
with tempfile.TemporaryDirectory() as td:
    run2 = load_log(log_file(Path(td), [("Read", "x")],
                             result={"permission_denials_count": 2}))
expect("unexplained denial is still reported",
       "could not be identified" in "\n".join(denial_section(run2, "")), True)

# --- non-permission tool errors are reported separately -----------------------
with tempfile.TemporaryDirectory() as td:
    run3 = load_log(log_file(
        Path(td), [("WebFetch", "https://cboe.example")],
        results_for={"WebFetch": ("HTTP 403 from upstream", True)}))
expect("tool error captured, not misread as a denial",
       (len(run3.denials), [t for t, _ in run3.errors]), (0, ["WebFetch"]))
expect("tool error appears in its own section",
       "`WebFetch`" in "\n".join(error_section(run3)), True)

# --- cost line ----------------------------------------------------------------
line = cost_line({"total_cost_usd": 6.0965125, "duration_ms": 1074067, "num_turns": 33})
expect("cost line shows dollars", "$6.10" in line, True)
expect("cost line shows minutes and turns", ("17.9 min" in line and "33 turns" in line), True)
expect("cost line is honest about tokens", "no token counts" in line, True)
expect("cost line survives an empty result", "no result entry" in cost_line({}), True)

print(f"\n{failures} failure(s)")
sys.exit(1 if failures else 0)
