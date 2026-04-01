# OPC Creative Failure Patterns

This file captures the most dangerous failure patterns seen in creative-production OPC runs.
It exists so the system does not repeat the same expensive mistakes under pressure.

## 1. False completion from unverified subagent claims

Failure shape:
- a subagent reports success
- the main session forwards that success too early
- the claimed artifact is missing, mocked, empty, or otherwise not directly usable

Required correction:
- never treat subagent success text as proof of delivery
- verify the claimed artifact or access path before user-facing completion language
- if verification fails, downgrade the completion level immediately

## 2. Planning-heavy start with downstream lanes missing

Failure shape:
- script or prompt work starts
- generation, audio, render, or delivery lanes are absent or under-owned
- the run looks busy but throughput is fake

Required correction:
- open enough production lanes early
- explicitly assign delivery ownership and audio ownership
- do not let planning activity masquerade as production progress

## 3. Commentary loop after sub-results

Failure shape:
- a result comes back
- instead of triggering the next action, the main session narrates progress
- the user must re-prompt to restart motion

Required correction:
- every material sub-result should have a default next action
- commentary should be secondary to continuation
- if no next action exists, that absence should be explicit

## 4. Delivery discovered too late

Failure shape:
- the system works on generation/render first
- only near the end does it test how the user will actually receive the result
- the result may exist but be inaccessible

Required correction:
- validate at least one delivery path early
- keep fallback delivery path explicit
- completion requires direct user access unless the user requested an earlier review layer

## 5. Manifest / project truth lag

Failure shape:
- scripts, assets, drafts, and final outputs drift away from project metadata
- workers and the chief controller act on stale assumptions

Required correction:
- asset arrival, draft upgrade, and delivery should each trigger truth sync
- current project truth must beat stale narration and stale memory

## 6. Mock / placeholder / empty artifact contamination

Failure shape:
- generated files are placeholders, zero-byte outputs, mocked stand-ins, or partial test artifacts
- they silently enter the production path as if they were real assets

Required correction:
- verify non-empty artifact existence before promoting state
- keep placeholder outputs clearly segregated from production-ready outputs
- do not announce delivery from mocked or inferred success

## 7. Cron / background continuation without validity checks

Failure shape:
- background jobs continue retrying or monitoring
- invalid credentials, dead processes, or empty outputs persist
- the system keeps “watching” a dead pipeline

Required correction:
- background monitors should detect dead-process states, invalid auth, empty artifacts, and stalled queues
- recurring jobs should be cancellable and should not imply progress by mere existence
- if the monitored pipeline is dead, surface that fact clearly instead of narrating optimism

## 7b. Broken delivery/auth path still treated as active

Failure shape:
- the chosen delivery path starts failing auth or access checks
- the system continues speaking as if delivery is merely delayed
- fallback remains hypothetical, but user updates sound operational

Required correction:
- mark the broken path invalid immediately
- do not let historical success override current auth failure
- either switch to a verified fallback or report the blocker cleanly

## 8. Audio treated as a late accessory

Failure shape:
- visual generation starts first
- audio is postponed until after draft or render pressure mounts
- preview quality and throughput both suffer

Required correction:
- if audio matters, start it early enough to support preview assembly
- keep audio as a lane, not as a cleanup chore

## 9. Concurrency underuse masked as caution

Failure shape:
- the system says it is being careful
- but independent production units remain idle
- total throughput collapses while no real safety is gained

Required correction:
- distinguish true serial bridges from independent units
- caution should narrow scope cleanly, not erase available parallelism

## 10. Render as fake repair layer

Failure shape:
- unresolved upstream problems are pushed into export/rerender attempts
- the system keeps producing versions instead of fixing the right layer

Required correction:
- script, shot, asset, voice, and render boundaries must stay explicit
- rerender is not a substitute for upstream repair

This file owns the failure-pattern slice of the creative operating protocol. For SSOT ownership, see `references/opc-creative-ssot-map.md`.
