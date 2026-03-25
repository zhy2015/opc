# Schemas

## 目标

把 OPC 从“概念架构”推进到“可实现规范”。

本文件定义四类核心 schema：

- Task Schema
- Node Schema
- Review Schema
- Event Schema

这些 schema 不绑定具体数据库，可先用于：

- Markdown front-matter
- JSON 文件
- JSONL 事件流
- 后续 API / DB 模型

---

## 1. Task Schema

任务是公司级经营对象。

### 必填字段

```json
{
  "task_id": "TASK-001",
  "title": "实现 OPC 的最小任务控制流",
  "goal": "构建一个可创建任务、派发节点、审核结果的最小运行闭环",
  "status": "triaged",
  "priority": "high",
  "owner": "ceo-session",
  "acceptance_criteria": [
    "可以创建任务",
    "可以生成计划",
    "可以审核计划",
    "可以分配执行节点"
  ],
  "created_at": "2026-03-25T02:00:00Z",
  "updated_at": "2026-03-25T02:10:00Z"
}
```

### 推荐字段

```json
{
  "constraints": ["优先使用 OpenClaw 原生能力", "MVP 不依赖数据库"],
  "context_refs": ["docs/vision.md", "docs/control-plane.md"],
  "tags": ["mvp", "control-plane"],
  "budget": {
    "max_parallel": 3,
    "preferred_models": ["default"],
    "token_budget": 200000,
    "cost_budget_usd": 10
  },
  "resume_cursor": {
    "completed_nodes": ["NODE-001"],
    "next_nodes": ["NODE-002"],
    "stable_artifacts": ["tasks/TASK-001/plan.md"]
  },
  "delivery": {
    "channel": "main-session",
    "format": "markdown"
  }
}
```

### 状态枚举

- `new`
- `triaged`
- `planned`
- `plan_review`
- `plan_rejected`
- `dispatched`
- `running`
- `blocked`
- `awaiting_review`
- `rework`
- `delivered`
- `archived`
- `paused`
- `resumable`
- `failed`
- `cancelled`

---

## 2. Node Schema

节点是任务之下的可执行单元。

### 必填字段

```json
{
  "node_id": "NODE-002",
  "task_id": "TASK-001",
  "kind": "execute",
  "title": "实现任务状态机文件模型",
  "assigned_role": "worker-code",
  "status": "queued",
  "depends_on": ["NODE-001"],
  "created_at": "2026-03-25T02:12:00Z",
  "updated_at": "2026-03-25T02:12:00Z"
}
```

### 推荐字段

```json
{
  "assigned_session": "sess_worker_code_01",
  "input_refs": ["tasks/TASK-001/plan.md"],
  "output_refs": ["tasks/TASK-001/artifacts/state-machine.json"],
  "instructions": "根据 plan 实现最小状态机文件结构",
  "acceptance_criteria": ["字段完整", "状态合法", "示例可读"],
  "retry_count": 0,
  "max_retries": 2,
  "last_error": null,
  "review_required": true,
  "estimated_effort": "medium"
}
```

### kind 枚举

- `triage`
- `plan`
- `review`
- `dispatch`
- `execute`
- `research`
- `document`
- `ops`
- `compliance`
- `summarize`

### 节点状态枚举

- `queued`
- `assigned`
- `running`
- `blocked`
- `review_pending`
- `rework`
- `done`
- `failed`
- `skipped`
- `cancelled`

---

## 3. Review Schema

审核记录必须结构化。

### 必填字段

```json
{
  "review_id": "REV-001",
  "task_id": "TASK-001",
  "target_node_id": "NODE-001",
  "reviewer_role": "reviewer",
  "reviewer_session": "sess_reviewer_01",
  "stage": "plan_gate",
  "decision": "reject",
  "reasons": [
    "缺少结果验收路径",
    "没有定义失败后恢复机制"
  ],
  "required_changes": [
    "补充恢复点设计",
    "补充交付标准"
  ],
  "created_at": "2026-03-25T02:15:00Z"
}
```

### stage 枚举

- `plan_gate`
- `result_gate`
- `compliance_gate`
- `manual_gate`

### decision 枚举

- `approve`
- `reject`
- `conditional_approve`

### 推荐字段

```json
{
  "severity": "medium",
  "score": 0.68,
  "notes": "计划结构基本正确，但还未满足可恢复要求"
}
```

---

## 4. Event Schema

事件是系统回放与审计基础。

### 基础结构

```json
{
  "event_id": "EVT-001",
  "task_id": "TASK-001",
  "node_id": "NODE-001",
  "type": "plan_submitted",
  "actor": {
    "role": "planner",
    "session": "sess_planner_01"
  },
  "payload": {
    "artifact": "tasks/TASK-001/plan.md"
  },
  "timestamp": "2026-03-25T02:14:00Z"
}
```

### type 枚举

- `task_created`
- `task_updated`
- `task_paused`
- `task_resumed`
- `task_cancelled`
- `plan_requested`
- `plan_submitted`
- `plan_rejected`
- `plan_approved`
- `node_dispatched`
- `node_started`
- `node_blocked`
- `node_completed`
- `node_failed`
- `review_requested`
- `review_passed`
- `review_failed`
- `delivery_completed`
- `task_archived`

---

## 5. Agent Resource Schema

如果 OPC 要真正管理 agent，就要为 agent 建模。

```json
{
  "agent_id": "worker-code-01",
  "role": "worker-code",
  "session_key": "sess_worker_code_01",
  "model": "default",
  "skills": ["coding-agent"],
  "capacity": 1,
  "current_load": 1,
  "health": "active",
  "permissions": ["read", "write", "exec"],
  "quality_history": {
    "completed": 12,
    "rework_count": 3,
    "failure_count": 1
  }
}
```

### health 枚举

- `idle`
- `active`
- `stalled`
- `error`
- `offline`

---

## 6. 文件落地建议

MVP 阶段建议：

```text
tasks/
  TASK-001/
    task.json
    plan.md
    review-plan.json
    review-result.json
    events.jsonl
    nodes/
      NODE-001.json
      NODE-002.json
    artifacts/
```

---

## 7. 设计原则

- schema 先服务控制面，而不是先服务 UI
- 字段必须支撑 pause / resume / review / reroute
- 所有关键决策都应有结构化记录
- 所有 schema 都应兼容后续 API 化

---

## 8. 结论

有了这些 schema，OPC 就不再只是“多 Agent 的想法”，而开始具备真正可实现的协议骨架。
