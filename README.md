# OPC — OpenClaw Process Company

OPC（OpenClaw Process Company）是面向 OpenClaw 的多 agent 派发与治理体系。

它的目标不是把 agent 变成会互相闲聊的“组织戏法”，而是把复杂任务收口成一套 **可路由、可派发、可审核、可恢复、可交付** 的任务流。

一句话：

> **skill 是入口层，OPC 是经营层。**

- skill 负责识别任务类型、提供方法边界
- OPC 负责拆解、派发、审核、恢复、交付

---

## 当前版本结论

**当前主线已经升级到 OPC v0.2。**

v0.2 的核心变化：
- **去 ACP 化**：ACP 不再是核心 runtime 前提
- **回归 OpenClaw-native**：主执行资源统一为 `main session / subagent / coding-agent`
- **借鉴 Edict 的制度设计**：角色分层、双 review gate、状态机保护、权限矩阵、可观测台账
- **补齐 delivery layer**：task 不再只停留在 node 完成，而能聚合到 `delivered`

所以当前推荐理解是：

> **OPC v0.2 = 去 ACP、参考 Edict、但坚持 OpenClaw 原生编排的轻量控制面。**

---

## 1. OPC 解决什么问题

当任务变复杂时，主会话很容易同时承担：

- 需求理解
- 任务拆解
- 多角色执行
- 风险审核
- 结果汇总
- 中断恢复

如果这些都靠临场记忆和临时 prompt，结果通常是：

- 任务边界漂移
- 子代理职责不清
- 审核点缺失
- 失败后只能从头再来
- 用户不知道当前卡在哪

OPC 要解决的就是这件事：

- 让复杂任务进入可管理状态机
- 让子代理拿到稳定 dispatch payload
- 让 review gate 变成制度，而不是临时想起
- 让 resume / recovery 成为默认能力
- 让 OpenClaw 的 skill、subagent、本地 coding agent 落到统一控制模型里

---

## 2. 核心定位

### OPC 不是

- 不是新的重型运行时
- 不是替代 OpenClaw session / subagent
- 不是把所有任务都强行多 agent 化
- 不是先做 dashboard 再找场景
- 不是 ACP bridge

### OPC 是

- 一套 OpenClaw-native 的任务派发协议
- 一套多 agent 治理模型
- 一层位于 skill 之上的控制面
- 一套让复杂任务可暂停、可恢复、可审计、可交付的最小制度

---

## 3. 与 OpenClaw 的关系

### OpenClaw 提供的原语

- 主会话
- `sessions_spawn`
- `sessions_send`
- subagent
- workspace 文件系统
- memory
- coding-agent skill 驱动的本地编码执行

### OPC 提供的制度

- task / node / review / event 台账
- task / node 状态机
- triage / planner / reviewer / dispatcher / worker / summarizer 角色边界
- dispatch payload 结构
- review gate 触发规则
- resume / recovery / delivery 约束

所以：

> **OpenClaw 提供运行时，OPC 提供经营与派发协议。**

---

## 4. 最小闭环

```text
User
  ↓
CEO Session
  ↓
Router / Triage
  ↓
Planner
  ↓
Plan Review Gate
  ↓
Dispatcher
  ↓
Workers
  ↓
Result Review Gate
  ↓
Summarizer
  ↓
Delivery
```

角色含义：

- **CEO Session**：主会话，接需求、拍板、交付
- **Router / Triage**：判断任务类型、匹配 skill、决定是否拆解
- **Planner**：拆节点、写依赖、定验收标准
- **Plan Review Gate**：审核计划是否合理
- **Dispatcher**：选择主会话 / subagent / coding-agent 执行策略
- **Workers**：完成具体节点
- **Result Review Gate**：审核结果、决定返工或放行
- **Summarizer**：汇总结果给 CEO 最终交付

---

## 5. 任务分层

### Type A：单步任务
- 低风险
- 不需要拆解
- 主会话直接做

### Type B：技能驱动任务
- 已有明确 skill
- 流程相对稳定
- 可由主会话或单个执行者完成

### Type C：多节点任务
- 需要拆解
- 需要 review / rework / resume
- 进入 OPC task 流

### Type D：持续会话任务
- 需要 session-bound 持续推进
- 优先使用 OpenClaw 原生持续 session
- 如需编码执行，优先挂接 `coding-agent` 作为 worker runtime
- OPC 只负责上层经营状态，不吞掉长会话语义

---

## 6. skill 是入口层，OPC 是经营层

### skill 层回答的是
- 这是什么任务？
- 应该用什么方法做？
- 有哪些边界、禁区、默认流程？

### OPC 层回答的是
- 要不要拆解？
- 谁来做？
- 用主会话、subagent 还是 coding-agent？
- 哪些节点必须过 review gate？
- 中断后从哪继续？
- 最终如何交付？

因此：
- `web-access` 决定联网任务怎么做
- `coding-agent` 决定编码任务怎么委派
- `social-media-manager` 决定社媒任务怎么路由
- `hidream-aigc-skills` 决定 AIGC 生成任务怎么发起
- **OPC 决定它们如何被串成一个完整任务流**

---

## 7. 当前仓库结构

```text
projects/opc/
  README.md
  docs/
  templates/
  scripts/
  tasks/
```

关键内容：

- `docs/opc-v0.2-upgrade.md`：v0.2 升级方向
- `docs/opc-v0.2-control-plane.md`：v0.2 控制面
- `docs/opc-v0.2-delivery-layer.md`：delivery 聚合层
- `scripts/opc.py`：当前 CLI 控制面
- `templates/`：task / node / review / event 模板
- `tasks/`：运行时任务台账

---

## 8. 当前进展

当前已经跑通：
- 最小 demo 闭环
- control plane 闭环
- research v0.2 两节点样板
- task delivered 聚合

也就是说，OPC 当前已经不是概念文档，而是有真实 ledger 和控制面命令支撑的可运行原型。
