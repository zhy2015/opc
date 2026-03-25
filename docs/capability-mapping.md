# Capability Mapping

## 目的

本文件回答一个核心问题：

> OPC 到底吸纳了哪些外部多 Agent 方案的优势，又做了哪些重构？

这里把能力来源分为两类：

1. **edict**：偏制度化、可观测、可干预的多 Agent 组织模型
2. **skillhub 中的多 Agent 编排 skill**：偏模式、协议、运行时编排与资源管理

---

## 一、来自 edict 的吸纳

### 1. 主流程分层

**来源特征**：
- 分拣
- 规划
- 审议
- 派发
- 执行
- 回奏

**OPC 吸纳后的表达**：
- Router
- Planner
- Reviewer
- Dispatcher
- Workers
- Synthesizer / CEO Delivery

**保留原因**：
这是最清晰的一条“制度化任务流”，优于纯并发多聊。

**OPC 的改造**：
不保留古风角色叙事，改造成通用组织语义，方便产品化与协议化。

---

### 2. 独立审核门

**来源特征**：
- 门下省独立审核
- 可封驳
- 执行前强制过关

**OPC 吸纳后的表达**：
- Plan Gate
- Result Gate
- Reviewer 与执行者分离

**保留原因**：
这是多 Agent 系统从“会分工”升级到“有质量控制”的关键。

**OPC 的增强**：
将审核结构化为 `review record`，要求明确 decision / reasons / required_changes。

---

### 3. 可观测与可干预

**来源特征**：
- 实时看板
- 任务状态
- 叫停 / 恢复 / 取消
- 心跳与活跃监控

**OPC 吸纳后的表达**：
- task state machine
- event log
- pause / resume / cancel / reroute
- agent health / load / capacity

**保留原因**：
没有管理动作和可见性，多 Agent 只能算自动流水线。

**OPC 的增强**：
强调 control plane，而不是只把它当 dashboard 功能。

---

### 4. 权限边界与分权

**来源特征**：
- 谁能给谁发消息
- 谁能派发、谁能审议
- 非法流转拒绝

**OPC 吸纳后的表达**：
- CEO 的管理权
- Planner / Reviewer / Worker 权限边界
- 状态跳转合法性约束

**保留原因**：
多 Agent 的混乱往往来自越权，而不是能力不足。

**OPC 的增强**：
将“组织分权”抽象为 runtime policy 与最小权限原则。

---

### 5. 恢复与重入

**来源特征**：
- 叫停
- 恢复
- 从中间继续

**OPC 吸纳后的表达**：
- resumable
- resume_cursor
- 节点级跳过与重跑

**保留原因**：
复杂任务没有恢复点，就没有经营连续性。

**OPC 的增强**：
把恢复设计前置为一等能力，而不是运维补丁。

---

## 二、来自 skillhub 多 Agent 技能的吸纳

### A. agent-orchestration

**提供的启发**：
- 子 Agent 的创建与管理
- 任务委派
- 监控运行中的 agent

**OPC 吸纳点**：
- CEO 可以 spawn / steer / retire 子 Agent
- 把 agent 生命周期纳入正式管理动作

---

### B. openclaw-swarm

**提供的启发**：
- 上下文共享
- 状态管理
- 并行任务
- 完成通知

**OPC 吸纳点**：
- context package 分发
- 多节点并行执行
- event / completion 反馈机制

**OPC 的改造**：
把“共享上下文”改为“按角色裁剪上下文”，避免信息洪泛。

---

### C. agent-orchestrator-molter

**提供的启发**：
- Work Crew
- Supervisor
- Pipeline
- Council
- Auto-Routing

**OPC 吸纳点**：
- Supervisor → CEO / Reviewer
- Pipeline → task lifecycle / node DAG
- Auto-Routing → dispatcher / routing policy
- Council → 多 reviewer / 多部门会审的扩展模式

**OPC 的改造**：
将这些模式沉入统一 control plane，而不是并列成互不相干的技巧集合。

---

### D. multi-agent-protocol

**提供的启发**：
- spec-first
- phase control
- dual review gates
- bounded retry

**OPC 吸纳点**：
- task / node / review schema
- phase-based lifecycle
- 双审核门
- 重试受控

**OPC 的改造**：
更强调 CEO 视角下的经营台账，而不只是交付协议。

---

### E. firm-agent-orchestration-pack

**提供的启发**：
- DAG 并行执行
- 团队状态监控

**OPC 吸纳点**：
- 节点依赖图
- 并行 worker 执行
- 团队级活跃与容量视图

---

### F. code-agent-orchestration

**提供的启发**：
- coding session 生命周期管理
- 多轮交互
- 生命周期控制

**OPC 吸纳点**：
- session 级别的管理是控制面的一部分
- worker 不只是一次性调用，而是可持续互动单元

---

### G. multi-agent-memory

**提供的启发**：
- 共享记忆
- 项目隔离
- 交接文档
- 版本意识

**OPC 吸纳点**：
- 任务台账
- 项目记忆隔离
- 审计与交接文档
- artifacts + memory 双层沉淀

**OPC 的改造**：
不主张“所有 agent 共享所有记忆”，而是分 mission / working / policy / memory context。

---

### H. multi-agent-builder / multi-agent-team

**提供的启发**：
- 快速搭团队
- 角色模板化
- 多角色协作

**OPC 吸纳点**：
- 组织模板可配置
- 部门岗位可以按场景生成

**OPC 的改造**：
模板服务于公司模型，而不是反过来让公司模型受限于模板。

---

## 三、OPC 主动放弃的东西

### 1. 过度角色化叙事

原因：
- 展示效果好，但协议表达与实现映射会变复杂
- 对长期产品化不够中性

### 2. 一开始就上 10+ 固定部门

原因：
- 早期复杂度高
- 真实收益未验证
- 角色越多，治理成本越高

### 3. 把 dashboard 当作核心

原因：
- 看板重要，但不是系统本体
- 系统本体是：状态机、控制面、审计、恢复

### 4. 粗放式共享上下文

原因：
- 容易造成 token 浪费
- 降低岗位边界感
- 让 worker 背负不必要上下文

---

## 四、OPC 的新增增强

相对 edict 和现有 skill，OPC 新强调四点：

### 1. 主会话 = CEO

不是“总控 agent”这么简单，而是明确赋予：
- 资源权
- 路由权
- 审核触发权
- 人事调度权

### 2. Agent = 可经营资源

每个 agent 需要纳入：
- capacity
- load
- health
- permissions
- model selection
- output quality history

### 3. Context = 可分配资产

上下文不只是提示词，而是 CEO 发给部门的经营资源。

### 4. 公司化控制面

把多 Agent 从“协作范式”升级为“经营系统”：
- 台账
- 状态
- 审计
- 预算
- 风险
- 恢复

---

## 五、结论

OPC 不是简单拼接 edict 与若干 skill。

它的做法是：

- **吸收 edict 的制度骨架**
- **吸收 skillhub 多 Agent 技能的运行时能力与模式**
- **在 OpenClaw 语境下重构成 CEO 视角的公司化管理架构**

最终目标不是“更多 agent”，而是：

> **让一个主会话，真的像一家公司一样管理 agent、资源、流程与结果。**
