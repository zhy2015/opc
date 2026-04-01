# OPC Creative Auto-Handoff Map

Use this map to reduce the failure mode where a result comes back, the system explains it, and then waits for the user to restart motion.

## Core rule

For creative-production runs, every meaningful result type should have a default next action.
If no default next action exists, that gap should be made explicit during planning.

## Planning-profile sensitivity

Auto-handoff should respect the chosen planning profile.
The default next action after a result is not always the same in a light profile and a full-controller run.

Use this bias:
- `direct_review` — keep handoffs minimal; prefer execution -> review unless a real blocker forces expansion
- `research_execute_review` — allow research -> execution -> review, but do not invent extra lanes unless the task shape changed
- `execute_verify_review` — bias toward execution -> verification -> review, especially when artifact truth matters
- `full_controller` — allow multi-lane automatic handoff and concurrent activation when several meaningful lanes truly exist

If results repeatedly force expansion beyond the chosen profile, upgrade the run shape instead of hiding the complexity inside ad-hoc handoffs.

## Result -> next action map

### Script / prompt pack ready
Default next action:
- hand off to shot breakdown if needed
- hand off to visual generation for parallelizable scenes
- hand off to audio lane if narration text is stable enough

### Shot breakdown ready
Default next action:
- mark parallelizable scenes vs continuity-dependent bridge scenes
- queue visual generation lanes accordingly
- update project truth for scene inventory

### New scene asset ready
Default next action:
- ingest asset into project inventory
- verify non-empty / non-placeholder state
- update manifest / asset truth
- trigger draft assembly or gap review

### Batch of scene assets ready
Default next action:
- attempt draft assembly
- inspect missing bridges or weak sections
- queue next generation batch or repair lane

### Audio asset ready
Default next action:
- validate file exists and is usable
- sync audio inventory
- trigger preview mix path when enough visual material exists

### Draft cut ready
Default next action:
- classify current level honestly as draft, not delivery
- identify missing scenes / bridges / audio gaps / delivery blockers
- trigger next production step rather than narrating momentum

### Preview ready
Default next action:
- validate delivery path if not already validated
- decide whether the user asked for preview-level review or whether true delivery is still required
- trigger final packaging if upstream is stable enough

### Final render ready
Default next action:
- verify artifact exists and is non-empty
- verify delivery path
- if the active path is broken, invalidate it and choose a real fallback before talking big
- deliver through the validated path
- sync final output and delivery record

### Delivery success confirmed
Default next action:
- mark level as delivered
- close out remaining background lanes if any
- report completion briefly and honestly

## Profile-specific handoff rule

When using a lighter profile:
- do not silently simulate full-controller behavior through many hidden lane jumps
- prefer explicit profile upgrade if repeated cross-lane handoff becomes necessary
- keep the handoff graph understandable enough that the main session can still explain why the chosen profile remains valid

When using `full_controller`:
- default next action should bias toward maintaining filled production lanes
- delivery validation and project-truth sync should run as first-class follow-on actions, not optional cleanup

## Anti-patterns

Do not let these become default:
- result arrives -> explain status -> wait
- asset arrives -> no manifest sync
- draft arrives -> call it almost done without gap review
- render arrives -> attempt delivery for the first time
- claimed send success -> no verification
- a lightweight profile quietly expanding into full-controller behavior without an explicit upgrade

This handoff map is one owned slice of the broader creative operating protocol. For SSOT ownership, see `references/opc-creative-ssot-map.md`