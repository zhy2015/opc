# Context Packaging

## 目标

定义 CEO 向子 Agent 下发上下文时的最小打包规范。

OPC 的核心思想之一是：

> 上下文不是广播，而是资源配给。

---

## 四类上下文

### 1. mission_context
回答：为什么做这件事。

包含：
- task goal
- node goal
- priority
- acceptance criteria

### 2. working_context
回答：做事需要哪些材料。

包含：
- plan refs
- input refs
- 关键已有结论
- 当前节点依赖结果

### 3. policy_context
回答：哪些不能做，哪些必须遵守。

包含：
- 角色边界
- 安全限制
- 输出格式约束
- 不可越过的 gate

### 4. output_contract
回答：最终要交什么。

包含：
- expected artifact path
- expected output format
- review required or not

---

## 示例

```json
{
  "task_id": "TASK-001",
  "node_id": "NODE-002",
  "role": "worker-doc",
  "mission_context": {
    "goal": "撰写 runtime skeleton 文档",
    "priority": "high",
    "acceptance_criteria": ["结构完整", "可执行"]
  },
  "working_context": {
    "input_refs": ["tasks/TASK-001/artifacts/plan.md"],
    "dependency_outputs": []
  },
  "policy_context": {
    "must_not": ["跳过审核", "擅自扩大范围"],
    "role_boundary": "只完成当前 node"
  },
  "output_contract": {
    "expected_artifact": "tasks/TASK-001/artifacts/runtime-skeleton.md",
    "review_required": true
  }
}
```

---

## 设计原则

- 少给，不多给
- 只给岗位必需上下文
- 不让 worker 承担 CEO 级上下文负担
- 返工时只补必要差量上下文

---

## 结论

上下文包是 OPC 调度质量的核心，不精确裁剪，就谈不上真正的资源管理。
