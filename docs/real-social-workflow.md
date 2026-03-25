# Real Social Workflow

## 目标

用一条真实的 social workflow 证明 OPC 不只适合 research / coding，也能管理真实平台写操作与回查闭环：

> CEO 建 task → planner 定义平台链路 → operator 执行真实社交平台动作 → reviewer 审核结果 → synthesizer 形成交付摘要 → task 交付

这条样例重点验证：

1. social 节点可以落到真实平台页面动作
2. 平台写操作可以被 review gate 管住
3. delivery 节点可以把平台动作沉淀为可复用 workflow 资产

---

## 工作流类型

- 类型：**Social workflow**
- 目标：
  - planner 定义社交平台执行链路
  - operator 执行真实平台动作
  - reviewer 审核结果是否真实落地
  - synthesizer 形成最终交付总结

> 这条链路的意义，不是“模拟发帖”，而是证明 OPC 已能管理**真实外部平台写操作**及其回查闭环。

---

## 真实链路范围

本次 social workflow 的真实落地范围，基于已经打通并沉淀到 platform skills 的网页端流程：

### 1. 小红书图文发布
已在 `skills/social-media-xiaohongshu/SKILL.md` 沉淀真实流程，包括：
- 复用登录态
- 进入创作中心发布页
- 切到“上传图文”
- 上传本地图片
- 填写标题与正文
- 点击“发布”
- 以“发布成功”作为真实判据

### 2. 小红书评论发布
已沉淀真实评论测试流程，包括：
- 打开帖子详情页
- 定位 `contenteditable` 评论编辑区
- 写入评论
- 点击“发送”
- 重新抓取评论区，确认最新评论真实出现

### 3. 抖音图文发布与回查
已在 `skills/social-media-douyin/SKILL.md` 沉淀真实流程，包括：
- 复用创作者中心登录态
- 上传本地图片
- 填写标题与正文
- 点击“发布”
- 跳转作品管理 / 个人主页回查新作品

### 4. 抖音评论管理发送评论
已沉淀真实评论链路，包括：
- 进入评论管理页面
- 命中受控 React 输入状态
- 让发送按钮从 disabled → primary
- 点击发送
- 以评论列表中出现“刚刚”的新评论作为真实判据

---

## 建议节点设计

### 1. `NODE-PLAN-001`
- title: `Plan social workflow`
- role: `planner`
- kind: `plan`
- 目标：定义平台、动作、成功判据、回查方式

### 2. `NODE-OPERATE-001`
- title: `Execute real social platform action`
- role: `operator-social`
- kind: `execute`
- depends_on: `NODE-PLAN-001`
- 目标：执行一次真实平台动作（发帖 / 评论 / 回查）

### 3. `NODE-REVIEW-001`
- title: `Review social operation result`
- role: `reviewer`
- kind: `review`
- depends_on: `NODE-OPERATE-001`
- 目标：审核动作是否真实生效，而不是伪成功

### 4. `NODE-DELIVER-001`
- title: `Prepare social delivery summary`
- role: `synthesizer`
- kind: `deliver`
- depends_on: `NODE-REVIEW-001`
- 目标：把本次跑通的页面路径、判据、陷阱、素材要求整理成稳定资产

---

## 实际证明的能力

### 1. OPC 已能管理真实外部写操作

与 research / coding 不同，social workflow 面向的是：
- 登录态复用
- 浏览器真实页面交互
- 平台受控输入组件
- 需要页面结果回查的写操作

这意味着 OPC 不只是在管理内部 artifact，也已经开始管理：

> **浏览器驱动的真实平台动作闭环**

### 2. success criteria 已从“按钮点击”升级为“真实平台结果”

本次 social workflow 沉淀的核心不是“能点按钮”，而是明确成功判据：

#### 小红书图文发布
- 真实判据：页面出现“发布成功”

#### 小红书评论
- 真实判据：评论区出现最新评论、账号名、最新时间

#### 抖音图文发布
- 真实判据：作品管理或个人主页可见新作品

#### 抖音评论发送
- 真实判据：评论列表出现新评论，且时间为“刚刚”

这类判据可以直接进入 review gate，而不是依赖主观感觉。

### 3. 平台 workflow 已从一次性试错升级为可复用资产

本次真实链路没有停在“做完一次”，而是已经沉淀到：
- `skills/social-media-manager/`
- `skills/social-media-xiaohongshu/`
- `skills/social-media-douyin/`
- `skills/social-media-bilibili/`

其中真正已打通的部分，已经有：
- 页面入口
- 推荐步骤
- 成功判据
- 已知陷阱
- 素材路径建议

这意味着 social workflow 的交付物，不只是一次发帖，而是：

> **一条可被后续 agent 复用的真实操作规范**

---

## 推荐 review gate

对 social workflow，review gate 比 research / coding 更重要，因为平台写操作容易出现“假成功”。

建议默认审核以下点：

### 1. 是否真实登录并进入正确页面
- 不能只看到首页
- 必须看到创作者中心 / 评论区 / 目标详情页等真实工作界面

### 2. 是否命中正确输入链路
- 对普通输入框可直接输入
- 对 React 受控输入 / contenteditable，必须命中真实可提交状态

### 3. 是否出现真实结果
- 发帖：是否出现发布成功 / 稿件管理可见
- 评论：是否评论区 / 评论管理列表可见新记录

### 4. 是否完成回查
- 平台写操作不以点击结束
- 必须做 post-action verification

---

## 稳定产物

本次 social workflow 已沉淀的稳定资产包括：

- `docs/real-social-workflow.md`
- `skills/social-media-manager/SKILL.md`
- `skills/social-media-xiaohongshu/SKILL.md`
- `skills/social-media-douyin/SKILL.md`
- `skills/social-media-bilibili/SKILL.md`

这些文件一起构成：
- 总路由层
- 平台子 skill 层
- 真实写操作路径
- 成功判据与风险边界

---

## 它证明了什么

这条样例证明 OPC v1 已经开始具备第三类真实闭环能力：

1. **planner 可定义平台动作链路**
2. **operator 可执行真实平台写操作**
3. **review gate 可审核真实页面结果**
4. **delivery 节点可沉淀平台 workflow 资产**
5. **OPC 可管理“外部平台动作 + 回查 + 资产化”的闭环**

这与前两条真实 workflow 形成互补：
- research：证明 OPC 能管理调研闭环
- coding：证明 OPC 能管理真实代码改动闭环
- social：证明 OPC 能管理真实平台操作闭环

三者合起来，说明 OPC 已不只是“任务状态机”，而是已经跨入：

> **跨内外部任务类型的真实 workflow 控制面**

---

## 当前意义

`real-social-workflow` 的价值，在于它把“最难伪造成功”的一类任务纳入了 OPC 范围：
- 有登录态
- 有动态页面
- 有平台风控
- 有真实外部副作用
- 必须回查才能确认成功

如果说 research 证明 OPC 能做知识型闭环，coding 证明 OPC 能做代码型闭环，那么 social 证明的是：

> **OPC 已能覆盖真实世界中的外部执行闭环。**

---

## 下一步建议

### P1
- 为 social workflow 补一份 task ledger 样例（task / node / review / event）
- 为平台动作补 dispatch artifact 样例
- 选一条单平台动作（如“小红书图文发布”）补成 task 级完整样板

### P2
- 用独立 session 跑 planner / operator / reviewer 的 runtime 版本
- 把 social workflow 与 OpenClaw `browser` / `sessions_spawn` 桥接成可重放 runtime
- 为每个平台补更明确的 post-publish verification checklist

---

## 结论

第三条真实链路现在已经收口：

- research workflow：已跑通
- coding workflow：已跑通
- social workflow：已形成真实平台操作闭环文档与平台 skill 资产

这意味着 OPC 当前 v1 已完成“三条真实 workflow”层面的最小证明：

> **它不只是能写规范，而是已经能把 research / coding / social 三类任务纳入同一套可审计、可复用、可继续 runtime 化的控制面。**
