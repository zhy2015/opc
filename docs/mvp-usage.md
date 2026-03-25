# MVP Usage

## 目标

演示 OPC 的最小可跑实现：
- 创建 task
- 创建 node
- 更新 node 状态
- 写入 review
- 查看 task 全貌

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

## 5. 查看任务全貌

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

这版 CLI 不是最终产品，而是 OPC 的最小控制面样机：

- 用文件台账验证 schema
- 用事件流验证生命周期
- 用 review 验证质量门
- 为后续接入 session orchestration 做准备
