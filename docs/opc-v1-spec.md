# OPC v1 - OpenClaw 多 Agent 派发规范

## 文档定位

本文档 `opc-v1-spec.md` 是当前 OPC 的**主规范基线**。

推荐统一分层如下：

- **主规范**：`opc-v1-spec.md`
- **README 总览**：`../README.md`
- **技能接轨说明**：`skill-mapping.md`
- **运行时桥接说明**：`openclaw-orchestration.md`
- **控制面盘点**：`opc-control-plane-audit.md`
- **背景参考旧稿**：`opc-architecture.md`、`runtime-architecture.md`、`protocols.md` 及其它早期文档

也就是说：

- `opc-v1-spec.md` 负责回答“OPC 到底是什么，核心原则是什么，v1 约束是什么”
- README 负责回答“新读者应该先怎么理解这个项目”
- mapping / orchestration / audit 文档负责回答“如何接现有 skill、如何接 OpenClaw runtime、当前控制面做到哪了”
- 旧 architecture / protocols 文档保留为背景参考，不再与主规范并列争抢基线地位

一句话：

> **README 是入口，总规范是 `opc-v1-spec.md`，其余文档按执行映射、运行时桥接、控制面盘点、背景参考分层。**

## 定位

OPC（OpenClaw Process Company）是我们自己的多 agent 派发与治理体系。

它不是重型组织戏仿，也不是为了“让 agent 自己聊天”。
它的目标很明确：

- 让复杂任务可以被拆解
- 让子代理有明确边界地执行
- 让结果经过审核后再回主会话
- 让任务可以暂停、恢复、追踪、复盘
- 让 skill 系统和多 agent 派发成为一套统一机制

一句话：

> OPC = 用最小制度，把 OpenClaw 里的复杂任务变成可管理、可恢复、可审计的任务流。

---

## 为什么叫 OPC

我们内部统一名称就叫 **OPC**。

这里的 OPC，不再强调古代官制或重型组织隐喻，而强调三件事：

- **O = OpenClaw-native**：原生贴合 OpenClaw 的 session / skill / subagent / ACP 能力
- **P = Process-controlled**：任务以流程和状态机管理，不靠临场记忆
- **C = Company-like execution**：主会话像经营者，子代理像岗位资源，但保持轻量

因此，OPC 是：
- 一个任务派发协议
- 一个多 agent 治理模型
- 一个 skill 编排与执行的统一约定

---

## OPC 的核心原则

### 1. 主会话是 CEO，不是流水线工人

主会话负责：
- 判断目标
- 判断是否需要拆解
- 判断是否派发
- 判断何处审核
- 判断何时终止或恢复
- 做最后交付

主会话不应该在复杂任务里一边做执行、一边做调度、一边做审核，把自己拖进泥里。

### 2. skill 是能力入口，agent 是执行资源

OPC 里必须明确区分：

- **skill**：告诉系统“这类任务该怎么做”
- **agent**：负责“谁来做这件事”

也就是说：
- skill 决定方法与边界
- agent 决定执行与产出

### 3. 先路由，再派发

不是看到复杂任务就先开一堆子代理。

正确顺序：
1. 判断任务类型
2. 判断是否已有合适 skill
3. 判断是主会话直做，还是子代理执行更优
4. 再决定派发策略

### 4. 两道质量门必须存在

OPC 默认有两道质量门：

- **Plan Gate**：方案是否合理，拆解是否清楚，边界是否正确
- **Result Gate**：结果是否达标，是否需要返工，是否能交付

不是所有任务都要重审，但复杂任务默认应至少有一个结果门。

### 5. 状态机优先于口头描述

复杂任务必须有状态。
没有状态机，就没有真正的恢复能力。

### 6. Resume 比“重新来一次”更重要

多 agent 真正有用，不在第一次跑得多漂亮，而在：

- 中断后能不能继续
- 失败后能不能局部返工
- 已完成节点能不能跳过
- 主会话能不能接管

---

## OPC 最小闭环

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

解释：

- **Router**：判断任务类型、匹配 skill、决定是否拆解
- **Planner**：把目标拆成可执行节点
- **Plan Gate**：审核任务拆解与风险边界
- **Dispatcher**：根据节点类型选择主会话 / subagent / ACP
- **Workers**：执行节点
- **Result Gate**：审结果、决定返工或放行
- **Synthesizer**：汇总子结果并给主会话交付材料

---

## OPC 与 skill 系统的关系

### 一层：Skill Routing

先由 skill 决定任务属于哪一类。

例如：
- 社媒任务 → `social-media-manager`
- 联网任务 → `web-access`
- 复杂编码任务 → `coding-agent`
- 需要生成图像/视频 → `hidream-aigc-skills`

### 二层：Execution Strategy

由 OPC 决定执行方式：

- 主会话直做
- subagent 并行做
- ACP harness 持久会话做

### 三层：Review & Delivery

由 OPC 决定：
- 是否审核
- 是否返工
- 如何汇总
- 如何回主会话

因此，**skill 是入口层，OPC 是经营层。**

---

## OPC 的任务分类

### Type A：单步任务

特点：
- 不需要拆解
- 不需要并行
- 风险低
- 结果判定简单

策略：
- 主会话直接执行
- 不进入完整 OPC 流程

示例：
- 读一个文件
- 改一个小段文案
- 回答一个事实性问题

### Type B：技能驱动任务

特点：
- 已有明确 skill
- 流程相对稳定
- 可由单代理串行完成

策略：
- 命中 skill
- 视复杂度决定主会话或单子代理执行

示例：
- 小红书发帖
- 抖音下载
- B站私信

### Type C：多节点任务

特点：
- 需要拆解
- 多个节点有前后关系
- 需要审核或返工

策略：
- 进入 OPC task 流
- 建 task / node / review / event

示例：
- 从调研到出文档
- 从需求到实现到 review
- 从脚本到素材到发布

### Type D：持续会话任务

特点：
- 需要 thread-bound / session-bound 持续推进
- 需要长期上下文
- 用户会多轮追加指令

策略：
- 优先 ACP persistent session
- OPC 负责上层任务状态，不吞掉长会话语义

示例：
- Codex 持续开发
- 长周期项目推进
- 多轮迭代内容生产

---

## OPC 的角色模型（轻量版）

我们不做过重的固定官制，只保留最有价值的 5 类角色：

### 1. CEO
主会话。
职责：
- 接需求
- 定目标
- 最终拍板
- 对用户交付

### 2. Router
可由 CEO 兼任。
职责：
- 判断任务类型
- 匹配 skill
- 判断是否需要拆解

### 3. Planner
可由主会话或独立子代理承担。
职责：
- 输出节点拆解
- 标明依赖关系
- 给出验收标准

### 4. Reviewer
职责：
- 审计划
- 审结果
- 给出返工意见

### 5. Worker
职责：
- 执行被分配节点
- 严格按节点边界产出

说明：
- 同一个会话可兼任多个角色
- 但复杂任务里，**执行者和审核者尽量不要是同一个子代理**

---

## OPC 的状态模型

### Task 状态

推荐最小集合：

- `new`
- `triaged`
- `planned`
- `plan_review`
- `plan_rejected`
- `dispatched`
- `running`
- `blocked`
- `awaiting_review`
- `rework`
- `paused`
- `resumable`
- `failed`
- `delivered`
- `archived`
- `cancelled`

### Node 状态

推荐最小集合：

- `queued`
- `assigned`
- `running`
- `blocked`
- `review_pending`
- `rework`
- `done`
- `failed`
- `skipped`
- `cancelled`

### Review 状态

- `approve`
- `conditional_approve`
- `reject`

---

## OPC 的派发规则

### 规则 1：优先少派发

能主会话直接完成的，不为了“显得高级”而派发。

### 规则 2：复杂任务优先派发

符合以下任一条件，优先考虑子代理：
- 需要大量文件探索
- 需要长时间运行
- 需要并行
- 需要隔离上下文
- 需要独立审核

### 规则 3：按 runtime 选择派发方式

#### subagent
适合：
- 一次性执行
- 中等复杂度
- 需要隔离但不需要长期线程

#### acp / persistent session
适合：
- 用户明确要求“在 codex/claude code/gemini 里做”
- 需要线程绑定长期推进
- 需要多轮连续开发

#### 主会话直做
适合：
- 简单任务
- 轻量 skill 任务
- 即时回复优先

### 规则 4：每个 node 必须有 output contract

至少说明：
- 预期产物是什么
- 成功判据是什么
- 产物放哪
- 是否需要审核

---

## OPC 的审核策略

### Plan Gate

在以下情况建议启用：
- 任务昂贵
- 任务跨多个 skill
- 任务会产生对外写操作
- 任务依赖复杂顺序
- 任务存在明显安全或合规风险

### Result Gate

在以下情况建议启用：
- 会改代码
- 会发外部消息
- 会改文档或记忆
- 会做公开发布
- 用户明确要求质量把关

### 条件通过机制

Reviewer 可给三种结论：
- `approve`
- `conditional_approve`
- `reject`

`conditional_approve` 适合：
- 方向对
- 但还缺少关键补丁或改动
- 不值得全盘重来

---

## OPC 的 resume / recovery 规则

### 基本要求

任务必须能回答：
- 哪些 node 已完成
- 哪些 node 失败了
- 哪些产物可复用
- 下一步从哪继续

### resume_cursor 至少记录

- `completed_nodes`
- `next_nodes`
- `stable_artifacts`

### 恢复原则

- 已完成节点默认不重跑
- 稳定产物优先复用
- 失败节点允许局部返工
- 主会话必须可手动接管

---

## OPC 与当前 skills 的接法

### 已适配较好的入口

- `coding-agent`
  - 适合作为复杂编码型 worker 能力入口
- `social-media-manager`
  - 适合作为社媒运营型 Router / skill 总入口
- `web-access`
  - 适合作为联网取数、网页登录、浏览器交互型 worker 入口
- `hidream-aigc-skills`
  - 适合作为图像/视频生成 worker 入口

### 当前最适合 OPC 收口的方向

1. **复杂编码任务**
   - 规划 → 子代理实现 → review → 交付
2. **社媒运营任务**
   - 总入口路由 → 平台子 skill → 审核 → 发布/汇报
3. **研究+交付任务**
   - web-access 调研 → planner 拆解 → writer / analyst 输出 → review
4. **内容生产流水线**
   - 脚本 → 生成 → 审核 → 发布

---

## OPC 当前版本建议

### 先做 v1，不追求全自动

v1 的目标不是让所有任务自动自治。
而是先把以下能力打稳：

- 统一任务状态机
- 统一 node / review / event 记录
- 统一 dispatch payload
- 统一 resume 语义
- 统一和 skill 的连接方式

### v1 不急着做的东西

- 复杂实时 dashboard
- 过重角色扮演体系
- 自动到处找 agent 自治聊天
- 过度抽象的部门模型

---

## 最终结论

我们的多 agent 体系，统一叫 **OPC**。

它不是照搬外部框架，也不是重新造一个夸张系统。
而是基于 OpenClaw 当前能力、基于已有 skills、基于 subagent / ACP / session 能力，做一个：

- 足够轻
- 足够稳
- 能恢复
- 能审核
- 能落地

的多 agent 派发规范。

下一阶段应该做的不是继续空谈架构，而是：

1. 把 OPC 文档设为主规范
2. 把 `projects/opc/scripts/opc.py` 继续收口成可执行控制面
3. 先接 2~3 条真实工作流（coding / social / research）跑通
4. 再决定哪些能力进入 dashboard / 可视化层
