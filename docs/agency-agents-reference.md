# agency-agents (msitarzewski) — Persona Reference

Source: https://github.com/msitarzewski/agency-agents
Captured: 2026-03-06

## Why it’s relevant
The repo is a big roster of role-based agent profiles (Claude Code style) with:
- identity/voice
- workflows
- deliverables + success metrics

This is useful for `poe-orchestration` as a **persona library**: we can port the best ones into our `personas/` format and keep them local.

## Shortlist worth porting first (for OpenClaw)
These map cleanly to how we actually work here:

1) **Reality Checker** (testing/testing-reality-checker.md)
- evidence-based certification / quality gates
- pairs well with autonomy: blocks “done” unless artifacts prove it

2) **Studio Producer / Project Shepherd** (project-management/...)
- turns a mission into a plan + sequencing + checkpoints

3) **Agents Orchestrator** (specialized/agents-orchestrator.md)
- explicit multi-agent coordination patterns

4) **Tool Evaluator** (testing/testing-tool-evaluator.md)
- perfect for “should we adopt X library/tool?” decisions

## Proposed port approach
- Keep upstream as **reference**, not a dependency.
- For each adopted persona, create a local `prototypes/poe-orchestration/personas/<name>.md` that:
  - matches our output-contract style
  - includes guardrails (no unsafe autonomy)
  - references the upstream file in a Provenance section
