# OpenClaw Workflow Engine → OPC 可复用映射表

## 目的

回答一个实际问题：

> `external/openclaw-workflow` 里哪些能力可以直接复用到 OPC，哪些只能作为结构参考，哪些应保持 OPC 自己的独立设计。

一句话结论：

**openclaw-workflow 适合作为 OPC 的 workflow runtime 参考底座，但不应直接替代 OPC 的 CEO 控制面、task ledger 与 review/delivery 语义。**

---

## 总体判断

| 模块 | 对 OPC 的价值 | 建议 |
|---|---|---|
| YAML / JSON workflow loader | 高 | 可直接借鉴定义层与 DAG 装载方式 |
| DAG engine | 高 | 可直接借鉴执行顺序、依赖求解、节点输入解析 |
| constitution runtime | 中高 | 可借鉴“治理式入口”思想，但需改造成 OPC 的 CEO 语义 |
| skill contracts / skill manager | 高 | 很适合做 OPC 的能力边界与执行契约层 |
| workflow context / WAL / registry | 高 | 非常适合复用为 OPC 的 resume / recover 底座 |
| progress / audit / policy | 中 | 可作为辅助治理层接入 OPC |
| workflow definition as primary product | 中低 | 不应反客为主压过 OPC 的 task / node ledger |

---

## 一、可直接复用的部分

### 1. Workflow Loader（定义装载层）
对应模块：
- `core/engine/yaml_workflow.py`
- `core/engine/json_workflow.py`

适合 OPC 直接借鉴的点：
- 声明式 workflow 文件加载
- 节点列表 + 依赖边解析
- `action` / `skill_name` / `tool_name` 这类轻量目标表达
- 由输入引用自动推导 DAG 边

对 OPC 的意义：
- 可作为 `task-plan-init` 之后的结构化 plan 输入层
- 让 planner 产出的不是纯文档，而是可执行节点定义
- 便于把 OPC 的 task 从“文档式拆解”提升为“可装载的工作流图”

建议接法：
- OPC 仍保留自己的 `task.json / node.json`
- loader 作为“plan import / workflow import”能力，而不是顶替台账本身

---

### 2. DAG Engine（依赖执行层）
对应模块：
- `core/engine/dag_engine.py`

适合 OPC 直接借鉴的点：
- topological sort
- 节点状态推进
- 通过 `node_id.output_key` 解析上游输入
- 已完成节点跳过 / resume-friendly 语义

对 OPC 的意义：
- OPC 现在已有 ledger，但执行推进更多是控制面口径
- DAG engine 可以补上“节点图真正怎么跑”的底层执行语义
- 特别适合 research / coding / content/social 这类多节点串并行任务

建议接法：
- DAG engine 作为 OPC `dispatch` 层内部引擎
- OPC 仍负责：是否派发、给谁派发、是否过 gate、如何交付
- 不要让 DAG engine 直接替代 CEO 决策层

---

### 3. Skill Contracts / Skill Manager（能力契约层）
对应模块：
- `core/infra/skill_contracts.py`
- `core/infra/skill_manager.py`

适合 OPC 直接复用的点：
- `ToolSchema`
- `CapabilityProfile`
- `ExecutionResult`
- 统一的 skill init / execute / shutdown 契约

对 OPC 的意义：
- 很适合作为 `skill 是入口层，agent 是执行资源` 这条原则的底层落点
- 可把 OPC 当前“任务分类 → worker 选择 → 风险限制”沉到一个更可验证的 contract 层
- 有利于做 capability-aware dispatch

建议接法：
- skill contract 进入 OPC v1.x 控制面核心
- node 在 dispatch 前先看 capability，而不是只看 role 命名
- 未来可把 `review_required` / `side_effect_level` / `requires_memory` 变成调度前约束条件

---

### 4. Context / WAL / Registry（恢复与追踪层）
对应模块：
- `core/engine/workflow_context.py`
- `core/engine/wal_engine.py`
- `core/engine/workflow_registry.py`

适合 OPC 高强度复用的点：
- workflow context 存节点结果
- WAL 双写日志
- registry 追踪 workflow / task 状态
- 成功节点 resume 跳过语义

对 OPC 的意义：
- 这是最适合反哺 OPC 的部分之一
- OPC 已有 task ledger / events / reviews / artifacts 概念，但运行时恢复可以更强
- WAL 可成为 `record-result` 与 `bind-session` 的下层恢复机制
- registry 可补充 CEO 对 runtime 健康状态的读取

建议接法：
- OPC 的 `task.json / nodes/*.json / events.jsonl` 保持主台账
- WAL / context / registry 作为运行时附属账本
- 主账回答“经营状态”，附属账回答“执行恢复状态”

---

## 二、适合借鉴思想，但不应直接照搬的部分

### 5. Constitution Runtime（治理式入口）
对应模块：
- `core/runtime/constitution.py`
- `core/runtime/router.py`
- `core/runtime/policies.py`

可借鉴的点：
- 所有执行都先走治理入口
- 先 route，再 enforce policy，再 dispatch
- fast / slow path 分流
- memory / side-effect / deprecated tool 这类约束前置

不应直接照搬的原因：
- 它当前是“runtime legal entrypoint”视角
- OPC 的核心不是单个 runtime 入口，而是 CEO 经营层
- OPC 还需要：plan gate、result gate、delivery、resume cursor、session accountability
- 这些语义比 constitution runtime 更上层

建议接法：
- 把 constitution runtime 当成 OPC Dispatcher 的内核之一
- 不要把它当成 OPC 全部
- OPC 应保留 CEO 可见的 task-level 决策与审计层

---

### 6. Progress / Audit / Policy 模块
对应模块：
- `core/runtime/progress*.py`
- `core/runtime/audit.py`
- `core/runtime/policies.py`

可借鉴的点：
- 进度检查点
- 审计日志
- 策略违例记录
- 长任务进度桥接

限制：
- 它们更偏运行时基础设施
- 对 OPC 来说重要，但不是产品主语义

建议接法：
- 用来增强 OPC 的运行时可观测性
- 不替代 OPC 自己的 review/event/delivery 文档资产

---

## 三、应保持 OPC 独立设计的部分

### 7. CEO 控制面
对应 OPC 现有设计：
- `opc-v1-spec.md`
- `openclaw-orchestration.md`
- `workflow-runtime-bridge-matrix.md`

必须由 OPC 独立保留的原因：
- CEO 视角是 OPC 的核心差异化
- 任务经营、资源经营、风险经营、结果经营，不等于 workflow execution
- openclaw-workflow 当前没有真正覆盖：
  - 谁该被 spawn
  - 哪个 session 绑定到哪个 node
  - 哪个 node 要 review gate
  - 是否返工 / 暂停 / 重试 / 归档

结论：
- workflow engine 可以成为 OPC 的“发动机”
- 但方向盘、刹车、后视镜仍必须在 OPC 手里

---

### 8. Review Gate / Delivery / Resume Cursor
对应 OPC 现有强项：
- review gate
- delivery summary
- artifacts
- resume cursor
- bind-session accountability

为什么不能让 workflow engine 直接取代：
- 引擎擅长“执行节点”
- OPC 擅长“管理结果”
- 特别是 social / coding 这类有副作用或质量门的任务，必须保留 result gate
- session accountability 也是 OPC 当前强语义，不应丢到纯 DAG runtime 里稀释掉

结论：
- 这些应该继续由 OPC 作为上层协议维护
- 底层 engine 只负责把节点跑起来并提供状态材料

---

### 9. Skill Routing 与业务入口选择
为什么也应由 OPC 保持主导：
- OPC 已明确：先 skill routing，再 OPC dispatch
- openclaw-workflow 更像执行底座，不是完整入口治理系统
- 业务任务首先要命中 `coding-agent` / `web-access` / `social-media-manager` 等入口，再决定是不是进入多节点流

结论：
- workflow engine 不该抢 skill router 的职责
- 它应该服务于已被路由后的复杂任务

---

## 四、建议的集成方式

## 方案 A：轻集成（推荐先做）

思路：
- OPC 保持主控制面不变
- 把 openclaw-workflow 当作底层 runtime prototype 参考

具体做法：
1. 保留 OPC 的 `task / node / review / event / artifact` 结构
2. 让 planner 产出可导入的 workflow 定义
3. 用 DAG engine 负责节点依赖执行
4. 用 WAL / registry 负责恢复
5. 用 OPC 的 review gate / bind-session / delivery 做上层闭环

优点：
- 风险低
- 不破坏现有 OPC 主叙事
- 可以逐模块迁移

---

## 方案 B：中集成（适合 v1.5）

思路：
- 把 openclaw-workflow 的 runtime 层嵌入 OPC scripts / runtime bridge

具体做法：
- `render-dispatch-payload` 之外，再支持生成 workflow definition
- `bind-session` 后，节点推进可由 runtime engine 自动推进一部分
- session 回写结果后，自动同步更新 node status / review pending

优点：
- 自动化更强
- 更接近真实多 agent orchestrator

代价：
- 需要认真处理“谁是源数据”问题
- 必须防止 OPC ledger 与 workflow registry 双主写冲突

---

## 方案 C：重集成（暂不建议）

思路：
- 直接让 openclaw-workflow 成为 OPC 的底层主仓 / 主引擎

不建议原因：
- 现在还在 rebuilding 阶段
- 产品边界仍偏 workflow engine，而不是 CEO control plane
- 会把 OPC 的差异化语义压扁成普通 DAG runtime

---

## 五、建议的实际落地顺序

### Step 1
把这几个抽象从 openclaw-workflow 吸收进 OPC：
- capability profile
- tool schema
- execution result
- WAL / resume 语义

### Step 2
让 OPC 的 research / coding runtime-bound 样板对齐 DAG 思维：
- 明确 node inputs / outputs
- 明确依赖边
- 明确可跳过节点

### Step 3
给 OPC 增加一个轻量 workflow import / export 层：
- task ledger ←→ workflow definition
- 保证 planner 产物既可读，也可执行

### Step 4
再决定是否把 OPC 抽成正式 skill 或独立仓库

---

## 六、一句话结论

**openclaw-workflow 最值得复用的是：执行引擎、契约层、恢复层；OPC 最必须保留的是：CEO 控制面、review gate、delivery、session accountability。**

所以最优路线不是“谁替代谁”，而是：

> **让 workflow engine 做 OPC 的发动机，让 OPC 继续做驾驶舱。**
