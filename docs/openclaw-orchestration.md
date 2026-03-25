# OpenClaw Orchestration Integration

## 目标

把 OPC 的文件台账 MVP，推进到真正可调度 OpenClaw session 的阶段。

核心变化：

- task 不再只管理文件
- node 不再只是静态记录
- CEO 可以真实创建 planner / reviewer / worker 子会话
- session_key 成为运行时一等字段

---

## 1. 角色到运行时映射

### CEO
- 当前主会话

### Planner / Reviewer / Worker
- 使用 `sessions_spawn` 创建
- 必要时复用持久 session
- 通过 `sessions_send` 下发任务

---

## 2. 建议的 node 扩展字段

在 `node.json` 中增加：

```json
{
  "assigned_session": "sess_xxx",
  "spawned_by": "ceo-session",
  "runtime": "subagent",
  "session_mode": "session",
  "dispatch_payload_ref": "tasks/TASK-001/artifacts/NODE-001-dispatch.json"
}
```

---

## 3. CEO 的运行时动作

### spawn_role_session
- 为 planner / reviewer / worker 创建新 session

### dispatch_node_to_session
- 将 node 的 mission / working / policy context 下发到目标 session

### record_session_binding
- 将 `session_key` 回写到 node

### request_followup
- 对已有 session 二次追问 / 返工

---

## 4. 推荐调度策略

### planner / reviewer
- 默认持久 session
- 因为其角色记忆和风格一致性更重要

### worker
- 默认按任务隔离
- 避免上下文污染
- 需要连续执行时可切换持久模式

---

## 5. 上下文包建议

dispatch payload 建议拆为：

- `mission_context`
- `working_context`
- `policy_context`
- `output_contract`

由 CEO 精准裁剪后发给子会话。

---

## 6. MVP 集成方式

第一步不在脚本内直接强绑 OpenClaw SDK，而是：

- 先定义 dispatch artifact 结构
- 先让 CLI 能生成标准 dispatch payload
- 再由 CEO / 主会话根据 payload 调用 `sessions_spawn` / `sessions_send`

这样可以先把控制协议和运行时边界分清。

---

## 7. 已验证的 bridge 口径

当前 OPC 与 OpenClaw runtime 的推荐桥接顺序已经比较明确：

1. CEO 用 `create-task` / `create-node` 建立 task 与 node 台账
2. CEO 用 `render-dispatch-payload` 生成 node 的标准 dispatch artifact
3. CEO 用 `sessions_spawn` 创建目标 planner / reviewer / worker session
4. CEO 用 `bind-session` 把 `session_key` 回写到 node
5. CEO 用 `sessions_send` 把 dispatch payload 下发到目标 session
6. 执行 session 返回结果后，CEO 用 `record-result` / `mark-review-pending` / `create-review` / `update-node-status` 完成闭环

这条顺序的意义是：
- **文件台账先行**：先有 task / node / dispatch artifact
- **运行时后接**：再把真实 session 绑定上去
- **状态变化回写**：所有关键结果都回到 OPC ledger，而不是散落在聊天记录里

---

## 8. 三类 workflow 的 runtime bridge 口径

### Research
- planner / research / writer / reviewer 都适合独立 session
- input 以本地 docs / spec / artifact 为主
- result 以 markdown artifact 为主

### Coding
- planner / worker-code / reviewer 可独立 session
- worker-code 最适合隔离 session，避免上下文污染
- result 既包括文档，也包括真实代码文件与 review artifact

### Social
- planner / reviewer 适合独立 session
- operator-social 既可由 CEO 直接配合 `browser` 执行，也可绑定独立 session 负责平台动作
- result 必须包含 post-action verification，而不能只记录页面点击
- 对 social 来说，`bind-session` 的价值尤其大，因为它能把“哪个 session 执行了哪次外部写操作”写回台账

---

## 9. `TASK-REAL-SOCIAL` 的 bind-session 示例

以 social workflow 为例，最小桥接口径可以写成：

```bash
python3 scripts/opc.py render-dispatch-payload TASK-REAL-SOCIAL NODE-OPERATE-001
python3 scripts/opc.py bind-session TASK-REAL-SOCIAL NODE-OPERATE-001 sess_social_worker_001 --runtime subagent --session-mode session
```

然后由 CEO：
- `sessions_spawn` 创建 operator-social session
- `sessions_send` 下发 `tasks/TASK-REAL-SOCIAL/artifacts/NODE-OPERATE-001-dispatch.json`
- 等 operator-social 完成平台动作与回查
- 用 `record-result` 回写平台 workflow 资产
- 用 `mark-review-pending` 把结果送入 reviewer gate

对应 node 中应出现这些字段：

```json
{
  "assigned_session": "sess_social_worker_001",
  "spawned_by": "ceo-session",
  "runtime": "subagent",
  "session_mode": "session",
  "dispatch_payload_ref": "tasks/TASK-REAL-SOCIAL/artifacts/NODE-OPERATE-001-dispatch.json"
}
```

这使得 social workflow 不再只是“谁记得自己刚刚点过哪个页面”，而是进入：
- 哪个 node
- 绑定哪个 session
- 收到哪个 dispatch
- 产出哪些 result refs
- 是否通过 review gate

都可以被台账追溯。

---

## 10. 下一阶段脚本演进

`scripts/opc.py` 可继续新增：

- `render-dispatch-payload`
- `bind-session`
- `record-result`
- `mark-review-pending`

这些命令负责文件台账和运行时之间的桥接。

---

## 8. 结论

这一步的意义是：

> 让 OPC 从“文件化任务管理器”进入“真实可调度 OpenClaw 子会话的 CEO 控制面”。
