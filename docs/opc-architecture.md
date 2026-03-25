# OPC Architecture

## 定义

OPC（One Person Company）是一套面向 OpenClaw 的多 Agent 管理架构。

它把主会话定义为 **CEO**，把子 Agent 定义为 **部门与岗位资源**，把复杂任务定义为 **公司内部可经营、可审计、可恢复的任务流**。

## 核心隐喻

不是“一个主 Agent 带几个工具人”。

而是：

- 主会话 = 公司 CEO
- 子 Agent = 公司员工 / 部门岗位
- 任务 = 公司项目 / 工单
- 上下文 = 预算与资料
- 状态 = 经营看板
- 审核 = 质量与风控体系
- 记忆 = 公司知识库与历史台账

## 设计原则

### 1. CEO 视角
主会话关心的是：
- 目标是否清晰
- 人力如何配置
- 哪些节点要审核
- 哪些工作可以并行
- 当前风险和卡点在哪
- 是否该暂停、重试、换人、结束

### 2. 部门化执行
子 Agent 必须职责清晰、边界明确。

### 3. 两道质量门
- Plan Gate
- Result Gate

### 4. 状态机优先
没有状态机，就没有真正的管理。

### 5. 恢复优先
复杂任务必须能 resume，而不是每次从头再来。

## 最小闭环

```text
User
  ↓
CEO Session
  ↓
Router
  ↓
Planner
  ↓
Reviewer (Plan Gate)
  ↓
Dispatcher / CEO
  ↓
Workers
  ↓
Reviewer (Result Gate)
  ↓
Synthesizer / CEO
  ↓
Delivery
```

## CEO 的五类能力

### 1. 任务经营
- 建 task
- 定优先级
- 定验收标准

### 2. 资源经营
- 派发上下文
- 控制并发
- 选择模型
- 指定 agent

### 3. 风险经营
- 触发审核
- 发现阻塞
- 终止危险路径

### 4. 过程经营
- 跟踪状态
- 查询事件流
- 看节点完成度

### 5. 结果经营
- 汇总交付
- 做最终判断
- 决定是否归档沉淀

## 子 Agent 的资源化抽象

每个子 Agent 不只是一个“聊天对象”，而是一个资源单元：

- role
- skills
- model
- permissions
- context package
- current load
- health status
- output quality history

## 为什么这个方向值得做

因为真正有价值的多 Agent 系统，不是“会自己分工”，而是：

- **会被管理**
- **能被解释**
- **可以被接管**
- **出问题后能恢复**

这才是从 demo 走向 production 的门槛。
