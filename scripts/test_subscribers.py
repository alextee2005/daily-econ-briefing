"""Pin the subscriber list. Run: python3 scripts/test_subscribers.py

The cases that matter here are the ones where getting it wrong sends the
briefing to someone who should not have it, or stops sending it to someone who
should. A silent mis-send is not recoverable — you cannot unsend a PDF — so the
default in every ambiguous case is "receives nothing".
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import subscribers  # noqa: E402
from subscribers import (  # noqa: E402
    approve, chats_from_updates, ids, load, parse_ids, recipients, remove, save, sync,
)

OWNER = 111111111
FRIEND = 222222222
STRANGER = 333333333


def updates(*chats):
    """A getUpdates payload for the given (id, type, first_name) chats."""
    return {"ok": True, "result": [
        {"message": {"chat": {"id": c[0], "type": c[1], "first_name": c[2]}}} for c in chats
    ]}


def fresh():
    return {"approved": [], "pending": []}


failures = 0


def expect(label, got, want):
    global failures
    ok = got == want
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        print(f"      want {want}")
        print(f"      got  {got}")


# --- discovery -----------------------------------------------------------------
data, report = sync(updates((OWNER, "private", "Alex"), (FRIEND, "private", "Sam")),
                    fresh(), OWNER)
expect("the owner is recognised, not enrolled",
       [r["state"] for r in report if r["chat_id"] == OWNER], ["owner"])
expect("an unknown chat lands in pending, not approved",
       (ids(data["pending"]), ids(data["approved"])), ({FRIEND}, set()))

# A stranger who messages the bot must not receive anything.
d2 = fresh()
d2, _ = sync(updates((STRANGER, "private", "Nobody")), d2, OWNER)
expect("a stranger receives nothing until approved", recipients(d2, OWNER), [OWNER])

# Syncing twice must not duplicate anyone.
d3, _ = sync(updates((FRIEND, "private", "Sam")), fresh(), OWNER)
d3, rep3 = sync(updates((FRIEND, "private", "Sam")), d3, OWNER)
expect("re-syncing the same chat does not duplicate it", len(d3["pending"]), 1)
expect("the second sight of a chat reads as pending, not new",
       [r["state"] for r in rep3], ["pending"])

# --- approval ------------------------------------------------------------------
d4, _ = sync(updates((FRIEND, "private", "Sam")), fresh(), OWNER)
approve({FRIEND}, d4, OWNER)
expect("approving moves the chat and empties pending",
       (ids(d4["approved"]), ids(d4["pending"])), ({FRIEND}, set()))
expect("an approved chat joins the delivery list after the owner",
       recipients(d4, OWNER), [OWNER, FRIEND])

notes = dict(approve({FRIEND}, d4, OWNER))
expect("approving twice is a no-op, not a duplicate",
       (len(d4["approved"]), "already approved" in notes[FRIEND]), (1, True))

# Approving someone the bot has never heard from cannot work: Telegram refuses
# sendDocument until the user has started the bot. Say so rather than adding a
# row that will fail every morning.
d5 = fresh()
notes = dict(approve({STRANGER}, d5, OWNER))
expect("approving an unseen chat is refused with a reason",
       (ids(d5["approved"]), "message the bot" in notes[STRANGER]), (set(), True))

# The owner is already served by the secret; approving them must not double-send.
d6, _ = sync(updates((OWNER, "private", "Alex")), fresh(), OWNER)
approve({OWNER}, d6, OWNER)
expect("approving the owner does not duplicate their delivery",
       recipients(d6, OWNER), [OWNER])

# --- removal -------------------------------------------------------------------
d7, _ = sync(updates((FRIEND, "private", "Sam")), fresh(), OWNER)
approve({FRIEND}, d7, OWNER)
remove({FRIEND}, d7)
expect("removing drops the chat from the delivery list", recipients(d7, OWNER), [OWNER])

d8, _ = sync(updates((STRANGER, "private", "Nobody")), fresh(), OWNER)
remove({STRANGER}, d8)
expect("removing also clears a pending chat", ids(d8["pending"]), set())

# --- the store round-trips, and never carries a name --------------------------
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "subscribers.json"
    d9, _ = sync(updates((FRIEND, "group", "Sam Smith")), fresh(), OWNER)
    approve({FRIEND}, d9, OWNER)
    save(d9, p)
    raw = p.read_text()
    reloaded = load(p)
    expect("saved then loaded is unchanged", ids(reloaded["approved"]), {FRIEND})
    expect("the stored file carries no display name",
           ("Sam" in raw, "Smith" in raw), (False, False))
    expect("the chat type survives the round trip",
           reloaded["approved"][0]["type"], "group")

# A hand-edit that drops a key must not crash the morning's delivery.
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "subscribers.json"
    p.write_text(json.dumps({"approved": [{"chat_id": FRIEND, "type": "private"}]}))
    expect("a hand-edited file missing 'pending' still loads",
           (ids(load(p)["approved"]), load(p)["pending"]), ({FRIEND}, []))

# A missing file is the first-run case, not an error.
with tempfile.TemporaryDirectory() as td:
    expect("a missing store reads as empty",
           load(Path(td) / "nope.json"), {"approved": [], "pending": []})

# --- the owner's id comes from the environment, and may be absent -------------
expect("owner id parses from the environment",
       (subscribers.owner_id.__name__, parse_ids("1, 2 3")), ("owner_id", {1, 2, 3}))

# With no owner configured, approved subscribers still receive the briefing —
# the alternative is silently delivering to nobody.
d10, _ = sync(updates((FRIEND, "private", "Sam")), fresh(), None)
approve({FRIEND}, d10, None)
expect("subscribers still receive it when no owner is set",
       recipients(d10, None), [FRIEND])

# --- getUpdates shapes ---------------------------------------------------------
expect("edited messages and channel posts are seen too",
       sorted(c["chat_id"] for c in chats_from_updates({"result": [
           {"edited_message": {"chat": {"id": 7, "type": "private"}}},
           {"channel_post": {"chat": {"id": 8, "type": "channel"}}},
       ]})), [7, 8])
expect("an update with no chat is ignored rather than crashing",
       chats_from_updates({"result": [{"poll_answer": {"poll_id": "x"}}]}), [])
expect("an empty payload yields nothing", chats_from_updates({}), [])

print(f"\n{failures} failure(s)")
sys.exit(1 if failures else 0)
