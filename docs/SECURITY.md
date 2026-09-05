# Rebound security posture

Last reviewed: 5 September 2026

Rebound is a local MVP, not a production payment processor. Its security model is deliberately conservative: no live Razorpay keys are accepted, decision-critical actions remain policy-gated, and the dashboard is private by default.

## Enforced controls

| Boundary | Control |
| --- | --- |
| Operator API | Every `/api/v1` route except health and the webhook ingress requires a constant-time-checked `X-Rebound-Token`. The API returns `503` until `REBOUND_API_TOKEN` is configured. |
| Browser session | The dashboard requests the token in a password field, stores it only in `sessionStorage`, and provides a lock action. It does not bundle the token in Vite environment variables or render it. |
| Webhook ingress | Razorpay webhooks require a configured secret and verify `X-Razorpay-Signature` against the unmodified raw request body. Replayed external event IDs are deduplicated. |
| Payment scope | `rzp_live_` credentials are rejected. Rebound supports only explicitly configured Razorpay Test Mode requests, and only allowlisted Payment Link actions plus read-only subscription/invoice reads. |
| Sensitive data | Inbound customer references are HMAC-pseudonymised before case storage. Webhook payload storage and audit/API output redact contact details, authentication material, card/bank fields, URLs, notes, and tokens. |
| Upstream responses | Subscription and invoice endpoints return allowlisted operational fields instead of raw Razorpay payloads. Payment-link URLs are never displayed in the Rebound UI. |
| API exposure | CORS is limited to the configured app origin and local development origins. Interactive API documentation and OpenAPI schema routes are disabled. Collection limits are bounded. |

## Verification performed

- Backend tests cover access denial, signed webhook verification, webhook idempotency, PII pseudonymisation/redaction, policy gates, Razorpay Test Mode guards, and read-only Razorpay access.
- The frontend build type-checks all dashboard/API changes.
- Dependency checks use `pip check` and `npm audit --omit=dev --audit-level=high` when the package registries are available.
- A repository scan is performed before release to ensure tracked files do not contain `.env` files or embedded credentials.

## Deliberate MVP boundaries

- The local token is a single-operator control, not merchant SSO, RBAC, or multi-tenant authorization.
- SQLite encryption at rest, managed secret rotation, WAF/rate limiting, production observability, and a formal penetration test are required before production use.
- A public webhook endpoint must use HTTPS and a unique secret in the authorised Razorpay account. Never expose local development credentials in a recording or repository.

These constraints are intentional. They ensure the buildathon MVP demonstrates real integration safely without implying unauthorised production payment handling.
