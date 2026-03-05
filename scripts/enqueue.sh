#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <project-slug> <task text...>" >&2
  exit 1
fi

SLUG="$1"
shift
TASK="$*"

WS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
QUEUE="$WS_ROOT/scripts/task-queue.sh"

if [[ ! -x "$QUEUE" ]]; then
  echo "error: task queue script not found/executable: $QUEUE" >&2
  exit 1
fi

# Encode as a simple payload: "project=<slug> task=<text>"
# (keep it human-readable; orchestration runner can parse later)
"$QUEUE" enqueue project_task "project=$SLUG :: $TASK"
