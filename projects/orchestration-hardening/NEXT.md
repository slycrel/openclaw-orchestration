# NEXT — orchestration-hardening

Mission:

> Replace arbitrary iteration gating with validation-driven autonomy. Detect loops, classify blockers, and escalate cleanly.

## Checklist

- [x] Add loop detection script (validator)
- [~] Extend validator to detect "no artifact progress" (runner stubs) vs "auth/rate limit" vs "task not advancing"
- [~] Add a standard "BLOCKED" mechanism in NEXT.md (e.g., `- [!]` or a BLOCKED section)
- [~] Update poe-orch-run.sh to mark tasks done when it actually produces required artifact
- [~] Add unit-ish tests for validator on synthetic logs

## Artifacts
- Persona: `prototypes/poe-orchestration/personas/loop-validator.md`
- Script: `scripts/poe-orch-validate.sh`
- Pump integration: `scripts/poe-orch-pump.sh`
