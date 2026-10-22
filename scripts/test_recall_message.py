"""Pin the recall walk. Run: python3 scripts/test_recall_message.py

This script deletes messages out of other people's chats, so the cases that
matter most are the ones about what it must NOT touch: a subscriber's own
message, a legitimate briefing, anything once the walk has seen a document
that is not the target.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from recall_message import mask, recall_from_chat, summarise  # noqa: E402

failures = 0


def check(label, passed, detail=""):
    global failures
    failures += not passed
    print(f"{'PASS' if passed else 'FAIL'}  {label}{f' — {detail}' if detail else ''}")


BAD = "Daily_Economic_Briefing_20260907.pdf"
GOOD = "Daily_Economic_Briefing_2026-10-22.pdf"


class Telegram:
    """A chat as Telegram would answer for it.

    `messages` maps message_id -> None for a message the bot did not send (a
    subscriber's own), or a file name for a document the bot sent.
    """

    def __init__(self, messages, next_id=None, edit_fails=()):
        self.messages = dict(messages)
        self.next_id = next_id or (max(messages) + 1 if messages else 1)
        self.edit_fails = set(edit_fails)
        self.calls = []

    def __call__(self, method, payload):
        self.calls.append((method, payload))
        mid = payload.get("message_id")
        if method == "sendMessage":
            sent = self.next_id
            self.next_id += 1
            self.messages[sent] = None  # a text message of ours
            return {"ok": True, "result": {"message_id": sent}}
        if method == "editMessageCaption":
            if mid in self.edit_fails or self.messages.get(mid) is None:
                # Not ours, or ours but with no caption to edit.
                return {"ok": False, "description": "message to edit not found"}
            return {"ok": True, "result": {
                "message_id": mid,
                "document": {"file_name": self.messages[mid]},
                "caption": payload["caption"],
            }}
        if method == "deleteMessage":
            if mid not in self.messages:
                return {"ok": False, "description": "message to delete not found"}
            del self.messages[mid]
            return {"ok": True, "result": True}
        raise AssertionError(f"unexpected method {method}")


def run(messages, **kw):
    tg = Telegram(messages)
    rep = recall_from_chat(tg, 111, BAD, "notice", **kw)
    return tg, rep


# --- the happy path ---------------------------------------------------------
tg, rep = run({10: GOOD, 11: None, 12: BAD})
check("the bad briefing is deleted", rep["deleted"] and 12 not in tg.messages)
check("the legitimate briefing survives", tg.messages.get(10) == GOOD)
check("the report names what it found", rep["found"]["file_name"] == BAD)

# --- a subscriber's own messages are never touched --------------------------
tg, rep = run({10: BAD, 11: None, 12: None, 13: None})
check("walks over the subscriber's own messages to reach the target",
      rep["deleted"] and 10 not in tg.messages)
deleted = [p["message_id"] for m, p in tg.calls if m == "deleteMessage"]
check("only ever asked to delete the one id", deleted == [10], str(deleted))

# --- the refusal that matters ----------------------------------------------
# If the most recent document is NOT the target, the operator's assumption is
# wrong. Stop. Do not keep walking back into older, legitimate editions.
tg, rep = run({10: BAD, 11: GOOD})
check("stops when the newest document is not the target", not rep["deleted"])
check("and the target is left alone rather than hunted for", tg.messages.get(10) == BAD)
check("and the legitimate briefing is still there", tg.messages.get(11) == GOOD)
check("and the caption it probed with is put back", rep["restored"] is True)
restored = [p["caption"] for m, p in tg.calls if m == "editMessageCaption"][-1]
check("restored to the right date, read from Telegram's own reply",
      restored == "Daily Economic Briefing — 2026-10-22", restored)

# --- nothing to find --------------------------------------------------------
tg, rep = run({10: None, 11: None})
check("an empty walk deletes nothing", not rep["deleted"] and rep["found"] is None)
check("and says so", "no document of ours" in rep["note"], rep["note"])

tg, rep = run({1: BAD, 2: None}, lookback=0)
check("lookback 0 probes nothing", rep["probed"] == 0 and not rep["deleted"])

# A target further back than the lookback allows is a miss, not a wrong hit.
tg, rep = run({1: BAD, **{i: None for i in range(2, 12)}}, lookback=3)
check("a target beyond the lookback is simply not found",
      not rep["deleted"] and tg.messages.get(1) == BAD)

# --- dry run ----------------------------------------------------------------
tg, rep = run({10: BAD}, dry_run=True)
check("dry run finds it", rep["found"]["file_name"] == BAD)
check("dry run deletes nothing", not rep["deleted"] and tg.messages.get(10) == BAD)
check("dry run issues no delete call", not any(m == "deleteMessage" for m, _ in tg.calls))

# --- failures are reported, not swallowed -----------------------------------
class NoSend(Telegram):
    def __call__(self, method, payload):
        if method == "sendMessage":
            return {"ok": False, "description": "bot was blocked by the user"}
        return super().__call__(method, payload)


rep = recall_from_chat(NoSend({10: BAD}), 111, BAD, "notice")
check("a chat that blocked the bot is reported, not crashed",
      not rep["deleted"] and "blocked" in rep["note"], rep["note"])


class NoDelete(Telegram):
    def __call__(self, method, payload):
        if method == "deleteMessage":
            return {"ok": False, "description": "message can't be deleted"}
        return super().__call__(method, payload)


rep = recall_from_chat(NoDelete({10: BAD}), 111, BAD, "notice")
check("a refused delete is reported as not deleted",
      not rep["deleted"] and "can't be deleted" in rep["note"], rep["note"])

# --- the log must not republish chat ids ------------------------------------
check("chat ids are masked", mask(619918917) == "…917")
out = summarise([{"chat": 619918917, "probed": 2, "found": {"file_name": BAD},
                  "deleted": True, "restored": None, "note": ""}], BAD, False)
check("the summary never prints a full chat id", "619918917" not in out)
check("the summary still distinguishes chats", "…917" in out)
check("the summary states the 48-hour limit", "48 hours" in out)

print(f"\n{failures} failure(s)")
sys.exit(1 if failures else 0)
