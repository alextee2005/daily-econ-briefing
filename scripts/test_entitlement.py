"""Pin who may receive an edition. Run: python3 scripts/test_entitlement.py

The failures that matter here are asymmetric. Wrongly entitling someone costs
$4.99 of goodwill. Wrongly DENYING someone who paid is the one that loses a
subscriber and is invisible until they complain, so most of these cases are
about not cutting people off.
"""

import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from entitlement import (  # noqa: E402
    GRACE_DAYS, REMIND_DAYS, TRIAL_EDITIONS,
    editions_since, entitled, expiring, grant, status,
)

failures = 0
TODAY = date(2026, 11, 2)


def check(label, passed, detail=""):
    global failures
    failures += not passed
    print(f"{'PASS' if passed else 'FAIL'}  {label}{f' — {detail}' if detail else ''}")


# --- the safe default ------------------------------------------------------
st = status({}, TODAY)
check("a bare entry is not entitled", not st["entitled"] and st["state"] == "none")
check("and an unknown chat never slips through",
      not entitled({"chat_id": 123}, TODAY))

# --- paid ------------------------------------------------------------------
check("paid through a future date", entitled({"paid_until": "2027-11-02"}, TODAY))
check("paid through today is still paid", entitled({"paid_until": "2026-11-02"}, TODAY))
check("the last paid day is inclusive",
      status({"paid_until": "2026-11-02"}, TODAY)["state"] == "paid")

# --- grace: the boundary that must not cut a payer off ---------------------
def expired_days_ago(n):
    return {"paid_until": (TODAY - timedelta(days=n)).isoformat()}


check(f"every day inside the {GRACE_DAYS}-day grace window still delivers",
      all(status(expired_days_ago(n), TODAY)["state"] == "grace"
          for n in range(1, GRACE_DAYS + 1)),
      f"checked 1..{GRACE_DAYS} days past expiry")
check("one day past grace does not",
      not entitled(expired_days_ago(GRACE_DAYS + 1), TODAY))
check("and past grace reads as lapsed, not as never-granted",
      status({"paid_until": "2026-01-01"}, TODAY)["state"] == "lapsed")

# --- the trial, counted in editions ---------------------------------------
EDS = ["2026-10-27", "2026-10-28", "2026-10-29", "2026-10-30"]
check("editions are counted strictly after the start date",
      editions_since("2026-10-27", EDS) == 3, str(editions_since("2026-10-27", EDS)))
check("a start date after every edition has consumed nothing",
      editions_since("2026-12-01", EDS) == 0)

# Someone starting before edition 1 of their trial: entitled for exactly three.
for used, eds in enumerate([EDS[:0], EDS[:1], EDS[:2], EDS[:3], EDS[:4]]):
    st = status({"trial_started": "2026-10-26"}, TODAY, eds)
    want = used <= TRIAL_EDITIONS
    check(f"trial with {used} edition(s) published: entitled={want}",
          st["entitled"] == want, st["detail"])

check("a used-up trial reads as lapsed",
      status({"trial_started": "2026-10-26"}, TODAY, EDS)["state"] == "lapsed")

# The loophole: /stop then /start must not mint a second trial. The module
# cannot enforce that by itself — it is enforced by never clearing the field —
# but a stale start date must stay used up rather than resetting.
check("an old trial start stays spent",
      not entitled({"trial_started": "2026-01-01"}, TODAY, EDS))

# --- paid beats trial ------------------------------------------------------
check("paid access wins over a spent trial",
      entitled({"trial_started": "2026-01-01", "paid_until": "2027-11-02"}, TODAY, EDS))
check("and a spent trial does not revive a lapsed payer",
      not entitled({"trial_started": "2026-10-26", "paid_until": "2026-01-01"}, TODAY, EDS))

# --- malformed data must not break the morning ----------------------------
for bad in (None, "", "not-a-date", "2026-13-99", 42, {}):
    st = status({"paid_until": bad}, TODAY)
    check(f"malformed paid_until {bad!r} grants nothing and does not raise",
          st["entitled"] is False)
check("a malformed trial date grants nothing",
      not entitled({"trial_started": "soon"}, TODAY, EDS))
check("a malformed edition date is skipped, not fatal",
      editions_since("2026-10-26", ["2026-10-27", "oops", "2026-10-28"]) == 2)

# --- renewal reminders ----------------------------------------------------
def expires_in(n):
    return {"paid_until": (TODAY + timedelta(days=n)).isoformat()}


check("a renewal inside the window is flagged", expiring(expires_in(REMIND_DAYS), TODAY))
check("a renewal just outside it is not", not expiring(expires_in(REMIND_DAYS + 1), TODAY))
check("expiring today is still flagged",
      expiring({"paid_until": TODAY.isoformat()}, TODAY))
check("an already-expired entry is not 'expiring'",
      not expiring({"paid_until": "2026-01-01"}, TODAY))
check("a trial entry has no renewal to remind about",
      not expiring({"trial_started": "2026-10-26"}, TODAY))

# --- granting and renewing -------------------------------------------------
e = grant({}, TODAY, "paid")
check("a fresh grant runs a year from today", e["paid_until"] == "2027-11-02", e["paid_until"])
check("and records the plan", e["plan"] == "paid")

# An early renewal must extend, not truncate. This is the one that would
# quietly rob someone of the time they already paid for.
e = grant({"paid_until": "2027-06-01"}, TODAY, "paid")
check("an early renewal extends from the existing expiry",
      e["paid_until"] == "2028-05-31", e["paid_until"])

# A late renewal must not backdate into the past.
e = grant({"paid_until": "2026-01-01"}, TODAY, "paid")
check("a late renewal runs from today, not from the old expiry",
      e["paid_until"] == "2027-11-02", e["paid_until"])

e = grant({}, TODAY, "comp")
check("a comp grant is a year like any other",
      e["paid_until"] == "2027-11-02" and e["plan"] == "comp")

print(f"\n{failures} failure(s)")
sys.exit(1 if failures else 0)
