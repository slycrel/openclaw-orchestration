#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "ERROR[E_USAGE] usage: $0 <project-slug> <task text...>" >&2
  exit 2
fi

SLUG="$1"
shift
TASK="$*"

WS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
QUEUE="$WS_ROOT/scripts/task-queue.sh"

if [[ ! -x "$QUEUE" ]]; then
  echo "ERROR[E_QUEUE_UNAVAILABLE] task queue script not found/executable: $QUEUE" >&2
  exit 3
fi

"$QUEUE" enqueue project_task "project=$SLUG :: $TASK"
