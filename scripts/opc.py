#!/usr/bin/env python3
import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "tasks"
TEMPLATES_DIR = ROOT / "templates"

VALID_TASK_TRANSITIONS = {
    "new": {"triaged", "cancelled"},
    "triaged": {"planned", "cancelled"},
    "planned": {"plan_review", "cancelled"},
    "plan_review": {"plan_rejected", "dispatched", "cancelled"},
    "plan_rejected": {"planned", "cancelled"},
    "dispatched": {"running", "cancelled"},
    "running": {"blocked", "awaiting_review", "paused", "failed", "cancelled"},
    "blocked": {"paused", "cancelled"},
    "awaiting_review": {"rework", "delivered", "cancelled"},
    "rework": {"running", "cancelled"},
    "paused": {"resumable", "cancelled"},
    "resumable": {"running", "cancelled"},
    "failed": {"paused", "cancelled"},
    "delivered": {"archived"},
    "archived": set(),
    "cancelled": set(),
}

VALID_NODE_TRANSITIONS = {
    "queued": {"assigned", "cancelled", "skipped"},
    "assigned": {"running", "cancelled", "skipped"},
    "running": {"blocked", "review_pending", "done", "failed", "cancelled"},
    "blocked": {"assigned", "cancelled"},
    "review_pending": {"rework", "done", "cancelled"},
    "rework": {"running", "cancelled"},
    "failed": {"assigned", "cancelled"},
    "done": set(),
    "skipped": set(),
    "cancelled": set(),
}

KEY_EVENT_TYPES = {
    "node_started",
    "result_recorded",
    "review_requested",
    "review_passed",
    "review_failed",
    "node_blocked",
    "node_completed",
    "node_failed",
    "node_skipped",
    "task_created",
    "task_updated",
}


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso(ts: Optional[str]):
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def minutes_since(ts: Optional[str]):
    dt = parse_iso(ts)
    if not dt:
        return None
    delta = datetime.now(timezone.utc) - dt
    return round(delta.total_seconds() / 60, 1)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def append_jsonl(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def next_id(prefix: str):
    return "{}-{}".format(prefix, uuid.uuid4().hex[:8].upper())


def ensure_task_dirs(task_id: str):
    task_dir = TASKS_DIR / task_id
    (task_dir / "nodes").mkdir(parents=True, exist_ok=True)
    (task_dir / "reviews").mkdir(parents=True, exist_ok=True)
    (task_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    return task_dir


def assert_transition(old_status: str, new_status: str, allowed_map: dict, kind: str):
    if old_status == new_status:
        return
    allowed = allowed_map.get(old_status, set())
    if new_status not in allowed:
        raise SystemExit("Illegal {} transition: {} -> {}".format(kind, old_status, new_status))


def append_event(task_id: str, node_id: Optional[str], event_type: str, actor_role: str, payload: dict):
    event = load_json(TEMPLATES_DIR / "event.template.json")
    event.update({
        "event_id": next_id("EVT"),
        "task_id": task_id,
        "node_id": node_id,
        "type": event_type,
        "actor": {"role": actor_role, "session": None},
        "payload": payload,
        "timestamp": now_iso(),
    })
    append_jsonl(TASKS_DIR / task_id / "events.jsonl", event)


def load_task(task_id: str):
    path = TASKS_DIR / task_id / "task.json"
    if not path.exists():
        raise SystemExit("Task not found: {}".format(task_id))
    return load_json(path), path


def load_node(task_id: str, node_id: str):
    path = TASKS_DIR / task_id / "nodes" / (node_id + ".json")
    if not path.exists():
        raise SystemExit("Node not found: {}".format(node_id))
    return load_json(path), path


def load_events(task_id: str):
    events_path = TASKS_DIR / task_id / "events.jsonl"
    events = []
    if not events_path.exists():
        return events
    with events_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))
    return events


def compute_task_progress(nodes):
    if not nodes:
        return 0
    done_like = sum(1 for n in nodes if n.get("status") in {"done", "skipped"})
    return round((done_like / len(nodes)) * 100)


def derive_stage(task, nodes):
    task_status = task.get("status")
    if task_status in {"delivered", "archived"}:
        return "delivered"
    if any(n.get("status") == "review_pending" for n in nodes):
        return "awaiting_result_review"
    if any(n.get("status") == "running" for n in nodes):
        return "execution_in_progress"
    if any(n.get("status") == "blocked" for n in nodes):
        return "blocked"
    if any(n.get("status") == "queued" for n in nodes):
        return "dispatch_ready"
    return task_status or "unknown"


def recent_key_events(events, limit):
    filtered = [e for e in events if e.get("type") in KEY_EVENT_TYPES]
    return filtered[-limit:]


def load_runtime_sessions_map(args):
    sessions = []
    if not args.sessions_file:
        return {}
    sessions_path = Path(args.sessions_file)
    if not sessions_path.exists():
        return {}
    with sessions_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    sessions = data.get("sessions", []) if isinstance(data, dict) else data
    session_map = {}
    for sess in sessions:
        key = sess.get("key") or sess.get("sessionKey")
        if key:
            session_map[key] = sess
    return session_map


def derive_session_health(node, runtime_session, stale_after_minutes):
    node_status = node.get("status")
    node_age = minutes_since(node.get("updated_at"))
    runtime_age = minutes_since(runtime_session.get("updatedAt")) if runtime_session else None

    if node_status in {"done", "skipped", "cancelled"}:
        return "done"
    if node_status == "blocked":
        return "blocked"
    if runtime_session is None and node.get("assigned_session"):
        return "unresolved"
    if runtime_session is None:
        if node_status in {"assigned", "running", "review_pending"}:
            return "idle"
        return "unbound"

    recent_min = None
    ages = [a for a in [node_age, runtime_age] if a is not None]
    if ages:
        recent_min = min(ages)
    if recent_min is not None and recent_min > stale_after_minutes and node_status not in {"done", "skipped", "cancelled"}:
        return "stale"
    if node_status in {"running", "review_pending"}:
        return "active"
    if node_status == "assigned":
        return "idle"
    return runtime_session.get("status", "unknown")


def build_agent_rows(nodes, args):
    session_map = load_runtime_sessions_map(args)
    rows = []
    for node in nodes:
        assigned_session = node.get("assigned_session")
        runtime_session = session_map.get(assigned_session, {}) if assigned_session else {}
        health = derive_session_health(node, runtime_session, args.stale_after_minutes)
        rows.append({
            "session_key": assigned_session,
            "node_id": node.get("node_id"),
            "role": node.get("assigned_role"),
            "node_status": node.get("status"),
            "runtime": node.get("runtime"),
            "session_mode": node.get("session_mode"),
            "last_ledger_update": node.get("updated_at"),
            "ledger_age_min": minutes_since(node.get("updated_at")),
            "runtime_status": runtime_session.get("status") if runtime_session else None,
            "runtime_updated_at": runtime_session.get("updatedAt") if runtime_session else None,
            "runtime_age_min": minutes_since(runtime_session.get("updatedAt")) if runtime_session else None,
            "result_summary": node.get("result_summary"),
            "health": health,
        })
    return rows


def sync_resume_cursor(task_id: str):
    task, path = load_task(task_id)
    task_dir = TASKS_DIR / task_id / "nodes"
    completed_nodes = []
    next_nodes = []
    stable_artifacts = list(task.get("resume_cursor", {}).get("stable_artifacts", []))
    for node_path in sorted(task_dir.glob("*.json")):
        node = load_json(node_path)
        status = node.get("status")
        node_id = node.get("node_id")
        if status in {"done", "skipped"}:
            completed_nodes.append(node_id)
            for ref in node.get("output_refs", []):
                if ref not in stable_artifacts:
                    stable_artifacts.append(ref)
        if status in {"queued", "assigned", "blocked", "rework", "review_pending", "failed"}:
            deps = node.get("depends_on", []) or []
            if all(dep in completed_nodes for dep in deps):
                next_nodes.append(node_id)
    task.setdefault("resume_cursor", {})
    task["resume_cursor"]["completed_nodes"] = completed_nodes
    task["resume_cursor"]["next_nodes"] = next_nodes
    task["resume_cursor"]["stable_artifacts"] = stable_artifacts
    task["updated_at"] = now_iso()
    save_json(path, task)


def create_task(args):
    task = load_json(TEMPLATES_DIR / "task.template.json")
    task_id = args.task_id or next_id("TASK")
    ts = now_iso()
    task.update({
        "task_id": task_id,
        "title": args.title,
        "goal": args.goal,
        "priority": args.priority,
        "owner": args.owner,
        "created_at": ts,
        "updated_at": ts,
    })
    if args.acceptance:
        task["acceptance_criteria"] = args.acceptance
    task_dir = ensure_task_dirs(task_id)
    save_json(task_dir / "task.json", task)
    append_event(task_id, None, "task_created", args.owner, {"title": args.title})
    print(task_id)


def update_task_status(args):
    task, path = load_task(args.task_id)
    old = task["status"]
    assert_transition(old, args.status, VALID_TASK_TRANSITIONS, "task")
    task["status"] = args.status
    task["updated_at"] = now_iso()
    save_json(path, task)
    append_event(args.task_id, None, "task_updated", args.actor, {"from": old, "to": args.status})
    print("{}: {} -> {}".format(args.task_id, old, args.status))


def create_node(args):
    task, task_path = load_task(args.task_id)
    node = load_json(TEMPLATES_DIR / "node.template.json")
    node_id = args.node_id or next_id("NODE")
    ts = now_iso()
    node.update({
        "node_id": node_id,
        "task_id": args.task_id,
        "kind": args.kind,
        "title": args.title,
        "assigned_role": args.role,
        "assigned_session": None,
        "spawned_by": None,
        "runtime": None,
        "session_mode": None,
        "dispatch_payload_ref": None,
        "status": args.status,
        "depends_on": args.depends_on or [],
        "instructions": args.instructions or "",
        "created_at": ts,
        "updated_at": ts,
    })
    if args.acceptance:
        node["acceptance_criteria"] = args.acceptance
    save_json(TASKS_DIR / args.task_id / "nodes" / (node_id + ".json"), node)
    append_event(args.task_id, node_id, "node_dispatched", args.actor, {"role": args.role, "kind": args.kind})
    if task["status"] == "plan_review":
        task["status"] = "dispatched"
        task["updated_at"] = now_iso()
        save_json(task_path, task)
    sync_resume_cursor(args.task_id)
    print(node_id)


def update_node_status(args):
    node, path = load_node(args.task_id, args.node_id)
    old = node["status"]
    assert_transition(old, args.status, VALID_NODE_TRANSITIONS, "node")
    node["status"] = args.status
    node["updated_at"] = now_iso()
    if args.output_ref:
        refs = list(node.get("output_refs", []))
        refs.append(args.output_ref)
        node["output_refs"] = refs
    save_json(path, node)
    event_map = {
        "running": "node_started",
        "blocked": "node_blocked",
        "done": "node_completed",
        "failed": "node_failed",
        "review_pending": "review_requested",
        "skipped": "node_skipped",
    }
    append_event(args.task_id, args.node_id, event_map.get(args.status, "task_updated"), args.actor, {"from": old, "to": args.status})
    sync_resume_cursor(args.task_id)
    print("{}: {} -> {}".format(args.node_id, old, args.status))


def create_review(args):
    review = load_json(TEMPLATES_DIR / "review.template.json")
    review_id = args.review_id or next_id("REV")
    review.update({
        "review_id": review_id,
        "task_id": args.task_id,
        "target_node_id": args.node_id,
        "reviewer_role": args.reviewer_role,
        "reviewer_session": None,
        "stage": args.stage,
        "decision": args.decision,
        "reasons": args.reasons or [],
        "required_changes": args.required_changes or [],
        "notes": args.notes or "",
        "created_at": now_iso(),
    })
    save_json(TASKS_DIR / args.task_id / "reviews" / (review_id + ".json"), review)
    event_type = "review_passed" if args.decision == "approve" else "review_failed"
    append_event(args.task_id, args.node_id, event_type, args.reviewer_role, {"stage": args.stage, "decision": args.decision})
    print(review_id)


def render_dispatch_payload(args):
    task, _ = load_task(args.task_id)
    node, node_path = load_node(args.task_id, args.node_id)
    payload = {
        "task_id": args.task_id,
        "node_id": args.node_id,
        "role": node.get("assigned_role"),
        "mission_context": {
            "task_title": task.get("title"),
            "goal": task.get("goal"),
            "priority": task.get("priority"),
            "node_title": node.get("title"),
            "acceptance_criteria": node.get("acceptance_criteria", []),
        },
        "working_context": {
            "task_context_refs": task.get("context_refs", []),
            "input_refs": node.get("input_refs", []),
            "depends_on": node.get("depends_on", []),
            "instructions": node.get("instructions", ""),
        },
        "policy_context": {
            "role_boundary": "Only complete the assigned node.",
            "must_not": [
                "Do not change task scope.",
                "Do not bypass review gates.",
                "Do not mark unrelated nodes complete."
            ]
        },
        "output_contract": {
            "review_required": node.get("review_required", True),
            "expected_output_refs": node.get("output_refs", []),
            "artifact_dir": "tasks/{}/artifacts".format(args.task_id)
        }
    }
    artifact_path = TASKS_DIR / args.task_id / "artifacts" / (args.node_id + "-dispatch.json")
    save_json(artifact_path, payload)
    node["dispatch_payload_ref"] = str(artifact_path.relative_to(ROOT))
    node["updated_at"] = now_iso()
    save_json(node_path, node)
    append_event(args.task_id, args.node_id, "task_updated", args.actor, {"dispatch_payload_ref": node["dispatch_payload_ref"]})
    print(node["dispatch_payload_ref"])


def bind_session(args):
    node, path = load_node(args.task_id, args.node_id)
    node["assigned_session"] = args.session_key
    node["spawned_by"] = args.actor
    node["runtime"] = args.runtime
    node["session_mode"] = args.session_mode
    node["updated_at"] = now_iso()
    save_json(path, node)
    append_event(args.task_id, args.node_id, "task_updated", args.actor, {
        "assigned_session": args.session_key,
        "runtime": args.runtime,
        "session_mode": args.session_mode,
    })
    print("{} bound to {}".format(args.node_id, args.session_key))


def record_result(args):
    node, path = load_node(args.task_id, args.node_id)
    output_refs = list(node.get("output_refs", []))
    for ref in args.output_ref or []:
        if ref not in output_refs:
            output_refs.append(ref)
    node["output_refs"] = output_refs
    if args.input_ref:
        input_refs = list(node.get("input_refs", []))
        for ref in args.input_ref:
            if ref not in input_refs:
                input_refs.append(ref)
        node["input_refs"] = input_refs
    if args.summary:
        node["result_summary"] = args.summary
    node["updated_at"] = now_iso()
    save_json(path, node)
    append_event(args.task_id, args.node_id, "result_recorded", args.actor, {
        "summary": args.summary or "",
        "output_refs": args.output_ref or [],
        "input_refs": args.input_ref or [],
    })
    sync_resume_cursor(args.task_id)
    print("{} recorded {} refs".format(args.node_id, len(args.output_ref or [])))


def mark_review_pending(args):
    node, path = load_node(args.task_id, args.node_id)
    old = node["status"]
    if old != "running":
        raise SystemExit("mark-review-pending requires node status 'running', got '{}'".format(old))
    node["status"] = "review_pending"
    node["updated_at"] = now_iso()
    save_json(path, node)
    append_event(args.task_id, args.node_id, "review_requested", args.actor, {
        "from": old,
        "to": "review_pending",
        "stage": args.stage,
        "note": args.note or "",
    })
    sync_resume_cursor(args.task_id)
    print("{}: {} -> review_pending".format(args.node_id, old))


def skip_node(args):
    node, path = load_node(args.task_id, args.node_id)
    old = node["status"]
    assert_transition(old, "skipped", VALID_NODE_TRANSITIONS, "node")
    node["status"] = "skipped"
    node["skip_reason"] = args.reason
    node["updated_at"] = now_iso()
    save_json(path, node)
    append_event(args.task_id, args.node_id, "node_skipped", args.actor, {
        "from": old,
        "to": "skipped",
        "reason": args.reason,
    })
    sync_resume_cursor(args.task_id)
    print("{}: {} -> skipped".format(args.node_id, old))


def task_summary(args):
    task, _ = load_task(args.task_id)
    task_dir = TASKS_DIR / args.task_id
    nodes = [load_json(p) for p in sorted((task_dir / "nodes").glob("*.json"))]
    reviews = [load_json(p) for p in sorted((task_dir / "reviews").glob("*.json"))]
    events = load_events(args.task_id)
    by_status = {}
    for node in nodes:
        by_status[node["status"]] = by_status.get(node["status"], 0) + 1
    summary = {
        "task_id": task["task_id"],
        "title": task["title"],
        "status": task["status"],
        "priority": task.get("priority"),
        "goal": task.get("goal"),
        "stage": derive_stage(task, nodes),
        "progress_pct": compute_task_progress(nodes),
        "node_counts": by_status,
        "resume_cursor": task.get("resume_cursor", {}),
        "review_count": len(reviews),
        "event_count": len(events),
        "recent_events": recent_key_events(events, 5),
        "nodes": [
            {
                "node_id": n["node_id"],
                "title": n["title"],
                "status": n["status"],
                "role": n.get("assigned_role"),
                "depends_on": n.get("depends_on", []),
                "assigned_session": n.get("assigned_session"),
            }
            for n in nodes
        ],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def task_brief(args):
    task, _ = load_task(args.task_id)
    task_dir = TASKS_DIR / args.task_id
    nodes = [load_json(p) for p in sorted((task_dir / "nodes").glob("*.json"))]
    events = load_events(args.task_id)
    counts = {}
    for node in nodes:
        counts[node["status"]] = counts.get(node["status"], 0) + 1
    active = [n for n in nodes if n.get("status") in {"running", "review_pending", "blocked", "assigned"}]
    recent = recent_key_events(events, 3)
    print("# {} | {} | {}%".format(task["task_id"], task.get("status"), compute_task_progress(nodes)))
    print("- 标题: {}".format(task.get("title")))
    print("- 阶段: {}".format(derive_stage(task, nodes)))
    print("- 节点计数: {}".format(json.dumps(counts, ensure_ascii=False)))
    if active:
        print("- 当前活跃:")
        for node in active:
            print("  - {} | {} | role={} | session={}".format(
                node.get("node_id"),
                node.get("status"),
                node.get("assigned_role"),
                node.get("assigned_session") or "-",
            ))
    if recent:
        print("- 最近事件:")
        for event in recent:
            print("  - {} | {} | {}".format(event.get("timestamp"), event.get("type"), event.get("node_id") or "task"))


def task_events(args):
    events = load_events(args.task_id)
    if args.key_only:
        events = [e for e in events if e.get("type") in KEY_EVENT_TYPES]
    if args.tail:
        events = events[-args.tail:]
    print(json.dumps(events, ensure_ascii=False, indent=2))


def task_agent_status(args):
    task_dir = TASKS_DIR / args.task_id
    nodes = [load_json(p) for p in sorted((task_dir / "nodes").glob("*.json"))]
    rows = build_agent_rows(nodes, args)
    print(json.dumps(rows, ensure_ascii=False, indent=2))


def task_report(args):
    task, _ = load_task(args.task_id)
    task_dir = TASKS_DIR / args.task_id
    nodes = [load_json(p) for p in sorted((task_dir / "nodes").glob("*.json"))]
    reviews = [load_json(p) for p in sorted((task_dir / "reviews").glob("*.json"))]
    events = load_events(args.task_id)
    progress = compute_task_progress(nodes)
    stage = derive_stage(task, nodes)
    print("# {} 状态汇报".format(task["task_id"]))
    print()
    print("## 总览")
    print("- 标题: {}".format(task.get("title")))
    print("- 目标: {}".format(task.get("goal")))
    print("- 状态: {}".format(task.get("status")))
    print("- 阶段: {}".format(stage))
    print("- 优先级: {}".format(task.get("priority")))
    print("- 完成度: {}%".format(progress))
    print("- review 数: {}".format(len(reviews)))
    print("- event 数: {}".format(len(events)))
    print("- 更新时间: {}".format(task.get("updated_at")))
    print()
    print("## 节点进展")
    for node in nodes:
        print("- {} | {} | role={} | session={}".format(
            node.get("node_id"),
            node.get("status"),
            node.get("assigned_role"),
            node.get("assigned_session") or "-",
        ))
        print("  - 标题: {}".format(node.get("title")))
        print("  - depends_on: {}".format(", ".join(node.get("depends_on", [])) or "-"))
        print("  - runtime: {} / {}".format(node.get("runtime") or "-", node.get("session_mode") or "-"))
        print("  - result: {}".format(node.get("result_summary") or "-"))
        print("  - output_refs: {}".format(", ".join(node.get("output_refs", [])) or "-"))
        print("  - input_refs: {}".format(", ".join(node.get("input_refs", [])) or "-"))
        print("  - review_required: {}".format(node.get("review_required")))
        print("  - updated_at: {}".format(node.get("updated_at")))
        if node.get("last_error"):
            print("  - last_error: {}".format(node.get("last_error")))
    if args.with_agents:
        print()
        print("## Agent / Session 健康")
        rows = build_agent_rows(nodes, args)
        for row in rows:
            print("- session={} | node={} | role={} | health={}".format(
                row.get("session_key") or "-",
                row.get("node_id"),
                row.get("role"),
                row.get("health"),
            ))
            print("  - node_status: {}".format(row.get("node_status")))
            print("  - runtime: {} / {}".format(row.get("runtime") or "-", row.get("session_mode") or "-"))
            print("  - ledger_age_min: {}".format(row.get("ledger_age_min")))
            print("  - runtime_status: {}".format(row.get("runtime_status") or "-"))
            print("  - runtime_age_min: {}".format(row.get("runtime_age_min")))
            print("  - result: {}".format(row.get("result_summary") or "-"))
    print()
    print("## 最近关键事件")
    for event in recent_key_events(events, args.tail):
        print("- {} | {} | {}".format(
            event.get("timestamp"),
            event.get("type"),
            event.get("node_id") or "task",
        ))
    print()
    print("## Resume Cursor")
    print(json.dumps(task.get("resume_cursor", {}), ensure_ascii=False, indent=2))
    print()
    print("## CEO 建议")
    blocked = [n for n in nodes if n.get("status") == "blocked"]
    review_pending = [n for n in nodes if n.get("status") == "review_pending"]
    running = [n for n in nodes if n.get("status") == "running"]
    if args.with_agents:
        stale_rows = [r for r in build_agent_rows(nodes, args) if r.get("health") == "stale"]
        if stale_rows:
            print("- 存在 stale session，优先干预：{}".format(", ".join((r.get("session_key") or r.get("node_id")) for r in stale_rows)))
            return
    if blocked:
        print("- 存在 blocked 节点，优先处理阻塞：{}".format(", ".join(n.get("node_id") for n in blocked)))
    elif review_pending:
        print("- 当前优先处理 review gate：{}".format(", ".join(n.get("node_id") for n in review_pending)))
    elif running:
        print("- 当前保持执行推进，重点关注运行中节点的结果回写：{}".format(", ".join(n.get("node_id") for n in running)))
    elif task.get("status") == "delivered":
        print("- 任务已 delivered，可转入归档或下一轮 runtime 强化。")
    else:
        print("- 可继续从 resume_cursor.next_nodes 推进下一批节点。")


def show_task(args):
    task, _ = load_task(args.task_id)
    task_dir = TASKS_DIR / args.task_id
    nodes = sorted((task_dir / "nodes").glob("*.json"))
    reviews = sorted((task_dir / "reviews").glob("*.json"))
    print(json.dumps({
        "task": task,
        "nodes": [load_json(p) for p in nodes],
        "reviews": [load_json(p) for p in reviews],
    }, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="OPC MVP task control CLI")
    sub = parser.add_subparsers(dest="cmd")
    sub.required = True

    p = sub.add_parser("create-task")
    p.add_argument("--task-id")
    p.add_argument("--title", required=True)
    p.add_argument("--goal", required=True)
    p.add_argument("--priority", default="medium")
    p.add_argument("--owner", default="ceo-session")
    p.add_argument("--acceptance", nargs="*")
    p.set_defaults(func=create_task)

    p = sub.add_parser("update-task-status")
    p.add_argument("task_id")
    p.add_argument("status")
    p.add_argument("--actor", default="ceo-session")
    p.set_defaults(func=update_task_status)

    p = sub.add_parser("create-node")
    p.add_argument("task_id")
    p.add_argument("--node-id")
    p.add_argument("--kind", default="execute")
    p.add_argument("--title", required=True)
    p.add_argument("--role", required=True)
    p.add_argument("--status", default="queued")
    p.add_argument("--depends-on", nargs="*")
    p.add_argument("--instructions")
    p.add_argument("--acceptance", nargs="*")
    p.add_argument("--actor", default="dispatcher")
    p.set_defaults(func=create_node)

    p = sub.add_parser("update-node-status")
    p.add_argument("task_id")
    p.add_argument("node_id")
    p.add_argument("status")
    p.add_argument("--output-ref")
    p.add_argument("--actor", default="worker")
    p.set_defaults(func=update_node_status)

    p = sub.add_parser("create-review")
    p.add_argument("task_id")
    p.add_argument("node_id")
    p.add_argument("--review-id")
    p.add_argument("--reviewer-role", default="reviewer")
    p.add_argument("--stage", default="result_gate")
    p.add_argument("--decision", required=True, choices=["approve", "reject", "conditional_approve"])
    p.add_argument("--reasons", nargs="*")
    p.add_argument("--required-changes", nargs="*")
    p.add_argument("--notes")
    p.set_defaults(func=create_review)

    p = sub.add_parser("render-dispatch-payload")
    p.add_argument("task_id")
    p.add_argument("node_id")
    p.add_argument("--actor", default="ceo-session")
    p.set_defaults(func=render_dispatch_payload)

    p = sub.add_parser("bind-session")
    p.add_argument("task_id")
    p.add_argument("node_id")
    p.add_argument("session_key")
    p.add_argument("--runtime", default="subagent")
    p.add_argument("--session-mode", default="session")
    p.add_argument("--actor", default="ceo-session")
    p.set_defaults(func=bind_session)

    p = sub.add_parser("record-result")
    p.add_argument("task_id")
    p.add_argument("node_id")
    p.add_argument("--output-ref", action="append")
    p.add_argument("--input-ref", action="append")
    p.add_argument("--summary")
    p.add_argument("--actor", default="worker")
    p.set_defaults(func=record_result)

    p = sub.add_parser("mark-review-pending")
    p.add_argument("task_id")
    p.add_argument("node_id")
    p.add_argument("--stage", default="result_gate")
    p.add_argument("--note")
    p.add_argument("--actor", default="worker")
    p.set_defaults(func=mark_review_pending)

    p = sub.add_parser("skip-node")
    p.add_argument("task_id")
    p.add_argument("node_id")
    p.add_argument("--reason", required=True)
    p.add_argument("--actor", default="dispatcher")
    p.set_defaults(func=skip_node)

    p = sub.add_parser("task-summary")
    p.add_argument("task_id")
    p.set_defaults(func=task_summary)

    p = sub.add_parser("task-brief")
    p.add_argument("task_id")
    p.set_defaults(func=task_brief)

    p = sub.add_parser("task-events")
    p.add_argument("task_id")
    p.add_argument("--tail", type=int, default=10)
    p.add_argument("--key-only", action="store_true")
    p.set_defaults(func=task_events)

    p = sub.add_parser("task-agent-status")
    p.add_argument("task_id")
    p.add_argument("--sessions-file")
    p.add_argument("--stale-after-minutes", type=float, default=30)
    p.set_defaults(func=task_agent_status)

    p = sub.add_parser("task-report")
    p.add_argument("task_id")
    p.add_argument("--tail", type=int, default=5)
    p.add_argument("--with-agents", action="store_true")
    p.add_argument("--sessions-file")
    p.add_argument("--stale-after-minutes", type=float, default=30)
    p.set_defaults(func=task_report)

    p = sub.add_parser("show-task")
    p.add_argument("task_id")
    p.set_defaults(func=show_task)

    args = parser.parse_args()
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    args.func(args)


if __name__ == "__main__":
    main()
