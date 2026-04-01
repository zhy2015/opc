# OPC Delivery / Auth Failure Handling

Use this file when a production run touches external delivery, user-identity sends, bot sends, cloud links, or background delivery monitors.

## Core rule

Authentication failure is not a cosmetic error.
It invalidates the claimed delivery path until repaired.

Do not keep talking as if delivery is still on track when the active send path has already failed auth.

## Hard-stop signals

Treat these as hard-stop signals for the affected path:
- invalid user
- access denied
- expired or rejected credential
- wrong account / wrong surface / wrong destination compatibility
- repeated provider rejection with no state change

Treat these as hard-stop equivalents for delivery truthfulness even when auth is not the root cause:
- backend unavailable
- delivery channel rejected the payload and no recovery occurred
- runtime path was only planned, not actually executed
- the only remaining object is a local fallback artifact

## Required response

When a delivery/auth path hard-stops:
1. mark that delivery path invalid
2. stop using that path in optimistic user updates
3. switch to a verified fallback only if it is real and available
4. if no verified fallback exists, surface the blocker honestly
5. remove or repair background jobs that are bound to the broken path

## Runtime degrade truthfulness

When a backend, executor, auth path, or delivery surface is degraded, the main session must keep result language aligned with what actually happened.

Hard rules:
- do not pretend a real external execution happened if only a local fallback path ran
- do not pretend a delivery completed if only preparation or fallback planning exists
- do not upgrade a local materialized object into true external delivery without saying it is fallback
- if the only surviving result is internal-only, say it is internal-only

Recommended delivery-status language:
- `delivered` = verified user-accessible delivery happened
- `fallback_delivered` = a real fallback object exists, but it is not the originally claimed delivery path
- `internal_only` = useful internal object exists, but user delivery is not complete
- `runtime_blocked` = backend/runtime failure prevents claimed execution or delivery
- `delivery_channel_failed` = output exists, but the intended delivery surface failed

## Anti-patterns

Do not do these:
- keep cron jobs alive on a broken auth path without repair
- say “still sending” after the provider has rejected the user or credential
- treat fallback planning as fallback execution
- announce delivery from a path that has not recovered
- blur the line between mock/fallback materialization and real user-facing delivery

## Recovery discipline

A repaired delivery path should be considered usable again only after a fresh successful action or equivalent direct verification.
Past success on the same path does not prove current validity.

This file owns the delivery/auth invalidation slice of the creative operating protocol. For SSOT ownership, see `references/opc-creative-ssot-map.md`.
