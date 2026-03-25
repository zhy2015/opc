# Bind-Session Real Run Demo（Coding）

## Goal

Record one actual end-to-end OPC control-plane run for the coding lane, proving bind-session works with implementation-oriented nodes.

---

## Demo task

- Task: `TASK-BIND-SESSION-DEMO-CODING`
- Node: `NODE-CODE-001`
- Session key: `sess_demo_code_001`
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
- role = `worker-code`
- session = `sess_demo_code_001`
- runtime = `subagent / session`
- result / input_refs / output_refs are all written into ledger

---

## Why this matters

This proves coding workflow can be runtime-bound with explicit session accountability before review and delivery.

---

## Related task

- `tasks/TASK-BIND-SESSION-DEMO-CODING/`
