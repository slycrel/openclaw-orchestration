# Conventions (Poe Orchestration)

## Philosophy

- **One mission, one folder.**
- **One living checklist.** (`NEXT.md`)
- **Artifacts are truth.** If it didn’t get written down, it didn’t happen.
- **Interruptions are expensive.** Only ping the human when required.

## Canonical docs

## Persona registry

Reusable focused personas live at:
- `prototypes/poe-orchestration/personas/`

List/show:
- `scripts/poe-personas.sh list`
- `scripts/poe-personas.sh show <name>`

### `NEXT.md`
The single living checklist for the project.

Rules:
- Top items should be concrete and independently shippable.
- Prefer small steps with clear outputs (files, reports, PRs).

### `RISKS.md`
Known risks, unknowns, assumptions, and things to watch.

### `DECISIONS.md`
Timestamped decisions.

### `PROVENANCE.md` (optional)
Pointers to source artifacts/data used for conclusions.

## Autonomy contract (default authority = C)
Poe may:
- edit files
- run scripts
- refactor workflows
- add/adjust OpenClaw cron jobs

Poe must ask before:
- spending money / placing real trades
- handling credentials/auth in a way that increases exposure
- destructive deletion of data
- posting externally (X/email/etc)
- major scope shifts ("this is a different project")
