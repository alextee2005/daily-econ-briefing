"""Who is entitled to receive an edition, and why.

Kept apart from subscribers.py deliberately. subscribers.py decides who has
ASKED for the briefing; this decides who may RECEIVE it. Mixing the two would
mean the paywall and the subscription bookkeeping share one body of code, and
the paywall is the half that can silently stop delivering to people who paid.

THE FIELDS

An entry in the subscriber list may carry, all optional:

    plan          "paid" | "comp" | "grandfathered" | "trial" | absent
    paid_until    ISO date — the last day of paid access, inclusive
    trial_started ISO date — when /start was first seen, written ONCE and
                  never cleared, so /stop followed by /start cannot mint a
                  second trial
    stripe_customer_id, stripe_subscription_id — opaque, for reconciliation

An entry with none of them is not entitled. That is the safe default: a new
chat receives nothing until something explicitly grants it.

WHY THE TRIAL IS COUNTED FROM GIT

The trial is three EDITIONS, not three days, so the obvious implementation is
a counter decremented as each one goes out. That would put a write into the
delivery path, which today only reads — and the delivery path is the one that
sent the 7 September edition to everybody on 22 October. So instead the trial
start date is written once, and how much of the trial is left is computed by
counting the editions committed since. A pure function of git state and one
stored date: idempotent, safe to replay, and nothing to corrupt.
"""

from datetime import date, timedelta

# Past paid_until, access continues this long. Covers a card that failed and
# a renewal still working its way through Stripe's retries, so a payment
# hiccup does not read to the subscriber as being cut off.
GRACE_DAYS = 7

# Editions a new chat receives before it has to pay.
TRIAL_EDITIONS = 3

# How long before paid_until to warn that a renewal is coming.
REMIND_DAYS = 7


def as_date(value):
    """An ISO date, or None for anything unparseable.

    Deliberately forgiving: a hand-edited list with a malformed date must not
    crash the morning delivery. An unreadable date means the field grants
    nothing, which is the same as it being absent.
    """
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def editions_since(start, edition_dates) -> int:
    """How many editions were published strictly after `start`.

    Strictly after, because the edition published the same day someone sends
    /start has already gone out by the time they are on the list.
    """
    start = as_date(start)
    if start is None:
        return 0
    return sum(1 for d in edition_dates if as_date(d) and as_date(d) > start)


def status(entry: dict, today: date, edition_dates=()) -> dict:
    """Why this entry may or may not receive the next edition.

    Returns {entitled, state, detail}. `state` is one of:

        paid        inside paid_until
        grace       past paid_until, inside GRACE_DAYS
        trial       trial started, fewer than TRIAL_EDITIONS consumed
        lapsed      was paid or on trial, and that has run out
        none        nothing has ever granted this chat anything
    """
    paid_until = as_date(entry.get("paid_until"))
    trial_started = as_date(entry.get("trial_started"))

    if paid_until is not None:
        if today <= paid_until:
            left = (paid_until - today).days
            return {"entitled": True, "state": "paid",
                    "detail": f"paid through {paid_until} ({left}d left)"}
        grace_end = paid_until + timedelta(days=GRACE_DAYS)
        if today <= grace_end:
            return {"entitled": True, "state": "grace",
                    "detail": f"expired {paid_until}, in grace until {grace_end}"}
        return {"entitled": False, "state": "lapsed",
                "detail": f"expired {paid_until}, grace ended {grace_end}"}

    if trial_started is not None:
        used = editions_since(trial_started, edition_dates)
        if used <= TRIAL_EDITIONS:
            return {"entitled": True, "state": "trial",
                    "detail": f"trial edition {max(used, 1)} of {TRIAL_EDITIONS}"}
        return {"entitled": False, "state": "lapsed",
                "detail": f"trial of {TRIAL_EDITIONS} editions used up"}

    return {"entitled": False, "state": "none", "detail": "never granted access"}


def entitled(entry: dict, today: date, edition_dates=()) -> bool:
    return status(entry, today, edition_dates)["entitled"]


def expiring(entry: dict, today: date) -> bool:
    """Is a renewal due within REMIND_DAYS? False once it has already passed."""
    paid_until = as_date(entry.get("paid_until"))
    if paid_until is None:
        return False
    days = (paid_until - today).days
    return 0 <= days <= REMIND_DAYS


def grant(entry: dict, today: date, plan: str, years: int = 1) -> dict:
    """Extend paid access by `years`, in place, and return the entry.

    Extends from whichever is later, today or the existing paid_until, so a
    renewal that lands early does not shorten what was already paid for and a
    renewal that lands late does not silently backdate.
    """
    current = as_date(entry.get("paid_until"))
    base = current if current and current > today else today
    entry["paid_until"] = (base + timedelta(days=365 * years)).isoformat()
    entry["plan"] = plan
    return entry
