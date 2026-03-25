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


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
    if task["status"] in {"new", "triaged", "planned", "plan_review", "plan_rejected"}:
        task["status"] = "dispatched"
        task["updated_at"] = now_iso()
        save_json(task_path, task)
    print(node_id)


def update_node_status(args):
    path = TASKS_DIR / args.task_id / "nodes" / (args.node_id + ".json")
    if not path.exists():
        raise SystemExit("Node not found: {}".format(args.node_id))
    node = load_json(path)
    old = node["status"]
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
    }
    append_event(args.task_id, args.node_id, event_map.get(args.status, "task_updated"), args.actor, {"from": old, "to": args.status})
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

    p = sub.add_parser("show-task")
    p.add_argument("task_id")
    p.set_defaults(func=show_task)

    args = parser.parse_args()
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    args.func(args)


if __name__ == "__main__":
    main()
