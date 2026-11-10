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

Nothing moves from pending to approved on its own, except a payment. That separation is the
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
import io
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

import entitlement

REPO = Path(__file__).resolve().parent.parent
STORE = REPO / "subscribers.json"

EMPTY = {"approved": [], "pending": [], "unsubscribed": [], "last_update_id": 0}

# ---------------------------------------------------------------------------
# Keeping chat ids out of public logs
# ---------------------------------------------------------------------------
# Chat ids are the personal data that moving the list to Cloudflare KV existed
# to protect. This repository is public, and so is every Actions log and run
# summary it produces, so an id reaching stdout, stderr or $GITHUB_STEP_SUMMARY
# is published as surely as one committed to git. The move to KV fixed the
# store and left this path open.
#
# Masking happens at the OUTPUT BOUNDARY rather than where each note is built.
# There are some forty places a chat id is formatted into a string, and a fix
# applied to each is a fix that the next note added forgets. Wrapping the three
# sinks instead covers whatever is written through them, now and later.
#
# Two things must keep their real ids, and both deliberately bypass this:
#   - the "recipients" action's stdout, which deliver.yml reads with mapfile to
#     address the sends. Masking it would deliver to nobody. It is not logged:
#     the workflow consumes it through a process substitution.
#   - the reply and notice payloads, whose "chat_id" routes a Telegram message
#     and whose text the owner reads privately to decide whom to approve. They
#     are written as JSON to a file for send_replies.sh, never printed.
# This is the policy process() already states for display names — "only to the
# owner's private chat, never to a public log" — applied to ids as well.

_ID_RE = re.compile(r"\d{6,}")


def mask(chat_id) -> str:
    """A chat id safe for a public log: enough to tell two chats apart."""
    s = str(chat_id)
    return f"…{s[-3:]}" if len(s) > 3 else "…"


def scrub(text: str) -> str:
    """Mask every chat id in free text.

    Six digits or more, so a year, a port or a four-digit count survives and
    only something id-shaped is touched; Telegram ids are nine or ten. A
    negative group id keeps its minus sign, which is worth seeing — the digits
    are what identify the chat.

    Assumes an id is formatted into a string whole, which is true of every
    f-string and of print()'s per-argument writes; nothing here builds a number
    a digit at a time.
    """
    return _ID_RE.sub(lambda m: mask(m.group()), text)


class _ScrubbedStream(io.TextIOBase):
    """A text stream that masks chat ids on the way out."""

    def __init__(self, stream):
        self._stream = stream

    def write(self, text: str) -> int:
        self._stream.write(scrub(text))
        return len(text)

    def flush(self) -> None:
        self._stream.flush()

    @property
    def encoding(self) -> str:
        return getattr(self._stream, "encoding", "utf-8")


# The "recipients" and "commands" actions put machine-readable text on stdout —
# ids for mapfile, JSON for setMyCommands — so stdout is left alone for those.
# Their stderr is still a log and is still masked.
RAW_STDOUT_ACTIONS = {"recipients", "commands"}


def write_public(path: str, text: str) -> None:
    """Append to a run summary, with chat ids masked."""
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(scrub(text))

# /subscribe and /unsubscribe are accepted alongside the conventional Telegram
# commands because people type what they mean, not what the bot documents.
COMMANDS = {
    "/start": "start", "/subscribe": "start",
    "/stop": "stop", "/unsubscribe": "stop",
}

# Everything the bot ever says, in one place, because these are the only part of
# the system a subscriber sees. Kept deliberately plain: they are read by people
# who did not ask for an explanation of how the pipeline works.
MSG = {
    "pending": "Your request for subscription is pending.",
    "approved": "Your request for subscription has been approved.",
    "stopped": ("We have received your unsubscribe request. "
                "Please give us time to process it."),
    "already-subscribed": "You are already subscribed. Send /stop to unsubscribe.",
    "owner-stop": ("You are the owner of this briefing. Your own copy is configured "
                   "in the repository, not by this bot, so it will keep arriving."),
    # Sent by the Worker the moment Stripe confirms, not at the next drain:
    # someone who has just paid and hears nothing for five minutes assumes it
    # failed. Duplicated in worker/src/index.js because the Worker cannot
    # fetch this file and still answer instantly; test_subscribers.py compares
    # the two so they cannot drift.
    "paid": ("Payment received — thank you. Your subscription runs for a year "
             "from today, and the next briefing is on its way."),
    "cancelled": ("Your subscription will not renew. You keep receiving the "
                  "briefing until the year you have paid for runs out."),

    # --- the paywall -------------------------------------------------------
    # These carry {placeholders}, filled by fill() here and by the same
    # substitution in the Worker. The drift test compares the RAW templates,
    # so the two sides cannot diverge even though each fills them its own way.
    "trial": ("You are on a free trial — the next {n} editions are yours, "
              "starting with the next one. After that it is $4.99 for a year: "
              "{link}"),
    # Deliberately says nothing about how many trial editions are left. Only
    # the delivery side can count those (they are counted out of git), and the
    # Worker answers before any of that is in reach. Saying "you are already
    # on the list" is true whether the trial is running or spent, and the
    # notices sweep tells them precisely when it does run out.
    "signed-up": ("You are already on the list. A year of the briefing is "
                  "$4.99 whenever you want it: {link}"),
    "pay": ("Your free editions are used up. A year of the briefing is $4.99: "
            "{link}"),
    # The answer to /checkout, which is a deliberate request for the link
    # rather than a consequence of something else happening.
    # No {link}: the Worker sends this with a button carrying the Payment Link,
    # so a URL in the body would be the same destination twice.
    "checkout": ("A year of the briefing is $4.99, and it starts with the next "
                 "edition. Tap below to subscribe."),
    "lapsed": ("Your subscription has ended, so the briefing has stopped. A "
               "year is $4.99 whenever you want it back: {link}"),
    "reminder": ("Your subscription renews in {n} day(s) at $4.99. It renews "
                 "automatically — nothing to do. Send /stop if you would "
                 "rather it did not."),
    "comp-applied": ("Code accepted — you are subscribed for a year. "
                     "Thank you."),
    "comp-bad": ("That code is not valid. If you think it should be, reply and "
                 "the owner will take a look."),

    # --- billing self-service ----------------------------------------------
    # Removing someone from the delivery list does not cancel what Stripe is
    # charging them. Without these they would stop receiving the briefing and
    # keep paying for it, which is the worst of both.
    "portal": ("Manage your subscription — update your card, see invoices, "
               "or cancel: {link}"),
    "stopped-billing": ("We have received your unsubscribe request. Please give "
                        "us time to process it. Your subscription is still "
                        "active with Stripe, so cancel it here to stop being "
                        "billed: {link}"),
    "portal-unavailable": ("I could not open the billing page just now. Reply "
                           "here and the owner will cancel it for you."),
}


# The command menu Telegram shows, for setMyCommands. Kept here, beside
# COMMANDS and OWNER_COMMANDS, so a command cannot be added to the bot without
# its menu entry being one line away — and so the descriptions a subscriber
# reads live next to the replies they get.
#
# Only canonical names are listed. /subscribe, /unsubscribe and /billing keep
# working as aliases but are left out: three ways to do the same thing in one
# menu reads as three different features.
#
# (command, description, owner_only, needs_paywall)
CMD_TEXT = {
    "start": "Subscribe to the daily briefing",
    "stop": "Stop receiving the briefing",
    "promo": "Redeem a promo code",
    "checkout": "Subscribe for $4.99 a year",
    "manage": "Update your card, see invoices, or cancel",
    "approve": "Owner: approve a chat by id",
    "deny": "Owner: deny or remove a chat by id",
    "pending": "Owner: list chats awaiting approval",
    "status": "Owner: subscriber counts",
}

# The menu depends on how far a chat has got, because being offered a command
# that then refuses you is worse than never being offered it. Telegram supports
# this directly: setMyCommands takes a scope, and a chat-scoped list replaces
# the default one for that chat alone.
#
#   new      the default scope, and anyone who has stopped — just /start
#   started  after /start, with no paid subscription yet
#   paid     after a checkout completes
#   owner    the owner's own chat
#
# Who publishes which: the Worker sets a chat's own menu as that chat changes,
# because it is the only part that hears from Telegram in real time. The
# commands workflow sets the default and owner scopes, and re-states every
# known subscriber's menu — which is also what migrates the chats that were
# already subscribed before any of this existed.
#
# Mirrored in worker/src/index.js; test_subscribers.py compares the two so the
# two copies cannot drift.
MENUS = {
    "new": ["start"],
    "started": ["promo", "checkout", "stop"],
    "paid": ["manage", "stop"],
    "owner": ["start", "stop", "promo", "checkout", "manage",
              "approve", "deny", "pending", "status"],
}

# Without PAY_URL there is nothing to sell, no code to redeem against a price
# and no card to manage, so these three return without replying. Hiding them
# until it is set keeps the menu honest about what the bot will actually do.
PAYWALL_ONLY = {"promo", "checkout", "manage"}


def bot_commands(paywall: bool = False, owner: bool = False,
                 tier: str = "new") -> list:
    """Menu entries for one Telegram scope.

    `owner` selects the owner's menu whatever `tier` says, since the owner's
    chat is a scope of its own. Otherwise `tier` picks one of MENUS.
    """
    names = MENUS["owner"] if owner else MENUS[tier]
    return [{"command": n, "description": CMD_TEXT[n]}
            for n in names if paywall or n not in PAYWALL_ONLY]


def tier_for(entry: dict) -> str:
    """Which menu this subscriber should see.

    Keyed on having paid rather than on entitlement: someone whose year has
    run out still has a card and invoices to manage, so /manage stays. A comp
    is deliberately not "paid" — there is no Stripe customer behind it, so the
    billing portal would have nothing to open.
    """
    billing = (entry.get("stripe_customer_id")
               or entry.get("plan") in ("paid", "cancelled"))
    return "paid" if billing else "started"


def fill(outcome: str, **kw) -> str:
    """A message with its placeholders filled.

    Unknown placeholders are left as they are rather than raising: a missing
    link is a cosmetic flaw in one message, and an exception here would stop
    the whole sweep sending anything to anybody.
    """
    text = MSG[outcome]
    for key, value in kw.items():
        text = text.replace("{" + key + "}", str(value))
    return text

# What the owner can do from the chat itself, so approving does not mean opening
# GitHub on a phone. Honoured only from the owner's own chat — see
# owner_requests() for why the chat id is sufficient authorisation.
OWNER_COMMANDS = {
    "/approve": "approve", "/deny": "deny",
    "/pending": "pending", "/status": "status",
}

# Replies are either about one chat's own subscription state, in which case only
# the last one that morning should be sent, or a note to the owner, in which case
# every one matters. Without this split, telling the owner about a new request
# and answering their /pending in the same sweep would lose one of the two.
STATE_OUTCOMES = {"pending", "approved", "stopped", "already-subscribed"}


def norm(data: dict) -> dict:
    """Fill in anything a hand-edit or an older file is missing."""
    for key, blank in EMPTY.items():
        data.setdefault(key, type(blank)())
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
        # The highest Telegram update already handled. This is what makes every
        # message act exactly once: the poller asks for offset = this + 1, and
        # process() ignores anything at or below it even if Telegram sends it
        # again. Without it, a poller running every few minutes would re-read the
        # same /start out of Telegram's 24-hour backlog and answer it on every
        # pass — roughly 288 identical messages a day to one person.
        "last_update_id": data["last_update_id"],
    }
    path.write_text(json.dumps(ordered, indent=2) + "\n", encoding="utf-8")


def ids(entries: list) -> set:
    return {e["chat_id"] for e in entries}


def reply(chat_id: int, outcome: str) -> dict:
    """One message for the send step: who, why, and what to say."""
    return {"chat_id": chat_id, "outcome": outcome, "text": MSG[outcome]}


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


def messages(updates: dict):
    """Every update that carries a chat, as (chat_id, type, text)."""
    for u in updates.get("result", []):
        msg = u.get("message") or u.get("channel_post") or u.get("edited_message") or {}
        chat = msg.get("chat") or {}
        cid = chat.get("id")
        if cid is not None:
            yield cid, chat.get("type", "?"), (msg.get("text") or "").strip()


def commands_from_updates(updates: dict) -> list:
    """The /start and /stop requests in a payload, at most one per chat.

    Later messages win, so a chat that sends /stop and then changes its mind
    with /start in the same 24-hour window ends up asking to join, not to
    leave. Telegram writes commands as `/stop@TheBot` in groups, hence the
    split on '@'.
    """
    latest = {}
    for cid, ctype, text in messages(updates):
        if not text.startswith("/"):
            continue
        verb = COMMANDS.get(text.split()[0].split("@")[0].lower())
        if verb:
            latest[cid] = {"chat_id": cid, "type": ctype, "command": verb}
    return list(latest.values())


def owner_requests(updates: dict, owner: int | None) -> tuple[list, list, list]:
    """The owner's instructions, in the order they were sent.

    Returns (accepted, rejected, unknown).

    Unlike /start and /stop these are NOT reduced to one per chat: the owner may
    well send `/approve 222` and then `/approve 333`, and both must be applied.

    Authorisation is the chat id alone, and that is sound rather than lazy —
    Telegram asserts the id in the payload, the sender cannot set it, and the
    owner's id comes from a repository secret no message can influence. A
    command from anyone else is returned in `rejected` rather than dropped
    silently, because someone probing for an admin interface is worth seeing in
    the log.
    """
    accepted, rejected, unknown = [], [], []
    for cid, _ctype, text in messages(updates):
        if not text.startswith("/"):
            continue
        head = text.split()[0].split("@")[0].lower()
        verb = OWNER_COMMANDS.get(head)
        if not verb:
            if head not in COMMANDS:
                unknown.append({"chat_id": cid, "command": head})
            continue
        if owner is None or cid != owner:
            rejected.append({"chat_id": cid, "command": verb})
            continue
        args, bad = [], []
        for tok in text.split()[1:]:
            try:
                args.append(int(tok.strip(",")))
            except ValueError:
                bad.append(tok)
        accepted.append({"command": verb, "ids": args, "unparsed": bad})
    return accepted, rejected, unknown


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


def sizes(data: dict) -> dict:
    return {k: len(data[k]) for k in ("approved", "pending", "unsubscribed")}


def apply_queue(items: list, data: dict, owner: int | None) -> tuple[dict, list]:
    """Apply decisions the webhook Worker has already answered.

    The Worker replies to people in milliseconds and queues what it decided;
    this brings the committed list into line afterwards. It therefore sends
    nothing — the sender was told at the time, and telling them again days later
    because a drain replayed would be worse than saying nothing.

    Every item must be idempotent, because the queue is at-least-once: items are
    handed out on read and deleted only after this has been committed, so a
    drain that dies mid-way replays. Deleting on read would instead lose an
    opt-out silently, which is the one outcome worth engineering against.

    Returns the store and one note per item, for the run log.
    """
    norm(data)
    notes = []
    for item in items:
        verb, cid = item.get("verb"), item.get("chat_id")
        ctype = item.get("type", "?")
        if not isinstance(cid, int) or verb not in (
                "start", "stop", "approve", "deny", "paid", "cancelled",
                "trial", "comp"):
            notes.append(f"{item.get('id', '?')}: ignored, not a decision I understand")
            continue

        if owner is not None and cid == owner:
            notes.append(f"{cid}: is the owner, skipped")
            continue

        if verb == "start":
            if cid in ids(data["approved"]):
                notes.append(f"{cid}: already approved, no change")
            else:
                data["unsubscribed"] = [e for e in data["unsubscribed"]
                                        if e["chat_id"] != cid]
                if cid in ids(data["pending"]):
                    notes.append(f"{cid}: already pending, no change")
                else:
                    data["pending"].append({"chat_id": cid, "type": ctype,
                                            "seen": date.today().isoformat()})
                    notes.append(f"{cid}: awaiting approval")

        elif verb in ("stop", "deny"):
            was = cid in ids(data["approved"]) | ids(data["pending"])
            # Carry the entry over rather than minting a bare one. It used to
            # build {chat_id, type, stopped} from scratch, which threw away
            # trial_started — so /stop then /start handed out another three
            # free editions, every time, for ever — and threw away paid_until
            # and the Stripe ids with it, so someone who had paid and opted
            # out came back looking like they never had.
            prior = next((e for e in data["approved"] + data["pending"]
                          if e["chat_id"] == cid), None)
            remove({cid}, data)
            if cid not in ids(data["unsubscribed"]):
                gone = dict(prior) if prior else {"chat_id": cid, "type": ctype}
                gone["stopped"] = date.today().isoformat()
                data["unsubscribed"].append(gone)
            notes.append(f"{cid}: {'removed and' if was else ''} opted out".replace("  ", " "))

        elif verb == "trial":
            # A /start under the paywall. Unlike "start", this enrols them
            # straight away: the trial IS the access, so leaving them pending
            # on an owner's approval would mean the three free editions never
            # arrive.
            #
            # trial_started is written once and never rewritten, which is the
            # whole defence against /stop then /start minting a second trial.
            # It is also why an already-trialled chat coming back is a no-op
            # here rather than a fresh grant.
            entry = next((e for e in data["approved"] if e["chat_id"] == cid), None)
            if entry is not None and entry.get("trial_started"):
                notes.append(f"{cid}: already had a trial, left as it was")
                continue
            if entry is not None and entry.get("paid_until"):
                notes.append(f"{cid}: already has paid access, no trial given")
                continue

            prior = next((e for e in data["pending"] + data["unsubscribed"]
                          if e["chat_id"] == cid), None)
            if prior is not None and prior.get("trial_started"):
                # They trialled, left, and are back. The spent trial follows
                # them rather than being forgotten on the way out.
                started = prior["trial_started"]
            else:
                started = date.today().isoformat()

            data["pending"] = [e for e in data["pending"] if e["chat_id"] != cid]
            data["unsubscribed"] = [e for e in data["unsubscribed"]
                                    if e["chat_id"] != cid]
            if entry is None:
                entry = {"chat_id": cid, "type": ctype,
                         "added": date.today().isoformat()}
                data["approved"].append(entry)
            entry["trial_started"] = started
            entry.setdefault("plan", "trial")
            notes.append(f"{cid}: trial from {started}")

        elif verb == "comp":
            # A free code redeemed in the bot. Discounts go through Stripe;
            # only 100%-free comps come this way, so there is no money to
            # reconcile and nothing to verify beyond the code itself, which
            # the Worker has already checked.
            code = item.get("code", "?")
            years = item.get("years", 1)
            entry = next((e for e in data["approved"] if e["chat_id"] == cid), None)
            if entry is not None and entry.get("last_comp_code") == code:
                notes.append(f"{cid}: comp {code} already applied, no change")
                continue
            if entry is None:
                prior = next((e for e in data["pending"] + data["unsubscribed"]
                              if e["chat_id"] == cid), None)
                entry = dict(prior) if prior else {"chat_id": cid, "type": ctype}
                entry.pop("stopped", None)
                entry.pop("seen", None)
                entry.setdefault("added", date.today().isoformat())
                data["pending"] = [e for e in data["pending"] if e["chat_id"] != cid]
                data["unsubscribed"] = [e for e in data["unsubscribed"]
                                        if e["chat_id"] != cid]
                data["approved"].append(entry)
            entitlement.grant(entry, date.today(), "comp", years)
            entry["last_comp_code"] = code
            notes.append(f"{cid}: comp {code}, access through {entry['paid_until']}")

        elif verb == "paid":
            # Payment auto-approves, by decision: someone who has just paid
            # should not then wait on a human. The owner's Approve/Deny
            # buttons stay for comps and for anything that arrives without a
            # payment.
            #
            # Idempotency here is not the usual "applying twice is a no-op" —
            # applying twice would grant two years. The Stripe event id is
            # recorded on the entry and a replay of the same event is skipped,
            # which matters because the queue is at-least-once by design.
            event_id = item.get("event_id")
            years = item.get("years", 1)

            entry = next((e for e in data["approved"] if e["chat_id"] == cid), None)
            if entry is None:
                entry = next((e for e in data["pending"] if e["chat_id"] == cid), None)
                if entry is None:
                    entry = next((e for e in data["unsubscribed"]
                                  if e["chat_id"] == cid), None)
                    if entry is not None:
                        entry = dict(entry)
                        entry.pop("stopped", None)
                if entry is None:
                    entry = {"chat_id": cid, "type": ctype}
                else:
                    entry = dict(entry)
                entry.setdefault("added", date.today().isoformat())
                data["pending"] = [e for e in data["pending"] if e["chat_id"] != cid]
                data["unsubscribed"] = [e for e in data["unsubscribed"]
                                        if e["chat_id"] != cid]
                data["approved"].append(entry)

            if event_id and entry.get("last_payment_event") == event_id:
                notes.append(f"{cid}: payment {event_id} already applied, no change")
                continue

            entitlement.grant(entry, date.today(), "paid", years)
            if event_id:
                entry["last_payment_event"] = event_id
            for key in ("stripe_customer_id", "stripe_subscription_id"):
                if item.get(key):
                    entry[key] = item[key]
            notes.append(f"{cid}: paid, access through {entry['paid_until']}")

        elif verb == "cancelled":
            # Stops the renewal. Deliberately does NOT revoke: they paid for a
            # year, and cancelling does not buy back the months already paid
            # for. paid_until is left exactly as it is and simply runs out.
            entry = next((e for e in data["approved"] if e["chat_id"] == cid), None)
            if entry is None:
                notes.append(f"{cid}: cancelled, but not on the list — no change")
            elif entry.get("plan") == "cancelled":
                notes.append(f"{cid}: already marked cancelled, no change")
            else:
                entry["plan"] = "cancelled"
                notes.append(f"{cid}: will not renew, access runs to "
                             f"{entry.get('paid_until', 'its existing expiry')}")

        elif verb == "approve":
            data["unsubscribed"] = [e for e in data["unsubscribed"] if e["chat_id"] != cid]
            if cid in ids(data["approved"]):
                notes.append(f"{cid}: already approved, no change")
            else:
                entry = next((e for e in data["pending"] if e["chat_id"] == cid), None)
                data["pending"] = [e for e in data["pending"] if e["chat_id"] != cid]
                # Approving a chat that never asked is still honoured here: the
                # owner tapped Approve on a real request, and the /start that
                # created it may simply not have been drained yet.
                data["approved"].append({"chat_id": cid,
                                         "type": (entry or {}).get("type", ctype),
                                         "added": date.today().isoformat()})
                notes.append(f"{cid}: now receiving the briefing")

    return data, notes


def process(updates: dict, data: dict, owner: int | None) -> tuple[dict, list, list, dict]:
    """Record new chats, act on /start and /stop, then on the owner's commands.

    Returns the store, the sync report, the replies to send, and a diagnostic
    record of everything that happened — every update classified, every command
    accepted, rejected or not understood, and the list sizes before and after.
    When this misbehaves it will be at 07:20 on someone else's phone, so the run
    log has to explain itself without a re-run.

    Ordering is deliberate, and it is the whole of the logic:

      1. sync        — an unseen chat becomes a candidate
      2. /start,/stop — the chat's own wishes, latest message winning
      3. owner       — /approve and /deny, which override the above

    So a /start and the owner's /approve arriving in the same 24-hour window are
    resolved in one sweep, and the subscriber is told only the outcome rather
    than "pending" followed immediately by "approved".
    """
    norm(data)
    before = sizes(data)

    # Act on each update once and only once. The poller asks Telegram for
    # offset = last_update_id + 1, but this filter is what actually guarantees
    # it: an offset that fails to stick, a retry, or a second reader would
    # otherwise replay the backlog and re-answer every message in it.
    seen = data["last_update_id"]
    incoming = updates.get("result", [])
    all_ids = [u["update_id"] for u in incoming if isinstance(u.get("update_id"), int)]

    def is_fresh(u):
        uid = u.get("update_id")
        # An update with no usable id cannot be de-duplicated. Process it and
        # risk a repeated reply rather than drop it: a duplicate confirmation is
        # a nuisance, an opt-out that vanished is a person still being messaged
        # after they asked us to stop.
        return not isinstance(uid, int) or uid > seen

    fresh = {"result": [u for u in incoming if is_fresh(u)]}
    skipped = len(incoming) - len(fresh["result"])
    highest = max(all_ids + [seen])

    updates = fresh
    data, report = sync(updates, data, owner)
    state, info, diag_cmds = {}, [], []

    def set_state(cid, outcome):
        state[cid] = reply(cid, outcome)

    # --- 2. the subscribers' own requests -------------------------------------
    for req in commands_from_updates(updates):
        cid, verb = req["chat_id"], req["command"]

        if owner is not None and cid == owner:
            # The owner's copy comes from a repository secret, which no message
            # can change. Say so rather than appearing to comply.
            if verb == "stop":
                info.append(reply(cid, "owner-stop"))
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
            set_state(cid, "stopped")
        else:
            data["unsubscribed"] = [e for e in data["unsubscribed"] if e["chat_id"] != cid]
            if cid in ids(data["approved"]):
                set_state(cid, "already-subscribed")
            else:
                if cid not in ids(data["pending"]):
                    data["pending"].append(
                        {"chat_id": cid, "type": req["type"],
                         "seen": date.today().isoformat()}
                    )
                set_state(cid, "pending")

    # --- 3. the owner's instructions ------------------------------------------
    accepted, rejected, unknown = owner_requests(updates, owner)
    for cmd in accepted:
        verb, targets = cmd["command"], cmd["ids"]
        outcome = {"command": verb, "ids": targets, "unparsed": cmd["unparsed"], "notes": []}

        if verb == "approve":
            told = []
            notes = approve(set(targets), data, owner, replies=told)
            outcome["notes"] = [f"{c}: {n}" for c, n in notes]
            for r in told:
                # Replaces any "pending" queued for this chat a moment ago.
                set_state(r["chat_id"], "approved")
        elif verb == "deny":
            outcome["notes"] = [f"{c}: {n}" for c, n in remove(set(targets), data, remember=True)]
            # Deliberately silent to the subscriber. "You were refused" helps
            # nobody, and denial is also how obvious spam is cleared.
        elif verb in ("pending", "status"):
            s = sizes(data)
            pend = ", ".join(str(e["chat_id"]) for e in data["pending"]) or "none"
            body = (f"Approved: {s['approved']}. Awaiting approval: {s['pending']}. "
                    f"Opted out: {s['unsubscribed']}.")
            if verb == "pending":
                body += (f"\nPending ids: {pend}"
                         f"\nReply /approve <id> to enable, /deny <id> to refuse.")
            info.append({"chat_id": owner, "outcome": f"owner-{verb}", "text": body})
            outcome["notes"] = [body.replace("\n", " | ")]

        diag_cmds.append(outcome)

    # Tell the owner who is waiting, with the display name, so the decision can
    # be made in the chat rather than against a bare number. This is the one
    # place a subscriber's name is used, and it goes only to the owner's private
    # chat — never to the store, never to a public log.
    #
    # Built last, and filtered to chats still pending, so the owner is not asked
    # to consider somebody who unsubscribed or was approved in this same sweep.
    still_waiting = ids(data["pending"])
    newcomers = [r for r in report if r["state"] == "new" and r["chat_id"] in still_waiting]
    if owner is not None and newcomers:
        lines = [f"{r['label']} — chat {r['chat_id']} ({r['type']})" for r in newcomers]
        info.append({"chat_id": owner, "outcome": "owner-new-requests", "text":
                     f"{len(newcomers)} new subscription request(s):\n"
                     + "\n".join(lines)
                     + "\n\nReply /approve <id> to enable, /deny <id> to refuse, "
                       "/pending to list everyone waiting."})

    data["last_update_id"] = highest

    diag = {
        "updates": len(updates.get("result", [])),
        "skipped_already_handled": skipped,
        "last_update_id": highest,
        "chats_seen": len(report),
        "states": {s: sum(1 for r in report if r["state"] == s)
                   for s in {r["state"] for r in report}},
        "owner_commands": diag_cmds,
        "rejected_commands": rejected,
        "unknown_commands": unknown,
        "before": before,
        "after": sizes(data),
    }
    return data, report, list(state.values()) + info, diag


def approve(targets: set, data: dict, owner: int | None,
            replies: list | None = None) -> list:
    """Move chats from pending to approved. Returns one note per target.

    Pass `replies` to collect the "approved" confirmation for each chat that
    actually changed state, so the caller can tell them. Only a real transition
    produces one — re-approving someone already on the list must not message
    them again every time the owner runs the workflow.
    """
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
            if replies is not None:
                replies.append(reply(cid, "approved"))
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


def notices(data: dict, today, edition_dates=(), link: str = "") -> list:
    """Messages owed to subscribers about their own access.

    Two kinds, and each is sent exactly once:

      reminder  a renewal falls inside the next REMIND_DAYS
      lapsed    access has run out, grace included, so delivery has stopped

    Called from the five-minute sweep, which means "exactly once" cannot rest
    on the schedule — it would otherwise send every five minutes for a week.
    So the entry records which expiry it has already spoken about:
    reminded_for and lapsed_for hold the paid_until (or the trial start) the
    message was about. A renewal moves paid_until, which makes the marker
    stale and lets next year's reminder through on its own.

    Mutates `data` and returns reply dicts for send_replies.sh.
    """
    out = []
    for e in sorted(data["approved"], key=lambda x: x["chat_id"]):
        st = entitlement.status(e, today, edition_dates)

        if st["state"] == "lapsed":
            about = e.get("paid_until") or e.get("trial_started") or "?"
            if e.get("lapsed_for") != about:
                e["lapsed_for"] = about
                out.append({"chat_id": e["chat_id"], "outcome": "lapsed",
                            "text": fill("lapsed", link=link)})
            continue

        # Only a real renewal gets a reminder. A trial has nothing to renew,
        # and a cancelled subscription is not going to renew either — telling
        # someone who has already cancelled that it renews automatically
        # would be straightforwardly false.
        if entitlement.expiring(e, today) and e.get("plan") != "cancelled":
            about = e["paid_until"]
            if e.get("reminded_for") != about:
                e["reminded_for"] = about
                days = (entitlement.as_date(about) - today).days
                out.append({"chat_id": e["chat_id"], "outcome": "reminder",
                            "text": fill("reminder", n=days)})
    return out


def grandfather(data: dict, today, years: int = 1) -> list:
    """Give every approved chat that has no entitlement yet a free year.

    The one-off migration onto the paywall. Only touches entries with neither
    paid_until nor trial_started, so it is idempotent: running it twice does
    not extend anyone, and it cannot overwrite a real payment that has landed
    in between.
    """
    notes = []
    for e in sorted(data["approved"], key=lambda x: x["chat_id"]):
        if e.get("paid_until") or e.get("trial_started"):
            notes.append(f"…{str(e['chat_id'])[-3:]} already has access, left alone")
            continue
        entitlement.grant(e, today, "grandfathered", years)
        notes.append(f"…{str(e['chat_id'])[-3:]} granted free access "
                     f"to {e['paid_until']}")
    return notes


def recipients(data: dict, owner: int | None,
               today=None, edition_dates=()) -> list:
    """Delivery list, owner first, filtered by entitlement.

    The owner leads so that the send loop can upload the PDF once to a chat
    that is certain to exist, then forward the resulting file_id to everyone
    else. Ordering is also why a failed owner delivery is the one that fails
    the job: if that send fails, nothing else can be attempted cheaply. The
    owner is never subject to the paywall — they are the sender.

    Approved chats are filtered through entitlement.entitled(). Being approved
    now means "asked for it and was let in"; being entitled means "has paid,
    is on trial, or is inside the grace window". Both are required.

    `today` and `edition_dates` default to no filtering at all, so a caller
    that has not been taught about entitlement yet keeps the old behaviour
    rather than silently delivering to nobody. Only deliver.yml passes them,
    and it is the only caller whose answer matters.
    """
    out = []
    if owner is not None:
        out.append(owner)

    approved = [e for e in data["approved"] if e["chat_id"] != owner]
    if today is None:
        out += [e["chat_id"] for e in approved]
        return out

    out += [e["chat_id"] for e in approved
            if entitlement.entitled(e, today, edition_dates)]
    return out


def entitlement_report(data: dict, owner: int | None, today, edition_dates=()):
    """Every approved chat with why it will or will not receive the edition.

    Separate from recipients() because the delivery log needs to say what it
    decided and why. A recipient count alone cannot distinguish "nobody has
    paid" from "the paywall is broken", and those need opposite responses.
    """
    rows = []
    for e in sorted(data["approved"], key=lambda x: x["chat_id"]):
        if e["chat_id"] == owner:
            continue
        st = entitlement.status(e, today, edition_dates)
        rows.append({"chat_id": e["chat_id"], "plan": e.get("plan") or "—", **st})
    return rows


def write_step_summary(diag: dict, data: dict, replies: list) -> None:
    """Put the sweep on the run's summary page, beside the stage table.

    The log already says everything, but nobody reads a log for a run that
    succeeded — and a subscription that silently did not happen looks exactly
    like a run that succeeded.
    """
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not path:
        return
    b, a = diag["before"], diag["after"]
    out = ["## Subscriptions", "",
           f"{diag['updates']} update(s) from {diag['chats_seen']} chat(s).", "",
           "| list | before | after |", "|---|---|---|"]
    for key, label in (("approved", "approved"), ("pending", "awaiting approval"),
                       ("unsubscribed", "opted out")):
        arrow = "" if b[key] == a[key] else " ←"
        out.append(f"| {label} | {b[key]} | **{a[key]}**{arrow} |")

    if diag["owner_commands"]:
        out += ["", "**Owner commands**", ""]
        for c in diag["owner_commands"]:
            arg = " ".join(str(i) for i in c["ids"])
            out.append(f"- `/{c['command']}{' ' + arg if arg else ''}`")
            out += [f"  - {n}" for n in c["notes"]]
            if c["unparsed"]:
                out.append(f"  - **ignored, not a chat id:** {', '.join(c['unparsed'])}")

    # Only what was queued. send_replies.sh appends the delivery result for each
    # one, which is the table worth reading — listing them twice would invite
    # mistaking "queued" for "sent".
    if replies:
        out += ["", f"{len(replies)} message(s) queued: "
                + ", ".join(sorted(r["outcome"] for r in replies)) + "."]

    if diag["rejected_commands"]:
        out += ["", "**Owner-only commands from other chats — ignored**", ""]
        out += [f"- `/{r['command']}` from `{r['chat_id']}`" for r in diag["rejected_commands"]]

    if data["pending"]:
        out += ["", "**Awaiting your approval:** "
                + ", ".join(f"`{e['chat_id']}`" for e in data["pending"])
                + " — reply `/pending` to the bot, or use the `approve` input on "
                  "*Find my Telegram chat ID*."]

    write_public(path, "\n".join(out) + "\n")


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
    ap.add_argument("action",
                    choices=["sync", "process", "drain", "approve", "remove",
                             "recipients", "grandfather", "notices",
                             "commands"])
    ap.add_argument("targets", nargs="?", default="", help="chat ids, comma or space separated")
    ap.add_argument("--updates", help="a getUpdates JSON payload (sync, process)")
    ap.add_argument("--replies", help="write the confirmations to send here (process)")
    ap.add_argument("--store", default=str(STORE))
    ap.add_argument("--editions", default="",
                    help="directory of edition PDFs; makes 'recipients' apply "
                         "the paywall. Without it every approved chat is "
                         "returned, as before the paywall existed.")
    ap.add_argument("--today", default="", help="override today's date (testing)")
    ap.add_argument("--paywall", action="store_true",
                    help="include the commands that only work once PAY_URL is set")
    ap.add_argument("--report", default="",
                    help="write the per-chat entitlement table here (recipients)")
    args = ap.parse_args()

    # From here on, anything printed is a public Actions log. See "Keeping chat
    # ids out of public logs" above for why this is done here and not at each
    # of the ~40 places an id is formatted, and for the two paths left raw.
    sys.stderr = _ScrubbedStream(sys.stderr)
    if args.action not in RAW_STDOUT_ACTIONS:
        sys.stdout = _ScrubbedStream(sys.stdout)

    store = Path(args.store)
    data = load(store)
    owner = owner_id()

    if args.action == "commands":
        # Every scope at once, so the caller cannot set one and forget another
        # and leave the menus out of step with each other.
        #
        # "chats" carries one entry per approved subscriber, which does two
        # jobs: it migrates the chats that subscribed before per-chat menus
        # existed — they have no chat-scoped list, so they would otherwise fall
        # back to the default one and see only /start — and re-running it
        # repairs any chat whose menu the Worker failed to publish.
        chats = [{"chat_id": e["chat_id"], "tier": tier_for(e),
                  "commands": bot_commands(paywall=args.paywall,
                                           tier=tier_for(e))}
                 for e in data["approved"]
                 if owner is None or e["chat_id"] != owner]
        print(json.dumps({
            "default": bot_commands(paywall=args.paywall, tier="new"),
            "owner": bot_commands(paywall=args.paywall, owner=True),
            "chats": chats,
        }, indent=2))
        return 0

    if args.action == "notices":
        today = date.fromisoformat(args.today) if args.today else date.today()
        edition_dates = []
        if args.editions:
            from pick_edition import edition_date
            edition_dates = [d for f in sorted(Path(args.editions).glob("*.pdf"))
                             if (d := edition_date(f))]
        link = (os.environ.get("PAY_URL") or "").strip()
        replies = notices(data, today, edition_dates, link)
        save(data, store)
        if args.replies:
            Path(args.replies).write_text(json.dumps(replies), encoding="utf-8")
        kinds = {}
        for r in replies:
            kinds[r["outcome"]] = kinds.get(r["outcome"], 0) + 1
        print(f"{len(replies)} notice(s) to send"
              + (f": {kinds}" if kinds else ""))
        return 0

    if args.action == "grandfather":
        today = date.fromisoformat(args.today) if args.today else date.today()
        notes = grandfather(data, today)
        save(data, store)
        print(f"Grandfathered onto the paywall, as of {today}:")
        for n in notes:
            print(f"  {n}")
        return 0

    if args.action == "recipients":
        # The paywall applies only when --editions says where the editions
        # are. Omitting it is the old, unfiltered behaviour: a caller that has
        # not been taught about entitlement keeps working rather than
        # delivering to nobody, which is the failure that would go unnoticed.
        today = date.fromisoformat(args.today) if args.today else date.today()
        edition_dates = []
        if args.editions:
            import entitlement as _ent  # noqa: F401  (already imported; explicit here)
            from pick_edition import edition_date
            edition_dates = [d for f in sorted(Path(args.editions).glob("*.pdf"))
                             if (d := edition_date(f))]

        chosen = (recipients(data, owner, today, edition_dates) if args.editions
                  else recipients(data, owner))

        # stdout is the machine-readable part: one id per line, nothing else.
        for cid in chosen:
            print(cid)

        # Everything explanatory goes to the report file or stderr, so that
        # mapfile on stdout keeps seeing only ids.
        if args.editions:
            rows = entitlement_report(data, owner, today, edition_dates)
            lines = ["| chat | plan | state | why |", "|---|---|---|---|"]
            for r in rows:
                shown = f"…{str(r['chat_id'])[-3:]}"
                lines.append(f"| `{shown}` | {r['plan']} | "
                             f"{'**' + r['state'] + '**' if r['entitled'] else r['state']} "
                             f"| {r['detail']} |")
            table = "\n".join(lines)
            if args.report:
                Path(args.report).write_text(table + "\n", encoding="utf-8")
            n_ent = sum(1 for r in rows if r["entitled"])
            print(f"{len(edition_dates)} edition(s) on disk; {n_ent} of "
                  f"{len(rows)} subscriber(s) entitled", file=sys.stderr)
        return 0

    if args.action == "drain":
        # The webhook path. --updates holds the Worker's {"items": [...]} and
        # --replies is written with the ids to acknowledge, so nothing is
        # acknowledged that was not committed.
        if not args.updates:
            raise SystemExit("drain needs --updates (the queue JSON)")
        payload = json.loads(Path(args.updates).read_text(encoding="utf-8"))
        items = payload.get("items", payload if isinstance(payload, list) else [])
        before = sizes(data)
        data, notes = apply_queue(items, data, owner)
        save(data, store)
        if args.replies:
            Path(args.replies).write_text(
                json.dumps([i["id"] for i in items if "id" in i]), encoding="utf-8")

        a = sizes(data)
        print(f"\n{len(items)} queued decision(s) applied:")
        for n in notes:
            print(f"  {n}")
        print(f"\nLists: approved {before['approved']}->{a['approved']}, "
              f"pending {before['pending']}->{a['pending']}, "
              f"opted out {before['unsubscribed']}->{a['unsubscribed']}")
        print(f"The next edition goes to the owner plus {a['approved']} subscriber(s).")
        if data["pending"]:
            print("::notice::Awaiting approval: "
                  + ", ".join(str(e["chat_id"]) for e in data["pending"]))

        path = os.environ.get("GITHUB_STEP_SUMMARY")
        if path:
            out = ["## Subscriptions (webhook queue)", "",
                   f"{len(items)} decision(s) applied.", "",
                   "| list | before | after |", "|---|---|---|"]
            for k, label in (("approved", "receiving it"), ("pending", "awaiting approval"),
                             ("unsubscribed", "opted out")):
                arrow = "" if before[k] == a[k] else " ←"
                out.append(f"| {label} | {before[k]} | **{a[k]}**{arrow} |")
            if notes:
                out += ["", "**What changed**", ""] + [f"- {n}" for n in notes]
            out += ["", "Replies were sent by the Worker at the time each message "
                    "arrived; this step only brings the committed list into line."]
            write_public(path, "\n".join(out) + "\n")
        return 0

    if args.action == "process":
        # The daily path, run before the briefing is sent so that today's
        # opt-outs are honoured by today's edition.
        if not args.updates:
            raise SystemExit("process needs --updates")
        payload = json.loads(Path(args.updates).read_text(encoding="utf-8"))
        data, report, replies, diag = process(payload, data, owner)
        save(data, store)
        if args.replies:
            Path(args.replies).write_text(json.dumps(replies), encoding="utf-8")

        print(f"\n{diag['updates']} update(s) from {diag['chats_seen']} chat(s): "
              + (", ".join(f"{n} {s}" for s, n in sorted(diag["states"].items())) or "none"))

        for r in report:
            print(f"  [{r['state']:>12}] {r['chat_id']:>14}  {r['type']:<9} {r['label']}")

        if diag["owner_commands"]:
            print("\nOwner commands:")
            for c in diag["owner_commands"]:
                arg = " ".join(str(i) for i in c["ids"]) or "-"
                print(f"  /{c['command']} {arg}")
                for n in c["notes"]:
                    print(f"      {n}")
                if c["unparsed"]:
                    # Say so rather than silently ignoring it: the owner thinks
                    # they approved somebody.
                    print(f"      ::warning::not a chat id, ignored: {', '.join(c['unparsed'])}")

        # A command from anyone but the owner is a security signal, not noise.
        for r in diag["rejected_commands"]:
            print(f"::warning::/{r['command']} from {r['chat_id']} is not the owner — ignored.")
        for u in diag["unknown_commands"]:
            print(f"  (ignored unknown command {u['command']} from {u['chat_id']})")

        b, a = diag["before"], diag["after"]
        print(f"\nLists: approved {b['approved']}->{a['approved']}, "
              f"pending {b['pending']}->{a['pending']}, "
              f"opted out {b['unsubscribed']}->{a['unsubscribed']}")
        print(f"Replies to send: {len(replies)}"
              + (f" ({', '.join(sorted(r['outcome'] for r in replies))})" if replies else ""))
        print(f"This edition goes to the owner plus {a['approved']} subscriber(s).")

        if data["pending"]:
            print("::notice::Awaiting approval: "
                  + ", ".join(str(e["chat_id"]) for e in data["pending"])
                  + " — reply /pending to the bot, or use the approve input here.")

        write_step_summary(diag, data, replies)
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
            print("\nThe ids above are masked to their last three digits, because this")
            print("log is public. To get the full ids, send the bot /pending — it")
            print("answers in your own chat. Then approve with:")
            print("  Actions -> Find my Telegram chat ID -> Run workflow, putting the")
            print("  id(s) in the 'approve' input.")
            print("\nNames above are shown only to help you decide and are NOT stored,")
            print("but note that on a public repository this log is public.")
        else:
            print("\nNo new chats. subscribers.json unchanged.")

        pend = data["pending"]
        if pend:
            print(f"\nStill pending approval: {', '.join(str(e['chat_id']) for e in pend)}")
        return 0

    if not args.targets:
        raise SystemExit(f"{args.action} needs at least one chat id")
    targets = parse_ids(args.targets)
    acted = []
    if args.action == "approve":
        notes = approve(targets, data, owner, replies=acted)
    else:
        notes = remove(targets, data, remember=True)
    if args.replies:
        Path(args.replies).write_text(json.dumps(acted), encoding="utf-8")
    save(data, store)
    print()
    for cid, note in notes:
        print(f"  {cid}: {note}")
    print(f"\nNow delivering to the owner plus {len(data['approved'])} subscriber(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
