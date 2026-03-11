# Publish Checklist (Go / No-Go)

Use this checklist before publishing changes to this repository.

## 1) Scope and messaging

- [ ] README clearly states prototype status and supported scope.
- [ ] Public-facing language is concise and avoids internal-only assumptions.
- [ ] Feature claims match current implementation.

## 2) Documentation completeness

- [ ] README includes prerequisites, setup, quickstart, architecture, commands, testing, security/privacy, limitations, troubleshooting, and release/version notes.
- [ ] Runbook/conventions links resolve correctly.
- [ ] New docs are linked from README where appropriate.

## 3) Security and privacy review

- [ ] No secrets, tokens, credentials, or private hostnames/paths are committed.
- [ ] Examples use generic placeholders (no personal account data).
- [ ] Operational guidance follows least-privilege principles.

## 4) Functional sanity checks

- [ ] `scripts/new_project.sh` runs successfully on a test slug.
- [ ] `scripts/enqueue.sh` behavior is validated (or clearly documented if backend unavailable).
- [ ] `scripts/mark_next_done.sh` updates expected checklist content.
- [ ] Core Python module (`src/orch.py`) imports and basic helpers execute without error.

## 5) Markdown quality

- [ ] Headings are consistent and nested correctly.
- [ ] Code fences are closed and language-tagged where useful.
- [ ] No broken internal links.
- [ ] No obvious lint issues (trailing whitespace, malformed lists, duplicate top headings).

## 6) Release gate

- [ ] Release/version section in README is updated.
- [ ] Changelog notes (if any) align with commit/tag intent.
- [ ] Rollback instruction is present and valid.

## Decision

- **GO** if all critical boxes (security/privacy + functional sanity + release gate) are checked.
- **NO-GO** if any critical box fails; fix and re-run this checklist.
