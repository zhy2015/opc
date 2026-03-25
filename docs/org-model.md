# Organization Model

## 总体组织图

```text
User / Owner
   ↓
CEO Session (主会话)
   ├─ Chief of Staff / Router
   ├─ Planning Office
   ├─ Review Office
   ├─ Dispatch Office
   └─ Execution Departments
        ├─ Engineering
        ├─ Research
        ├─ Documentation
        ├─ Operations
        ├─ Compliance
        └─ Data / Analysis
```

## 1. CEO Session（主会话）

主会话是公司 CEO，不直接承担全部执行，而是承担以下职责：

- 接收外部目标
- 建立任务单
- 判断任务复杂度与经营优先级
- 分配预算、模型、上下文、并行度
- 任命子 Agent 承担具体职责
- 决定何时触发审核、返工、接管或终止
- 对最终结果负责

### CEO 的四项核心管理权

1. **资源分配权**：决定给谁上下文、时间、模型、并发槽位
2. **路由决策权**：决定哪个部门或哪个 Agent 接单
3. **审核触发权**：决定哪些阶段必须走 review gate
4. **人事调度权**：决定新建、暂停、恢复、替换、结束子 Agent

## 2. Chief of Staff / Router

相当于 CEO 办公室前置分拣岗位。

职责：

- 判断是不是复杂任务
- 提炼目标、约束、交付标准
- 将闲聊与正式任务分流
- 生成标准任务标题与摘要

## 3. Planning Office

负责把目标转成可执行计划。

职责：

- 拆解阶段
- 设计 DAG / 依赖关系
- 标记可并行与必须串行的节点
- 为每个节点指定建议角色
- 输出计划草案与风险点

## 4. Review Office

独立于执行部门。

职责：

- 审核 plan 是否合理
- 审核执行结果是否达标
- 拒绝未达标产出并要求返工
- 记录审核意见

这是 OPC 的关键制度之一：

> **执行者不能兼任最终裁决者。**

## 5. Dispatch Office

负责把计划映射到具体 Agent 资源。

职责：

- 选择合适的子 Agent / session
- 按能力、模型、负载、成本分配任务
- 管理并发与队列
- 进行 reroute 与 failover

## 6. Execution Departments

执行部门是专业岗位集合，不是无限泛化 agent。

建议初始部门：

- **Engineering**：代码实现、修复、测试
- **Research**：资料搜集、对比、情报分析
- **Documentation**：文档、PRD、规范、总结
- **Operations**：部署、CI、自动化、环境巡检
- **Compliance**：风险、合规、安全审查
- **Data / Analysis**：数据清洗、报表、分析

## 7. 最小组织集

MVP 不需要完整公司，只需 5 类角色：

- CEO Session
- Router
- Planner
- Reviewer
- Worker(s)

这样已经能形成最小闭环：

`目标 → 规划 → 审核 → 执行 → 复核 → 交付`

## 8. 组织设计原则

### 少而精

不要一上来创建 10+ 固定角色。
先定义少量高价值岗位，再按真实工作量扩展。

### 权责清晰

每个 Agent 都必须回答：

- 我负责什么？
- 我不负责什么？
- 我能向谁汇报？
- 谁能给我派单？

### 可替换

部门职责应大于 конкретный Agent 实例。
换句话说，worker-code-1 坏了，应该能由 worker-code-2 替补。

### 可审计

角色定义必须映射到日志与状态台账，否则组织只是叙事，不是系统。
