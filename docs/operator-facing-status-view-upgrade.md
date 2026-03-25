# Operator-Facing Status View Upgrade

## Goal

Make OPC status output more useful for operator / manager style usage, not just low-level ledger inspection.

---

## Change made

Enhanced `task-board` in `scripts/opc.py` to include:
- `priority`
- `node_counts`
- `active_session_count`
- `active_sessions`
- `delivery_ready`
- `operator_summary.focus`
- `operator_summary.headline`

This makes `task-board` a compact operations-facing snapshot instead of a thin raw status dump.

---

## What operator can now see quickly

For one task, `task-board` now answers:
- 当前任务优先级是什么
- 节点状态分布是什么
- 有没有活跃 session
- 当前是卡在 blocked / review / rework / delivery 哪一层
- 是否接近可交付
- 运营上下一步应该关注什么

---

## Verified examples

Validated with:
- `TASK-BIND-SESSION-DEMO-SOCIAL` → focus = `review`
- `TASK-BIND-SESSION-DEMO-CODING` → focus = `delivery`
- `TASK-REVIEW-REWORK-DEMO` → focus = `execution`

This confirms the view can distinguish different operating states.

---

## One-line conclusion

**`task-board` is now good enough to act as a compact operator-facing task panel for OPC.**
