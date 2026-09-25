"""Pin the subscriber list. Run: python3 scripts/test_subscribers.py

The cases that matter here are the ones where getting it wrong sends the
briefing to someone who should not have it, or stops sending it to someone who
should. A silent mis-send is not recoverable — you cannot unsend a PDF — so the
default in every ambiguous case is "receives nothing".
"""

import json
import re
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


# Telegram's update_id increases monotonically and forever, so the helpers mint
# ids the same way. Reusing an id across two payloads would look to the code like
# a replay of an already-handled message — which is exactly what it is designed
# to ignore, and would silently hollow out most of the cases below.
_uid = [1000]


def next_uid():
    _uid[0] += 1
    return _uid[0]


def updates(*chats):
    """A getUpdates payload for the given (id, type, first_name) chats."""
    return {"ok": True, "result": [
        {"update_id": next_uid(),
         "message": {"chat": {"id": c[0], "type": c[1], "first_name": c[2]}}} for c in chats
    ]}


def says(*pairs):
    """A getUpdates payload of (chat_id, text) messages, in order."""
    return {"ok": True, "result": [
        {"update_id": next_uid(),
         "message": {"chat": {"id": c, "type": "private", "first_name": "X"}, "text": t}}
        for c, t in pairs
    ]}


def fresh():
    return {"approved": [], "pending": [], "unsubscribed": [], "last_update_id": 0}


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
    d11, _, _, _ = process({"ok": True, "result": [{"update_id": next_uid(), "message": {
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
# Only the lists must be untouched. last_update_id does advance — the command
# has been handled and must not be answered again on the next poll.
lists_only = lambda d: json.dumps({k: d[k] for k in
                                   ("approved", "pending", "unsubscribed")}, sort_keys=True)
snapshot = lists_only(d21)
d21, _, r21, _ = process(says((OWNER, "/pending")), d21, OWNER)
expect("/pending answers the owner without changing the lists",
       (lists_only(d21) == snapshot,
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

# --- exactly once, however often we poll ----------------------------------------
# The poller runs every five minutes and Telegram keeps its backlog for 24 hours.
# Without this, one /start would be answered on every pass — about 288 identical
# messages a day to one person. These are the cases that make frequent polling
# safe, and they are the reason last_update_id exists.

def says_ids(*triples):
    """A payload of (update_id, chat_id, text)."""
    return {"ok": True, "result": [
        {"update_id": uid,
         "message": {"chat": {"id": c, "type": "private", "first_name": "X"}, "text": t}}
        for uid, c, t in triples
    ]}


payload = says_ids((10, FRIEND, "/start"))
d26, _, r26, diag26 = process(payload, fresh(), OWNER)
expect("a first sighting is acted on",
       ([r["outcome"] for r in r26 if r["chat_id"] == FRIEND], d26["last_update_id"]),
       (["pending"], 10))

# The same payload again — exactly what the next poll receives if the offset has
# not yet taken effect.
d26, _, r26b, diag26b = process(payload, d26, OWNER)
expect("re-reading the same update replies to nobody", r26b, [])
expect("and says why it did nothing",
       (diag26b["skipped_already_handled"], diag26b["updates"]), (1, 0))

# A newer update in the same payload is still acted on.
d27, _, r27, _ = process(says_ids((10, FRIEND, "/start"), (11, STRANGER, "/start")),
                         d26, OWNER)
expect("a newer update alongside a handled one is acted on",
       sorted(r["chat_id"] for r in r27 if r["chat_id"] != OWNER), [STRANGER])
expect("the mark advances to the newest seen", d27["last_update_id"], 11)

# The owner's commands must not repeat either — a /pending sitting in the backlog
# would otherwise be answered every five minutes.
d28, _, r28, _ = process(says_ids((20, OWNER, "/pending")), fresh(), OWNER)
d28, _, r28b, _ = process(says_ids((20, OWNER, "/pending")), d28, OWNER)
expect("an owner command is answered once, not on every poll",
       ([r["outcome"] for r in r28], r28b), (["owner-pending"], []))

# Nor may an approval be re-announced.
d29, _, _, _ = process(says_ids((30, FRIEND, "/start")), fresh(), OWNER)
d29, _, r29, _ = process(says_ids((31, OWNER, "/approve %d" % FRIEND)), d29, OWNER)
d29, _, r29b, _ = process(says_ids((31, OWNER, "/approve %d" % FRIEND)), d29, OWNER)
expect("an approval is announced once",
       ([r["outcome"] for r in r29], r29b), (["approved"], []))
expect("and the subscriber stays on the list", recipients(d29, OWNER), [OWNER, FRIEND])

# An empty poll must not move the mark backwards.
d30, _, r30, _ = process({"ok": True, "result": []}, d29, OWNER)
expect("an empty poll changes nothing",
       (r30, d30["last_update_id"]), ([], 31))

# A store written before last_update_id existed must not replay the whole backlog
# as brand new — it should still work, treating the mark as 0 and acting once.
legacy = {"approved": [], "pending": []}
d31, _, r31, _ = process(says_ids((5, FRIEND, "/start")), legacy, OWNER)
expect("a store predating last_update_id still works",
       ([r["outcome"] for r in r31 if r["chat_id"] == FRIEND], d31["last_update_id"]),
       (["pending"], 5))

# The mark has to survive a save/load round trip or none of the above holds.
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "s.json"
    save(d31, p)
    expect("the mark survives the round trip", load(p)["last_update_id"], 5)
    _, _, r32, _ = process(says_ids((5, FRIEND, "/start")), load(p), OWNER)
    expect("and still suppresses a replay after reloading", r32, [])

# --- the webhook queue ----------------------------------------------------------
# The Worker answers people in milliseconds and queues what it decided; these
# cases cover bringing the committed list into line afterwards. The queue is
# at-least-once — items are deleted only after this has been committed — so every
# one of them must survive being applied twice. Deleting on read instead would
# lose an opt-out silently, which is the failure worth engineering against.
from subscribers import apply_queue, sizes  # noqa: E402


def q(*triples):
    """Queue items as the Worker writes them: (id, verb, chat_id)."""
    return [{"id": i, "verb": v, "chat_id": c, "type": "private"} for i, v, c in triples]


d33, notes33 = apply_queue(q(("1", "start", FRIEND)), fresh(), OWNER)
expect("a queued /start lands in pending, not approved",
       (ids(d33["pending"]), ids(d33["approved"])), ({FRIEND}, set()))

# The property everything else depends on.
d34, _ = apply_queue(q(("1", "start", FRIEND)), fresh(), OWNER)
d34, notes34 = apply_queue(q(("1", "start", FRIEND)), d34, OWNER)
expect("replaying a /start changes nothing",
       (len(d34["pending"]), "no change" in notes34[0]), (1, True))

d35, _ = apply_queue(q(("1", "start", FRIEND), ("2", "approve", FRIEND)), fresh(), OWNER)
expect("a queued approval puts them on the delivery list",
       recipients(d35, OWNER), [OWNER, FRIEND])
d35, notes35 = apply_queue(q(("2", "approve", FRIEND)), d35, OWNER)
expect("replaying an approval changes nothing",
       (recipients(d35, OWNER), "no change" in notes35[0]), ([OWNER, FRIEND], True))

d36, _ = apply_queue(q(("1", "start", FRIEND), ("2", "approve", FRIEND),
                       ("3", "stop", FRIEND)), fresh(), OWNER)
expect("a queued /stop removes and remembers them",
       (recipients(d36, OWNER), ids(d36["unsubscribed"])), ([OWNER], {FRIEND}))
d36, _ = apply_queue(q(("3", "stop", FRIEND)), d36, OWNER)
expect("replaying a /stop keeps them off, exactly once",
       (recipients(d36, OWNER), len(d36["unsubscribed"])), ([OWNER], 1))

# Order within one drain must be honoured: the Worker queues chronologically.
d37, _ = apply_queue(q(("1", "start", FRIEND), ("2", "stop", FRIEND),
                       ("3", "start", FRIEND)), fresh(), OWNER)
expect("the last decision in a batch wins",
       (ids(d37["pending"]), ids(d37["unsubscribed"])), ({FRIEND}, set()))

# Deny is a removal, and is silent — apply_queue sends nothing at all, ever.
d38, _ = apply_queue(q(("1", "start", STRANGER), ("2", "deny", STRANGER)), fresh(), OWNER)
expect("a queued denial removes and remembers them",
       (ids(d38["pending"]), ids(d38["unsubscribed"])), (set(), {STRANGER}))

# The Worker may queue an approval before the /start that caused it has drained —
# they are separate writes. Honour it rather than dropping the owner's decision.
d39, _ = apply_queue(q(("9", "approve", FRIEND)), fresh(), OWNER)
expect("an approval with no pending row still enrols them",
       recipients(d39, OWNER), [OWNER, FRIEND])

# An approval must clear a remembered opt-out, or the two would fight.
d40, _ = apply_queue(q(("1", "stop", FRIEND), ("2", "approve", FRIEND)), fresh(), OWNER)
expect("a queued approval overrides an earlier opt-out",
       (ids(d40["unsubscribed"]), FRIEND in ids(d40["approved"])), (set(), True))

# The owner cannot be enrolled or removed by queue traffic.
d41, notes41 = apply_queue(q(("1", "start", OWNER), ("2", "stop", OWNER)), fresh(), OWNER)
expect("queue items about the owner are skipped",
       (recipients(d41, OWNER), all("owner" in n for n in notes41)), ([OWNER], True))

# Junk must not crash the drain or silently corrupt the list.
d42, notes42 = apply_queue(
    [{"id": "x", "verb": "explode", "chat_id": FRIEND},
     {"id": "y", "verb": "start", "chat_id": "not-a-number"},
     {"id": "z"}],
    fresh(), OWNER)
expect("unrecognised queue items are reported and ignored",
       (sizes(d42), len(notes42)),
       ({"approved": 0, "pending": 0, "unsubscribed": 0}, 3))

# apply_queue never messages anybody: the Worker already did, at the time.
expect("apply_queue returns notes, never replies",
       all(isinstance(n, str) for n in notes33), True)

# --- the Worker's copy of the wording must not drift --------------------------
# The Worker answers people in milliseconds, so it cannot fetch its wording over
# the network first; it carries its own copy. Two copies of anything drift, and
# the drift would be invisible — the subscriber would simply be told something
# slightly different depending on which path answered. So compare them.
WORKER = Path(__file__).resolve().parent.parent / "worker/src/index.js"
if WORKER.is_file():
    js = WORKER.read_text(encoding="utf-8")
    block = js.split("const MSG = {", 1)[1].split("\n};", 1)[0]
    # Join the string concatenations the JS uses for line length, then read the
    # "key": "value" pairs back out.
    flat = re.sub(r'"\s*\+\s*\n?\s*"', "", block)
    worker_msg = {k: v for k, v in re.findall(r'"?([a-z-]+)"?:\s*\n?\s*"((?:[^"\\]|\\.)*)"', flat)}

    for key, text in MSG.items():
        expect(f"the Worker's {key!r} wording matches",
               worker_msg.get(key), text)
    extra = set(worker_msg) - set(MSG) - {"denied"}
    expect("the Worker says nothing the Python side does not know about",
           sorted(extra), [])
else:
    print("SKIP  worker/src/index.js not present")

print(f"\n{failures} failure(s)")
sys.exit(1 if failures else 0)
