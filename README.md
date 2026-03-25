# OPC — OpenClaw Process Company

OPC（OpenClaw Process Company）是面向 OpenClaw 的多 agent 派发与治理体系。

它的目标不是把 agent 变成会互相闲聊的“组织戏法”，而是把复杂任务收口成一套 **可路由、可派发、可审核、可恢复、可交付** 的任务流。

一句话：

> **skill 是入口层，OPC 是经营层。**

- skill 负责识别任务类型、提供方法边界
- OPC 负责拆解、派发、审核、恢复、交付

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
- 让 OpenClaw 的 skill、subagent、ACP 落到统一控制模型里

---

## 2. 核心定位

### OPC 不是

- 不是新的重型运行时
- 不是替代 OpenClaw session / subagent / ACP
- 不是把所有任务都强行多 agent 化
- 不是先做 dashboard 再找场景

### OPC 是

- 一套 OpenClaw-native 的任务派发协议
- 一套多 agent 治理模型
- 一层位于 skill 之上的控制面
- 一套让复杂任务可暂停、可恢复、可审计的最小制度

---

## 3. 与 OpenClaw 的关系

### OpenClaw 提供的原语

- 主会话
- `sessions_spawn`
- `sessions_send`
- subagent
- ACP persistent session
- workspace 文件系统
- memory

### OPC 提供的制度

- task / node / review / event 台账
- task / node 状态机
- Router / Planner / Reviewer / Worker 角色边界
- dispatch payload 结构
- review gate 触发规则
- resume / recovery 约束

所以：

> **OpenClaw 提供运行时，OPC 提供经营与派发协议。**

---

## 4. 最小闭环

```text
User
  ↓
CEO Session
  ↓
Router
  ↓
Planner
  ↓
Plan Gate
  ↓
Dispatcher
  ↓
Workers
  ↓
Result Gate
  ↓
Synthesizer / CEO
  ↓
Delivery
```

角色含义：

- **CEO Session**：主会话，接需求、拍板、交付
- **Router**：判断任务类型、匹配 skill、决定是否拆解
- **Planner**：拆节点、写依赖、定验收标准
- **Plan Gate**：审核计划是否合理
- **Dispatcher**：选择主会话 / subagent / ACP 执行策略
- **Workers**：完成具体节点
- **Result Gate**：审核结果、决定返工或放行
- **Synthesizer**：汇总结果给 CEO 最终交付

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
- 需要 thread-bound / session-bound 持续推进
- 优先 ACP persistent session
- OPC 只负责上层经营状态，不吞掉长会话语义

---

## 6. skill 是入口层，OPC 是经营层

推荐统一口径：

### skill 层回答的是
- 这是什么任务？
- 应该用什么方法做？
- 有哪些边界、禁区、默认流程？

### OPC 层回答的是
- 要不要拆解？
- 谁来做？
- 用主会话、subagent 还是 ACP？
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

- `docs/opc-v1-spec.md`：**当前主规范基线**
- `docs/skill-mapping.md`：OPC 与现有 skill 的接轨方式
- `scripts/opc.py`：v1 轻控制面 CLI
- `templates/`：task / node / review / event 模板
- `tasks/`：运行时任务台账

---

## 8. 推荐阅读顺序

### 主路径（新读者）
1. `docs/opc-v1-spec.md`
2. `docs/skill-mapping.md`
3. `docs/openclaw-orchestration.md`
4. `docs/workflow-runtime-bridge-matrix.md`
5. `docs/mvp-usage.md`
6. `docs/agent-reporting-commands.md`
7. `scripts/opc.py`

### 参考路径（旧稿 / 背景说明）
- `docs/first-real-workflow.md`
- `docs/real-coding-workflow.md`
- `docs/real-social-workflow.md`
- `docs/task-real-research-bind-session-example.md`
- `docs/task-real-coding-bind-session-example.md`
- `docs/task-real-social-bind-session-example.md`
- `docs/runtime-bridge-checklist.md`
- `docs/opc-architecture.md`
- `docs/runtime-architecture.md`
- `docs/protocols.md`
- 其它早期设计文档

文档关系建议统一为：

- **主规范**：`opc-v1-spec.md`
- **执行映射**：`skill-mapping.md`、`openclaw-orchestration.md`
- **控制面说明**：`opc.py` + `mvp-usage.md`
- **背景参考**：旧 architecture / protocols / vision 系列文档

---

## 9. 三条真实 workflow 现状

| Workflow | 当前状态 | 关键产物 |
|---|---|---|
| Research | 已闭环 | `docs/first-real-workflow.md`, `tasks/TASK-REAL-RESEARCH/` |
| Coding | 已闭环 | `docs/real-coding-workflow.md`, `tasks/TASK-REAL-CODING/` |
| Social | 已闭环并补齐 task 样板 | `docs/real-social-workflow.md`, `tasks/TASK-REAL-SOCIAL/` |

这三条链路共同证明：

- OPC 已能覆盖 research / coding / social 三类不同任务形态
- 不只是有说明文档，也已有 task / node / review / event / dispatch artifact 样板
- 下一步重点不再是“证明能不能做”，而是继续补 runtime bridge

---

## 10. 当前 v1 控制面能力

`scripts/opc.py` 当前已经覆盖：

- create task
- update task status
- create node
- update node status
- create review
- render dispatch payload
- bind session
- task summary / brief / report / events
- task agent status / session health snapshot
- task / node 状态迁移校验
- event 写入

这意味着它已经不只是“样例脚本”，而是一个可操作的轻控制面样机。

仍待补强的方向：

- task 摘要视图更适合真实运营
- review 结果与 task / node 联动更自动化
- result recording 更结构化
- resume cursor / recoverability 表达更显式
- 对 OpenClaw session 操作增加桥接层说明或命令

---

## 11. 最小示例

```bash
python3 scripts/opc.py create-task \
  --title "Run a real coding workflow" \
  --goal "Route planning, execution, review, and delivery through OPC"

python3 scripts/opc.py create-node TASK-XXXX \
  --title "Implement feature" \
  --role worker-code \
  --kind execute

python3 scripts/opc.py render-dispatch-payload TASK-XXXX NODE-XXXX
python3 scripts/opc.py bind-session TASK-XXXX NODE-XXXX sess_xxx --runtime subagent --session-mode session
python3 scripts/opc.py show-task TASK-XXXX
```

---

## 11. v1 近期推进重点

### P0
- 明确 `opc-v1-spec.md` 为主规范
- 收口 README 级总览
- 补 `skill-mapping.md`
- 盘点并收口 `scripts/opc.py`

### P1
- 已跑通 coding workflow
- 已跑通 social workflow
- 已跑通 research workflow
- 明确 review gate 规则
- 明确 resume / recovery 规则

### P2
- 整理旧文档层级
- 评估 dashboard 是否真有必要
- 评估是否抽成独立 skill / 独立仓库

---

## 12. 当前结论

OPC 当前最优路线不是推倒重建。

应该做的是：

1. 以 `opc-v1-spec.md` 作为主规范收口
2. 统一口径为“skill 是入口层，OPC 是经营层”
3. 用 `opc.py` 先把轻控制面跑稳
4. 再接真实 coding / social / research 工作流
5. 最后再决定是否产品化、可视化、独立化
