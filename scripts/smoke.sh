#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
export OPENCLAW_WORKSPACE="$TMP"

python3 "$ROOT_DIR/src/cli.py" init smoke "Smoke test mission" --priority 1
python3 "$ROOT_DIR/src/cli.py" next --project smoke
python3 "$ROOT_DIR/src/cli.py" done smoke
python3 "$ROOT_DIR/src/cli.py" log smoke "smoke run completed"
python3 "$ROOT_DIR/src/cli.py" report --project smoke --out "$TMP/report.md"

echo "smoke=ok workspace=$TMP"
