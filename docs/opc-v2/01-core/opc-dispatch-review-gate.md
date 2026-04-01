# OPC Dispatch Review Gate

This file defines the pre-dispatch review gate for OPC.
The goal is to prevent parallelism from creating chaos rather than leverage.

## Core rule

Before spawning sub-agents, the main session should review whether delegation is actually warranted and whether the sub-task boundaries are good enough.

## Default dispatch reflex

Before spawning, check these five things fast:

1. **Worth delegating?** If not, stay in main session.
2. **Scope clear?** If not, clarify before dispatch.
3. **Parallel or staged?** Do not fan out serial work.
4. **Expected artifact clear?** Each sub-agent should have a concrete output shape.
5. **Done condition / fallback clear?** The main session should know how this returns for review.

If any of these are missing, dispatch is not ready yet.

## Review questions

1. Is this task complex enough to benefit from controlled parallel execution?
2. Which parts are truly parallelizable, and which parts require sequence or shared context?
3. Are the sub-task boundaries explicit enough to avoid duplicated work?
4. Does each sub-agent have a clear expected output?
5. Is there an obvious blocker, dependency, or ownership ambiguity that should be resolved before dispatch?
6. Would one or two sub-agents outperform a larger fan-out here?

For creative-production tasks, add these extra gate questions before dispatch:
7. Have we opened enough production lanes, or are we only dispatching planning work?
8. Which lane owns delivery-path validation?
9. Which lane owns audio early enough to support preview rather than late patching?
10. Which outputs must trigger automatic handoff when they return?
11. What project-truth object must be updated after each meaningful asset or draft result?

## Default outcomes

- if the task is not worth parallelizing -> stay in main session
- if decomposition is still fuzzy -> improve the plan before dispatch
- if sub-task boundaries are clear -> approve dispatch
- if the task contains strong serial dependencies -> use staged delegation rather than all-at-once fan-out

For creative-production tasks, reject dispatch plans that launch only upstream planning lanes while leaving generation, audio, render, or delivery ownership undefined.

## Anti-patterns

- spawning because parallelism feels powerful
- splitting work before the object boundary is clear
- assigning overlapping scopes to multiple sub-agents
- dispatching without a clear expected output per agent
- treating cron/background monitoring as a substitute for active production ownership
- dispatching delivery or monitoring lanes without defining verification conditions
