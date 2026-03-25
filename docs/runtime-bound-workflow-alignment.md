# OPC Runtime-Bound Workflow Alignment（Research / Coding / Social）

## Goal

Confirm that the three real workflows now meet the same minimum runtime-bound standard, rather than leaving social as the only fully articulated lane.

---

## Minimum standard

A workflow lane is considered **runtime-bound ready** when it has:

1. a real `task.json`
2. concrete `nodes/*.json`
3. at least one dispatch artifact under `artifacts/`
4. `events.jsonl`
5. a bind-session example document
6. stable delivery/result artifacts
7. an explicit review / resume story

---

## Lane check

| Workflow | task.json | nodes | dispatch artifacts | events | bind-session doc | result artifacts | review / resume story | Verdict |
|---|---|---|---|---|---|---|---|---|
| Research | yes | yes | yes | yes | yes | yes | yes | aligned |
| Coding | yes | yes | yes | yes | yes | yes | yes | aligned |
| Social | yes | yes | yes | yes | yes | yes | yes | aligned |

---

## Research lane

Key assets:
- `tasks/TASK-REAL-RESEARCH/task.json`
- `tasks/TASK-REAL-RESEARCH/nodes/*.json`
- `tasks/TASK-REAL-RESEARCH/artifacts/NODE-RESEARCH-001-dispatch.json`
- `tasks/TASK-REAL-RESEARCH/artifacts/NODE-WRITE-001-dispatch.json`
- `tasks/TASK-REAL-RESEARCH/artifacts/NODE-REVIEW-001-dispatch.json`
- `tasks/TASK-REAL-RESEARCH/artifacts/research-brief.md`
- `tasks/TASK-REAL-RESEARCH/artifacts/final-brief.md`
- `tasks/TASK-REAL-RESEARCH/events.jsonl`
- `docs/task-real-research-bind-session-example.md`

Runtime-bound meaning:
- research collection can be bound to an accountable session
- synthesis and review can be resumed from stable artifacts
- final brief is not only a chat output, but a ledger-backed artifact

---

## Coding lane

Key assets:
- `tasks/TASK-REAL-CODING/task.json`
- `tasks/TASK-REAL-CODING/nodes/*.json`
- `tasks/TASK-REAL-CODING/artifacts/NODE-CODE-001-dispatch.json`
- `tasks/TASK-REAL-CODING/artifacts/NODE-REVIEW-001-dispatch.json`
- `tasks/TASK-REAL-CODING/artifacts/NODE-DELIVER-001-dispatch.json`
- `tasks/TASK-REAL-CODING/artifacts/delivery-summary.md`
- `tasks/TASK-REAL-CODING/events.jsonl`
- `docs/task-real-coding-bind-session-example.md`

Runtime-bound meaning:
- implementation can be assigned to a specific coding session
- reviewer gate remains explicit before delivery
- code changes and approval artifacts can be traced back to one node/session path

---

## Social lane

Key assets:
- `tasks/TASK-REAL-SOCIAL/task.json`
- `tasks/TASK-REAL-SOCIAL/nodes/*.json`
- `tasks/TASK-REAL-SOCIAL/artifacts/NODE-OPERATE-001-dispatch.json`
- `tasks/TASK-REAL-SOCIAL/artifacts/NODE-REVIEW-001-dispatch.json`
- `tasks/TASK-REAL-SOCIAL/artifacts/NODE-DELIVER-001-dispatch.json`
- `tasks/TASK-REAL-SOCIAL/artifacts/delivery-summary.md`
- `tasks/TASK-REAL-SOCIAL/events.jsonl`
- `docs/task-real-social-bind-session-example.md`

Runtime-bound meaning:
- external write action is tied to accountable session execution
- post-action verification is part of the lane, not an afterthought
- external side effects remain reviewable in ledger form

---

## What changed in understanding

Earlier wording suggested research / coding still needed to be upgraded to social-grade runtime-bound samples.

After re-checking the repository, the more accurate statement is:

> Research / Coding / Social already all have the minimum runtime-bound sample shape; the remaining work is no longer “create them from scratch”, but “improve automation, expand real bind-session runs, and tighten status linkage”.

---

## Remaining gap after alignment

The remaining gaps are now:

1. more real bind-session runs, not just example docs
2. tighter review-result → node/task status writeback
3. better operator-facing summary/status views
4. product decision: project vs skill vs standalone repo

---

## One-line conclusion

**All three real OPC lanes are now aligned at the minimum runtime-bound sample level; the next stage is operational hardening, not structural catch-up.**
