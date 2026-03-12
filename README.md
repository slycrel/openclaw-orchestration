# openclaw-orchestration

File-first orchestration with a stable CLI and auditable Markdown artifacts.

## What shipped overnight

- `orch` CLI (`init`, `next`, `done`, `log`, `blocked`, `report`)
- priority-aware global selection (`projects/<slug>/PRIORITY`)
- blocked-project triage view + report generation (Markdown/JSON)
- parser hardening + unit tests for edge states/malformed lines/nested checklists
- smoke harness (`scripts/smoke.sh`)
- CI workflow (shellcheck + pytest + smoke)
- migration/compat/security docs

## Quickstart

```bash
cd prototypes/poe-orchestration
python3 src/cli.py init demo "Ship demo flow" --priority 3
python3 src/cli.py next
python3 src/cli.py done demo
python3 src/cli.py report --project demo
```

## Verify

```bash
cd prototypes/poe-orchestration
pytest
bash scripts/smoke.sh
```

## Docs

- `docs/MIGRATION_GUIDE.md`
- `docs/QUEUE_ADAPTER.md`
- `docs/BACKWARD_COMPATIBILITY.md`
- `docs/SECURITY_MODEL.md`
- `docs/END_TO_END.md`

## Versioning

CLI and artifact contract now follow semantic versioning policy in `docs/BACKWARD_COMPATIBILITY.md`.
