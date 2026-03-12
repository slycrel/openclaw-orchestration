# Roadmap

This roadmap converts the former “v1 list” intent into phased, shippable milestones.

## Principles

- Ship thin vertical slices.
- Keep file-first compatibility as a non-negotiable.
- Avoid hidden state and irreversible automation.

## Milestones

## M0 — Baseline mainline (`v0.1.0`) ✅

- [x] Canonical artifact contract (`NEXT/RISKS/DECISIONS/PROVENANCE`)
- [x] Core parser + next-item selection (`src/orch.py`)
- [x] Bootstrap + enqueue + checklist progression scripts
- [x] Public-facing docs cleanup (README, CONTRIBUTING, changelog)
- [x] Mainline plan + release/tag instructions

## M1 — Reliability hardening (`v0.2.x`)

- [ ] Unit tests for parser edge-cases (`[ ] [~] [x] [!]`, malformed lines, nested lists)
- [ ] Smoke test script for scripts + Python helpers
- [ ] CI workflow (lint + tests + shellcheck)
- [ ] Clear error taxonomy in CLI/script outputs

## M2 — Default orchestration path (`v0.3.x`)

- [ ] Add a single entrypoint command (`orch next`, `orch done`, `orch log`)
- [ ] Optional local loop runner with explicit stop conditions
- [ ] Queue adapter interface docs + reference implementation
- [ ] Migration guide from ad-hoc project notes to canonical artifacts

## M3 — Multi-project operations (`v0.4.x`)

- [ ] Priority policy for global selection (mtime + explicit priority)
- [ ] Blocked-state triage views
- [ ] Decision/provenance report generation helpers

## M4 — v1 readiness (`v1.0.0`)

- [ ] Backward-compatibility policy documented
- [ ] Stable CLI surface with semantic versioning guarantees
- [ ] End-to-end examples validated in clean environment
- [ ] Security model documented (secrets, permissions, trust boundaries)

## Deferred / Nice-to-have

- Persona package registry + validation schema
- Web UI for artifact browsing
- Optional hosted queue backends

## Exit criteria for “mainline default”

The project can be treated as the default orchestration path when:
1. M1 is complete (tests + CI reliability), and
2. M2 entrypoint flow is available/documented, and
3. migration guidance is proven on at least two real projects.
