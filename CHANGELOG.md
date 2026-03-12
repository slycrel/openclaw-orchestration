# Changelog

## [0.4.0] - 2026-03-11

### Added
- `src/cli.py` with `init|next|done|log|blocked|report`
- priority file support (`projects/<slug>/PRIORITY`) and priority-aware global scheduling
- blocked-project triage and report generation helpers
- parser/unit tests and CLI integration tests (`tests/`)
- smoke harness (`scripts/smoke.sh`)
- CI workflow (`.github/workflows/ci.yml`)
- migration + queue adapter + compatibility + security + end-to-end docs

### Changed
- `scripts/new_project.sh` and `scripts/mark_next_done.sh` now route through CLI
- scripts and CLI now emit explicit error taxonomy codes for common failures

### Fixed
- roadmap M1-M4 items were converted from plan-only to executable implementation
