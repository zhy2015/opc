# OPC Skill Mapping

## 目标

明确 OPC 如何接当前 OpenClaw skill 体系，并统一口径：

> **skill 是入口层，OPC 是经营层。**

- skill 负责识别任务类型、限定方法边界
- OPC 负责拆解、派发、审核、恢复、交付

---

## 1. 总体判定顺序

复杂任务进入系统时，推荐按以下顺序判定：

1. 判断任务类型
2. 判断是否已有明确 skill 入口
3. 判断主会话直做是否更优
4. 如需拆解，再进入 OPC task / node 流
5. 决定每个 node 的执行策略：主会话 / subagent / ACP persistent session
6. 对高风险节点挂 review gate

换句话说：

- **先 skill routing**
- **再 OPC dispatch**
- **最后 review / delivery**

---

## 2. 执行策略分层

### 主会话直做
适用：
- 单步任务
- 低风险
- 无需长期上下文
- 不值得建 task 台账

### 单次 subagent
适用：
- 中等复杂度
- 需要隔离上下文
- 结果可以一次性回收
- 不需要长期 thread 记忆

### ACP persistent session
适用：
- 编码 / 长周期项目推进
- 用户会多轮追加指令
- 需要 thread-bound / session-bound 上下文
- 需要持续迭代而非一次性执行

---

## 3. 首批接入 skill

### 3.1 `coding-agent`

**入口职责**
- 识别复杂编码、重构、PR review、迭代开发任务
- 决定使用 Codex / Claude Code / Pi / OpenCode 等执行资源
- 约束代理执行方式（如 PTY、工作目录、后台模式）

**OPC 中的定位**
- 属于 `coding` 类任务入口
- 常见节点角色：
  - planner
  - worker-code
  - reviewer / review-code
  - synthesizer

**何时主会话直做**
- 极小改动
- 单文件单点修复
- 不需要长时间探索

**何时派 subagent / ACP**
- 多文件改动
- 需要探索代码库
- 需要持续推进
- 需要 thread-bound 持久开发

**默认执行策略**
- 一次性编码任务：subagent 或 coding agent session
- 持续开发任务：优先 ACP persistent session

**默认 review gate**
以下情况默认进入 result gate：
- 改代码
- 改测试
- 改核心文档
- 涉及部署、权限、凭据、危险脚本

**恢复语义**
- 已完成 node 不重跑
- 复用已有提交、测试结果、产物路径
- 返工只重开被 review 打回的 node

---

### 3.2 `social-media-manager`

**入口职责**
- 识别社媒运营类任务
- 将任务路由到平台专项能力，如小红书 / 抖音 / B站
- 统一外部写操作的风险边界

**OPC 中的定位**
- 属于 `social` 类总入口
- 常见节点角色：
  - planner
  - worker-research
  - worker-platform
  - reviewer
  - delivery

**何时主会话直做**
- 低风险读取
- 单平台轻量查询
- 不涉及对外发送

**何时派 subagent**
- 多平台比对
- 内容生成 + 平台执行链路
- 需要浏览器/登录态隔离

**何时用 ACP persistent session**
- 持续运营任务
- 多轮追加修改同一批内容
- 需要在一个长线程中反复迭代发布素材

**默认 review gate**
以下情况默认必须 review：
- 发帖
- 评论
- 私信
- 账号设置更改
- 任何对外可见写操作

**恢复语义**
- 已完成的平台读取节点直接跳过
- 内容草稿、平台截图、待发文案应作为可复用产物
- 发布前中断时，应从最后一个未完成平台节点继续

---

### 3.3 `web-access`

**入口职责**
- 处理所有联网操作
- 统一搜索、网页抓取、浏览器操作、登录后访问
- 决定用搜索 / fetch / 浏览器自动化哪条链路

**OPC 中的定位**
- 属于 `research` / `web-ops` 基础入口
- 常作为其它 workflow 的底层依赖 skill

**何时主会话直做**
- 单页读取
- 简单搜索
- 一次性轻量抓取

**何时派 subagent**
- 多来源调研
- 动态页面抓取
- 需要结构化汇总
- 任务本身需要长上下文整理

**何时用 ACP persistent session**
- 一般不优先
- 除非该 research 任务本身是长周期持续项目的一部分

**默认 review gate**
以下情况建议 review：
- 需要登录后操作
- 涉及表单提交
- 涉及账户写入行为
- 调研结果将直接作为公开对外材料

**恢复语义**
- 已抓取页面、已整理摘要、已保存链接清单均应复用
- 中断后优先从未完成来源继续，不重新抓所有站点

---

### 3.4 `hidream-aigc-skills`

**入口职责**
- 处理图片 / 视频 AIGC 生成任务
- 统一模型调用、任务提交、轮询、结果回收
- 对接本地生成脚本或远端生成平台

**OPC 中的定位**
- 属于 `aigc-generation` 类入口
- 常见节点角色：
  - planner
  - worker-prompt
  - worker-gen
  - reviewer
  - delivery

**何时主会话直做**
- 单次轻量生成
- 不需要复杂 prompt 迭代
- 不需要批量对比

**何时派 subagent**
- 多方案 prompt 探索
- 多图/多视频并行生成
- 需要从参考资料整理生成包

**何时用 ACP persistent session**
- 长周期创作项目
- 多轮风格迭代
- 需要稳定维护同一创作上下文

**默认 review gate**
以下情况建议 review：
- 对外交付前选片
- 高成本批量生成前的 prompt 定稿
- 涉及版权/品牌/人物一致性的生成任务

**恢复语义**
- 已完成的 prompt 包、参考图、任务 ID、生成结果路径必须复用
- 失败时只重跑失败批次，不全量重提

---

## 4. 三类真实 workflow 的推荐接法

### 4.1 Coding Workflow

链路建议：

```text
User
  → skill routing: coding-agent
  → OPC planner
  → worker-code (subagent / ACP)
  → result gate
  → CEO delivery
```

默认策略：
- 小改动：主会话直做
- 中型任务：subagent
- 持续开发：ACP persistent session
- 改代码默认 review

---

### 4.2 Social Workflow

链路建议：

```text
User
  → skill routing: social-media-manager
  → platform routing
  → worker-platform
  → review gate for external write
  → CEO delivery
```

默认策略：
- 读取可轻做
- 对外写必须 review
- 多平台任务进入 OPC task 流

---

### 4.3 Research Workflow

链路建议：

```text
User
  → skill routing: web-access
  → planner
  → worker-research
  → reviewer
  → writer / synthesizer
  → CEO delivery
```

默认策略：
- 单页查询不建 task
- 多来源调研建 task
- 公开材料前建议结果审核

---

## 5. Review Gate 统一规则

默认高优先触发场景：

- 改代码
- 对外发送
- 公开发布
- 修改长期文档 / 记忆
- 涉及敏感凭据或登录态
- 高成本批量生成

低风险场景可放宽：

- 只读查询
- 单步整理
- 临时草稿
- 纯内部中间产物

原则：

- 不是所有节点都审
- 但高风险节点默认不能裸奔

---

## 6. Resume / Recovery 统一规则

无论命中哪个 skill，进入 OPC 后都应遵守：

1. 已完成节点优先跳过
2. 稳定产物必须可复用
3. 返工仅重开相关节点
4. 主会话保留人工接管权
5. 恢复点必须能回答“从哪续跑”

恢复时至少应明确：

- 哪些 node 已 done
- 哪些 node blocked / failed / paused
- 哪个 dispatch payload 仍有效
- 哪些 artifacts 可直接复用
- 哪些 session 仍可继续使用

---

## 7. 推荐的统一对外表述

可在 README / spec / 说明文档中统一用以下话术：

> Skill 负责把任务归类并给出方法边界；OPC 负责把复杂任务经营成一条可派发、可审核、可恢复的执行链路。

或更短版：

> Skill 是入口层，OPC 是经营层。
