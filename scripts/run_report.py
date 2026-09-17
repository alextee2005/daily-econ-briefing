"""Report which stage of the briefing each run actually reached.

A full run takes ~18 minutes and real subscription quota, so a failure that
only says "no PDF" costs another full run to localise. This reconstructs the
pipeline from two sources of evidence — the files on disk and Claude's own
execution log — and prints a stage table, so one run says where it broke.

Evidence is deliberately of two kinds per stage where possible: an artifact
(did the output appear on disk) and an action (did Claude invoke the thing
that produces it). A stage with the action but not the artifact failed while
running; a stage with neither was never reached.

It also reports what the run cost, and — where the raw log allows — which
tools were denied or errored. `permission_denials_count: 1` on its own says
something was blocked without saying what, which is not enough to act on.

Usage:
    python3 scripts/run_report.py --pdf P --html H --new-spec S [--log L]
                                  [--allowed-tools "A,B,C"] [--require-pdf]

Writes the table to stdout and, when set, to $GITHUB_STEP_SUMMARY.
"""

import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import NamedTuple

REPO = Path(__file__).resolve().parent.parent

OK, MISSING, PARTIAL = "ok", "missing", "partial"
MARK = {OK: "ok", MISSING: "MISSING", PARTIAL: "PARTIAL"}

# A denied tool call comes back as an error result whose text says so. The
# wording varies by version, so match the shapes rather than one exact string.
DENIAL_RE = re.compile(
    r"permission|denied|not allowed|haven't granted|has not granted|"
    r"requested permissions|blocked by|not permitted",
    re.I,
)


class Run(NamedTuple):
    calls: list          # (tool_name, serialised_input)
    texts: list          # assistant text blocks
    result: dict         # the SDK result entry
    denials: list        # (tool_name, reason)
    errors: list         # (tool_name, message) for non-denial tool errors


def load_log(path: Path) -> Run:
    """Tool calls, assistant text, denials and tool errors from the SDK log."""
    if not path or not path.is_file():
        return Run([], [], {}, [], [])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return Run([], [], {}, [], [])
    entries = data if isinstance(data, list) else [data]

    calls, texts, result, denials, errors = [], [], {}, [], []
    by_id = {}  # tool_use_id -> tool name, so a result can name its tool

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
            kind = b.get("type")
            if kind == "tool_use":
                name = b.get("name", "?")
                calls.append((name, json.dumps(b.get("input", ""))[:4000]))
                if b.get("id"):
                    by_id[b["id"]] = name
            elif kind == "text" and b.get("text", "").strip():
                texts.append(b["text"].strip())
            elif kind == "tool_result":
                content = b.get("content")
                if isinstance(content, list):
                    content = " ".join(
                        c.get("text", "") for c in content if isinstance(c, dict)
                    )
                content = str(content or "")
                tool = by_id.get(b.get("tool_use_id"), "?")
                if DENIAL_RE.search(content):
                    denials.append((tool, content.strip()[:300]))
                elif b.get("is_error"):
                    errors.append((tool, content.strip()[:300]))

    return Run(calls, texts, result, denials, errors)


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


def cost_line(result: dict) -> str:
    """One line of what the run spent. Token counts are not in the log."""
    if not result:
        return "**Cost:** no result entry in the execution log."
    bits = []
    if (c := result.get("total_cost_usd")) is not None:
        bits.append(f"**${c:.2f}**")
    if (d := result.get("duration_ms")) is not None:
        bits.append(f"{d / 60000:.1f} min")
    if (t := result.get("num_turns")) is not None:
        bits.append(f"{t} turns")
    # The SDK's modelUsage carries context limits, not consumption, so there is
    # no token count to report. Say so rather than leaving it looking omitted.
    return ("**Cost:** " + ", ".join(bits) +
            " — the log records cost but no token counts.")


def denial_section(run: Run, allowed: str) -> list:
    """Name what was denied. The count alone is not actionable."""
    declared = {t.strip() for t in (allowed or "").split(",") if t.strip()}
    stated = run.result.get("permission_denials_count")
    out = []

    if not run.denials:
        if stated:
            out += ["", f"**Permission denials: {stated}**, but the execution log "
                        "records no denial message — the tool could not be identified."]
        return out

    counts = Counter(tool for tool, _ in run.denials)
    out += ["", f"**Permission denials: {stated if stated is not None else len(run.denials)}**",
            "", "| tool | times | in --allowedTools | first reason |", "|---|---|---|---|"]
    for tool, n in counts.most_common():
        reason = next(r for t, r in run.denials if t == tool)
        listed = "yes" if tool in declared else ("**no**" if declared else "?")
        out.append(f"| `{tool}` | {n} | {listed} | {reason[:160]} |")
    if declared and any(t not in declared for t in counts):
        out += ["", "A tool denied and absent from `--allowedTools` is a workflow "
                    "fix: add it there. A denied tool that *is* listed is a "
                    "different problem — check the settings the action applies."]
    return out


def error_section(run: Run) -> list:
    if not run.errors:
        return []
    counts = Counter(tool for tool, _ in run.errors)
    out = ["", f"**Tool errors (not permission-related): {len(run.errors)}**",
           "", "| tool | times | first message |", "|---|---|---|"]
    for tool, n in counts.most_common(8):
        msg = next(m for t, m in run.errors if t == tool)
        out.append(f"| `{tool}` | {n} | {msg[:160]} |")
    return out


def render(stages, run: Run, allowed: str = "") -> str:
    out = ["| stage | status | detail |", "|---|---|---|"]
    for name, status, detail in stages:
        out.append(f"| {name} | {MARK[status]} | {detail} |")

    out += ["", cost_line(run.result)]

    if run.result:
        bits = [f"{k}={run.result[k]}" for k in
                ("subtype", "is_error", "num_turns", "permission_denials_count")
                if k in run.result]
        out += ["", "**Result:** " + ", ".join(bits)]
        if run.result.get("result"):
            out += ["", "> " + str(run.result["result"])[:600].replace("\n", "\n> ")]

    first_bad = next((n for n, s, _ in stages if s is not OK), None)
    if first_bad:
        out += ["", f"**First stage that did not complete: {first_bad}**"]

    out += denial_section(run, allowed)
    out += error_section(run)

    if run.calls:
        seq = " -> ".join(t for t, _ in run.calls[:40])
        out += ["", "<details><summary>tool calls</summary>", "", "```", seq, "```", "</details>"]
    if run.texts:
        out += ["", "<details><summary>Claude's last messages</summary>", ""]
        for t in run.texts[-2:]:
            out += ["```", t[:1000], "```"]
        out += ["</details>"]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--html", default="build/briefing.html")
    ap.add_argument("--new-spec", required=True)
    ap.add_argument("--log", default=os.environ.get("RUNNER_TEMP", "/tmp") + "/claude-execution-output.json")
    ap.add_argument("--allowed-tools", default="",
                    help="the --allowedTools list, to say whether a denied tool was declared")
    ap.add_argument("--repo", default=str(REPO))
    ap.add_argument("--require-pdf", action="store_true",
                    help="exit 1 when the PDF is missing, so the job fails")
    args = ap.parse_args()

    repo = Path(args.repo)
    pdf, html, spec = repo / args.pdf, repo / args.html, repo / args.new_spec
    run = load_log(Path(args.log))
    stages = build_stages(run.calls, pdf, html, spec, repo / "build")

    report = render(stages, run, args.allowed_tools)
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
