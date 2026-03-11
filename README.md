# Poe Orchestration (Prototype v0)

Poe Orchestration is a file-first workflow for turning a mission into repeatable execution:

**mission → plan → execute → checkpoint**

It is designed for chat-driven operation with durable artifacts on disk, minimal interruption, and clear decision gates.

## Scope and status

This repository is an early public prototype. It standardizes project structure and core helpers for task selection and checklist progression.

- **Current maturity:** v0 (prototype)
- **Primary interface:** Markdown artifacts + helper scripts
- **Not yet included:** full autonomous runner, production-grade scheduling, policy enforcement layer

## Prerequisites

- Linux or macOS shell environment
- Bash 4+
- Python 3.10+
- Git
- Optional: a queue runner compatible with `scripts/task-queue.sh` in your workspace

## Repository layout

```text
poe-orchestration/
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

### Project artifact contract

Each project lives under `projects/<slug>/` and should contain:

- `NEXT.md` — active checklist and near-term plan
- `RISKS.md` — risks, assumptions, unknowns
- `DECISIONS.md` — timestamped decision log
- `PROVENANCE.md` — references to evidence/artifacts

These files are the operational source of truth.

## Setup

From the repository root:

```bash
cd prototypes/poe-orchestration
chmod +x scripts/*.sh
python3 -m venv .venv
source .venv/bin/activate
```

No external package installation is required for the current helper scripts.

## Quickstart

1. **Create a project**

   ```bash
   scripts/new_project.sh "demo-project" "Define and ship a demo orchestration flow"
   ```

2. **Add work to queue**

   ```bash
   scripts/enqueue.sh "demo-project" "Draft implementation plan"
   ```

3. **Mark first numbered NEXT item complete**

   ```bash
   scripts/mark_next_done.sh "demo-project"
   ```

4. **Inspect/checkpoint artifacts**

   - `projects/demo-project/NEXT.md`
   - `projects/demo-project/DECISIONS.md`

## Architecture overview

Core behavior is implemented in `src/orch.py`:

- Parses `NEXT.md` checklist entries with strict state markers (`[ ]`, `[~]`, `[x]`, `[!]`)
- Selects next actionable item per project, or globally across projects
- Appends timestamped decision entries to `DECISIONS.md`
- Ensures project bootstrap files exist

Design choices:

- **File-first state:** plain Markdown remains inspectable and editable
- **Deterministic selection:** explicit parsing rules reduce ambiguity
- **Checkpoint logging:** decisions are append-only and timestamped

## Commands reference

- `scripts/new_project.sh <slug> <mission...>`
  - Bootstraps project folder and canonical docs.
- `scripts/enqueue.sh <slug> <task...>`
  - Sends project-scoped task payload to shared task queue.
- `scripts/mark_next_done.sh <slug>`
  - Converts first numbered item in `NEXT.md` to `- [x] ...`.

## Testing and validation

Current repo-level validation is lightweight:

- Shell scripts can be smoke-tested by running `--help`/usage paths and a demo project bootstrap.
- Python behavior can be verified with a short REPL or script invoking `src/orch.py` functions.
- Markdown quality should pass heading consistency, link validity, and basic lint checks.

Suggested next step for contributors: add automated tests for parser edge cases in `src/orch.py`.

## Operations and runbook links

- Conventions: [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md)
- Research artifact template: [`docs/research-brief-template.md`](docs/research-brief-template.md)
- Persona catalog: [`personas/README.md`](personas/README.md)

For publish readiness, use: [`docs/PUBLISH_CHECKLIST.md`](docs/PUBLISH_CHECKLIST.md)

## Security and privacy notes

- Do not commit secrets, credentials, private tokens, or personal chat exports.
- Keep environment-specific paths and hostnames out of public docs.
- Treat project artifacts as potentially sensitive until reviewed.
- If queue backends or external services are used, require least-privilege credentials.

## Limitations

- Prototype quality; interfaces may change without backward compatibility.
- No built-in auth, ACLs, or tenancy boundaries.
- Assumes disciplined artifact updates by operator/automation.
- Queue integration depends on an external workspace script.

## Troubleshooting

- **`task-queue.sh not found/executable`**
  - Ensure your workspace provides an executable queue script, or adapt `scripts/enqueue.sh`.
- **Project files missing**
  - Re-run `scripts/new_project.sh` for the same slug; it creates missing canonical docs.
- **Checklist item not detected**
  - Use supported checklist syntax (`- [ ] task` or numbered list for `mark_next_done.sh`).
- **Permission errors on scripts**
  - Run `chmod +x scripts/*.sh`.

## Release and versioning

Current release: **v0-systemic-2026-03-10**

Versioning guidance:

- Use date-stamped tags for major checkpoints in prototype phase.
- Document notable behavior changes in this section.
- Promote to semver (`v1.0.0+`) once interfaces stabilize.

Rollback example:

```bash
git checkout v0-systemic-2026-03-10
```
