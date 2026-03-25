# Bind-Session Real Run Demo（Social）

## Goal

Record one actual end-to-end OPC control-plane run for the social lane, proving bind-session works with external-action-oriented nodes.

---

## Demo task

- Task: `TASK-BIND-SESSION-DEMO-SOCIAL`
- Node: `NODE-OPERATE-001`
- Session key: `sess_demo_social_001`
- Runtime: `subagent`
- Session mode: `session`

---

## Verified sequence

1. create task / node
2. render dispatch payload
3. bind session into node ledger
4. move node to `running`
5. write stable result refs back into ledger
6. request `result_gate`

---

## Verified outcome

`task-report` confirms:
- node status = `review_pending`
- role = `operator-social`
- session = `sess_demo_social_001`
- runtime = `subagent / session`
- result / input_refs / output_refs are all written into ledger

---

## Why this matters

This proves social workflow can bind real external-action responsibility to a specific session before review and delivery.

---

## Related task

- `tasks/TASK-BIND-SESSION-DEMO-SOCIAL/`
