# OPC — One Person Company

OPC 是一套面向 OpenClaw 的多 Agent 管理架构草案。

核心思想：**一个主会话，就是一家公司。**

- 主会话 = CEO / 公司总控
- 子 Agent = 各执行部门与专业岗位
- 任务流 = 公司内部从立项、规划、审核、派发到交付的经营流程
- 记忆、状态、审计 = 公司的经营台账

这个仓库聚焦三件事：

1. 定义 OpenClaw-native 的多 Agent 管理模型
2. 将“主会话管理子 Agent”的模式制度化
3. 为后续 MVP / 实现 / 可视化看板提供统一设计基线

## 核心原则

- **主会话即 CEO**：负责目标设定、资源分配、上下文裁剪、风险兜底
- **子 Agent 即部门**：按专业能力接单，不直接越权
- **制度优先于数量**：不是堆更多 Agent，而是建立状态机、审核门、恢复点、权限边界
- **OpenClaw 原生落地**：优先复用 sessions / subagents / memory / docs，而不是先造重框架
- **可管理 > 可演示**：可暂停、可恢复、可审计、可解释，比“自动跑起来”更重要

## 推荐阅读顺序

1. `docs/vision.md` — 愿景与核心思想
2. `docs/opc-architecture.md` — 总体架构总览
3. `docs/org-model.md` — 组织模型：CEO、部门、岗位
4. `docs/control-plane.md` — 管理面：状态、资源、上下文、权限
5. `docs/runtime-architecture.md` — OpenClaw 运行时映射
6. `docs/task-lifecycle.md` — 任务状态机与流转规则
7. `docs/capability-mapping.md` — 对 edict 与其他 skill 的能力吸纳矩阵
8. `docs/design-deltas.md` — OPC 相对其他方案的设计差异
9. `docs/schemas.md` — Task / Node / Review / Event 核心 schema
10. `docs/protocols.md` — CEO 与各角色的交互协议
11. `docs/runtime-skeleton.md` — 最小可跑运行骨架
12. `docs/mvp-plan.md` — 最小可跑落地路径

## 一句话定义

> OPC = 把主会话当 CEO，把子 Agent 当部门，把任务流当经营流程，把状态与记忆当公司的操作系统。

## MVP 骨架已包含

- `templates/`：task / node / review / event 模板
- `scripts/opc.py`：最小控制面 CLI
- `tasks/`：运行时任务台账目录
- `docs/mvp-usage.md`：最小使用说明
- `docs/state-validation.md`：task / node 状态合法迁移规则
- `docs/openclaw-orchestration.md`：接入真实 OpenClaw session 的桥接设计
- `docs/context-packaging.md`：CEO 向子 agent 配给上下文的打包规范
- `docs/operating-rules.md`：独立会话 / 禁止套娃 / 并发上限 / 自动通告
- `docs/session-governance.md`：会话治理与 CEO 独占调度权
- `docs/first-real-workflow.md`：第一条真实 orchestration 工作流

最小演示：

```bash
python3 scripts/opc.py create-task \
  --title "Design OPC runtime MVP" \
  --goal "Build a minimal runnable control loop for OPC"
```

## 已完成的真实演练

- `docs/multi-agent-demo-comic-run.md`：一次真实的 CEO → planner → reviewer → writer 多 agent 演练记录
- `artifacts/comics/opc-architecture-comic-script.md`：用该链路产出的 OPC 架构知识漫画脚本
