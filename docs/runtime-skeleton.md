# Runtime Skeleton

## 目标

为 OPC 提供一个最小可跑的运行骨架建议，使其能在 OpenClaw 环境中以文件台账 + session 协作方式落地。

---

## 目录结构

```text
opc/
  docs/
  tasks/
    TASK-001/
      task.json
      events.jsonl
      nodes/
        NODE-001.json
        NODE-002.json
      reviews/
        REV-001.json
      artifacts/
        plan.md
        protocols.md
  templates/
    task.template.json
    node.template.json
    review.template.json
    event.template.jsonl
```

---

## 最小运行循环

### 1. create_task
CEO 创建 `task.json`

### 2. request_plan
向 planner session 下发 planning 包

### 3. write_plan_nodes
将返回的 plan 写入：
- `artifacts/plan.md`
- `nodes/*.json`
- `events.jsonl`

### 4. request_plan_review
向 reviewer session 下发审核请求

### 5. dispatch_nodes
将 approved node 派发给 worker sessions

### 6. collect_outputs
回收 artifacts，并写入 node 状态

### 7. request_result_review
将结果送 reviewer 审核

### 8. finalize_delivery
汇总交付，并写入 archived / delivered 事件

---

## 最小命令集建议

即使先不用 CLI，也建议内部统一这些管理动作：

- `create_task`
- `request_plan`
- `approve_plan`
- `reject_plan`
- `dispatch_node`
- `pause_task`
- `resume_task`
- `cancel_task`
- `request_review`
- `complete_delivery`

---

## 文件级原则

- `task.json` 只放任务级事实
- `nodes/*.json` 只放节点级事实
- `reviews/*.json` 只放 reviewer 判断
- `events.jsonl` 作为时间线真相源
- `artifacts/` 放内容产出

---

## Session 绑定建议

### 固定角色 session
适合：
- planner
- reviewer
- 高频 worker

优点：
- 可保留角色记忆
- 适合连续协作

### 临时 session
适合：
- 一次性专项研究
- 短时文档生成
- 独立实验

优点：
- 隔离性强
- 上下文污染低

---

## MVP 成功信号

如果 Runtime Skeleton 能完成以下闭环，就说明 OPC 已进入可实现阶段：

- task 能创建
- plan 能被 reviewer 审核
- node 能被 worker 执行
- result 能被 reviewer 复核
- 中途能 pause / resume
- 所有过程可从 events.jsonl 回放

---

## 结论

Runtime Skeleton 是 OPC 从文档架构迈向工程实现的桥梁层。
