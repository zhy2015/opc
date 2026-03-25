# MVP Plan

## MVP 目标

用最少实现，验证 OPC 的核心命题：

> 主会话是否能像 CEO 一样，管理多个子 Agent 完成复杂任务，并且具备可审、可控、可恢复能力。

## 第一阶段只做 5 个角色

- CEO Session
- Router
- Planner
- Reviewer
- Worker-Code

必要时再加：

- Worker-Doc
- Worker-Research

## 第一阶段只做 6 个能力

1. **任务建单**
2. **计划生成**
3. **计划审核**
4. **执行派发**
5. **结果审核**
6. **暂停/恢复/取消**

## 不急着做的东西

- 大而全 dashboard
- 十几个固定部门
- 全自动复杂路由
- 数据库优先设计
- 过早优化的模型编排

## 建议实现顺序

### Phase 0: 文档与协议

先定：

- task schema
- node schema
- review schema
- status machine
- 角色边界

### Phase 1: 文件台账版

产物：

- `tasks/`
- `events.jsonl`
- 手工/半自动 session 调度
- 可恢复任务单

### Phase 2: 命令化控制版

加入：

- create/pause/resume/cancel/reroute 命令
- 标准化事件写入
- 统一 artifacts 目录

### Phase 3: 简单看板版

可视化：

- 任务列表
- 状态分布
- 当前活跃 session
- 卡住任务
- reviewer 打回记录

## MVP 成功标准

如果下面 5 条能成立，MVP 就成功：

- 主会话能把复杂任务拆给多个子 Agent
- reviewer 能独立打回不合格方案或结果
- 中途暂停后能恢复，而不是从头再来
- 所有流转都有台账可追溯
- 最终交付前有明确质量门

## 示例闭环

以“做一个新功能并交付文档”为例：

1. CEO 建 task
2. Planner 拆出代码、测试、文档节点
3. Reviewer 审核计划
4. Worker-Code 执行代码
5. Worker-Doc 写文档
6. Reviewer 审核结果
7. CEO 汇总交付
8. 归档 task 与 artifacts

## 最后判断

MVP 的重点不是功能多，而是验证一个判断：

> OpenClaw 是否已经足够作为 One Person Company 的运行底座。

我的结论是：大概率足够。差的不是底座，而是控制协议和组织模型。
