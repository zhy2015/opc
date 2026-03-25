# First Real Workflow

## 目标

用一条真实的 research workflow 证明 OPC 已经不只是文档概念，而是可落地的 v1 任务流：

> CEO 建 task → planner 定义节点 → research 产出研究材料 → writer 产出综合简报 → reviewer 审核放行 → task 交付

这条样例重点验证三件事：

1. task / node / review / event 台账可真实落地
2. dispatch payload 可稳定输出给后续执行者
3. resume / review / delivery 可以串成完整闭环

---

## 工作流类型

- 类型：**Research workflow**
- Task ID：`TASK-REAL-RESEARCH`
- 目标：
  - planner 定义节点与依赖
  - research 收集一手规则依据
  - writer 产出结构化简报
  - reviewer 做结果门
  - CEO 完成交付

---

## 节点设计

### 1. `NODE-PLAN-001`
- title: `Plan research workflow`
- role: `planner`
- kind: `plan`
- 目标：定义本次 research 流程的节点与依赖

### 2. `NODE-RESEARCH-001`
- title: `Collect primary-source research`
- role: `worker-research`
- kind: `execute`
- depends_on: `NODE-PLAN-001`
- 目标：采集本地一手规范依据

### 3. `NODE-WRITE-001`
- title: `Write synthesis brief`
- role: `writer`
- kind: `synthesize`
- depends_on: `NODE-RESEARCH-001`
- 目标：输出结构化研究简报

### 4. `NODE-REVIEW-001`
- title: `Review final brief`
- role: `reviewer`
- kind: `review`
- depends_on: `NODE-WRITE-001`
- 目标：做最终结果门，决定 approve / reject

---

## 实际运行结果

### Task 最终状态
- `delivered`

### Node 最终状态
- `NODE-PLAN-001`: `done`
- `NODE-RESEARCH-001`: `done`
- `NODE-WRITE-001`: `done`
- `NODE-REVIEW-001`: `done`

### Review 结果
- review count: `2`
- research 节点已过一次结果门
- final brief 已过一次结果门

### Event 记录
- event count: `34`

---

## 已验证能力

### 1. dispatch payload 已生成

已为以下节点输出 dispatch artifact：

- `tasks/TASK-REAL-RESEARCH/artifacts/NODE-RESEARCH-001-dispatch.json`
- `tasks/TASK-REAL-RESEARCH/artifacts/NODE-WRITE-001-dispatch.json`
- `tasks/TASK-REAL-RESEARCH/artifacts/NODE-REVIEW-001-dispatch.json`

说明 OPC 已可把 mission / working / policy / output contract 稳定下发给执行者。

### 2. result recording 已落地

本次 workflow 形成的稳定产物包括：

- `docs/first-real-workflow.md`
- `tasks/TASK-REAL-RESEARCH/artifacts/research-brief.md`
- `tasks/TASK-REAL-RESEARCH/artifacts/final-brief.md`

说明 `record-result` 已可用于把节点成果沉淀成稳定 artifact。

### 3. review gate 已闭环

本次 workflow 明确经历了：

- research 节点进入 `review_pending` 并通过 review
- write 节点进入 `review_pending`
- reviewer 节点完成结果门放行

说明 review gate 已从文档概念进入可执行流程。

### 4. resume cursor 已闭环

最终 `task-summary`：

```json
{
  "completed_nodes": [
    "NODE-PLAN-001",
    "NODE-RESEARCH-001",
    "NODE-REVIEW-001",
    "NODE-WRITE-001"
  ],
  "next_nodes": [],
  "stable_artifacts": [
    "docs/first-real-workflow.md",
    "tasks/TASK-REAL-RESEARCH/artifacts/research-brief.md",
    "tasks/TASK-REAL-RESEARCH/artifacts/final-brief.md"
  ]
}
```

这意味着：

- 已完成节点可默认跳过
- 没有待执行节点时可直接判定闭环完成
- 稳定产物可供后续 resume / audit / reuse

---

## 任务产出摘要

本次 research workflow 的最终简报，沉淀了 OPC v1 的两类硬规则：

### Review gate
默认高优先触发场景：
- 改代码
- 对外发送
- 公开发布
- 修改长期文档 / 记忆
- 涉及敏感凭据或登录态

### Resume / recovery
默认硬约束：
- 从 task state 恢复，而不是从聊天记录猜
- completed nodes 默认跳过
- stable artifacts 默认可复用
- next executable nodes 必须可从依赖状态直接推导
- CEO session 可手动接管 blocked / failed 节点

---

## 它证明了什么

这条样例证明 OPC v1 已经具备以下最小闭环能力：

1. **真实 task 台账**：task / node / review / event 均已落地
2. **状态机治理**：节点按合法状态推进
3. **稳定派发**：dispatch payload 可生成并持久化
4. **结果沉淀**：worker / writer / reviewer 产出都能写回 artifact ledger
5. **质量门闭环**：review gate 已真实触发并记录
6. **恢复语义**：resume cursor 可回答“完成了什么、还能从哪续跑”
7. **最终交付**：task 已可从 planning 推进到 delivered

---

## 当前意义

`TASK-REAL-RESEARCH` 不是单节点 demo，也不是纸面流程图。

它已经是 OPC 第一条**真实跑完闭环**的 workflow 样例，标志着 OPC 已从“概念性文档系统”进入：

> **可操作的轻控制面 + 已验证的真实 workflow 阶段**

---

## 下一步建议

### P1
- 补一条同等粒度的 coding workflow
- 补一条同等粒度的 social workflow
- 把 TODO 中“三条真实工作流跑通”从 research 扩到全套

### P2
- 给 research / coding / social 都补带 `bind-session` 的 runtime 版本
- 用 `sessions_spawn` / `sessions_send` 跑真正独立会话的 planner / worker / reviewer
- 继续验证 OPC 与 OpenClaw runtime 的桥接强度

---

## 结论

`TASK-REAL-RESEARCH` 已完成并交付。

它证明 OPC 当前控制面已经足以支撑一条真实的、可审计的、可恢复的 research workflow；下一步重点不再是重写设计，而是继续把 coding / social 两条真实链路跑通。
