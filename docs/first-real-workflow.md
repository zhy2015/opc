# First Real Workflow

## 目标

定义 OPC 第一条真实可执行的 OpenClaw 工作流：

> CEO 创建任务 → spawn planner → 接收规划结果 → spawn reviewer → 接收审核结果 → 决定是否派发 worker

这是 OPC 从“桥接”走向“真实 orchestration”的第一步。

---

## 前提规则

本工作流遵守以下硬约束：

1. 子 Agent 在独立会话中运行
2. 子 Agent 不得再生成子 Agent
3. 默认全局并发上限为 8
4. 子 Agent 完成后自动向主会话通告结果

---

## Phase 1：CEO 建 task

CEO 在文件台账中完成：
- create-task
- create-node（plan 节点）
- render-dispatch-payload

产物：
- `task.json`
- `nodes/NODE-PLAN.json`
- `artifacts/NODE-PLAN-dispatch.json`

---

## Phase 2：CEO spawn planner

CEO 使用 `sessions_spawn` 创建独立 planner 会话。

要求：
- 独立 session
- 明确告知：不可再 spawn 子 Agent
- 明确只处理当前 plan node
- 返回结构化规划结果

同时：
- 用 `bind-session` 将 `session_key` 绑定回 node
- 记录事件流

---

## Phase 3：自动通告回主会话

当 planner 完成后：
- 运行时自动向主会话回传完成结果
- CEO 将结果写入 artifacts / events / node status

如果 planner 阻塞或失败：
- 同样自动通告主会话
- CEO 决定重试、改派或暂停

---

## Phase 4：CEO spawn reviewer

当 plan node 完成后：
- CEO 创建 review node 或直接创建 review request
- spawn reviewer 独立会话
- reviewer 审核 planner 输出

返回：
- approve / reject / conditional_approve
- reasons[]
- required_changes[]

---

## Phase 5：CEO 决策

### 若 approve
- task 进入 `dispatched` 或下一阶段
- CEO 可继续派发 worker node

### 若 reject
- task 进入 `plan_rejected`
- planner node 返工
- CEO 决定是否复用原 planner session

---

## 会话治理要求

### 1. 独立会话
planner / reviewer 必须是独立会话，不在主会话内串行执行。

### 2. 禁止套娃
对子 Agent 的 prompt / protocol 必须明确声明：
- 不允许生成新的 agent / session
- 如需更多资源，必须回报 CEO

### 3. 并发预算
在 spawn 前，CEO 应先检查当前活跃子会话数。

默认策略：
- `< 8`：可继续 spawn
- `>= 8`：进入排队或延后

### 4. 自动通告
要求子会话完成后：
- 结果能自动回流主会话
- 主会话收到后更新 task/node 台账

---

## 最小成功标准

这条工作流跑通，说明 OPC 已经具备：

- 真正的独立会话调度
- session 与 node 的绑定关系
- 主会话接收自动结果回流
- 单层多 Agent 治理秩序
- 向后扩展 worker 执行层的基础

---

## 下一步

当这条工作流稳定后，可扩展到：
- planner -> reviewer -> worker-code
- planner -> reviewer -> worker-doc
- 并行 worker + 汇总 reviewer
