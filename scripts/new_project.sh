#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <slug> <mission text...>" >&2
  exit 1
fi

SLUG="$1"
shift
MISSION="$*"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJ_DIR="$ROOT_DIR/projects/$SLUG"

mkdir -p "$PROJ_DIR"

stamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

if [[ ! -f "$PROJ_DIR/NEXT.md" ]]; then
  cat >"$PROJ_DIR/NEXT.md" <<EOF
# NEXT — $SLUG

Mission:

> $MISSION

## Checklist

1. Clarify objective + constraints (define success).
2. Build first-pass plan (phases + deliverables).
3. Execute next leaf task.

EOF
fi

if [[ ! -f "$PROJ_DIR/RISKS.md" ]]; then
  cat >"$PROJ_DIR/RISKS.md" <<'EOF'
# RISKS

## Risks / Unknowns

- (fill in)
EOF
fi

if [[ ! -f "$PROJ_DIR/DECISIONS.md" ]]; then
  cat >"$PROJ_DIR/DECISIONS.md" <<EOF
# DECISIONS

## $(stamp)
- Project created.
EOF
fi

if [[ ! -f "$PROJ_DIR/PROVENANCE.md" ]]; then
  cat >"$PROJ_DIR/PROVENANCE.md" <<'EOF'
# PROVENANCE

- (links to key artifacts, datasets, runs)
EOF
fi

echo "project_dir=$PROJ_DIR"
