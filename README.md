# openclaw-orchestration

File-first orchestration for turning a mission into shippable work with durable artifacts:

**mission → plan → execute → checkpoint**

This repo is intentionally simple: Markdown is the source of truth, scripts are thin helpers, and state stays inspectable.

## Why this exists

Most orchestration prototypes die in chat history. This one keeps the loop on disk so work survives model/runtime changes.

You get:
- predictable project structure (`NEXT`, `RISKS`, `DECISIONS`, `PROVENANCE`)
- deterministic task selection (`src/orch.py`)
- lightweight shell tooling for bootstrapping and progression
- portable docs/personas that do not depend on private infrastructure

## Status

- **Maturity:** pre-1.0, stable baseline candidate
- **Recommended baseline tag:** `v0.1.0`
- **Current scope:** single-user, local artifact-driven orchestration

See [`MAINLINE_PLAN.md`](MAINLINE_PLAN.md) for the path to default/mainline usage.

## Repository layout

```text
openclaw-orchestration/
├── docs/
├── personas/
├── projects/
├── scripts/
│   ├── new_project.sh
│   ├── enqueue.sh
│   └── mark_next_done.sh
└── src/
    └── orch.py
```

## Prerequisites

- Linux or macOS
- Bash 4+
- Python 3.10+
- Git
- Optional: queue runner compatible with `scripts/task-queue.sh` (for `enqueue.sh`)

## Quickstart

```bash
# from this repo root
chmod +x scripts/*.sh

# 1) create a project
scripts/new_project.sh demo "Define and ship a demo orchestration flow"

# 2) inspect next task (python helper)
python3 - <<'PY'
from src.orch import select_next_item
print(select_next_item("demo"))
PY

# 3) mark first numbered task as done
scripts/mark_next_done.sh demo
```

Optional queue submission:

```bash
scripts/enqueue.sh demo "Draft implementation plan"
```

> `enqueue.sh` expects a workspace-level `scripts/task-queue.sh`. If unavailable, you can still run fully file-first without queueing.

## Architecture (current)

### Data model

Each project lives in `projects/<slug>/`:
- `NEXT.md` — active checklist (supports `- [ ]`, `- [~]`, `- [x]`, `- [!]`)
- `RISKS.md` — known unknowns and watch items
- `DECISIONS.md` — append-only decision log
- `PROVENANCE.md` — source links/evidence pointers

### Runtime helpers

`src/orch.py` provides:
- parsing of checklist state with strict patterns
- selection of next actionable item per project or globally
- decision appends with UTC timestamps
- project bootstrapping fallback (`ensure_project`)

### Design constraints

- human-readable artifacts over hidden state
- deterministic behavior over opaque autonomy
- safe defaults over magical automation

## Usage examples

### Pick next work item across all projects

```bash
python3 - <<'PY'
from src.orch import select_global_next
print(select_global_next())
PY
```

### Log a decision

```bash
python3 - <<'PY'
from src.orch import append_decision
append_decision("demo", ["Completed bootstrap.", "Next: add parser tests."])
PY
```

## Limitations

- no scheduler/daemon included yet
- no multi-user permissions model
- queue integration is adapter-based, not bundled
- interface may evolve before `v1.0.0`

## Documentation index

- Conventions: [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md)
- Publish gate: [`docs/PUBLISH_CHECKLIST.md`](docs/PUBLISH_CHECKLIST.md)
- Research brief template: [`docs/research-brief-template.md`](docs/research-brief-template.md)
- Persona catalog: [`personas/README.md`](personas/README.md)
- Roadmap: [`ROADMAP.md`](ROADMAP.md)
- Contribution guide: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Changelog: [`CHANGELOG.md`](CHANGELOG.md)

## Related research references

Context docs included in this repo:
- [`docs/agency-agents-reference.md`](docs/agency-agents-reference.md)
- [`docs/system-design-fundamentals-reference.md`](docs/system-design-fundamentals-reference.md)

These are references, not runtime dependencies.

## Security and privacy

- never commit `.env`, secrets, tokens, or private exports
- keep examples generic and portable
- treat project artifacts as sensitive until reviewed for publication

## Release notes (baseline)

### Candidate: `v0.1.0`

- establishes canonical project artifact contract
- ships minimal orchestration core (`src/orch.py`)
- includes helper scripts for project lifecycle
- adds roadmap + mainline migration docs + community templates

Tagging instructions live in [`MAINLINE_PLAN.md`](MAINLINE_PLAN.md).

## License

MIT (add `LICENSE` if missing in your target repo root).
