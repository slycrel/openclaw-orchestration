#!/usr/bin/env bash
set -euo pipefail

# Marks the first numbered checklist item in NEXT.md as done by converting:
#   1. foo
# into:
#   - [x] foo
# This is intentionally dumb-but-safe.

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <project-slug>" >&2
  exit 1
fi

SLUG="$1"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NEXT="$ROOT_DIR/projects/$SLUG/NEXT.md"

if [[ ! -f "$NEXT" ]]; then
  echo "error: missing $NEXT" >&2
  exit 1
fi

python3 - "$NEXT" <<'PY'
from __future__ import annotations

import re
import sys
from pathlib import Path

p = Path(sys.argv[1])
lines = p.read_text().splitlines()
out = []
done = False
pat = re.compile(r"^(\s*)\d+\.\s+(.*)$")
for line in lines:
    if (not done) and pat.match(line):
        m = pat.match(line)
        out.append(f"- [x] {m.group(2)}")
        done = True
    else:
        out.append(line)

p.write_text("\n".join(out) + "\n")
print("updated=1" if done else "updated=0")
PY
