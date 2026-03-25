# OPC Control Plane Audit — `scripts/opc.py`

## 结论

`scripts/opc.py` 当前已经具备 **v1 轻控制面** 的主体能力，不应再被描述为“只做样例”。

它已经能支撑：

- task 建单
- task / node 状态机管理
- review 记录
- event 记录
- dispatch payload 渲染
- session 绑定
- task 汇总查看

因此更准确的定位应是：

> **OPC v1 文件台账控制面样机（light control plane）**

---

## 一、当前已实现能力

### 1. Task 层

已实现：
- `create-task`
- `update-task-status`
- `show-task`

覆盖点：
- task 基本元数据
- task 状态流转
- task 事件记录

评价：
- 已满足“create task / mark task running|paused|resumable|delivered”的基础要求
- 缺少更友好的 task 摘要视图，但底层能力已在

---

### 2. Node 层

已实现：
- `create-node`
- `update-node-status`
- `bind-session`

覆盖点：
- node 创建
- assigned role
- 依赖关系 `depends_on`
- node 状态流转
- output refs 追加
- runtime / session_mode / assigned_session 绑定

评价：
- 已满足“create node / mark node running|done|blocked|failed”的主体需求
- 还缺少 `skip node` 的显式操作入口，虽然 schema 中已有 `skipped` 终态

---

### 3. Review 层

已实现：
- `create-review`

覆盖点：
- reviewer role
- stage
- decision
- reasons
- required_changes
- notes
- review 事件记录

评价：
- 已具备 request review / 记录 review 结果的基础能力
- 但 review 决策与 node / task 状态联动仍偏手动

---

### 4. Dispatch 层

已实现：
- `render-dispatch-payload`

当前 payload 已包含：
- `task_id`
- `node_id`
- `role`
- `mission_context`
- `working_context`
- `policy_context`
- `output_contract`

评价：
- 已满足“稳定 dispatch payload 规范”的主体要求
- 这是当前控制面里最接近 runtime bridge 的关键能力

---

### 5. Runtime Bridge 层

已实现：
- `bind-session`

覆盖点：
- `assigned_session`
- `spawned_by`
- `runtime`
- `session_mode`

评价：
- 已完成文件台账与 OpenClaw session runtime 的最小桥接
- 还未直接内建 spawn / send，但文档路线是清晰的

---

### 6. Validation / Audit 层

已实现：
- task transition validation
- node transition validation
- event append

评价：
- 状态机校验已落地，不再只是文档建议
- event 流可满足最基础可审计性

---

## 二、对照 TODO 的盘点结果

### 1. task 状态流转
**状态：已实现**

通过 `VALID_TASK_TRANSITIONS` + `update-task-status` 落地。

---

### 2. node 状态流转
**状态：已实现**

通过 `VALID_NODE_TRANSITIONS` + `update-node-status` 落地。

---

### 3. review 记录
**状态：已实现**

通过 `create-review` 落地。

---

### 4. event 记录
**状态：已实现**

通过 `append_event()` + 各命令副作用落地。

---

### 5. dispatch payload 输出
**状态：已实现**

通过 `render-dispatch-payload` 落地。

---

### 6. resume cursor 语义
**状态：部分实现**

现状：
- 通过 task / node 状态、depends_on、output_refs、dispatch_payload_ref、assigned_session 已能表达“恢复到哪里”
- 但尚无单独的 `resume_cursor` / `recovery_hint` / `last_good_node` 等显式字段

结论：
- **恢复语义已具备基础表达能力，但尚未显式产品化**

---

## 三、已有 / 缺失 / 待改

## 已有

- 文件台账目录结构
- task / node / review / event 模板
- task / node 状态机
- review 记录
- dispatch payload 渲染
- session 绑定
- 事件审计流
- task 全貌查看

## 缺失

- `record-result` 命令
- `mark-review-pending` 显式命令
- `skip-node` 显式命令
- 更适合 CEO 的 task summary / board view
- review 与 task/node 状态自动联动
- resume cursor 显式字段
- 对 completed node 的自动跳过策略说明

## 待改

- 将 `show-task` 补充为更偏运营摘要的输出
- 把 review 决策与 node/task 流转规则进一步编码
- 增加恢复视角字段，如 `recovery_hint` / `next_action` / `resume_from_nodes`
- 评估是否要加 `list-tasks` / `task-summary` / `show-events`

---

## 四、建议的 v1 定位调整

建议在 README / 规范文档中统一把 `opc.py` 描述为：

> 一个可操作的 OPC v1 轻控制面 CLI，用于管理 task、node、review、dispatch payload、session binding 与事件台账。

不建议再使用以下说法：
- “只是样例”
- “只有最小演示价值”
- “还没有真正进入控制面阶段”

因为从能力面看，它已经进入了控制面阶段，只是还未产品化。

---

## 五、建议的下一步

### P0
- 在 README 中同步更新 `opc.py` 定位
- 补本盘点文档并纳入推荐阅读
- 明确 `opc-v1-spec.md` 是主规范、`opc.py` 是当前 v1 控制面

### P1
- 增加 `record-result`
- 增加 `mark-review-pending`
- 增加 `skip-node`
- 增加更友好的 `task-summary`

### P2
- 增加恢复视角字段
- 增加任务列表 / 事件查看命令
- 视真实 workflow 压力再决定是否需要 dashboard

---

## 六、当前判断

当前最优路线不是重写 `opc.py`。

而是：

1. 先承认它已经是 v1 轻控制面
2. 先把 README / spec / mapping / audit 文档口径统一
3. 再围绕真实 workflow 补少量缺口
4. 最后根据真实使用压力决定是否扩为更完整控制面
