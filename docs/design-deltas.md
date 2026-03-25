# Design Deltas

## 目的

本文件说明：

- OPC 相对 edict 改了什么
- OPC 相对通用 multi-agent skill 多了什么
- 为什么要这样改

---

## 一、相对 edict 的差异

### 1. 从“制度隐喻”转向“公司模型”

**edict**：
- 用三省六部作为组织比喻
- 强调制度分权与审议流程

**OPC**：
- 改用 CEO / Office / Department / Worker 的通用公司模型

**原因**：
- 更适合协议化与工程实现
- 更容易映射到 OpenClaw session / subagent / role
- 更适合后续扩展到不同业务域

---

### 2. 从“角色展示”转向“控制面抽象”

**edict**：
- 强项是流程与看板可见性

**OPC**：
- 更强调 task / node / event / review / budget / health 这些控制对象

**原因**：
- 管理系统的本体不在 UI，而在 underlying control plane

---

### 3. 从“部门并行”转向“CEO 资源调度”

**edict**：
- 更强调部门协作与派发

**OPC**：
- 更强调 CEO 对上下文、模型、并发、人力的分配能力

**原因**：
- 多 Agent 管理的真正稀缺点是资源经营，而不是只是派单

---

### 4. 从“制度审核”转向“结构化审核记录”

**edict**：
- 有明确审核角色与封驳机制

**OPC**：
- 要求形成 review schema：decision / reasons / required_changes / target

**原因**：
- 便于自动化处理、追责、统计与回放

---

### 5. 从“流程可恢复”转向“恢复点优先设计”

**edict**：
- 提供暂停 / 恢复 / 取消能力

**OPC**：
- 把 resume_cursor 设计成任务一等字段
- 强调节点级跳过、重跑、工件复用

**原因**：
- 恢复不是异常功能，而是复杂任务的基本能力

---

## 二、相对通用 multi-agent skills 的差异

### 1. 从“模式集合”转向“统一经营框架”

很多 skill 提供的是：
- supervisor 模式
- pipeline 模式
- council 模式
- auto-routing 模式

**OPC 的不同点**：
- 把这些模式都收敛到一个统一控制面里
- 由 CEO 决定什么时候使用何种模式

**原因**：
- 模式本身不是产品，管理一致性才是产品

---

### 2. 从“协作”转向“经营”

很多 multi-agent skill 关注：
- 多角色怎么协作
- 怎么并行
- 怎么沟通

**OPC 的不同点**：
- 增加经营视角：预算、容量、质量门、恢复点、审计台账

**原因**：
- 真正落地时，失败成本、资源浪费、不可解释性比协作本身更痛

---

### 3. 从“上下文共享”转向“上下文配给”

很多 skill 倾向共享上下文池。

**OPC 的不同点**：
- 把上下文视作 CEO 分配给子部门的资源包
- 强调按角色裁剪上下文

**原因**：
- 降低 token 成本
- 提高角色聚焦
- 强化岗位边界

---

### 4. 从“临时 agent”转向“可管理人力”

很多 skill 把 agent 当临时执行器。

**OPC 的不同点**：
- agent 拥有 capacity / load / health / output history 等管理属性

**原因**：
- 只有把 agent 视作资源，才能谈调度、替补、考核与稳态运行

---

## 三、OPC 的核心新增价值

### 1. CEO 原语化

OPC 最大的新增，不是新 worker，而是把主会话能力提升到 CEO 原语：

- 管目标
- 管资源
- 管流程
- 管质量
- 管风险
- 管结果

---

### 2. 公司化组织原语

OPC 把以下内容都原语化：

- role
- office
- department
- task
- node
- review
- event
- budget
- health

这使它更像一个“agent 经营系统”。

---

### 3. 控制面优先于体验层

OPC 的优先级是：

1. schema
2. 状态机
3. 调度动作
4. 审核协议
5. 恢复机制
6. 可视化看板

这与很多先做演示层的方案不同。

---

### 4. OpenClaw-native 落地性

OPC 不是理论框架，而是明确可映射到：

- sessions_spawn
- sessions_send
- tasks/ 台账
- memory
- artifacts
- future dashboard

也就是说，它天然适合往 OpenClaw 环境里继续生长。

---

## 四、下一步演进建议

要让 OPC 从“架构文档”继续进化，优先级建议是：

1. **Schema 层**
   - task schema
   - node schema
   - review schema
   - event schema

2. **Protocol 层**
   - CEO → Planner 协议
   - Planner → Reviewer 协议
   - CEO / Dispatcher → Worker 协议
   - Reviewer → Rework 协议

3. **Runtime 层**
   - task 目录规范
   - session 角色绑定
   - resume 实现

4. **UI 层**
   - 任务看板
   - agent 状态板
   - review / block / retry 时间线

---

## 五、结论

如果说 edict 提供的是“制度灵感”，skillhub 提供的是“模式与能力碎片”，那么 OPC 做的是：

> **把这些灵感和能力碎片，统一重构成一个可经营、可审计、可恢复的 OpenClaw 公司化多 Agent 管理框架。**
