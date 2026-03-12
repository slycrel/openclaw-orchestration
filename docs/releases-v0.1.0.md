# openclaw-orchestration v0.1.0

Initial stable baseline for file-first orchestration.

## Why this release matters

This release gives you a practical orchestration loop that survives model/runtime churn by keeping state and decisions on disk.

## Included

- File-first project scaffolding (`NEXT.md`, `DECISIONS.md`, and companion docs)
- Deterministic next-task selection utilities in `src/orch.py`
- Helper scripts for common flow:
  - `scripts/new_project.sh`
  - `scripts/mark_next_done.sh`
  - `scripts/enqueue.sh`
- Publish-ready documentation:
  - `README.md`
  - `ROADMAP.md`
  - `MAINLINE_PLAN.md`
  - `CONTRIBUTING.md`
- Community repo hygiene:
  - issue templates
  - PR template
  - CODEOWNERS

## Current boundaries

- Single-user local workflow first
- No CI pipeline yet
- Queue integration depends on compatible external queue runner

## Next focus (post-v0.1.0)

- CI smoke checks
- Unified runner/CLI
- Better portability presets and sample adapters
