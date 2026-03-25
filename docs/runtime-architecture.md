# Runtime Architecture

## OpenClaw-native 映射

OPC 不假设先开发一个全新的多 Agent 框架。

相反，第一原则是：**尽量使用 OpenClaw 现有原语搭建公司化控制系统。**

## 运行时映射表

### 1. CEO Session = 主会话

主会话承担：

- 用户接口
- 任务建单
- 路由与组织决策
- 资源分配
- 结果汇总

### 2. 子 Agent = sessions / subagents / ACP sessions

用于承载：

- planner
- reviewer
- worker-code
- worker-doc
- worker-research
- worker-ops

### 3. 任务台账 = 文件 + memory

第一版不必上数据库。
可先采用：

- `tasks/*.md`：任务单
- `tasks/<task_id>/nodes/*.json`：节点状态
- `tasks/<task_id>/artifacts/`：产物
- `tasks/<task_id>/events.jsonl`：事件流
- `memory/`：长期决策与项目记忆

### 4. 调度动作 = sessions_spawn / sessions_send

- `sessions_spawn`：创建新角色会话
- `sessions_send`：向已有子 Agent 下发任务或追问
- `sessions_list`：按需查看当前子会话状态

### 5. 观测层 = 本地文档 + 简单 dashboard

MVP 阶段可先采用：

- markdown 看板
- JSON/JSONL 事件流
- 后续再接前端可视化

## 推荐目录结构

```text
opc/
  docs/
  tasks/
    TASK-001/
      task.md
      plan.md
      review.md
      events.jsonl
      nodes/
      artifacts/
  agents/
    router/
    planner/
    reviewer/
    worker-code/
    worker-doc/
```

## 基础运行流

### Step 1: CEO 建单

主会话根据用户请求生成 task。

### Step 2: 启动 planner

向 planner session 发送：

- 任务目标
- 约束
- 交付物要求
- 可用资源说明

### Step 3: 启动 reviewer 评审计划

reviewer 只评计划，不直接替 planner 干活。

### Step 4: dispatcher / CEO 派发执行

对不同节点选择不同 worker。

### Step 5: 回收产出并请求复核

结果先过 reviewer，再汇总交付。

### Step 6: 归档与可恢复点写入

写入：

- 哪些节点已完成
- 哪些节点失败
- 从哪里恢复
- 有哪些工件可复用

## 为什么这种映射适合 OpenClaw

因为 OpenClaw 已经天然有：

- 多 session / 子代理能力
- 跨 session 通信能力
- 文件工作区
- 记忆系统
- ACP harness 运行时

也就是说，OPC 的创新点不在“再造运行时”，而在：

- 定义组织与控制协议
- 约束角色与任务流
- 给现有能力加管理制度

## 两种实现路线

### 轻量路线

- markdown + json 台账
- 手工/半自动调度
- 低成本验证控制模型

### 产品化路线

- 统一 task schema
- 命令式管理 API
- dashboard
- 实时状态流
- 权限矩阵与资源配额

## 结论

OpenClaw 已经具备“公司运行时”的基础设施。
OPC 要做的是把这些原语组织成一个 CEO 可经营的系统。
