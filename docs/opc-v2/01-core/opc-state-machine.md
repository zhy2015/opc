# OPC State Machine

This file defines the minimal state machine for OPC-controlled work.

## States

- `queued` — task has been recognized as a candidate for OPC, but not yet decomposed
- `planned` — sub-task structure exists
- `reviewed` — the dispatch plan has passed the dispatch review gate
- `dispatched` — sub-agents have been spawned / assigned
- `doing` — delegated work is in active execution
- `blocked` — progress is stalled or a blocker requires intervention
- `review` — sub-results are back and are being checked / integrated
- `done` — final integrated result is ready
- `cancelled` — OPC run intentionally stopped

## Attached dimensions

Keep the main flow state small, but also track attached dimensions when they matter:
- `delivery_status` — `not_ready` / `partial` / `delivered` / `fallback_delivered` / `internal_only`
- `review_outcome` — `approved` / `changes_requested`
- `sendback_target` — `planning` / `research` / `execution` / `verification` / `delivery_packaging`

These attached dimensions exist to prevent a common mistake: treating workflow progress and delivery truth as the same thing.

## Default operating reflex

Think in this short path first:

`queued -> planned -> reviewed -> dispatched -> doing -> review -> done`

Meaning:
- do not dispatch before the plan exists
- do not confuse dispatched with meaningful progress
- do not skip review on the way to done
- do not upgrade to true completion if delivery_status still says `partial`, `fallback_delivered`, or `internal_only`

## Default transition path

`queued -> planned -> reviewed -> dispatched -> doing -> review -> done`

## Allowed exception paths

- `planned -> blocked`
- `reviewed -> blocked`
- `dispatched -> blocked`
- `doing -> blocked`
- `blocked -> doing`
- `blocked -> review`
- `blocked -> cancelled`
- `review -> planned` when changes are requested and work must go back through a structured send-back path
- any pre-done state -> `cancelled`

## Responsibility hints

- main session owns: `queued`, `planned`, `reviewed`, `review`, `done`, `cancelled`
- sub-agent execution usually lives inside: `doing`
- `blocked` may be identified by either the main session or a sub-agent, but the main session owns the intervention decision
- delivery-status truth remains a main-session responsibility even when workers report progress

## Anti-patterns

- spawning sub-agents without reaching at least `planned`
- treating `dispatched` and `doing` as identical
- letting blocked work remain invisible
- skipping `review` and sending fragmented sub-results directly to the user
- letting a positive workflow state override a weaker delivery state