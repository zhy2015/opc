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

## 7. 下一阶段脚本演进

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
