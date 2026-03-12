# End-to-end verification

Run in a clean environment:

```bash
cd prototypes/poe-orchestration
python3 -m pip install -U pytest
pytest
bash scripts/smoke.sh
```

Expected:
- tests pass
- smoke prints `smoke=ok`
