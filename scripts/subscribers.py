"""Who receives the briefing, besides its owner.

The owner's own chat stays in the TELEGRAM_CHAT_ID secret and is never written
here. Everyone else lives in subscribers.json, which is committed — so this
file deliberately stores the bare minimum: a numeric chat id, the chat type,
and a date. No names, no usernames, no message text. This repository is
public, and a subscriber's display name is not ours to publish.

Three lists, because being able to message the bot is not the same as being
entitled to the briefing, and neither is the same as having said no:

    pending       the bot has heard from this chat, and that is all it means.
                  Anyone who finds the bot can put themselves here.
    approved      the owner has decided this chat should receive the briefing.
    unsubscribed  this chat asked to stop. It is remembered so that an older
                  message still sitting in Telegram's 24-hour backlog cannot
                  quietly re-propose them as a candidate tomorrow.

Nothing moves from pending to approved on its own. That separation is the
whole point: an open list would mean whoever discovers the bot receives the
briefing and spends the owner's Telegram quota. `/start` therefore asks to be
considered; it does not enrol.

Leaving, by contrast, needs nobody's permission. `/stop` takes effect at once,
and a chat that has said stop stays out until it asks again.

Usage:
    python3 scripts/subscribers.py sync --updates updates.json
    python3 scripts/subscribers.py process --updates updates.json [--replies out.json]
    python3 scripts/subscribers.py approve 123456789,987654321
    python3 scripts/subscribers.py remove 123456789
    python3 scripts/subscribers.py recipients

The owner's chat id is read from the OWNER_CHAT_ID environment variable, never
an argument, so it cannot end up in a process list or a public run log.
"""

import argparse
import json
import os
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STORE = REPO / "subscribers.json"

EMPTY = {"approved": [], "pending": [], "unsubscribed": []}

# /subscribe and /unsubscribe are accepted alongside the conventional Telegram
# commands because people type what they mean, not what the bot documents.
COMMANDS = {
    "/start": "start", "/subscribe": "start",
    "/stop": "stop", "/unsubscribe": "stop",
}


def norm(data: dict) -> dict:
    """Fill in any list a hand-edit or an older file is missing."""
    for key in EMPTY:
        data.setdefault(key, [])
    return data


def load(path: Path = STORE) -> dict:
    """Read the store, tolerating absence and a hand-edit that lost a key."""
    if not path.is_file():
        return json.loads(json.dumps(EMPTY))
    return norm(json.loads(path.read_text(encoding="utf-8")))


def save(data: dict, path: Path = STORE) -> None:
    norm(data)
    ordered = {
        "_comment": (
            "Recipients of the daily briefing, besides the owner. Approved chats "
            "receive it; pending chats have only messaged the bot and receive "
            "nothing; unsubscribed chats asked to stop and are remembered so a "
            "stale message cannot re-propose them. Move an id between the lists "
            "with scripts/subscribers.py, or by hand. Numeric ids only — never "
            "add names or usernames, this repository is public."
        ),
        "approved": sorted(data["approved"], key=lambda e: e["chat_id"]),
        "pending": sorted(data["pending"], key=lambda e: e["chat_id"]),
        "unsubscribed": sorted(data["unsubscribed"], key=lambda e: e["chat_id"]),
    }
    path.write_text(json.dumps(ordered, indent=2) + "\n", encoding="utf-8")


def ids(entries: list) -> set:
    return {e["chat_id"] for e in entries}


def owner_id() -> int | None:
    """The owner's chat id, from the environment. Absent is not an error here."""
    raw = (os.environ.get("OWNER_CHAT_ID") or "").strip()
    try:
        return int(raw)
    except ValueError:
        return None


def chats_from_updates(updates: dict) -> list:
    """Distinct chats seen in a getUpdates payload, newest name kept.

    The display name is returned for the caller to print so the owner can tell
    who is asking to be added — it is never stored.
    """
    seen = {}
    for u in updates.get("result", []):
        msg = u.get("message") or u.get("channel_post") or u.get("edited_message") or {}
        chat = msg.get("chat") or {}
        cid = chat.get("id")
        if cid is None:
            continue
        label = " ".join(
            p for p in (chat.get("title"), chat.get("first_name"), chat.get("last_name")) if p
        )
        if chat.get("username"):
            label = f"{label} (@{chat['username']})".strip()
        seen[cid] = {"chat_id": cid, "type": chat.get("type", "?"), "label": label or "?"}
    return list(seen.values())


def commands_from_updates(updates: dict) -> list:
    """The /start and /stop requests in a payload, at most one per chat.

    Later messages win, so a chat that sends /stop and then changes its mind
    with /start in the same 24-hour window ends up asking to join, not to
    leave. Telegram writes commands as `/stop@TheBot` in groups, hence the
    split on '@'.
    """
    latest = {}
    for u in updates.get("result", []):
        msg = u.get("message") or u.get("channel_post") or u.get("edited_message") or {}
        chat = msg.get("chat") or {}
        cid = chat.get("id")
        text = (msg.get("text") or "").strip()
        if cid is None or not text.startswith("/"):
            continue
        verb = COMMANDS.get(text.split()[0].split("@")[0].lower())
        if verb:
            latest[cid] = {"chat_id": cid, "type": chat.get("type", "?"), "command": verb}
    return list(latest.values())


def sync(updates: dict, data: dict, owner: int | None) -> tuple[dict, list]:
    """Record chats we have not seen before as pending.

    Returns the store and a classification of every chat in the payload, so the
    caller can report what happened without recomputing it.
    """
    norm(data)
    approved, pending = ids(data["approved"]), ids(data["pending"])
    gone = ids(data["unsubscribed"])
    report = []
    for chat in chats_from_updates(updates):
        cid = chat["chat_id"]
        if owner is not None and cid == owner:
            state = "owner"
        elif cid in approved:
            state = "approved"
        elif cid in gone:
            # They asked to stop. Any message still in the backlog — including
            # the /stop itself — must not put them back up for approval.
            state = "unsubscribed"
        elif cid in pending:
            state = "pending"
        else:
            state = "new"
            data["pending"].append(
                {"chat_id": cid, "type": chat["type"], "seen": date.today().isoformat()}
            )
        report.append({**chat, "state": state})
    return data, report


def process(updates: dict, data: dict, owner: int | None) -> tuple[dict, list, list]:
    """Record new chats, then act on /start and /stop.

    Commands are applied after the sweep so that a /stop wins over the same
    message having just registered the chat as a candidate. Returns the store,
    the sync report, and the replies to send — a silent /stop is worse than no
    /stop at all, because the person believes they have left.
    """
    norm(data)
    data, report = sync(updates, data, owner)
    replies = []

    for req in commands_from_updates(updates):
        cid, verb = req["chat_id"], req["command"]

        if owner is not None and cid == owner:
            # The owner's copy comes from a repository secret, which no message
            # can change. Say so rather than appearing to comply.
            if verb == "stop":
                replies.append({"chat_id": cid, "outcome": "owner-stop", "text":
                                "You are the owner of this briefing. Your own copy is "
                                "configured in the repository, not by this bot, so it "
                                "will keep arriving."})
            continue

        if verb == "stop":
            remove({cid}, data)
            if cid not in ids(data["unsubscribed"]):
                data["unsubscribed"].append(
                    {"chat_id": cid, "type": req["type"], "stopped": date.today().isoformat()}
                )
            # Always confirm, even to a chat that was never on the list. Someone
            # who sends /stop wants to know it worked, and "you were not
            # subscribed anyway" is not reassurance they can act on.
            replies.append({"chat_id": cid, "outcome": "stopped", "text":
                            "You have been unsubscribed and will not receive further "
                            "editions of the Daily Economic Briefing. Send /start if "
                            "you would like to be considered again."})
        else:
            data["unsubscribed"] = [e for e in data["unsubscribed"] if e["chat_id"] != cid]
            if cid in ids(data["approved"]):
                replies.append({"chat_id": cid, "outcome": "already-subscribed", "text":
                                "You are already subscribed to the Daily Economic "
                                "Briefing. Send /stop at any time to unsubscribe."})
            else:
                if cid not in ids(data["pending"]):
                    data["pending"].append(
                        {"chat_id": cid, "type": req["type"],
                         "seen": date.today().isoformat()}
                    )
                replies.append({"chat_id": cid, "outcome": "pending", "text":
                                "Thanks — your request has been recorded. The briefing is "
                                "sent to an approved list, so you will start receiving it "
                                "once the owner confirms. Send /stop to withdraw."})

    return data, report, replies


def approve(targets: set, data: dict, owner: int | None) -> list:
    """Move chats from pending to approved. Returns one note per target."""
    norm(data)
    notes = []
    pending = {e["chat_id"]: e for e in data["pending"]}
    approved = ids(data["approved"])
    for cid in sorted(targets):
        # An explicit approval overrides an earlier /stop: the owner is saying
        # to send to this chat, so stop remembering it as opted out. Otherwise
        # the next sweep would fight the approval.
        data["unsubscribed"] = [e for e in data["unsubscribed"] if e["chat_id"] != cid]
        if owner is not None and cid == owner:
            notes.append((cid, "is the owner — already receives it via the secret, skipped"))
        elif cid in approved:
            notes.append((cid, "was already approved, no change"))
        elif cid in pending:
            entry = pending.pop(cid)
            data["approved"].append(
                {"chat_id": cid, "type": entry.get("type", "?"),
                 "added": date.today().isoformat()}
            )
            data["pending"] = [e for e in data["pending"] if e["chat_id"] != cid]
            notes.append((cid, "approved — will receive the next edition"))
        else:
            # Approving a chat the bot has never heard from cannot work:
            # Telegram refuses sendDocument until the user starts the bot.
            notes.append((cid, "is not in either list — have them message the bot, then sync"))
    return notes


def remove(targets: set, data: dict, remember: bool = False) -> list:
    """Drop chats from both active lists.

    `remember` also records them as unsubscribed, which is what stops the next
    sweep re-proposing them from a message still in Telegram's backlog. The
    owner's own `remove` sets it, because "removed" should mean removed rather
    than removed until tomorrow morning. The internal call from process() does
    not, since process() writes its own richer entry.
    """
    norm(data)
    notes = []
    for cid in sorted(targets):
        before = len(data["approved"]) + len(data["pending"])
        data["approved"] = [e for e in data["approved"] if e["chat_id"] != cid]
        data["pending"] = [e for e in data["pending"] if e["chat_id"] != cid]
        after = len(data["approved"]) + len(data["pending"])
        if remember and cid not in ids(data["unsubscribed"]):
            data["unsubscribed"].append(
                {"chat_id": cid, "type": "?", "stopped": date.today().isoformat()}
            )
        notes.append((cid, "removed" if after < before else "was not listed, no change"))
    return notes


def recipients(data: dict, owner: int | None) -> list:
    """Delivery list, owner first.

    The owner leads so that the send loop can upload the PDF once to a chat
    that is certain to exist, then forward the resulting file_id to everyone
    else. Ordering is also why a failed owner delivery is the one that fails
    the job: if that send fails, nothing else can be attempted cheaply.
    """
    out = []
    if owner is not None:
        out.append(owner)
    out += [e["chat_id"] for e in data["approved"] if e["chat_id"] != owner]
    return out


def parse_ids(raw: str) -> set:
    out = set()
    for part in raw.replace(",", " ").split():
        try:
            out.add(int(part))
        except ValueError:
            raise SystemExit(f"not a chat id: {part!r}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", choices=["sync", "process", "approve", "remove", "recipients"])
    ap.add_argument("targets", nargs="?", default="", help="chat ids, comma or space separated")
    ap.add_argument("--updates", help="a getUpdates JSON payload (sync, process)")
    ap.add_argument("--replies", help="write the confirmations to send here (process)")
    ap.add_argument("--store", default=str(STORE))
    args = ap.parse_args()

    store = Path(args.store)
    data = load(store)
    owner = owner_id()

    if args.action == "recipients":
        # stdout is the machine-readable part: one id per line, nothing else.
        for cid in recipients(data, owner):
            print(cid)
        return 0

    if args.action == "process":
        # The daily path, run before the briefing is sent so that today's
        # opt-outs are honoured by today's edition.
        if not args.updates:
            raise SystemExit("process needs --updates")
        payload = json.loads(Path(args.updates).read_text(encoding="utf-8"))
        data, report, replies = process(payload, data, owner)
        save(data, store)
        if args.replies:
            Path(args.replies).write_text(json.dumps(replies), encoding="utf-8")

        acted = {r["outcome"] for r in replies}
        print(f"{len(report)} chat(s) seen, {len(replies)} command(s) acted on"
              f"{': ' + ', '.join(sorted(acted)) if acted else ''}")
        for r in replies:
            print(f"  {r['chat_id']}: {r['outcome']}")
        print(f"Delivering to the owner plus {len(data['approved'])} subscriber(s); "
              f"{len(data['pending'])} awaiting approval, "
              f"{len(data['unsubscribed'])} opted out.")
        if data["pending"]:
            print("::notice::Chats awaiting approval: "
                  + ", ".join(str(e["chat_id"]) for e in data["pending"]))
        return 0

    if args.action == "sync":
        if not args.updates:
            raise SystemExit("sync needs --updates")
        payload = json.loads(Path(args.updates).read_text(encoding="utf-8"))
        data, report = sync(payload, data, owner)
        new = [r for r in report if r["state"] == "new"]

        print(f"\n{len(report)} chat(s) have messaged the bot recently:\n")
        for r in report:
            mark = {"owner": "owner  ", "approved": "sending", "pending": "PENDING",
                    "new": "NEW    "}[r["state"]]
            print(f"  [{mark}] {r['chat_id']:>14}  {r['type']:<10} {r['label']}")

        if new:
            save(data, store)
            print(f"\n{len(new)} new chat(s) recorded as pending. They receive NOTHING yet.")
            print("Approve with:  Actions -> Find my Telegram chat ID -> Run workflow,")
            print("               and put the id(s) in the 'approve' input. Or edit")
            print("               subscribers.json directly.")
            print("\nNames above are shown only to help you decide and are NOT stored.")
            print("Note: on a public repository, run logs are public too.")
        else:
            print("\nNo new chats. subscribers.json unchanged.")

        pend = data["pending"]
        if pend:
            print(f"\nStill pending approval: {', '.join(str(e['chat_id']) for e in pend)}")
        return 0

    if not args.targets:
        raise SystemExit(f"{args.action} needs at least one chat id")
    targets = parse_ids(args.targets)
    if args.action == "approve":
        notes = approve(targets, data, owner)
    else:
        notes = remove(targets, data, remember=True)
    save(data, store)
    print()
    for cid, note in notes:
        print(f"  {cid}: {note}")
    print(f"\nNow delivering to the owner plus {len(data['approved'])} subscriber(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
