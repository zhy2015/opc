# Control Plane

## 为什么先谈管理面

多 Agent 系统最容易把注意力放在“执行层”。
但 OPC 的重点是控制面：

- 谁能接单
- 任务现在在哪
- 为什么被打回
- 哪个 Agent 卡住了
- 是否可以恢复
- 是否需要人工接管

如果没有控制面，多 Agent 只是并发脚本集合。

## 控制面的六个核心对象

### 1. Task

任务单是整个系统的经营主对象。

必须至少包含：

- `task_id`
- `title`
- `goal`
- `constraints`
- `acceptance_criteria`
- `priority`
- `status`
- `owner`
- `created_at`
- `updated_at`
- `resume_cursor`

### 2. Stage / Node

每个任务由多个阶段或 DAG 节点组成。

每个节点包含：

- `node_id`
- `task_id`
- `kind`（plan/review/execute/summarize/...）
- `assigned_role`
- `assigned_session`
- `depends_on[]`
- `status`
- `input_refs[]`
- `output_refs[]`
- `retry_count`
- `last_error`

### 3. Agent Resource

Agent 在管理层必须被视作资源对象。

属性建议：

- `agent_id`
- `role`
- `skills[]`
- `model`
- `capacity`
- `current_load`
- `health`
- `session_key`
- `visibility`

### 4. Review Record

审核必须有正式记录，而不是一句“感觉不行”。

- `review_id`
- `target_task_id`
- `target_node_id`
- `reviewer`
- `decision`（approve / reject / conditional）
- `reasons[]`
- `required_changes[]`
- `timestamp`

### 5. Event Log

事件流是审计和回放基础。

示例事件：

- task_created
- plan_submitted
- plan_rejected
- node_dispatched
- node_started
- node_blocked
- node_completed
- review_requested
- review_passed
- review_failed
- task_paused
- task_resumed
- task_cancelled

### 6. Resource Budget

CEO 需要对资源有显式感知：

- token / cost 预算
- 最大并发数
- 允许使用的模型范围
- 对外联网权限
- 执行时限

## CEO 的管理动作

主会话至少应支持以下动作：

- `create_task`
- `approve_plan`
- `reject_plan`
- `dispatch_node`
- `pause_task`
- `resume_task`
- `cancel_task`
- `reroute_node`
- `spawn_agent`
- `retire_agent`
- `request_review`
- `finalize_delivery`

## 上下文分配机制

OPC 的一个关键思想是：

> CEO 不是把全部上下文一股脑扔给所有子 Agent，而是**按岗位切上下文**。

建议把上下文分为：

- **mission context**：任务目标、验收标准、优先级
- **working context**：当前节点所需资料
- **policy context**：规则、红线、风格约束
- **memory context**：项目历史、过往决策

不同角色拿到不同上下文包。

## 权限边界

需要建立最小权限原则：

- planner 不能直接宣布任务 done
- worker 不能绕过 reviewer 直接交付
- reviewer 不直接修改执行结果，只提意见或封驳
- dispatcher 不擅自改业务目标，只负责资源映射

## 干预机制

管理系统必须支持：

- pause
- resume
- cancel
- reroute
- escalate_to_ceo
- fallback_to_manual

这决定了系统是“自动化工具”，还是“真正可经营系统”。

## 可观测性

至少需要以下监控指标：

- 任务总数 / 各状态数量
- 节点平均耗时
- Agent 活跃度与空闲度
- 失败率 / 重试率
- 被 reviewer 打回的比例
- token / cost 消耗
- 长时间卡住任务列表

## 结论

控制面是 OPC 的灵魂。

执行层负责做事，控制面负责让这家公司不失控。
