#!/usr/bin/env bash
#
# Every self-test, in one place.
#
# This exists because "run the tests" meant different things in different
# places. briefing.yml listed eight commands, the last of them `node
# worker/test.mjs`; working locally it was easy to run the Python ones, see them
# pass, and never discover that the Worker suite was part of the gate. A change
# to the Worker then failed the morning briefing on tests that had passed on
# every run before it.
#
# So the list lives here and briefing.yml calls this. Local and CI now mean the
# same thing by construction rather than by remembering.
#
#   bash scripts/test_all.sh
#
# test_gate.py needs the packages in requirements.txt; the others need only the
# standard library, and the Worker suite needs node. Fails on the first failing
# suite, because a gate that reports everything and then runs anyway is not a
# gate.
set -euo pipefail

cd "$(dirname "$0")/.."

for suite in \
  scripts/test_gate.py \
  scripts/test_verify.py \
  scripts/test_run_report.py \
  scripts/test_subscribers.py \
  scripts/test_pick_edition.py \
  scripts/test_recall_message.py \
  scripts/test_entitlement.py
do
  echo "=== $suite"
  python3 "$suite"
done

# The Worker answers subscribers in real time and carries its own copy of the
# wording and the command menus; the Python suite compares the two so they
# cannot drift. This runs the Worker's own behaviour.
echo "=== worker/test.mjs"
node worker/test.mjs
