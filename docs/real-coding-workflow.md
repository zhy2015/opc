# Real Coding Workflow

## 目标

用一条真实的 coding workflow 证明 OPC 不只是能管理文档任务，也能管理真实代码改动：

> CEO 建 task → planner 定义节点 → worker-code 修改控制面代码 → reviewer 审核放行 → synthesizer 生成交付摘要 → task 交付

这条样例重点验证：

1. coding 节点可以落到真实代码修改
2. review gate 可以作用于代码结果
3. delivery 节点可以把变更总结成可复用交付材料

---

## 工作流类型

- 类型：**Coding workflow**
- Task ID：`TASK-REAL-CODING`
- 目标：
  - planner 定义编码链路
  - worker-code 做真实改动
  - reviewer 审核改动
  - synthesizer 形成交付总结

---

## 节点设计

### 1. `NODE-PLAN-001`
- title: `Plan coding workflow`
- role: `planner`
- kind: `plan`
- 目标：定义 coding sequence

### 2. `NODE-CODE-001`
- title: `Implement control-plane improvements`
- role: `worker-code`
- kind: `execute`
- depends_on: `NODE-PLAN-001`
- 目标：做一处真实、有限、可审核的控制面改动

### 3. `NODE-REVIEW-001`
- title: `Review implementation result`
- role: `reviewer`
- kind: `review`
- depends_on: `NODE-CODE-001`
- 目标：审核代码改动是否满足范围与价值

### 4. `NODE-DELIVER-001`
- title: `Prepare coding delivery summary`
- role: `synthesizer`
- kind: `deliver`
- depends_on: `NODE-REVIEW-001`
- 目标：形成最终交付摘要

---

## 实际代码改动

本次 coding workflow 的真实改动是：

### `scripts/opc.py`
为 `record-result` 新增 `input_refs` 支持。

改动后，`record-result` 不仅能记录：
- `output_refs`

也能记录：
- `input_refs`

这意味着 downstream node 能显式声明：
- 自己依赖了哪些稳定上游产物
- 结果是基于哪些输入形成的

---

## 为什么这次改动有价值

### 1. 更清楚的 artifact lineage
之前只记录输出，不记录输入。现在可以明确：
- 一个 review 结论基于哪份代码 / 哪份草稿
- 一个 delivery summary 基于哪份实现结果 / 哪份审核结果

### 2. 更利于 resume / audit
恢复任务时，不止知道“产出了什么”，还知道“这步是基于什么做的”。
这让 resume 和审计都更稳。

### 3. 证明 coding workflow 不是纸面流程
这次不是写“coding workflow 说明文档”，而是：
- 真建 task
- 真建 node
- 真改代码
- 真过 review
- 真做 delivery

---

## 实际运行结果

### Task 最终状态
- `delivered`

### Node 最终状态
- `NODE-PLAN-001`: `done`
- `NODE-CODE-001`: `done`
- `NODE-REVIEW-001`: `done`
- `NODE-DELIVER-001`: `done`

### Review 结果
- review count: `1`
- 代码改动已通过 reviewer gate

### Event 记录
- event count: `32`

---

## 稳定产物

本次 workflow 形成的稳定产物包括：

- `docs/real-coding-workflow.md`
- `scripts/opc.py`
- `reviews/TASK-REAL-CODING-approval.md`
- `tasks/TASK-REAL-CODING/artifacts/delivery-summary.md`

最终 `resume_cursor` 已可表达：

```json
{
  "completed_nodes": [
    "NODE-CODE-001",
    "NODE-DELIVER-001",
    "NODE-PLAN-001",
    "NODE-REVIEW-001"
  ],
  "next_nodes": [],
  "stable_artifacts": [
    "docs/real-coding-workflow.md",
    "reviews/TASK-REAL-CODING-approval.md",
    "scripts/opc.py",
    "tasks/TASK-REAL-CODING/artifacts/delivery-summary.md"
  ]
}
```

---

## 它证明了什么

这条样例证明 OPC v1 已经能支撑一条真实 coding workflow：

1. **planner 可定义编码链路**
2. **worker-code 可做真实代码改动**
3. **review gate 可审核代码结果**
4. **delivery 节点可总结已交付变更**
5. **resume_cursor 可沉淀代码任务的稳定产物**

---

## 当前意义

`TASK-REAL-CODING` 是 OPC 第二条真实闭环样例。

它与 `TASK-REAL-RESEARCH` 形成互补：
- research 证明 OPC 能管理调研与文档闭环
- coding 证明 OPC 能管理真实代码修改闭环

这说明 OPC 已不再只是“有规范、有控制面”，而是已经开始具备：

> **跨任务类型的真实闭环能力**

---

## 下一步建议

### P1
- research / coding / social 三条真实链路已并列成立
- 下一步从“补第三条”转向“补 task ledger / dispatch / runtime bridge”

### P2
- 给 coding workflow 补带 `bind-session` 的 runtime 版
- 用独立 session 跑 planner / worker-code / reviewer
- 验证 OPC 与 OpenClaw runtime 桥接

---

## 结论

`TASK-REAL-CODING` 已完成并交付。

它证明 OPC 当前控制面已经足以管理一条真实代码改动链路；现在 research / coding / social 三条真实工作流都已成立，下一步重点是补 task ledger、dispatch artifact 与 runtime 化桥接。
