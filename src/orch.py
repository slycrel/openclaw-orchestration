#!/usr/bin/env python3
"""Poe orchestration core utilities."""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

STATE_TODO = " "
STATE_DOING = "~"
STATE_DONE = "x"
STATE_BLOCKED = "!"
VALID_STATES = {STATE_TODO, STATE_DOING, STATE_DONE, STATE_BLOCKED}

ITEM_RE = re.compile(r"^(?P<indent>\s*)-\s*\[(?P<state>[ xX~!])\]\s*(?P<text>.+?)\s*$")


@dataclass
class NextItem:
    index: int
    state: str
    text: str
    line: str
    indent: int = 0


@dataclass
class ProjectStatus:
    slug: str
    priority: int
    todo: int
    doing: int
    blocked: int
    done: int
    next_item: Optional[NextItem]


def ws_root() -> Path:
    env_root = os.environ.get("OPENCLAW_WORKSPACE") or os.environ.get("WORKSPACE_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[3]


def orch_root() -> Path:
    return ws_root() / "prototypes" / "poe-orchestration"


def projects_root() -> Path:
    return orch_root() / "projects"


def project_dir(slug: str) -> Path:
    return projects_root() / slug


def next_path(slug: str) -> Path:
    return project_dir(slug) / "NEXT.md"


def decisions_path(slug: str) -> Path:
    return project_dir(slug) / "DECISIONS.md"


def risks_path(slug: str) -> Path:
    return project_dir(slug) / "RISKS.md"


def provenance_path(slug: str) -> Path:
    return project_dir(slug) / "PROVENANCE.md"


def priority_path(slug: str) -> Path:
    return project_dir(slug) / "PRIORITY"


def now_utc_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def list_projects() -> List[str]:
    root = projects_root()
    if not root.exists():
        return []
    slugs = []
    for p in root.iterdir():
        if p.is_dir() and next_path(p.name).exists():
            slugs.append(p.name)
    return sorted(slugs)


def project_priority(slug: str) -> int:
    p = priority_path(slug)
    if not p.exists():
        return 0
    raw = p.read_text(encoding="utf-8").strip()
    if not raw:
        return 0
    try:
        return int(raw)
    except ValueError:
        return 0


def parse_next(slug: str) -> Tuple[List[str], List[NextItem]]:
    p = next_path(slug)
    lines = p.read_text(encoding="utf-8").splitlines()
    items: List[NextItem] = []
    for i, line in enumerate(lines):
        m = ITEM_RE.match(line)
        if not m:
            continue
        state = m.group("state")
        if state == "X":
            state = STATE_DONE
        items.append(
            NextItem(
                index=i,
                state=state,
                text=m.group("text").strip(),
                line=line,
                indent=len(m.group("indent")),
            )
        )
    return lines, items


def write_next_lines(slug: str, lines: List[str]) -> None:
    p = next_path(slug)
    p.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def mark_item(slug: str, item_index: int, new_state: str) -> None:
    if new_state not in VALID_STATES:
        raise ValueError(f"invalid new state: {new_state}")
    lines, items = parse_next(slug)
    item = next((it for it in items if it.index == item_index), None)
    if item is None:
        raise ValueError(f"item_index {item_index} not found in NEXT.md for {slug}")
    lines[item.index] = re.sub(r"\[(.)\]", f"[{new_state}]", lines[item.index], count=1)
    write_next_lines(slug, lines)


def mark_first_todo_done(slug: str) -> Optional[NextItem]:
    item = select_next_item(slug)
    if not item:
        return None
    mark_item(slug, item.index, STATE_DONE)
    return item


def select_next_item(slug: str) -> Optional[NextItem]:
    _lines, items = parse_next(slug)
    for it in items:
        if it.state == STATE_TODO:
            return it
    return None


def item_counts(slug: str) -> dict:
    _lines, items = parse_next(slug)
    counts = {"todo": 0, "doing": 0, "blocked": 0, "done": 0}
    for item in items:
        if item.state == STATE_TODO:
            counts["todo"] += 1
        elif item.state == STATE_DOING:
            counts["doing"] += 1
        elif item.state == STATE_BLOCKED:
            counts["blocked"] += 1
        elif item.state == STATE_DONE:
            counts["done"] += 1
    return counts


def project_status(slug: str) -> ProjectStatus:
    counts = item_counts(slug)
    return ProjectStatus(
        slug=slug,
        priority=project_priority(slug),
        todo=counts["todo"],
        doing=counts["doing"],
        blocked=counts["blocked"],
        done=counts["done"],
        next_item=select_next_item(slug),
    )


def select_global_next() -> Optional[Tuple[str, NextItem]]:
    candidates: List[Tuple[int, float, str]] = []
    for slug in list_projects():
        p = next_path(slug)
        try:
            mtime = p.stat().st_mtime
        except FileNotFoundError:
            continue
        candidates.append((project_priority(slug), mtime, slug))

    for _priority, _mtime, slug in sorted(candidates, key=lambda row: (row[0], row[1]), reverse=True):
        it = select_next_item(slug)
        if it:
            return slug, it
    return None


def list_blocked_projects() -> List[ProjectStatus]:
    out: List[ProjectStatus] = []
    for slug in list_projects():
        status = project_status(slug)
        if status.blocked > 0:
            out.append(status)
    return sorted(out, key=lambda s: (s.priority, s.blocked, s.slug), reverse=True)


def append_decision(slug: str, lines: Iterable[str]) -> None:
    dp = decisions_path(slug)
    dp.parent.mkdir(parents=True, exist_ok=True)
    if not dp.exists():
        dp.write_text("# DECISIONS\n\n", encoding="utf-8")
    stamp = now_utc_iso()
    payload = ["", f"## {stamp}", *[f"- {ln}" for ln in lines]]
    with dp.open("a", encoding="utf-8") as f:
        f.write("\n".join(payload) + "\n")


def ensure_project(slug: str, mission: str, priority: int = 0) -> Path:
    pdir = project_dir(slug)
    pdir.mkdir(parents=True, exist_ok=True)
    if not next_path(slug).exists():
        next_path(slug).write_text(
            (
                f"# NEXT — {slug}\n\n"
                "Mission:\n\n"
                f"> {mission}\n\n"
                "## Checklist\n\n"
                "- [ ] Define success criteria\n"
                "- [ ] Create first-pass plan\n"
                "- [ ] Execute next leaf task\n"
            ),
            encoding="utf-8",
        )
    if not risks_path(slug).exists():
        risks_path(slug).write_text("# RISKS\n\n## Risks / Unknowns\n\n- (fill in)\n", encoding="utf-8")
    if not decisions_path(slug).exists():
        decisions_path(slug).write_text("# DECISIONS\n\n", encoding="utf-8")
        append_decision(slug, ["Project created.", f"Mission: {mission}"])
    if not provenance_path(slug).exists():
        provenance_path(slug).write_text("# PROVENANCE\n\n- (links to key artifacts, datasets, runs)\n", encoding="utf-8")
    priority_path(slug).write_text(f"{priority}\n", encoding="utf-8")
    return pdir


def status_report(project: Optional[str] = None) -> dict:
    slugs = [project] if project else list_projects()
    projects = [project_status(slug) for slug in slugs]
    return {
        "generated_at": now_utc_iso(),
        "projects": [
            {
                **asdict(p),
                "next_item": asdict(p.next_item) if p.next_item else None,
            }
            for p in projects
        ],
    }


def status_report_markdown(project: Optional[str] = None) -> str:
    report = status_report(project)
    lines = [f"# Orchestration Report ({report['generated_at']})", ""]
    for p in report["projects"]:
        lines.append(f"## {p['slug']} (priority={p['priority']})")
        lines.append(f"- todo: {p['todo']}")
        lines.append(f"- doing: {p['doing']}")
        lines.append(f"- blocked: {p['blocked']}")
        lines.append(f"- done: {p['done']}")
        nxt = p.get("next_item")
        lines.append(f"- next: {nxt['text'] if nxt else '(none)'}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def status_report_json(project: Optional[str] = None) -> str:
    return json.dumps(status_report(project), indent=2) + "\n"
