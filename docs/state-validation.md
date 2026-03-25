# State Validation

## 目标

为 OPC MVP 补上最基本的状态合法性约束，避免 task / node 被任意跳转。

---

## 1. Task 合法迁移

推荐允许：

- `new -> triaged`
- `triaged -> planned`
- `planned -> plan_review`
- `plan_review -> plan_rejected`
- `plan_review -> dispatched`
- `plan_rejected -> planned`
- `dispatched -> running`
- `running -> blocked`
- `running -> awaiting_review`
- `awaiting_review -> rework`
- `awaiting_review -> delivered`
- `rework -> running`
- `running -> paused`
- `paused -> resumable`
- `resumable -> running`
- `running -> failed`
- `blocked -> paused`
- `blocked -> cancelled`
- `failed -> paused`
- `delivered -> archived`

可全局打断：
- `new|triaged|planned|plan_review|plan_rejected|dispatched|running|blocked|awaiting_review|rework|paused|resumable|failed -> cancelled`

---

## 2. Node 合法迁移

推荐允许：

- `queued -> assigned`
- `assigned -> running`
- `running -> blocked`
- `running -> review_pending`
- `running -> done`
- `running -> failed`
- `review_pending -> rework`
- `review_pending -> done`
- `rework -> running`
- `blocked -> assigned`
- `blocked -> cancelled`
- `failed -> assigned`

可全局打断：
- `queued|assigned|running|blocked|review_pending|rework|failed -> cancelled`

---

## 3. 校验原则

- 不允许跳过关键 gate
- 不允许从完成态回退到早期态
- `cancelled` 与 `archived` 默认视为终态
- 所有非法跳转必须明确报错

---

## 4. 为什么先做轻量校验

MVP 阶段不需要复杂工作流引擎，但必须先阻止最明显的管理失控：

- worker 直接把 task 改成 delivered
- reviewer 尚未审核就把 node 标 done
- paused 任务被跳过 resumable 直接归档

---

## 5. 下一步

在 `scripts/opc.py` 中加入：

- `VALID_TASK_TRANSITIONS`
- `VALID_NODE_TRANSITIONS`
- `assert_transition()`

这样文件台账版也具备最基础的制度约束。
