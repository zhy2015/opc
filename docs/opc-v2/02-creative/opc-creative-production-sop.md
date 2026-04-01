# OPC Creative Production SOP

This file defines the default operating skeleton for OPC when the task is a creative production workflow such as short-video creation, multi-asset narrative assembly, or other production-style jobs where the user ultimately wants a directly accessible result object.

## Core rule

In creative production, OPC is not successful because it spawned workers.
It is successful only when it forms a production loop from the beginning:
- concurrent production
- automatic handoff
- continuous convergence
- stable delivery

If the system only produces plans, commentary, or partial assets without pushing toward an accessible deliverable, the run is not behaving correctly yet.

## Default activation posture

Use this SOP when most of the following are true:
- the task is creative or production-like rather than a single-object micro edit
- multiple production layers exist, such as script, shot, media generation, audio, edit, or delivery
- several meaningful sub-tasks can run in parallel
- the user wants a result object, not just advice

Do not use this SOP for trivial one-turn tasks or for narrowly scoped single-layer revisions that already fit a normal execution skill.

## Lightweight run-shape selection

Creative OPC does not need to launch the heaviest controller shape every time.
Pick the smallest run shape that still protects delivery truth and production continuity.

Suggested mapping:
- `direct_review` — small creative revision where one main execution lane plus review is enough
- `research_execute_review` — concept or preproduction ambiguity is still material, but the job is not yet full production-lane heavy
- `execute_verify_review` — assets or render work can start directly, but verification and delivery checks must remain explicit
- `full_controller` — multi-lane production with real concurrency, handoff, and delivery complexity

Upgrade to `full_controller` when:
- several meaningful lanes can run in parallel
- the run has drift risk
- delivery complexity is non-trivial
- project-state truth or artifact synchronization matters continuously

## Default five-lane launch

Creative OPC should default to a five-lane launch only when the task really qualifies for `full_controller` and one lane clearly has meaningful work.

1. script / shot lane
2. visual generation lane
3. render / draft lane
4. audio / music lane
5. delivery / handoff lane

The default bias is to start all meaningful lanes early.
Do not launch only “idea-layer” workers while leaving downstream production and delivery unstarted.

If a lane is intentionally omitted, the main session should be able to say why that lane truly had no useful work yet.

## Chief-controller posture for creative runs

In creative production, the main session should behave like a chief controller, not a progress narrator.

Default main-session duties:
1. assign non-overlapping scopes
2. keep concurrency filled where valid
3. collect sub-results
4. detect gaps
5. trigger the next production step automatically
6. integrate outputs into a coherent deliverable
7. verify delivery path before claiming completion

The main session should not drift into frequent user-facing commentary about internal movement.
Commentary is not production.

## User-visible output discipline

Default to low-noise output during creative runs.
Only interrupt with a proactive user-facing update when at least one of these is true:
- a real playable / viewable / downloadable artifact exists
- a blocker exists that the system cannot reasonably solve internally
- the user explicitly asks for status

Before the first real artifact exists, avoid repeated “making progress” style updates.
Those updates create false completion signals.

## Concurrency posture

Creative runs should distinguish:
- parallelizable units
- serial bridge units

Default policy:
- fill parallelizable units first
- reserve serial handling only for true continuity-dependent work

The main session should maintain a lightweight concurrency view:
- active lanes
- free concurrency budget
- next ready work units
- blocked units and why

Do not leave concurrency idle when clear independent work exists.

## Multi-scene continuity discipline

When a video production involves multiple separately-generated scenes:
1. **Protagonist lock**: generate a single protagonist reference image (text-to-image) at the start; all subsequent scene generations must use this same reference to maintain character identity.
2. **Tail-frame chaining**: each scene after the first must use the **last frame** of the preceding scene as the image-to-video input, ensuring visual continuity across cuts.
3. **Distinct scene actions**: each scene must depict a different action or story beat. Do not let multiple scenes repeat the same activity — every scene should advance the story.

These are default production rules. They do not require user reminders.

## Automatic handoff rule

Sub-results should trigger default next actions.
The system should not require the user to manually restart momentum after every completed worker.

Typical default handoffs:
- new visual asset arrives -> ingest into project state, update manifest, attempt redraft
- draft output arrives -> inspect gaps, queue bridge shots / missing segments / next render
- audio asset arrives -> prepare preview mix path
- final render arrives -> enter delivery flow immediately
- delivery-path validation succeeds -> prefer that path for the real output

A creative run should become quiet only when there is truly no next productive action.

## Completion ladder

Use the following layered completion model.
Do not confuse upstream progress with user completion.

### L1 plan layer
Script, outline, shot list, prompt pack, or concept only.
Not complete.

### L2 asset layer
Real media assets exist.
Still not complete.

### L3 draft layer
A draft cut exists for internal review.
Still not complete.

### L4 preview layer
A user-meaningful preview exists, typically with enough audio/packaging to review.
Near delivery, but still not final completion.

### L5 delivery layer
The final result object has been delivered to a place the user can directly access and open.
Only this counts as true completion unless the user explicitly asked for an earlier layer.

## Delivery-first discipline

Delivery should not be postponed until the end.
A delivery lane should validate at least one viable delivery path early.

For example, validate one or more of:
- direct attachment send
- user-identity send path when appropriate
- doc-based delivery
- drive/cloud link delivery
- alternate fallback path

The goal is to prevent the failure mode where the result exists but the user still cannot get it.

## Audio synchronization rule

If audio is likely to matter for the final result, audio work should not wait until the visual path is nearly done.
Audio should normally begin alongside visual generation unless there is a strong reason not to.

At minimum, the system should aim to have an audio package ready early enough that preview assembly does not become a last-minute scramble.

## Manifest / project-state truth rule

Creative runs often fail when project metadata lags behind real assets.
Whenever a meaningful asset, draft, or final output is produced, project truth should be updated as part of closeout rather than as an optional afterthought.

Typical synchronized truth objects include:
- manifest
- shot inventory
- concat lists
- output inventory
- delivery record

The chief controller should prefer current project truth over stale internal assumptions.

## Minimum acceptance checklist for a healthy creative OPC run

A good run should usually satisfy most of these:
- the chosen planning profile matched the real task shape
- multiple meaningful production lanes started early when `full_controller` was warranted
- concurrency was used where independent work existed
- sub-results triggered next actions automatically
- audio was not treated as a late afterthought when relevant
- project truth stayed aligned with actual produced assets
- at least one delivery path was validated before final closeout
- completion claims matched the real completion ladder
- user-facing updates were artifact-led, not explanation-led

## Anti-patterns

Do not normalize these failure modes:
- spawning only planning workers while downstream production is idle
- acting like a status reporter instead of a chief controller
- leaving concurrency budget idle without reason
- waiting for the user to push the next step after each sub-result
- calling drafts or raw assets “basically done”
- discovering delivery failure only after final output exists
- adding audio only after the visual pipeline is largely finished
- letting manifest/project truth drift behind reality
- using a light profile when the task clearly needed full-controller behavior

## Relationship to adjacent OPC references

This file specializes OPC for creative production.
It should be read together with the more general OPC references for:
- chief-controller posture
- status/intervention
- result closeout
- minimal run spec
- delivery closeout

Use this file when the missing guidance is not “whether OPC exists,” but how OPC should behave when the job is production-shaped.
This file owns the production-skeleton / five-lane / completion-ladder slice of the broader creative operating protocol.
For current SSOT ownership across the creative-production guidance set, see `references/opc-creative-ssot-map.md`