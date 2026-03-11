# Poe Orchestration (Prototype)

Purpose: a **mission → plan → execute → checkpoint** system for Poe (this assistant) to run *any* project with minimal human touch.

Design goals:
- **Chat-first, light-touch**: Jeremy gives a mission in Telegram; Poe executes.
- **Artifacts as ground truth**: everything important is written to disk.
- **Decision-gated pings**: only interrupt for real forks/risk boundaries.
- **Autonomy-friendly**: work happens in small, shippable steps.

## Project layout

Each project lives under:

`prototypes/poe-orchestration/projects/<slug>/`

Canonical living docs:
- `NEXT.md` — single living checklist (auto/hand-updated)
- `RISKS.md` — risks/unknowns/watchouts
- `DECISIONS.md` — important decisions + timestamps
- `PROVENANCE.md` — links to source artifacts (optional)

## Scripts

- `scripts/new_project.sh "<slug>" "<mission text>"`
  - Creates the project folder + canonical docs.

- `scripts/enqueue.sh "<slug>" "<task>"`
  - Adds a task to the global task queue (OpenClaw `scripts/task-queue.sh`).

## Current status

This prototype is intentionally minimal right now: it establishes the **workflow contract** and filesystem conventions first.

Next step: wire an autonomy loop that repeatedly pulls the next queued task and executes it to a checkpoint (or decision gate).

## Templates
- `docs/research-brief-template.md` — standard output shape for deep research runs.

---

## Release notes — v0 systemic checkpoint (2026-03-10)

Release tag: `v0-systemic-2026-03-10`

Highlights shipped in this checkpoint:
- Queue/runtime hardening for orchestrator v0 (stall prevention, safer degraded behavior).
- Iteration harness + deterministic NOW-lane fixture testing.
- Queue maintenance/archive path with audit-preserving behavior.
- Local Telegram history store (SQLite+FTS) with idempotent ingest, search, and artifact linking.
- Telegram sync automation + cadence wrapper + actionable status/alert artifacts.
- X ingestion unification on `twitter-cli` path with quote-tweet enrichment + compatibility wrappers.

Rollback:
```bash
git checkout v0-systemic-2026-03-10
```
