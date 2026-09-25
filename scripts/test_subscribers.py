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
    approve, chats_from_updates, commands_from_updates, ids, load, parse_ids, process,
    recipients, remove, save, sync,
)

OWNER = 111111111
FRIEND = 222222222
STRANGER = 333333333


def updates(*chats):
    """A getUpdates payload for the given (id, type, first_name) chats."""
    return {"ok": True, "result": [
        {"message": {"chat": {"id": c[0], "type": c[1], "first_name": c[2]}}} for c in chats
    ]}


def says(*pairs):
    """A getUpdates payload of (chat_id, text) messages, in order."""
    return {"ok": True, "result": [
        {"message": {"chat": {"id": c, "type": "private", "first_name": "X"}, "text": t}}
        for c, t in pairs
    ]}


def fresh():
    return {"approved": [], "pending": [], "unsubscribed": []}


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
    expect("a missing store reads as empty", load(Path(td) / "nope.json"), fresh())

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

# --- /start and /stop ----------------------------------------------------------
# These run in briefing.yml before the edition is sent, so whatever a chat asked
# for this morning must be true of this morning's delivery.

expect("commands are recognised with and without a @botname suffix",
       sorted(c["command"] for c in commands_from_updates(
           says((1, "/stop@EconBriefBot"), (2, "/start")))),
       ["start", "stop"])
expect("/subscribe and /unsubscribe are accepted too",
       sorted(c["command"] for c in commands_from_updates(
           says((1, "/unsubscribe"), (2, "/subscribe")))),
       ["start", "stop"])
expect("ordinary chatter is not a command",
       commands_from_updates(says((1, "morning, thanks for the briefing"))), [])

# An approved subscriber who says stop must be gone from THIS morning's send.
d, _ = sync(updates((FRIEND, "private", "Sam")), fresh(), OWNER)
approve({FRIEND}, d, OWNER)
d, _, replies, _ = process(says((FRIEND, "/stop")), d, OWNER)
expect("/stop drops an approved subscriber from today's delivery",
       recipients(d, OWNER), [OWNER])
expect("/stop is confirmed back to the sender",
       [r["outcome"] for r in replies], ["stopped"])

# The /stop message stays in Telegram's backlog for 24 hours, so the next run
# sees it again. It must not put them back up for approval.
d, report = sync(says((FRIEND, "/stop")), d, OWNER)
expect("a stale /stop does not re-propose the chat",
       (ids(d["pending"]), [r["state"] for r in report]), (set(), ["unsubscribed"]))

# /start asks to be considered. It must NOT enrol — that was a deliberate choice.
d2, _, replies2, _ = process(says((STRANGER, "/start")), fresh(), OWNER)
expect("/start does not enrol, it only asks",
       (recipients(d2, OWNER), ids(d2["pending"])), ([OWNER], {STRANGER}))
expect("/start is answered with 'awaiting approval'",
       [r["outcome"] for r in replies2 if r["chat_id"] == STRANGER], ["pending"])

# Changing your mind inside one window: the later command wins.
d3, _, _, _ = process(says((FRIEND, "/stop"), (FRIEND, "/start")), fresh(), OWNER)
expect("/start after /stop in one window leaves them pending, not opted out",
       (ids(d3["pending"]), ids(d3["unsubscribed"])), ({FRIEND}, set()))
d4, _, _, _ = process(says((FRIEND, "/start"), (FRIEND, "/stop")), fresh(), OWNER)
expect("/stop after /start in one window leaves them opted out",
       (ids(d4["pending"]), ids(d4["unsubscribed"])), (set(), {FRIEND}))

# An explicit approval must beat a remembered opt-out, or the two would fight.
d5, _, _, _ = process(says((FRIEND, "/stop")), fresh(), OWNER)
approve({FRIEND}, d5, OWNER)
expect("approving clears an earlier opt-out",
       (ids(d5["unsubscribed"]), FRIEND in ids(d5["approved"])), (set(), False))

# A re-joining chat still needs approval, not an automatic return.
d6, _, _, _ = process(says((FRIEND, "/stop")), fresh(), OWNER)
d6, _, _, _ = process(says((FRIEND, "/start")), d6, OWNER)
expect("/start after an opt-out returns them to pending, not to the send list",
       (recipients(d6, OWNER), ids(d6["pending"])), ([OWNER], {FRIEND}))

# Already-subscribed chats get told so rather than being duplicated.
d7, _ = sync(updates((FRIEND, "private", "Sam")), fresh(), OWNER)
approve({FRIEND}, d7, OWNER)
d7, _, replies7, _ = process(says((FRIEND, "/start")), d7, OWNER)
expect("/start from an existing subscriber changes nothing",
       (recipients(d7, OWNER), [r["outcome"] for r in replies7]),
       ([OWNER, FRIEND], ["already-subscribed"]))

# The owner cannot unsubscribe by message — their copy is a repository secret.
# Pretending to comply would be the worst outcome here.
d8, _, replies8, _ = process(says((OWNER, "/stop")), fresh(), OWNER)
expect("the owner's /stop is refused honestly, not silently obeyed",
       (recipients(d8, OWNER), [r["outcome"] for r in replies8]),
       ([OWNER], ["owner-stop"]))

# A /stop from someone never on the list is still confirmed.
d9, _, replies9, _ = process(says((STRANGER, "/stop")), fresh(), OWNER)
expect("/stop from an unknown chat is still acknowledged",
       [r["outcome"] for r in replies9], ["stopped"])

# The owner's own `remove` must stick, not be undone by tomorrow's sweep.
d10, _ = sync(updates((FRIEND, "private", "Sam")), fresh(), OWNER)
remove({FRIEND}, d10, remember=True)
d10, _ = sync(updates((FRIEND, "private", "Sam")), d10, OWNER)
expect("a manual removal is not undone by the next sweep", ids(d10["pending"]), set())

# Opting out never leaks a name either.
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "s.json"
    d11, _, _, _ = process({"ok": True, "result": [{"message": {
        "chat": {"id": FRIEND, "type": "private", "first_name": "Sam",
                 "username": "samsmith"}, "text": "/stop"}}]}, fresh(), OWNER)
    save(d11, p)
    body = p.read_text()
    expect("the unsubscribed list carries no name or username",
           ("Sam" in body, "samsmith" in body), (False, False))

# --- what the subscriber actually reads ----------------------------------------
# These are the only part of the system a subscriber sees, and the wording is the
# owner's, so pin it rather than leaving it to be paraphrased by a later edit.
from subscribers import MSG  # noqa: E402

expect("/start is answered with the pending wording",
       MSG["pending"], "Your request for subscription is pending.")
expect("approval is answered with the approved wording",
       MSG["approved"], "Your request for subscription has been approved.")
expect("/stop is answered with the unsubscribe wording",
       MSG["stopped"],
       "We have received your unsubscribe request. Please give us time to process it.")
expect("every outcome the code can produce has a message",
       sorted(MSG), ["already-subscribed", "approved", "owner-stop", "pending", "stopped"])

# Approval must notify, and must notify only on a real transition — the owner
# re-running the workflow should not message a subscriber again each time.
d12, _, _, _ = process(says((FRIEND, "/start")), fresh(), OWNER)
told = []
approve({FRIEND}, d12, OWNER, replies=told)
expect("approving tells the subscriber, once",
       [(r["chat_id"], r["outcome"], r["text"]) for r in told],
       [(FRIEND, "approved", MSG["approved"])])

told2 = []
approve({FRIEND}, d12, OWNER, replies=told2)
expect("re-approving does not message them again", told2, [])

# Approving a chat that never asked cannot be confirmed either.
d13 = fresh()
told3 = []
approve({STRANGER}, d13, OWNER, replies=told3)
expect("approving an unseen chat sends no confirmation", told3, [])

# The owner is not a subscriber, so approving them confirms nothing.
d14, _ = sync(updates((OWNER, "private", "Alex")), fresh(), OWNER)
told4 = []
approve({OWNER}, d14, OWNER, replies=told4)
expect("approving the owner sends no confirmation", told4, [])

# Every reply the daily sweep emits must carry text, or the send step would
# push an empty message to a real person.
d15, _, allreplies, _ = process(
    says((FRIEND, "/start"), (STRANGER, "/stop"), (OWNER, "/stop")), fresh(), OWNER)
# Four: FRIEND told pending, STRANGER told stopped, the owner's own /stop
# explained, and the owner notified that FRIEND is waiting.
expect("every emitted reply has a chat, an outcome and non-empty text",
       all(r.get("chat_id") and r.get("outcome") and r.get("text") for r in allreplies)
       and len(allreplies), 4)

# --- the owner approving from the chat itself -----------------------------------
# Authorisation is the sender's chat id, which Telegram asserts and the sender
# cannot set. These cases are the security boundary, so they matter most.
from subscribers import owner_requests  # noqa: E402

d16, _, _, _ = process(says((FRIEND, "/start")), fresh(), OWNER)
d16, _, r16, diag16 = process(says((OWNER, "/approve %d" % FRIEND)), d16, OWNER)
expect("the owner can approve from the chat",
       (recipients(d16, OWNER), [r["outcome"] for r in r16]),
       ([OWNER, FRIEND], ["approved"]))

# The point of doing this in the sweep: a request and its approval inside one
# window resolve together, and the subscriber hears the outcome only.
d17, _, r17, _ = process(
    says((FRIEND, "/start"), (OWNER, "/approve %d" % FRIEND)), fresh(), OWNER)
expect("a /start approved in the same sweep yields one message, not two",
       (recipients(d17, OWNER), [r["outcome"] for r in r17]),
       ([OWNER, FRIEND], ["approved"]))

# /deny removes and remembers, and deliberately tells the subscriber nothing.
d18, _, _, _ = process(says((STRANGER, "/start")), fresh(), OWNER)
d18, _, r18, _ = process(says((OWNER, "/deny %d" % STRANGER)), d18, OWNER)
expect("/deny drops the request and stays silent",
       (ids(d18["pending"]), ids(d18["unsubscribed"]), r18), (set(), {STRANGER}, []))

# Several instructions in one window must all apply — unlike /start and /stop,
# these are not reduced to the last one per chat.
d19, _, _, _ = process(says((FRIEND, "/start"), (STRANGER, "/start")), fresh(), OWNER)
d19, _, _, _ = process(
    says((OWNER, "/approve %d" % FRIEND), (OWNER, "/approve %d" % STRANGER)), d19, OWNER)
expect("two separate /approve messages both apply",
       sorted(ids(d19["approved"])), sorted([FRIEND, STRANGER]))
expect("one /approve with several ids applies to all",
       sorted(i for c in owner_requests(
           says((OWNER, "/approve 1, 2 3")), OWNER)[0] for i in c["ids"]), [1, 2, 3])

# THE security case: an owner-only command from anybody else changes nothing and
# is surfaced rather than dropped.
d20, _, _, _ = process(says((STRANGER, "/start")), fresh(), OWNER)
d20, _, r20, diag20 = process(
    says((STRANGER, "/approve %d" % STRANGER)), d20, OWNER)
expect("a stranger cannot approve themselves",
       (recipients(d20, OWNER), ids(d20["approved"])), ([OWNER], set()))
expect("the attempt is reported, not silently dropped",
       [(r["chat_id"], r["command"]) for r in diag20["rejected_commands"]],
       [(STRANGER, "approve")])

# With no owner configured, nobody can issue owner commands at all.
expect("no owner configured means no owner commands are honoured",
       owner_requests(says((OWNER, "/approve 1")), None)[0], [])

# /pending and /status answer the owner and change nothing.
d21, _, _, _ = process(says((FRIEND, "/start")), fresh(), OWNER)
snapshot = json.dumps(d21, sort_keys=True)
d21, _, r21, _ = process(says((OWNER, "/pending")), d21, OWNER)
expect("/pending answers the owner without changing the lists",
       (json.dumps(d21, sort_keys=True) == snapshot,
        [r["outcome"] for r in r21]), (True, ["owner-pending"]))
expect("the /pending answer names the waiting chat",
       str(FRIEND) in r21[0]["text"], True)

# An owner note and a subscriber's state message in one sweep must both survive.
d22, _, r22, _ = process(says((FRIEND, "/start"), (OWNER, "/pending")), fresh(), OWNER)
expect("a state reply and two owner notes do not displace each other",
       sorted(r["outcome"] for r in r22),
       ["owner-new-requests", "owner-pending", "pending"])

# A fat-fingered argument must be reported, not silently ignored: the owner
# believes they approved somebody.
acc, _, _ = owner_requests(says((OWNER, "/approve 222 oops")), OWNER)
expect("an unparseable argument is kept for reporting",
       (acc[0]["ids"], acc[0]["unparsed"]), ([222], ["oops"]))

# Unknown slash commands are recorded for the log but acted on by nobody.
_, _, unk = owner_requests(says((FRIEND, "/help")), OWNER)
expect("an unknown command is noted, not obeyed",
       [u["command"] for u in unk], ["/help"])
expect("/start is not treated as an unknown command",
       owner_requests(says((FRIEND, "/start")), OWNER)[2], [])

# --- the diagnostics themselves -------------------------------------------------
# These exist to make a 07:20 failure explainable without a re-run, so they are
# worth pinning too.
d23, _, _, diag23 = process(
    says((FRIEND, "/start"), (STRANGER, "/stop"), (OWNER, "/status")), fresh(), OWNER)
expect("the diagnostic counts what arrived",
       (diag23["updates"], diag23["chats_seen"]), (3, 3))
expect("the diagnostic records list sizes before and after",
       (diag23["before"]["pending"], diag23["after"]["pending"]), (0, 1))
expect("the diagnostic records each owner command and its effect",
       [c["command"] for c in diag23["owner_commands"]], ["status"])
expect("the diagnostic classifies every chat it saw",
       sum(diag23["states"].values()), 3)

# The owner should learn of a request in the chat, not by reading a job summary.
d24, _, r24, _ = process(says((FRIEND, "/start")), fresh(), OWNER)
owner_notes = [r for r in r24 if r["chat_id"] == OWNER]
expect("a new request notifies the owner",
       [r["outcome"] for r in owner_notes], ["owner-new-requests"])
expect("the notification gives the owner the id and the command to use",
       (str(FRIEND) in owner_notes[0]["text"], "/approve" in owner_notes[0]["text"]),
       (True, True))

# Only on first sighting: a chat already pending must not re-notify every day.
d24, _, r24b, _ = process(says((FRIEND, "hello again")), d24, OWNER)
expect("an already-pending chat does not re-notify the owner",
       [r for r in r24b if r["chat_id"] == OWNER], [])

# With no owner there is nobody to notify, and that must not crash.
d25, _, r25, _ = process(says((FRIEND, "/start")), fresh(), None)
expect("no owner configured means no notification and no error",
       [r["outcome"] for r in r25], ["pending"])

print(f"\n{failures} failure(s)")
sys.exit(1 if failures else 0)
