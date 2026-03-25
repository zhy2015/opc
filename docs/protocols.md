# Protocols

## 目标

定义 OPC 中主会话与各类子 Agent 的标准交互协议。

这里的“协议”不是网络协议，而是：

- 谁给谁发什么
- 输入必须包含什么
- 输出必须返回什么
- 哪些阶段必须经过审核

---

## 1. CEO → Router Protocol

### 用途
用于初始分拣与任务建单前整理。

### 输入
- 原始用户请求
- 当前已知约束
- 是否已有相关 task

### Router 输出
```json
{
  "classification": "complex_task",
  "title": "为 OPC 设计可实现协议层",
  "goal_summary": "将多 agent 管理架构推进到 schema 与协议级别",
  "constraints": ["优先 OpenClaw 原生", "文档先行"],
  "suggested_next_role": "planner"
}
```

### 规则
- Router 不直接生成执行计划
- Router 不直接交付结果
- Router 的职责是压缩和标准化任务入口

---

## 2. CEO → Planner Protocol

### 输入包
```json
{
  "task_id": "TASK-001",
  "goal": "构建 OPC 协议层",
  "acceptance_criteria": ["定义 schema", "定义协议"],
  "constraints": ["MVP 先文件化"],
  "context_refs": ["docs/vision.md", "docs/control-plane.md"],
  "budget": {
    "max_parallel": 2,
    "preferred_models": ["default"]
  }
}
```

### Planner 输出
```json
{
  "plan_summary": "先定义 schema，再定义协议，再定义目录落地",
  "nodes": [
    {"node_id": "NODE-001", "kind": "plan", "title": "整理 schema 草案"},
    {"node_id": "NODE-002", "kind": "document", "title": "整理协议草案", "depends_on": ["NODE-001"]}
  ],
  "risks": ["协议过早复杂化"],
  "parallel_groups": []
}
```

### 规则
- Planner 必须输出节点、依赖、风险
- Planner 不直接启动执行
- Planner 的输出必须进入 Plan Gate

---

## 3. Planner → Reviewer (Plan Gate) Protocol

### 输入
- plan summary
- node list
- risks
- acceptance criteria

### Reviewer 输出
```json
{
  "decision": "approve",
  "reasons": ["计划结构清晰，范围可控"],
  "required_changes": []
}
```

或

```json
{
  "decision": "reject",
  "reasons": ["缺少恢复机制设计"],
  "required_changes": ["补充 resume 路径"]
}
```

### 规则
- Reviewer 不自己改 plan，只提出意见或封驳
- 拒绝时必须给出可执行修改要求

---

## 4. CEO / Dispatcher → Worker Protocol

### 输入包
```json
{
  "task_id": "TASK-001",
  "node_id": "NODE-002",
  "role": "worker-doc",
  "mission_context": {
    "goal": "定义协议层文档"
  },
  "working_context": {
    "input_refs": ["tasks/TASK-001/plan.md"]
  },
  "policy_context": {
    "must_not": ["跳过审核", "私自修改任务范围"]
  },
  "acceptance_criteria": ["结构完整", "可落地"],
  "output_contract": {
    "expected_artifact": "tasks/TASK-001/artifacts/protocols.md"
  }
}
```

### Worker 输出
```json
{
  "status": "completed",
  "artifact_refs": ["tasks/TASK-001/artifacts/protocols.md"],
  "summary": "已完成协议文档草案",
  "issues": []
}
```

### 规则
- Worker 只处理被分配节点
- Worker 不能擅自扩大范围
- Worker 完成后进入 Result Gate（若 review_required=true）

---

## 5. Worker → Reviewer (Result Gate) Protocol

### 输入
- node output
- artifact refs
- node acceptance criteria

### Reviewer 输出
```json
{
  "decision": "conditional_approve",
  "reasons": ["整体可用，但需补充 event schema 示例"],
  "required_changes": ["增加示例"],
  "severity": "low"
}
```

### 规则
- Reviewer 针对结果与验收标准对齐
- 不允许“模糊通过”

---

## 6. Reviewer → Rework Protocol

当 reviewer 打回时，必须返回结构化返工单：

```json
{
  "task_id": "TASK-001",
  "node_id": "NODE-002",
  "rework_reason": "缺少 event schema 示例",
  "required_changes": ["补充 1 个 JSON 示例"],
  "deadline_hint": "same_day"
}
```

### 规则
- 返工必须具体到可执行动作
- 返工不重置整个任务，只重开相关 node

---

## 7. CEO → Synthesizer Protocol

### 用途
汇总多个节点结果，对外形成最终交付。

### 输入
- 已批准结果的 artifact refs
- 交付对象
- 交付格式要求

### 输出
```json
{
  "delivery_summary": "已完成 OPC 协议层定义",
  "included_artifacts": [
    "docs/schemas.md",
    "docs/protocols.md"
  ],
  "followups": ["下一步进入 runtime skeleton"]
}
```

---

## 8. CEO 管理动作协议

### pause_task
```json
{"action": "pause_task", "task_id": "TASK-001", "reason": "waiting_for_user"}
```

### resume_task
```json
{"action": "resume_task", "task_id": "TASK-001", "resume_from": "NODE-002"}
```

### reroute_node
```json
{"action": "reroute_node", "task_id": "TASK-001", "node_id": "NODE-002", "new_role": "worker-doc"}
```

### cancel_task
```json
{"action": "cancel_task", "task_id": "TASK-001", "reason": "scope_changed"}
```

---

## 9. 协议设计原则

- 输入尽量结构化
- 输出尽量可验证
- 所有 gate 都必须显式化
- 所有返工都要可执行
- 所有管理动作都应能落入 event log

---

## 10. 结论

协议层让 OPC 从“组织思想”变成“可以实际驱动 session 与任务流的操作规范”。
