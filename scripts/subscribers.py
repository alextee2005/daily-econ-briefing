"""Who receives the briefing, besides its owner.

The owner's own chat stays in the TELEGRAM_CHAT_ID secret and is never written
here. Everyone else lives in subscribers.json, which is committed — so this
file deliberately stores the bare minimum: a numeric chat id, the chat type,
and a date. No names, no usernames, no message text. This repository is
public, and a subscriber's display name is not ours to publish.

Two lists, because being able to message the bot is not the same as being
entitled to the briefing:

    pending    the bot has heard from this chat, and that is all it means.
               Anyone who finds the bot can put themselves here.
    approved   the owner has decided this chat should receive the briefing.

Nothing moves from pending to approved on its own. That separation is the
whole point: an open list would mean whoever discovers the bot receives the
briefing and spends the owner's Telegram quota.

Usage:
    python3 scripts/subscribers.py sync --updates updates.json
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

EMPTY = {"approved": [], "pending": []}


def load(path: Path = STORE) -> dict:
    """Read the store, tolerating absence and a hand-edit that lost a key."""
    if not path.is_file():
        return json.loads(json.dumps(EMPTY))
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in EMPTY:
        data.setdefault(key, [])
    return data


def save(data: dict, path: Path = STORE) -> None:
    ordered = {
        "_comment": (
            "Recipients of the daily briefing, besides the owner. Approved chats "
            "receive it; pending chats have only messaged the bot and receive "
            "nothing. Move an id between the lists with "
            "scripts/subscribers.py, or by hand. Numeric ids only — never add "
            "names or usernames, this repository is public."
        ),
        "approved": sorted(data["approved"], key=lambda e: e["chat_id"]),
        "pending": sorted(data["pending"], key=lambda e: e["chat_id"]),
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


def sync(updates: dict, data: dict, owner: int | None) -> tuple[dict, list]:
    """Record chats we have not seen before as pending.

    Returns the store and a classification of every chat in the payload, so the
    caller can report what happened without recomputing it.
    """
    approved, pending = ids(data["approved"]), ids(data["pending"])
    report = []
    for chat in chats_from_updates(updates):
        cid = chat["chat_id"]
        if owner is not None and cid == owner:
            state = "owner"
        elif cid in approved:
            state = "approved"
        elif cid in pending:
            state = "pending"
        else:
            state = "new"
            data["pending"].append(
                {"chat_id": cid, "type": chat["type"], "seen": date.today().isoformat()}
            )
        report.append({**chat, "state": state})
    return data, report


def approve(targets: set, data: dict, owner: int | None) -> list:
    """Move chats from pending to approved. Returns one note per target."""
    notes = []
    pending = {e["chat_id"]: e for e in data["pending"]}
    approved = ids(data["approved"])
    for cid in sorted(targets):
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


def remove(targets: set, data: dict) -> list:
    notes = []
    for cid in sorted(targets):
        before = len(data["approved"]) + len(data["pending"])
        data["approved"] = [e for e in data["approved"] if e["chat_id"] != cid]
        data["pending"] = [e for e in data["pending"] if e["chat_id"] != cid]
        after = len(data["approved"]) + len(data["pending"])
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
    ap.add_argument("action", choices=["sync", "approve", "remove", "recipients"])
    ap.add_argument("targets", nargs="?", default="", help="chat ids, comma or space separated")
    ap.add_argument("--updates", help="a getUpdates JSON payload (sync only)")
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
    notes = approve(targets, data, owner) if args.action == "approve" else remove(targets, data)
    save(data, store)
    print()
    for cid, note in notes:
        print(f"  {cid}: {note}")
    print(f"\nNow delivering to the owner plus {len(data['approved'])} subscriber(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
