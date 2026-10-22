"""Delete one specific document the bot sent, from every recipient's chat.

Written for the 22 October 2026 misdelivery, when every subscriber was sent
the 7 September edition. It is deliberately narrow: it deletes a message only
after reading that message's own `document.file_name` back from Telegram and
matching it against the name the operator typed. Nothing is deleted on a
guess about position, age, or "it was probably the last one".

HOW IT FINDS THE MESSAGE

Telegram gives a bot no way to list what it has sent, so there is no record of
the message ids to delete. What it does give:

  * a message id for anything the bot sends now, and private-chat ids run as
    one ascending counter, so a message sent now is an anchor to walk back
    from;
  * `editMessageCaption`, which succeeds **only** on the bot's own captioned
    messages and returns the whole Message object, including the document.

So `editMessageCaption` is the probe. Its crucial property is what it cannot
do: it cannot touch a message the subscriber wrote. A walk backwards from the
anchor therefore steps straight over every incoming message without reading,
copying or altering it — which rules out the obvious alternative probes,
`forwardMessage` and `copyMessage`, since both would relay a subscriber's
private messages to the owner to find out what they were.

THE CAPTION THE PROBE WRITES

It writes the caption the *target* is already known to have, plus one or more
zero-width spaces. The padding is invisible in Telegram and is not decoration:
`editMessageCaption` fails with "message is not modified" when the new caption
equals the old one, and that failure is indistinguishable from "this message
is not ours". The first delete run hit exactly that — a report run had already
written the plain caption onto the owner's copy, so the real run skipped
straight past it, walked on to the previous edition and stopped. Four
subscribers were cleaned; the owner's copy survived the run meant to remove
it. The padding makes every probe a genuine change, and a "not modified" reply
is retried with more padding rather than read as a miss.

A miss — some other edition — is put back using the date in the file name
Telegram just returned, so the restore is read from the response rather than
guessed, and the walk stops: the first document found going backwards is the
most recent one the bot sent, and if that is not the target then the
operator's assumption is wrong and the run should say so rather than keep
digging through older briefings. A dry run restores the caption on a hit too,
so that rehearsing leaves nothing behind for the real run to trip over.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pick_edition import edition_date  # noqa: E402

DEFAULT_LOOKBACK = 25

# Invisible in Telegram, and enough to make a caption differ from itself.
PAD = "\u200b"
MAX_PAD = 4


def caption_for(file_name: str) -> str:
    """The caption deliver.yml would have written for this document."""
    d = edition_date(file_name)
    return f"Daily Economic Briefing — {d if d else Path(file_name).stem}"


def recall_from_chat(call, chat_id, target_file, notice,
                     lookback=DEFAULT_LOOKBACK, dry_run=False):
    """Find and delete `target_file` in one chat. Returns a report dict.

    `call(method, payload)` returns Telegram's decoded response. It must not
    raise on an API-level error — an `{"ok": false, ...}` body is expected and
    is how the walk learns that an id is not ours.
    """
    report = {"chat": chat_id, "probed": 0, "found": None, "deleted": False,
              "restored": None, "note": ""}

    anchor = call("sendMessage", {"chat_id": chat_id, "text": notice})
    if not anchor.get("ok"):
        report["note"] = f"could not send the notice: {anchor.get('description', '?')}"
        return report
    anchor_id = anchor["result"]["message_id"]
    report["anchor"] = anchor_id

    for mid in range(anchor_id - 1, max(anchor_id - 1 - lookback, 0), -1):
        report["probed"] += 1
        # Pad until the caption genuinely differs from whatever is stored, so
        # "message is not modified" can never be mistaken for "not ours".
        for pad in range(1, MAX_PAD + 1):
            probe = call("editMessageCaption", {
                "chat_id": chat_id, "message_id": mid,
                "caption": caption_for(target_file) + PAD * pad,
            })
            if probe.get("ok") or "not modified" not in (
                    probe.get("description") or "").lower():
                break

        if not probe.get("ok"):
            # Not ours, not captioned, or older than Telegram will edit. The
            # subscriber's own messages land here and are never touched.
            continue

        doc = (probe.get("result") or {}).get("document") or {}
        name = doc.get("file_name") or ""
        report["found"] = {"message_id": mid, "file_name": name}

        if name == target_file:
            if dry_run:
                report["note"] = "would delete (dry run)"
                # Undo the padding. A rehearsal that leaves the caption
                # altered is what made the first real run skip this message.
                restore = call("editMessageCaption", {
                    "chat_id": chat_id, "message_id": mid,
                    "caption": caption_for(target_file),
                })
                report["restored"] = bool(restore.get("ok"))
                if not report["restored"]:
                    report["note"] += " — WARNING: could not undo the probe caption"
                return report
            gone = call("deleteMessage", {"chat_id": chat_id, "message_id": mid})
            report["deleted"] = bool(gone.get("ok"))
            if not report["deleted"]:
                report["note"] = f"delete refused: {gone.get('description', '?')}"
            return report

        # Wrong document — put its caption back from what Telegram just told
        # us, and stop rather than walking deeper into older briefings.
        restore = call("editMessageCaption", {
            "chat_id": chat_id, "message_id": mid, "caption": caption_for(name),
        })
        report["restored"] = bool(restore.get("ok"))
        report["note"] = (
            f"the most recent document in this chat is {name!r}, not "
            f"{target_file!r} — nothing deleted"
        )
        return report

    report["note"] = f"no document of ours in the last {lookback} message ids"
    return report


def mask(chat_id) -> str:
    """A chat id safe for a public log: enough to tell two chats apart."""
    s = str(chat_id)
    return f"…{s[-3:]}" if len(s) > 3 else "…"


def summarise(reports, target_file, dry_run):
    lines = [f"## Recall of `{target_file}`", ""]
    if dry_run:
        lines += ["**Dry run — nothing was deleted.**", ""]
    lines += ["| chat | probed | found | result |", "|---|---|---|---|"]
    for r in reports:
        found = r["found"]["file_name"] if r["found"] else "—"
        if r["deleted"]:
            result = "**deleted**"
        elif r["note"]:
            result = r["note"]
        else:
            result = "no action"
        lines.append(f"| `{mask(r['chat'])}` | {r['probed']} | `{found}` | {result} |")
    done = sum(1 for r in reports if r["deleted"])
    lines += ["", f"Deleted from **{done} of {len(reports)}** chats.",
              "", "Telegram only lets a bot delete its own messages for 48 hours. "
              "After that the message can no longer be removed from a subscriber's "
              "chat by any means available here."]
    return "\n".join(lines)


def main() -> int:
    import argparse
    import json
    import os
    import time
    import urllib.error
    import urllib.parse
    import urllib.request

    ap = argparse.ArgumentParser()
    ap.add_argument("--file-name", required=True,
                    help="exact document file_name to delete, e.g. "
                         "Daily_Economic_Briefing_20260907.pdf")
    ap.add_argument("--notice", required=True,
                    help="the correction message sent to each chat; it is also "
                         "the anchor the walk counts back from")
    ap.add_argument("--chats", required=True,
                    help="comma-separated chat ids")
    ap.add_argument("--lookback", type=int, default=DEFAULT_LOOKBACK)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--summary", default="")
    args = ap.parse_args()

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        print("::error::TELEGRAM_BOT_TOKEN is not set.")
        return 1

    def call(method, payload):
        url = f"https://api.telegram.org/bot{token}/{method}"
        data = urllib.parse.urlencode(payload).encode()
        try:
            with urllib.request.urlopen(url, data=data, timeout=30) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as exc:
            # Telegram returns the real reason in the body of a 4xx, and the
            # walk depends on reading it rather than on the status code.
            try:
                return json.loads(exc.read())
            except Exception:
                return {"ok": False, "description": f"HTTP {exc.code}"}
        except Exception as exc:
            return {"ok": False, "description": str(exc)}

    chats = [c.strip() for c in args.chats.split(",") if c.strip()]
    if not chats:
        print("::error::No chats given.")
        return 1

    reports = []
    for i, chat in enumerate(chats):
        rep = recall_from_chat(call, chat, args.file_name, args.notice,
                               lookback=args.lookback, dry_run=args.dry_run)
        reports.append(rep)
        print(f"  {mask(chat)}: probed {rep['probed']}, "
              f"deleted={rep['deleted']}{', ' + rep['note'] if rep['note'] else ''}")
        if i < len(chats) - 1:
            time.sleep(1)  # stay inside Telegram's bulk limits

    text = summarise(reports, args.file_name, args.dry_run)
    print(text)
    if args.summary:
        with open(args.summary, "a", encoding="utf-8") as fh:
            fh.write(text + "\n")

    # Never fails the job on a chat that could not be reached: the remaining
    # chats still need their copy removed, and the table says which is which.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
