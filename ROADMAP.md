# Roadmap (Post-M4)

The original M0-M4 plan is complete in this branch. Next phase focuses on scale and operator UX.

## N1 — Execution adapters & policy enforcement
- queue adapter plugin loading (local/file/redis)
- optional policy hooks before `done` transitions
- provenance lint checks in CI

## N2 — Multi-project scheduling intelligence
- weighted fair scheduling across priorities
- blocked-age escalation and SLA alerts
- scheduling simulation test corpus

## N3 — Collaboration and review workflows
- project-level ownership metadata
- review-required decision gates
- signed decision/provenance snapshots

## N4 — Distribution hardening (`v1.0.0` target)
- packaged CLI entrypoint (`pipx install`)
- reproducible release artifacts + checksums
- formal threat model review and security test suite

## Research anchors used
- Existing local references: `docs/system-design-fundamentals-reference.md`, `docs/agency-agents-reference.md`
- Engineering practice references: pytest docs, GitHub Actions workflow docs, shellcheck best practices
