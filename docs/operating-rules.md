# Operating Rules

## 目标

定义 OPC 在 OpenClaw 运行时中的硬约束。

这些不是建议，而是默认运行规则。

---

## 1. 独立会话

### 规则
子 Agent 必须在**独立会话**中运行。

### 含义
- 主会话是 CEO 控制面
- Planner / Reviewer / Worker 等子角色不直接占用主会话执行槽位
- 子任务执行不应阻塞主会话的管理动作

### 目的
- 保持 CEO 会话轻量
- 避免长任务污染主上下文
- 让主会话始终保留调度与接管能力

---

## 2. 禁止套娃

### 规则
子 Agent **不能再生成子 Agent**。

### 含义
- 只有 CEO / 主会话拥有 spawn 权
- Planner 不能再拉 worker
- Worker 不能再拉 sub-worker
- Reviewer 不能再拉外部审查链

### 目的
- 防止无限递归与结构失控
- 保持组织树清晰：只有一层管理，一层执行
- 所有新增人力都必须经过 CEO 批准

---

## 3. 并发上限

### 规则
默认最多同时运行 **8 个**子 Agent。

### 含义
- 并发是 CEO 管理的资源预算之一
- 超过上限的新任务必须排队，不直接启动
- 不同任务应共享同一全局并发预算

### 目的
- 控制 token / cost /注意力开销
- 防止任务风暴
- 确保 reviewer 与关键 worker 获得稳定资源

---

## 4. 自动通告

### 规则
子 Agent 完成后，必须**自动向主会话回传结果**。

### 含义
- 结果不能只停留在子会话内部
- 完成、失败、阻塞、返工都必须回传主控制面
- 回传结果应能被写入 event log 与 task/node 台账

### 目的
- 保持主会话全局可见性
- 让 CEO 可以继续派发、审核、收口
- 避免完成结果沉没在边缘会话中

---

## 5. CEO 独占能力

基于以上规则，以下能力默认仅 CEO 拥有：

- spawn session
- bind session
- reroute node
- approve / reject final delivery
- change task priority
- override concurrency budget

---

## 6. 默认实现建议

### 对应 OpenClaw
- 使用独立 `sessions_spawn`
- 使用主会话统一 `sessions_send`
- 不向子 Agent 暴露二次调度权
- 利用 runtime completion event 做自动通告

---

## 7. 结论

这四条规则定义了 OPC 的基本秩序：

> **独立运行、单层组织、受控并发、结果自动回流。**
