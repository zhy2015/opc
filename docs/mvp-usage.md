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
- 各 node 状态计数
- `resume_cursor`
- review 数量
- event 数量
- 每个 node 的最小运营视图

---

## 10. 查看任务全貌

```bash
python3 scripts/opc.py show-task TASK-AB12CD34
```

---

## 目录结果

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
