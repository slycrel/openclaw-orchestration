#!/usr/bin/env python3
"""Poe Orchestration core utilities.

Goal: turn "missions" into durable project state and support a loop-until-blocked
executor without relying on arbitrary iteration limits.

Markdown conventions (project-local):
- NEXT.md contains checklist items in the form:
  - [ ] task
  - [~] in progress
  - [x] done
  - [!] blocked

We intentionally keep parsing rules strict and explicit.
"""

from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple


STATE_TODO = " "
STATE_DOING = "~"
STATE_DONE = "x"
STATE_BLOCKED = "!"

ITEM_RE = re.compile(r"^(?P<indent>\s*)-\s*\[(?P<state>[ xX~!])\]\s*(?P<text>.+?)\s*$")


@dataclass
class NextItem:
    index: int
    state: str
    text: str
    line: str


def ws_root() -> Path:
    return Path("/home/clawd/.openclaw/workspace")


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


def now_utc_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def list_projects() -> List[str]:
    root = projects_root()
    if not root.exists():
        return []
    slugs = []
    for p in root.iterdir():
        if p.is_dir() and (p / "NEXT.md").exists():
            slugs.append(p.name)
    return sorted(slugs)


def parse_next(slug: str) -> Tuple[List[str], List[NextItem]]:
    p = next_path(slug)
    lines = p.read_text(encoding="utf-8").splitlines()
    items: List[NextItem] = []
    for i, line in enumerate(lines):
        m = ITEM_RE.match(line)
        if not m:
            continue
        state = m.group("state")
        if state in ("X",):
            state = "x"
        text = m.group("text").strip()
        items.append(NextItem(index=i, state=state, text=text, line=line))
    return lines, items


def write_next_lines(slug: str, lines: List[str]) -> None:
    p = next_path(slug)
    p.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def mark_item(slug: str, item_index: int, new_state: str) -> None:
    lines, items = parse_next(slug)
    item = next((it for it in items if it.index == item_index), None)
    if item is None:
        raise ValueError(f"item_index {item_index} not found in NEXT.md for {slug}")
    # Replace only the state token.
    lines[item.index] = re.sub(r"\[(.)\]", f"[{new_state}]", lines[item.index], count=1)
    write_next_lines(slug, lines)


def select_next_item(slug: str) -> Optional[NextItem]:
    _lines, items = parse_next(slug)
    for it in items:
        if it.state == STATE_TODO:
            return it
    return None


def select_global_next() -> Optional[Tuple[str, NextItem]]:
    # Newest-modified project wins.
    candidates: List[Tuple[float, str]] = []
    for slug in list_projects():
        p = next_path(slug)
        try:
            mtime = p.stat().st_mtime
        except FileNotFoundError:
            continue
        candidates.append((mtime, slug))
    for _mtime, slug in sorted(candidates, reverse=True):
        it = select_next_item(slug)
        if it:
            return slug, it
    return None


def append_decision(slug: str, lines: List[str]) -> None:
    dp = decisions_path(slug)
    dp.parent.mkdir(parents=True, exist_ok=True)
    if not dp.exists():
        dp.write_text("# DECISIONS\n\n", encoding="utf-8")
    stamp = now_utc_iso()
    payload = ["", f"## {stamp}", *[f"- {ln}" for ln in lines]]
    with dp.open("a", encoding="utf-8") as f:
        f.write("\n".join(payload) + "\n")


def ensure_project(slug: str, mission: str) -> Path:
    # Use existing new_project.sh for now; but ensure folder exists.
    pdir = project_dir(slug)
    pdir.mkdir(parents=True, exist_ok=True)
    if not next_path(slug).exists():
        # minimal NEXT
        next_path(slug).write_text(
            f"# NEXT — {slug}\n\nMission:\n\n> {mission}\n\n## Checklist\n\n- [ ] Define success criteria\n- [ ] Create first-pass plan\n- [ ] Execute next leaf task\n\n",
            encoding="utf-8",
        )
    if not decisions_path(slug).exists():
        decisions_path(slug).write_text("# DECISIONS\n\n", encoding="utf-8")
        append_decision(slug, ["Project created.", f"Mission: {mission}"])
    return pdir
