# Mainline Plan

## What “mainline” means for this repo

For `openclaw-orchestration`, “mainline” means:
1. `main` is safe as the default branch for day-to-day usage.
2. There is a documented stable baseline tag (`v0.1.0`).
3. New work follows roadmap milestones instead of ad-hoc v1 bullet lists.

## Stable baseline definition (`v0.1.0`)

Scope included in baseline:
- file-first artifact contract
- `src/orch.py` next-item and decision helpers
- lifecycle scripts in `scripts/`
- public docs + contributor workflow + community templates

Out of scope for baseline:
- daemonized autonomous runner
- full policy enforcement layer
- multi-tenant auth/ACL model

## Release steps

1. Ensure clean working tree and passing smoke checks.
2. Commit docs + hygiene updates.
3. Create annotated tag:

```bash
git tag -a v0.1.0 -m "v0.1.0: stable baseline for file-first orchestration"
```

4. Push branch + tag:

```bash
git push origin main --follow-tags
```

## Default-path migration notes

If you are adopting this as your default orchestration path:

1. Create/normalize each active project into `projects/<slug>/` with the canonical files.
2. Move active tasks into `NEXT.md` checklist syntax.
3. Start decision logging in `DECISIONS.md` for every meaningful scope/architecture change.
4. Keep external evidence links in `PROVENANCE.md`.
5. Use roadmap milestones for planning instead of freeform “v1 someday” lists.

## Branch and contribution policy

- `main` remains deployable/usable.
- Feature work lands via PRs (even in solo mode when practical).
- Changelog updates required for user-facing behavior changes.

## Post-`v0.1.0` immediate follow-ups

- Implement parser tests (M1)
- Add CI for shell + Python checks (M1)
- Add thin CLI wrapper for core actions (M2)
