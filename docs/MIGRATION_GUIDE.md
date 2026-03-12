# Migration guide: ad-hoc notes → canonical artifacts

1. Create project folder with `scripts/new_project.sh <slug> "<mission>"`.
2. Move existing task bullets into `projects/<slug>/NEXT.md` using checklist syntax (`- [ ]`).
3. Add top risks in `RISKS.md` and evidence links in `PROVENANCE.md`.
4. Record first normalization decision in `DECISIONS.md`.
5. Set optional urgency in `PRIORITY` (integer, higher = sooner).
6. Use `python3 src/cli.py next` and `done` as the default loop.
