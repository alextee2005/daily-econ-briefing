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

# One record per line, with the text base64-encoded.
#
# An earlier version put the raw text in a tab-separated field and documented
# that messages were single-line "by construction". The owner's /pending answer
# and the new-request notice are both multi-line, so every line after the first
# became its own bogus record and the loop tried to send a message to a chat id
# of "Pending ids: 555, 777, 888". Encoding removes the whole class of problem
# rather than escaping one character of it.
#
# stderr is dropped: a malformed file raises a traceback that says nothing the
# warning below does not, and on a public repository these logs are public.
if ! python3 - "$FILE" <<'PY' > /tmp/replies.tsv 2>/dev/null
import base64, json, sys
for r in json.load(open(sys.argv[1])):
    blob = base64.b64encode(r["text"].encode()).decode()
    print(f"{r['chat_id']}\t{r['outcome']}\t{blob}")
PY
then
  echo "::warning::Could not read $FILE; no confirmations sent."
  exit 0
fi

SENT=0
FAILED=0
ROWS=""
while IFS=$'\t' read -r CID OUTCOME BLOB; do
  [ -n "${CID:-}" ] || continue
  TEXT=$(printf '%s' "$BLOB" | base64 -d)

  # Capture Telegram's own verdict, not just curl's. An HTTP 200 with
  # "ok": false is the case that would otherwise read as success and leave
  # somebody wondering why they were never told anything.
  set +e
  HTTP=$(curl -sS -o /tmp/reply_resp.json -w '%{http_code}' \
    --retry 2 --retry-delay 3 --retry-all-errors \
    -F "chat_id=${CID}" -F "text=${TEXT}" \
    "https://api.telegram.org/bot${TOKEN}/sendMessage")
  RC=$?
  set -e
  if [ "$RC" != "0" ]; then
    HTTP="000"
    echo '{"ok":false,"description":"curl failed to reach Telegram"}' > /tmp/reply_resp.json
  fi

  DESC=$(python3 -c "
import json
try:
    d = json.load(open('/tmp/reply_resp.json'))
except Exception:
    print('unparseable response'); raise SystemExit
print('ok' if d.get('ok') else (d.get('description') or 'refused, no reason given'))
" 2>/dev/null || echo "unparseable response")

  if [ "$HTTP" = "200" ] && [ "$DESC" = "ok" ]; then
    SENT=$((SENT + 1))
    echo "  told ${CID}: ${OUTCOME}"
    ROWS="${ROWS}| \`${CID}\` | ${OUTCOME} | sent |"$'\n'
  else
    FAILED=$((FAILED + 1))
    # A chat that has blocked the bot cannot be told anything, which is fine —
    # they have already achieved what the message would have confirmed.
    echo "::warning::Could not send the '${OUTCOME}' confirmation to ${CID} — HTTP ${HTTP}: ${DESC}"
    ROWS="${ROWS}| \`${CID}\` | ${OUTCOME} | **failed** — HTTP ${HTTP}: ${DESC} |"$'\n'
  fi
done < /tmp/replies.tsv

echo "Confirmations: ${SENT} sent, ${FAILED} failed."

# The summary is where this gets noticed. A confirmation that silently never
# arrived looks identical to one that did, unless it is written down.
if [ -n "${GITHUB_STEP_SUMMARY:-}" ] && [ -n "$ROWS" ]; then
  {
    echo "### Bot confirmations"
    echo
    echo "${SENT} sent, ${FAILED} failed."
    echo
    echo "| chat | message | result |"
    echo "|---|---|---|"
    printf '%s' "$ROWS"
  } >> "$GITHUB_STEP_SUMMARY"
fi

exit 0
