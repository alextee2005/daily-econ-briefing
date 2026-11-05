# Stripe integration — remaining steps

Hosted Stripe Checkout, configured in Checkout Studio. This file is the single
source of truth for what is left to do.

**Scenario B applied.** No Checkout Session API call existed anywhere in this
repository, so one was added. Nothing else was changed: the webhook handler,
secret loading and subscriber bookkeeping already existed and were left alone.

## Decision taken: the Payment Link

**5 November 2026 — the Payment Link is the live path.** The Checkout Session
route added for Checkout Studio stays in the code but **dormant**: without
`STRIPE_SECRET_KEY` it returns 404, exactly as an unknown path does.

That is the simpler half of the fork, and deliberately so: no key capable of
moving money lives in the Worker, which only verifies webhooks. It needs
**three** variables rather than nine.

| Variable | Where | Needed? |
|---|---|---|
| `PAY_URL` | Cloudflare | **yes** — the Payment Link itself |
| `STRIPE_WEBHOOK_SECRET` | Cloudflare | **yes** — or payments are never recorded |
| `STRIPE_PAY_URL` | GitHub | **yes, last** — starts enforcing at delivery |
| `PORTAL_URL` | Cloudflare | recommended — lets subscribers cancel themselves |
| `COMP_CODES` | Cloudflare | optional — free comp codes |
| `STRIPE_SECRET_KEY` | Cloudflare | no |
| `STRIPE_PRICE_ID` | Cloudflare | no — Checkout Session only |
| `CHECKOUT_SUCCESS_URL` | Cloudflare | no — Checkout Session only |
| `CHECKOUT_CANCEL_URL` | Cloudflare | no — Checkout Session only |
| `PORTAL_RETURN_URL` | Cloudflare | no — portal sessions only |

### What skipping the secret key costs

One thing, and it is acceptable: the customer portal link becomes the
**login page** rather than a one-time deep link, so a subscriber types their
email and Stripe sends them a magic link. The deep-link version needs
`STRIPE_SECRET_KEY`. Everything else is identical.

### The trap that will catch you

**Test mode and live mode are separate worlds.** The Payment Link is a
different URL and the webhook signing secret is a different value. Going live
is not a toggle — it means creating the link and the webhook again in live
mode and replacing both variables. Nothing warns you: a live payment against
a test-mode secret simply fails signature verification and is never recorded.

## Values to Replace

The following values are placeholders and must be updated before going live.

**Files containing placeholders:**
- [worker/src/index.js](worker/src/index.js) — `checkoutForm()`

Each one reads from a Worker variable and falls back to a placeholder, so you
set these in the Cloudflare dashboard rather than editing code.

| Field | Current Value | What to Set |
|-------|--------------|-------------|
| line_items[].price | `price_...` | Your real Stripe Price ID — the $4.99/year recurring price. Dashboard → Product catalogue, or https://dashboard.stripe.com/prices. Set it as the Worker variable `STRIPE_PRICE_ID`. |
| success_url | `https://example.com/success?session_id={CHECKOUT_SESSION_ID}` | Where to send someone after paying. **This project has no website** — it is a Telegram bot — so the sensible value is your bot's deep link, e.g. `https://t.me/your_bot`. Set the Worker variable `CHECKOUT_SUCCESS_URL`; the `?session_id={CHECKOUT_SESSION_ID}` template is appended automatically, so do not include it yourself. |
| cancel_url | `https://example.com/cancel` | Where to send someone who abandons checkout. Again your bot link is the natural choice. Worker variable `CHECKOUT_CANCEL_URL`. |

### mode — already correct, no change needed

`mode` is listed as a placeholder in the Checkout Studio brief, but the
product type here is not in doubt: the briefing is sold as **$4.99 per year,
recurring**, so it is set to `subscription`. `payment_method_collection` is
only valid in that mode and is included for the same reason. Change it only if
you switch to selling one-off editions.

## Configured Parameters

These parameters were configured in Checkout Studio and are already set
correctly.

**Files containing these parameters:**
- [worker/src/index.js](worker/src/index.js) — `checkoutForm()`

| Parameter | Value |
|-----------|-------|
| ui_mode | `hosted_page` |
| billing_address_collection | `auto` |
| phone_number_collection | `{ enabled: false }` |
| automatic_tax | `{ enabled: false }` |
| allow_promotion_codes | `true` |
| payment_method_collection | `always` |
| submit_type | `auto` |
| saved_payment_method_options | `{ payment_method_save: enabled }` |
| integration_identifier | `hosted_web_0001` |
| origin_context | `web` |

Each is asserted individually in `worker/test.mjs`. A dropped parameter is the
failure that would otherwise go unnoticed: Stripe accepts the call, checkout
works, and the setting you chose in the UI simply is not in effect.

### A version dependency you should know about

`ui_mode` is set to `hosted_page`, which is correct for Stripe SDK **21.0.0
and above**. Below that it must be `hosted`.

**There is no Stripe SDK in this project to read a version from.** The Worker
is a single file pasted into the Cloudflare dashboard with no build step and
no imports, so it calls the REST API directly with `fetch` and form encoding —
the same way it already calls Telegram. `package.json` carries only
`playwright`, for PDF rendering.

Because the REST API is versioned by account rather than by SDK, `hosted_page`
is the right default. If Stripe rejects `ui_mode`, change it to `hosted` in
`checkoutForm()`.

No API version is pinned anywhere, as instructed — your account default
applies.

## Setup

### Worker variables (Cloudflare dashboard)

Settings → **Variables and Secrets**. Note the trap this project has hit
before: *Settings → Build → Build variables* is build-time only and invisible
to the Worker. Use **Variables and Secrets**, then **Deploy**.

For the Payment Link path:

| Name | Type | Purpose |
|---|---|---|
| `PAY_URL` | Text | The Payment Link URL. The bot appends `?client_reference_id=<chat id>` |
| `STRIPE_WEBHOOK_SECRET` | Secret | `whsec_…` from the webhook endpoint, for `/stripe` |
| `PORTAL_URL` | Text | The customer portal login page |
| `COMP_CODES` | Text | Optional, e.g. `FRIENDS:1, PRESS:2` |

The Checkout Session variables (`STRIPE_SECRET_KEY`, `STRIPE_PRICE_ID`,
`CHECKOUT_SUCCESS_URL`, `CHECKOUT_CANCEL_URL`) are **not needed** and should be
left unset, which keeps that route dormant.

Never commit a key. This repository is public and has no `.env` by design:
secrets live in GitHub Actions secrets and Cloudflare Worker variables. See
https://docs.stripe.com/keys-best-practices.

### Already present — do not add again

- **Webhook handler** at `/stripe`, with signature verification, replay
  protection and idempotency keyed on the Stripe event id
- **Event handling** for `checkout.session.completed`, `invoice.paid`,
  `customer.subscription.deleted` and `invoice.payment_failed`
- **Entitlement and fulfilment** — `scripts/entitlement.py`, applied at
  delivery
- **Secret loading** — GitHub Actions secrets and Worker variables

## Project structure

No new files were created for the integration itself. The change is one route
and one helper inside the existing Worker:

```
worker/src/index.js          POST /create-checkout-session  (new)
                             checkoutForm()                 (new)
                             POST /stripe                   (already existed)
worker/test.mjs              24 new cases for the above
STRIPE_INTEGRATION_TODO.md   this file
```

## How it works

```
Telegram /start
  → bot replies with a pay link
  → customer pays on Stripe's hosted page
  → Stripe fires checkout.session.completed
  → Worker POST /stripe verifies the signature, queues "paid"
  → subscriptions.yml drains the queue, grants a year
  → deliver.yml sends only to entitled chats
```

The new route sits at the first step as an alternative to the static Payment
Link: `POST /create-checkout-session` with `{"chat_id": 12345}` (or
`?chat_id=12345`) returns `{"url": "https://checkout.stripe.com/…"}` to send
to the subscriber.

**`client_reference_id` is not optional.** `/stripe` matches a completed
payment to a Telegram chat by that field alone; without it a payment cannot be
attributed to anybody and the owner is messaged to sort it out by hand.

One caveat, unchanged from the Payment Link: `chat_id` is caller-supplied, so
somebody could create a session for a chat that is not theirs. The only
outcome is paying for someone else's subscription, so it is left as is.

## Testing

Use test mode (`sk_test_…`) with a test Price ID.

| Card | Behaviour |
|---|---|
| `4242 4242 4242 4242` | succeeds |
| `4000 0025 0000 3155` | requires 3D Secure authentication |
| `4000 0000 0000 9995` | declined, insufficient funds |
| `4000 0000 0000 0341` | attaches but fails on the first charge — useful for renewals |

Any future expiry, any CVC, any postcode.

```bash
curl -X POST "$WORKER/create-checkout-session" \
  -H 'content-type: application/json' -d '{"chat_id": 123456}'
```

Then check `$WORKER/health` shows the expected `version`, and watch the
delivery summary's entitlement table for the chat moving to `paid`.

Run the suites with `node worker/test.mjs` and
`python3 scripts/test_subscribers.py`.

## Next steps

1. ~~Decide: Payment Link or Checkout Session.~~ **Done — Payment Link.**
2. Set `PAY_URL`, `STRIPE_WEBHOOK_SECRET` and `PORTAL_URL`, then **Deploy**.
3. Point a Stripe webhook at `<worker>/stripe` if you have not already, and
   paste its signing secret into `STRIPE_WEBHOOK_SECRET`.
4. Test with a test-mode card end to end, through to the entitlement table.
5. Switch to live keys, and set `STRIPE_PAY_URL` in GitHub secrets — **that is
   the step that starts enforcing the paywall at delivery.**
6. **Turn the customer portal on in Stripe.** The code side is done — see
   *Customer portal* below — but it cannot work until you enable the portal in
   your own dashboard, which is not something this repository can do for you.
7. Fulfilment and order tracking already exist — payments become entitlement
   in `subscribers.json` (held in Cloudflare KV, not in this repository,
   because chat ids are personal data and this repository is public).

## Customer portal

`/stop` takes someone off the delivery list but **cannot cancel what Stripe is
charging them**. Without a portal they stop receiving the briefing and keep
paying for it — the worst of both, and not something they can fix themselves.
That is now handled, in two ways, best first:

1. **A billing portal session**, created through the API for the chat's stored
   `stripe_customer_id`. A one-time deep link: they land straight in their own
   subscription, no email step. Needs `STRIPE_SECRET_KEY`, which the Checkout
   route already requires.
2. **`PORTAL_URL`** — the shareable login page from the dashboard. No key
   needed, but it asks for their email and sends a magic link, so it is the
   fallback.

With neither configured, nothing is sent and **the owner is messaged to cancel
it by hand**. That is the old behaviour, kept as the floor so a missing
variable degrades rather than misleads.

### What you have to do in Stripe

This part is yours — the dashboard cannot be changed from here.

1. https://dashboard.stripe.com/settings/billing/portal
2. Under **Functionality**, allow customers to **cancel subscriptions** (and
   update payment methods, which is the other reason they would open it).
3. **Save**. That alone makes option 1 work, since the API needs a saved
   portal configuration — until it exists, Stripe refuses the session with
   *"No configuration provided"* and the code falls back.
4. Optional: copy the **login page** link from the same screen into the Worker
   variable `PORTAL_URL`, as the fallback for anyone without a stored customer
   id.

### Worker variables

| Name | Type | Purpose |
|---|---|---|
| `PORTAL_URL` | Text | Shareable login page, used when no session can be created |
| `PORTAL_RETURN_URL` | Text | Where Stripe sends them when finished — your bot link, e.g. `https://t.me/your_bot`. This project has no web pages. |

### What a subscriber can do

| Command | Effect |
|---|---|
| `/manage` or `/billing` | Portal link. Update a card or cancel, without unsubscribing |
| `/stop` | Removes them from delivery **and**, if there is a live subscription, includes the cancel link |

A trial or a comped subscriber is not offered a portal: there is no money
behind either, so there is nothing to cancel.

## Resources

- https://docs.stripe.com/mcp
- https://support.stripe.com
- https://docs.stripe.com/keys-best-practices
- `docs/RUNBOOK.md` — the paywall section, for how entitlement is decided
