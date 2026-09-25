#!/usr/bin/env bash
# Send the bot's confirmations. Used by both briefing.yml (which answers /start
# and /stop) and find-chat-id.yml (which answers an approval), so the two cannot
# drift apart in how they treat a failure.
#
# Usage:  TELEGRAM_BOT_TOKEN=... scripts/send_replies.sh replies.json
#
# Never fails. A confirmation that does not arrive is a nuisance; a briefing
# that does not arrive because a confirmation failed is a fault. The caller's
# job is the briefing, so this exits 0 no matter what happens.
set -uo pipefail

FILE="${1:-}"
TOKEN="${TELEGRAM_BOT_TOKEN:-}"

if [ -z "$FILE" ] || [ ! -s "$FILE" ]; then
  echo "No confirmations to send."
  exit 0
fi

if [ -z "$TOKEN" ]; then
  echo "::warning::TELEGRAM_BOT_TOKEN is not set; cannot send confirmations."
  exit 0
fi

# Tab-separated so the loop below needs no JSON parsing. Texts are single-line
# by construction (see MSG in scripts/subscribers.py).
# stderr is dropped: a malformed file raises a traceback that says nothing the
# warning below does not, and on a public repository these logs are public.
if ! python3 - "$FILE" <<'PY' > /tmp/replies.tsv 2>/dev/null
import json, sys
for r in json.load(open(sys.argv[1])):
    print(f"{r['chat_id']}\t{r['outcome']}\t{r['text']}")
PY
then
  echo "::warning::Could not read $FILE; no confirmations sent."
  exit 0
fi

SENT=0
FAILED=0
while IFS=$'\t' read -r CID OUTCOME TEXT; do
  [ -n "${CID:-}" ] || continue
  if curl -sS -o /dev/null --retry 2 --retry-delay 3 --retry-all-errors \
       -F "chat_id=${CID}" -F "text=${TEXT}" \
       "https://api.telegram.org/bot${TOKEN}/sendMessage"; then
    SENT=$((SENT + 1))
    echo "  told ${CID}: ${OUTCOME}"
  else
    FAILED=$((FAILED + 1))
    # A chat that has blocked the bot cannot be told anything, which is fine —
    # they have already achieved what the message would have confirmed.
    echo "::warning::Could not send the '${OUTCOME}' confirmation to ${CID}."
  fi
done < /tmp/replies.tsv

echo "Confirmations: ${SENT} sent, ${FAILED} failed."
exit 0
