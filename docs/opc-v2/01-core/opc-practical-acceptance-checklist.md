# OPC Practical Acceptance Checklist

Use this checklist to verify whether OPC is actually improving complex work rather than merely making it more elaborate.

## Default acceptance reflex

Ask these first:
- **did delegation create real leverage?**
- **did the main session stay in control?**
- **did the user get one coherent result instead of orchestration residue?**

If the answer to any of these is no, OPC did not really pass acceptance yet.

## Throughput

- [ ] Did controlled delegation reduce main-session bottleneck?
- [ ] Did the task complete faster or with more parallel useful progress than a single-thread run would likely allow?
- [ ] For production-shaped tasks, were enough real production lanes active early instead of only analysis/planning lanes?
- [ ] Was available parallelism actually used where independent work existed?

## Clarity

- [ ] Were sub-task boundaries explicit?
- [ ] Was the main session able to see each worker's state clearly enough to intervene?
- [ ] Did the run avoid duplicated or overlapping work?

## Intervention

- [ ] Were blockers made visible rather than silently waited on?
- [ ] Did the main session intervene when needed?
- [ ] Did the intervention choice match the problem (steer vs reassign vs kill)?

## Integration quality

- [ ] Were sub-results integrated into a coherent final delivery?
- [ ] Were blockers / risks / remaining items surfaced honestly?
- [ ] Did the user receive one clean result rather than internal fragments?
- [ ] For creative-production tasks, did sub-results automatically trigger the next meaningful action rather than stalling into commentary?
- [ ] Did completion language stay honest about whether the run was at plan, asset, draft, preview, or true delivery level?

## User-consumable result

- [ ] Does a task-level deliverable exist, rather than only worker-local fragments?
- [ ] Can the user directly access the result object now?
- [ ] Is the object clearly one of: external delivery / fallback artifact / internal-only result?
- [ ] If it is fallback, is it labeled as fallback rather than as the intended delivery path?
- [ ] If it is internal-only or partial, is the user-facing language keeping it below true completion?

## Cost discipline

- [ ] Was the number of sub-agents proportional to task complexity?
- [ ] Did parallelism create more leverage than confusion?
- [ ] Did the system avoid the opposite failure mode of under-delegating and leaving obvious independent production work idle?

## Retention discipline

- [ ] Was useful orchestration continuity preserved only when warranted?
- [ ] Was orchestration residue kept out of core memory?

## Creative-production truthfulness

- [ ] Did user-facing language stay aligned with the highest verified completion layer?
- [ ] Were worker claims, monitors, and planned fallbacks prevented from inflating the apparent state?
- [ ] Did background continuation represent real liveness rather than ritualized optimism?