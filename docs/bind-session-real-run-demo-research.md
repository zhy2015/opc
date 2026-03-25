# Bind-Session Real Run Demo（Research）

## Goal

Record one actual end-to-end OPC control-plane run that proves bind-session is not only a documentation pattern, but an executable ledger workflow.

---

## Demo task

- Task: `TASK-BIND-SESSION-DEMO-RESEARCH`
- Node: `NODE-RESEARCH-001`
- Session key: `sess_demo_research_001`
- Runtime: `subagent`
- Session mode: `session`

---

## Commands executed

```bash
python3 scripts/opc.py create-task \
  --task-id TASK-BIND-SESSION-DEMO-RESEARCH \
  --title 'Bind session demo research' \
  --goal 'Validate render-bind-result-review closure on a research lane'

python3 scripts/opc.py task-plan-init TASK-BIND-SESSION-DEMO-RESEARCH \
  --task-class C \
  --acceptance 'dispatch rendered' 'session bound' 'review pending'

python3 scripts/opc.py create-node TASK-BIND-SESSION-DEMO-RESEARCH \
  --node-id NODE-RESEARCH-001 \
  --title 'Collect research under bound session' \
  --role worker-research \
  --worker-type subagent \
  --status queued

python3 scripts/opc.py update-node-status TASK-BIND-SESSION-DEMO-RESEARCH NODE-RESEARCH-001 assigned --actor ceo
python3 scripts/opc.py render-dispatch-payload TASK-BIND-SESSION-DEMO-RESEARCH NODE-RESEARCH-001 --actor ceo
python3 scripts/opc.py bind-session TASK-BIND-SESSION-DEMO-RESEARCH NODE-RESEARCH-001 \
  sess_demo_research_001 \
  --runtime subagent \
  --worker-type research-worker \
  --session-mode session \
  --actor ceo
python3 scripts/opc.py update-node-status TASK-BIND-SESSION-DEMO-RESEARCH NODE-RESEARCH-001 running --actor ceo
python3 scripts/opc.py record-result TASK-BIND-SESSION-DEMO-RESEARCH NODE-RESEARCH-001 \
  --summary 'Bound demo session and validated ledger writeback path.' \
  --output-ref tasks/TASK-BIND-SESSION-DEMO-RESEARCH/artifacts/research-findings.md \
  --input-ref tasks/TASK-BIND-SESSION-DEMO-RESEARCH/artifacts/NODE-RESEARCH-001-dispatch.json \
  --actor ceo
python3 scripts/opc.py mark-review-pending TASK-BIND-SESSION-DEMO-RESEARCH NODE-RESEARCH-001 --stage result_gate --actor ceo
```

---

## What was verified

### 1. Dispatch artifact rendering works
Confirmed artifact path:
- `tasks/TASK-BIND-SESSION-DEMO-RESEARCH/artifacts/NODE-RESEARCH-001-dispatch.json`

### 2. Session binding writes back into node ledger
Confirmed node carries:
- `assigned_session = sess_demo_research_001`
- `runtime = subagent`
- `session_mode = session`

### 3. Result writeback works after bind-session
Confirmed node result writeback includes:
- summary
- input refs
- output refs

### 4. Review gate can be requested after running state
Confirmed node transitions into:
- `review_pending`

### 5. Task report reflects runtime-bound state
Observed in `task-report`:
- node shown with `session=sess_demo_research_001`
- stage shown as `awaiting_result_review`
- review gate identified as next CEO action

---

## Important finding

Trying to run `mark-review-pending` directly on an already completed real task fails as expected:

> `mark-review-pending requires node status 'running', got 'done'`

This is good news: the state machine is enforcing legal order. It also means real bind-session closure demos should be run on dedicated demo tasks, not by mutating already delivered reference tasks.

---

## Why this matters

This demo proves OPC already supports the minimum real control-plane sequence:

1. create task / node
2. render dispatch artifact
3. bind node to session
4. move node to running
5. write result back into ledger
6. request result gate

That is the first real evidence that bind-session is executable control-plane behavior, not just architecture prose.

---

## Suggested next step

Repeat the same demo pattern for:
- coding lane
- social lane

Then compare the three demos under one runtime-bridge validation sheet.
