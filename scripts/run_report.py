"""Report which stage of the briefing each run actually reached.

A full run takes ~18 minutes and real subscription quota, so a failure that
only says "no PDF" costs another full run to localise. This reconstructs the
pipeline from two sources of evidence — the files on disk and Claude's own
execution log — and prints a stage table, so one run says where it broke.

Evidence is deliberately of two kinds per stage where possible: an artifact
(did the output appear on disk) and an action (did Claude invoke the thing
that produces it). A stage with the action but not the artifact failed while
running; a stage with neither was never reached.

Usage:
    python3 scripts/run_report.py --pdf P --html H --new-spec S [--log L] [--require-pdf]

Writes the table to stdout and, when set, to $GITHUB_STEP_SUMMARY.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

OK, MISSING, PARTIAL = "ok", "missing", "partial"
MARK = {OK: "ok", MISSING: "MISSING", PARTIAL: "PARTIAL"}


def load_log(path: Path):
    """Tool calls and assistant text from the SDK execution log."""
    if not path or not path.is_file():
        return [], [], {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return [], [], {}
    entries = data if isinstance(data, list) else [data]

    calls, texts, result = [], [], {}
    for e in entries:
        if not isinstance(e, dict):
            continue
        if e.get("type") == "result":
            result = e
        msg = e.get("message")
        blocks = msg.get("content") if isinstance(msg, dict) else None
        for b in blocks or []:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "tool_use":
                calls.append((b.get("name", "?"), json.dumps(b.get("input", ""))[:4000]))
            elif b.get("type") == "text" and b.get("text", "").strip():
                texts.append(b["text"].strip())
    return calls, texts, result


def ran(calls, name=None, pattern=None) -> int:
    """How many tool calls match a tool name and/or a pattern in its input."""
    n = 0
    for tool, payload in calls:
        if name and tool != name:
            continue
        if pattern and not re.search(pattern, payload, re.I):
            continue
        n += 1
    return n


def build_stages(calls, pdf: Path, html: Path, spec: Path, build_dir: Path):
    charts = sorted(build_dir.glob("*.png")) if build_dir.is_dir() else []
    research = ran(calls, "Agent") + ran(calls, "Task")
    searches = ran(calls, "WebSearch") + ran(calls, "WebFetch")

    def verdict(artifact_ok: bool, action_count: int) -> str:
        if artifact_ok:
            return OK
        return PARTIAL if action_count else MISSING

    # Research leaves no artifact of its own, and "subagents were launched" is
    # precisely the evidence that misled us once already — they were killed
    # mid-flight and the run built nothing. So research counts as complete only
    # if the run went on to produce something downstream.
    produced_something = bool(charts) or html.is_file() or pdf.is_file()

    return [
        ("1. Read the standing spec", verdict(True, 1) if ran(calls, "Read") else MISSING,
         f"{ran(calls, 'Read')} Read calls"),
        ("2. Research passes", verdict(research > 0 and produced_something, research),
         f"{research} subagents, {searches} web lookups"),
        ("3. Charts rendered", verdict(bool(charts), ran(calls, pattern=r"make_charts|matplotlib")),
         f"{len(charts)} PNG(s) in build/"),
        ("4. Briefing HTML written", verdict(html.is_file(), ran(calls, pattern=r"briefing\.html")),
         html.name if html.is_file() else "not written"),
        ("5. Citations self-checked", verdict(ran(calls, pattern=r"check_refs") > 0,
                                              ran(calls, pattern=r"check_refs")),
         f"{ran(calls, pattern=r'check_refs')} check_refs runs"),
        ("6. PDF rendered", verdict(pdf.is_file(), ran(calls, pattern=r"render_pdf|chromium")),
         f"{pdf.stat().st_size:,} bytes" if pdf.is_file() else "not produced"),
        ("7. Render self-verified", verdict(ran(calls, pattern=r"pdftoppm|pdfinfo") > 0,
                                            ran(calls, pattern=r"pdftoppm|pdfinfo")),
         f"{ran(calls, pattern=r'pdftoppm|pdfinfo')} page-image checks"),
        ("8. Next spec written", verdict(spec.is_file(), ran(calls, pattern=r"spec/daily-economic")),
         f"{spec.stat().st_size:,} bytes" if spec.is_file() else "not written"),
    ]


def render(stages, result, texts, calls) -> str:
    out = ["| stage | status | detail |", "|---|---|---|"]
    for name, status, detail in stages:
        out.append(f"| {name} | {MARK[status]} | {detail} |")

    if result:
        bits = [f"{k}={result[k]}" for k in
                ("subtype", "is_error", "num_turns", "duration_ms", "permission_denials_count")
                if k in result]
        out += ["", "**Claude's own result:** " + ", ".join(bits)]
        if result.get("result"):
            out += ["", "> " + str(result["result"])[:600].replace("\n", "\n> ")]

    first_bad = next((n for n, s, _ in stages if s is not OK), None)
    if first_bad:
        out += ["", f"**First stage that did not complete: {first_bad}**"]

    if calls:
        seq = " -> ".join(t for t, _ in calls[:40])
        out += ["", "<details><summary>tool calls</summary>", "", "```", seq, "```", "</details>"]
    if texts:
        out += ["", "<details><summary>Claude's last messages</summary>", ""]
        for t in texts[-2:]:
            out += ["```", t[:1000], "```"]
        out += ["</details>"]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--html", default="build/briefing.html")
    ap.add_argument("--new-spec", required=True)
    ap.add_argument("--log", default=os.environ.get("RUNNER_TEMP", "/tmp") + "/claude-execution-output.json")
    ap.add_argument("--repo", default=str(REPO))
    ap.add_argument("--require-pdf", action="store_true",
                    help="exit 1 when the PDF is missing, so the job fails")
    args = ap.parse_args()

    repo = Path(args.repo)
    pdf, html, spec = repo / args.pdf, repo / args.html, repo / args.new_spec
    calls, texts, result = load_log(Path(args.log))
    stages = build_stages(calls, pdf, html, spec, repo / "build")

    report = render(stages, result, texts, calls)
    print(report)
    if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write("## Briefing run stages\n\n" + report + "\n")

    if args.require_pdf and not pdf.is_file():
        print(f"\n::error::No PDF at {args.pdf} — see the stage table above for where it stopped.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
