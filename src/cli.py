#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from orch import (
    append_decision,
    ensure_project,
    list_blocked_projects,
    mark_first_todo_done,
    mark_item,
    project_dir,
    select_global_next,
    select_next_item,
    status_report_json,
    status_report_markdown,
)


def fail(code: str, msg: str) -> int:
    print(f"ERROR[{code}] {msg}", file=sys.stderr)
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="orch", description="File-first orchestration CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Initialize a project")
    p_init.add_argument("slug")
    p_init.add_argument("mission", nargs="+")
    p_init.add_argument("--priority", type=int, default=0)

    p_next = sub.add_parser("next", help="Show next item")
    p_next.add_argument("--project")

    p_done = sub.add_parser("done", help="Mark task done")
    p_done.add_argument("project")
    p_done.add_argument("--index", type=int)

    p_log = sub.add_parser("log", help="Append decision log entry")
    p_log.add_argument("project")
    p_log.add_argument("message", nargs="+")

    p_blocked = sub.add_parser("blocked", help="List blocked projects")

    p_report = sub.add_parser("report", help="Generate summary report")
    p_report.add_argument("--project")
    p_report.add_argument("--format", choices=["md", "json"], default="md")
    p_report.add_argument("--out")

    args = parser.parse_args(argv)

    if args.cmd == "init":
        p = ensure_project(args.slug, " ".join(args.mission), priority=args.priority)
        print(f"initialized={p}")
        return 0

    if args.cmd == "next":
        if args.project:
            p = project_dir(args.project)
            if not p.exists():
                return fail("E_PROJECT_NOT_FOUND", args.project)
            item = select_next_item(args.project)
            if item:
                print(f"project={args.project} index={item.index} state=[{item.state}] text={item.text}")
                return 0
            print(f"project={args.project} next=(none)")
            return 1

        sel = select_global_next()
        if not sel:
            print("next=(none)")
            return 1
        slug, item = sel
        print(f"project={slug} index={item.index} state=[{item.state}] text={item.text}")
        return 0

    if args.cmd == "done":
        if not project_dir(args.project).exists():
            return fail("E_PROJECT_NOT_FOUND", args.project)
        if args.index is None:
            item = mark_first_todo_done(args.project)
            if not item:
                print(f"project={args.project} updated=0")
                return 1
            print(f"project={args.project} updated=1 index={item.index} text={item.text}")
            return 0
        mark_item(args.project, args.index, "x")
        print(f"project={args.project} updated=1 index={args.index}")
        return 0

    if args.cmd == "log":
        if not project_dir(args.project).exists():
            return fail("E_PROJECT_NOT_FOUND", args.project)
        append_decision(args.project, [" ".join(args.message)])
        print(f"project={args.project} logged=1")
        return 0

    if args.cmd == "blocked":
        blocked = list_blocked_projects()
        if not blocked:
            print("blocked=(none)")
            return 0
        for b in blocked:
            print(f"project={b.slug} priority={b.priority} blocked={b.blocked} todo={b.todo}")
        return 0

    if args.cmd == "report":
        content = status_report_markdown(args.project) if args.format == "md" else status_report_json(args.project)
        if args.out:
            out = Path(args.out)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(content, encoding="utf-8")
            print(f"written={out}")
        else:
            print(content, end="")
        return 0

    return fail("E_INTERNAL", "unknown command")


if __name__ == "__main__":
    raise SystemExit(main())
