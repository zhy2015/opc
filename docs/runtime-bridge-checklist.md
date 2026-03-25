# Runtime Bridge Checklist

## Goal

Use one shared checklist to verify that research / coding / social workflows are all bridged correctly from OPC ledger to real OpenClaw sessions.

---

## 1. Ledger readiness

- [ ] `task.json` exists
- [ ] `nodes/*.json` exists for the active workflow
- [ ] `artifacts/*-dispatch.json` exists for each runtime-bound node
- [ ] `events.jsonl` is present

## 2. Session binding

- [ ] target node has `assigned_session`
- [ ] target node has `runtime`
- [ ] target node has `session_mode`
- [ ] target node has `dispatch_payload_ref`
- [ ] binding was written by CEO / dispatcher role

## 3. Dispatch delivery

- [ ] CEO created or reused the correct session
- [ ] CEO sent the dispatch payload into that session
- [ ] worker stayed inside node scope
- [ ] execution output maps back to expected `output_refs`

## 4. Result recording

- [ ] `record-result` wrote stable `output_refs`
- [ ] upstream dependencies are captured in `input_refs` where applicable
- [ ] node has `result_summary`
- [ ] event log contains `result_recorded`

## 5. Review gate

- [ ] node entered `review_pending` when required
- [ ] reviewer decision was recorded
- [ ] event log contains `review_passed` or review failure equivalent
- [ ] node only becomes `done` after result gate resolution

## 6. Workflow-specific checks

### Research
- [ ] source findings became stable artifacts
- [ ] synthesis / review chain stayed auditable

### Coding
- [ ] code change is traceable to a bound session
- [ ] modified files and review artifact are linked back to the node

### Social
- [ ] platform action used real page flow rather than guessed API writes
- [ ] post-action verification was recorded
- [ ] external write action is attributable to one bound session

## 7. Done definition

A workflow is runtime-bridge complete when:

- ledger exists
- runtime session binding exists
- dispatch was sent
- result was written back
- review gate resolved
- final stable artifacts are recoverable from `resume_cursor`
