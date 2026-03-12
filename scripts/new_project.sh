#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "ERROR[E_USAGE] usage: $0 <slug> <mission text...>" >&2
  exit 2
fi

SLUG="$1"
shift
MISSION="$*"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$ROOT_DIR/src/cli.py" init "$SLUG" "$MISSION"
