# Session Governance

## 目标

把 OPC 对 OpenClaw session 的治理规则明确化。

---

## 一、单层会话树

OPC 默认只允许两层：

- 第 0 层：CEO 主会话
- 第 1 层：planner / reviewer / worker 子会话

禁止出现第 2 层及更深层。

### 原因
- 防止套娃
- 防止责任模糊
- 防止成本与上下文失控

---

## 二、活跃会话并发上限

默认全局活跃子会话上限：**8**

### CEO 责任
- 控制 spawn 节奏
- 必要时排队
- 为 reviewer 预留关键并发槽

### 建议策略
- 1 个 reviewer 槽位保留
- 1 个 planner 槽位保留
- 其余用于 worker

---

## 三、自动通告义务

所有子会话必须满足：
- 完成时通告主会话
- 失败时通告主会话
- 阻塞时通告主会话
- 需要更多资源时请求主会话，不得自行扩容

---

## 四、会话分类

### 持久会话
适合：planner / reviewer

### 临时会话
适合：worker / 一次性专项节点

---

## 五、session_key 绑定

每个 node 必须能追踪：
- `assigned_session`
- `runtime`
- `session_mode`
- `spawned_by`

这样 CEO 才能做到：
- reroute
- resume
- follow-up
- 统计活跃负载

---

## 六、CEO 独占 spawn 权

spawn 权只属于 CEO。

任何子会话如果觉得需要更多人力，只能：
- 回报需求
- 提供理由
- 等 CEO 决策

不能自建会话。

---

## 七、结论

Session governance 决定 OPC 能否在 OpenClaw 里保持长期稳定：

> **单层治理、受控并发、结果回流、CEO 独占调度权。**
