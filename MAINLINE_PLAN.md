# Mainline Plan

## Current baseline

Mainline now includes:
- deterministic orchestration core (`src/orch.py`)
- stable CLI (`src/cli.py`)
- tests, smoke harness, CI
- migration/compat/security docs

## Release steps (`v0.4.0`)

```bash
cd prototypes/poe-orchestration
pytest
bash scripts/smoke.sh
git add .
git commit -m "feat(poe-orchestration): complete M1-M4 roadmap"
git tag -a v0.4.0 -m "v0.4.0: complete M1-M4 implementation"
git push origin HEAD --follow-tags
```
