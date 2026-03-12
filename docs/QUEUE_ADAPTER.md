# Queue adapter interface

`enqueue.sh` emits payloads in this format:

- type: `project_task`
- payload: `project=<slug> :: <task text>`

Reference implementation: workspace-level `scripts/task-queue.sh`.

Adapter contract for alternative queues:

- command: `enqueue <type> <payload>`
- exit code 0 on success
- non-zero + stderr on failure
