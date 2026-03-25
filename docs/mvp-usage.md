# MVP Usage

## 目标

演示 OPC v1 轻控制面的最小可跑实现：
- 创建 task
- 创建 node
- 更新 task / node 状态
- 写入 review
- 渲染 dispatch payload
- 记录结果
- 查看 CEO 视角 summary

---

## 1. 创建任务

```bash
python3 scripts/opc.py create-task \
  --title "Design OPC runtime MVP" \
  --goal "Build a minimal runnable control loop for OPC" \
  --priority high \
  --acceptance "task created" "nodes can be tracked" "reviews can be recorded"
```

输出示例：

```bash
TASK-AB12CD34
```

---

## 2. 创建节点

```bash
python3 scripts/opc.py create-node TASK-AB12CD34 \
  --title "Write runtime skeleton doc" \
  --role worker-doc \
  --kind document \
  --acceptance "doc created" "structure is clear"
```

---

## 3. 更新节点状态

```bash
python3 scripts/opc.py update-node-status TASK-AB12CD34 NODE-XXXX assigned
python3 scripts/opc.py update-node-status TASK-AB12CD34 NODE-XXXX running
python3 scripts/opc.py update-node-status TASK-AB12CD34 NODE-XXXX done --output-ref tasks/TASK-AB12CD34/artifacts/runtime.md
```

---

## 4. 创建审核记录

```bash
python3 scripts/opc.py create-review TASK-AB12CD34 NODE-XXXX \
  --stage result_gate \
  --decision approve \
  --reasons "meets acceptance criteria"
```

---

## 5. 渲染派发载荷

```bash
python3 scripts/opc.py render-dispatch-payload TASK-AB12CD34 NODE-XXXX
```

这会生成：

```text
tasks/TASK-AB12CD34/artifacts/NODE-XXXX-dispatch.json
```

---

## 6. 记录执行结果

```bash
python3 scripts/opc.py record-result TASK-AB12CD34 NODE-XXXX \
  --summary "worker completed runtime draft" \
  --output-ref docs/runtime-draft.md
```

---

## 7. 显式进入审核中

```bash
python3 scripts/opc.py mark-review-pending TASK-AB12CD34 NODE-XXXX \
  --stage result_gate \
  --note "ready for reviewer"
```

---

## 8. 显式跳过节点

```bash
python3 scripts/opc.py skip-node TASK-AB12CD34 NODE-OPTIONAL \
  --reason "covered by stable prior artifact"
```

---

## 9. 查看 CEO 摘要视图

```bash
python3 scripts/opc.py task-summary TASK-AB12CD34
```

摘要会包含：
- task 当前状态
- 当前阶段与完成度
- 各 node 状态计数
- `resume_cursor`
- review 数量
- event 数量
- 最近关键事件
- 每个 node 的最小运营视图

---

## 10. 查看简版汇报

```bash
python3 scripts/opc.py task-brief TASK-AB12CD34
```

适合聊天内快速问：
- 现在任务到哪了
- 哪些 node 在活跃
- 最近发生了什么

---

## 11. 查看详细汇报

```bash
python3 scripts/opc.py task-report TASK-AB12CD34
```

详细汇报会包含：
- 总览
- 节点进展
- 当前活跃 agent / session
- 最近关键事件
- `resume_cursor`
- CEO 建议

---

## 12. 查看事件尾部

```bash
python3 scripts/opc.py task-events TASK-AB12CD34 --tail 10 --key-only
```

适合排查：
- 最近 10 条关键事件
- 是否进入 review gate
- 是否 result 已回写

---

## 13. 查看 agent / session 健康

```bash
python3 scripts/opc.py task-agent-status TASK-AB12CD34 --sessions-file tmp-sessions.json
python3 scripts/opc.py task-report TASK-AB12CD34 --with-agents --sessions-file tmp-sessions.json
```

适合回答：
- 哪个 agent 真在推进
- 哪个 session stale / idle / done
- 哪个 node 需要 intervention

---

## 14. runtime bridge 最小口径

当 node 不再只停留在文件台账，而要进入真实 OpenClaw session 时，推荐最小桥接方式如下：

```bash
python3 scripts/opc.py render-dispatch-payload TASK-AB12CD34 NODE-XXXX
python3 scripts/opc.py bind-session TASK-AB12CD34 NODE-XXXX sess_xxx --runtime subagent --session-mode session
```

然后由 CEO：
- 使用 `sessions_spawn` 创建目标 session
- 使用 `sessions_send` 把 dispatch payload 下发给该 session
- 等结果返回后，用 `record-result` / `create-review` / `update-node-status` 回写台账

这意味着：
- `opc.py` 先负责 **台账与协议**
- OpenClaw session runtime 负责 **真实执行**
- `bind-session` 负责把 node 与真实执行会话绑定起来

---

## 11. 目录结果

运行后会形成：

```text
tasks/
  TASK-AB12CD34/
    task.json
    events.jsonl
    nodes/
      NODE-XXXX.json
    reviews/
      REV-XXXX.json
    artifacts/
```

---

## 结论

这版 CLI 不再只是“最小演示脚本”，而是 OPC v1 的轻控制面样机：

- 用文件台账验证 schema
- 用事件流验证生命周期
- 用 review 验证质量门
- 用 dispatch payload 桥接运行时
- 用 result / summary / resume cursor 支撑真实 workflow 运营
