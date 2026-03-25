# Task Lifecycle

## 任务主链

OPC 推荐的标准链路：

```text
new
→ triaged
→ planned
→ plan_review
→ dispatched
→ running
→ awaiting_review
→ delivered
→ archived
```

同时允许异常分支：

- `plan_rejected`
- `rework`
- `blocked`
- `paused`
- `cancelled`
- `failed`
- `resumable`

## 状态定义

### new
新建任务，尚未分拣。

### triaged
已识别目标、约束、优先级。

### planned
planner 已提交执行计划。

### plan_review
reviewer 正在审核计划。

### plan_rejected
计划被打回，需要重新规划。

### dispatched
任务已拆为节点并完成派单。

### running
至少一个节点正在执行。

### blocked
任务因依赖、报错、外部条件缺失而阻塞。

### awaiting_review
执行结果已提交，等待 reviewer 审核。

### rework
reviewer 未通过，返回执行层修正。

### delivered
结果已由 CEO / synthesizer 对外交付。

### archived
任务收口并归档。

### paused
人为暂停，可恢复。

### resumable
系统确认存在恢复点，可继续执行剩余节点。

### failed
确认失败，暂不继续。

### cancelled
人为取消。

## 合法转换

推荐只允许以下关键跳转：

- `new -> triaged`
- `triaged -> planned`
- `planned -> plan_review`
- `plan_review -> dispatched`
- `plan_review -> plan_rejected`
- `plan_rejected -> planned`
- `dispatched -> running`
- `running -> blocked`
- `running -> awaiting_review`
- `awaiting_review -> rework`
- `awaiting_review -> delivered`
- `rework -> running`
- `running -> paused`
- `paused -> resumable`
- `resumable -> running`
- `running -> failed`
- `any_active -> cancelled`
- `delivered -> archived`

## 为什么要有显式状态机

因为 CEO 需要知道：

- 任务是还没规划，还是规划被打回
- 是真的失败了，还是只是等待恢复
- 是卡在执行层，还是卡在审核层

状态机的价值在于把“感觉”变成“经营台账”。

## 节点级生命周期

任务之下的 node 也应独立维护状态：

- `queued`
- `assigned`
- `running`
- `blocked`
- `done`
- `failed`
- `review_pending`
- `rework`
- `skipped`

## 恢复点设计

每个任务需要一个 `resume_cursor`，至少记录：

- 已完成节点列表
- 可复用工件
- 最后稳定状态
- 下一批待执行节点
- 失败节点原因

这样在 resume 时，可以：

- 跳过已完成节点
- 只重跑失败或未完成节点
- 保持计划与审计连续性

## 审核门

### Plan Gate

目标：防止错误计划进入执行层。

检查项：

- 是否满足目标
- 是否漏关键子任务
- 是否依赖关系合理
- 是否角色分配合理
- 是否存在明显高风险动作

### Result Gate

目标：防止低质量结果直接交付用户。

检查项：

- 是否满足验收标准
- 是否存在事实/逻辑/实现错误
- 是否缺失必要工件
- 是否需要返工或补充说明

## 结论

OPC 的任务生命周期不是“为了好看”，而是为了让主会话真正具备 CEO 的经营视角与干预能力。
