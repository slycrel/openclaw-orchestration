# Security model

Trust boundaries:
- Local filesystem in `projects/` is source of truth.
- Queue execution is external and untrusted by default.

Controls:
- No secrets stored in project artifacts by default.
- Scripts emit explicit error codes; no hidden retries.
- All state changes are plain-text and reviewable in git.

Operator guidance:
- Keep `.env` out of VCS.
- Review `DECISIONS.md` / `PROVENANCE.md` before sharing.
- Run CI before pushing changes.
