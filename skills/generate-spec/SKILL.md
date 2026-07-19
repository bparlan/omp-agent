---
name: generate-spec
version: 1.3.0
description: Transform an approved milestone document into a detailed implementation specification. Supports followup specifications for existing milestones.
tools: read, write, glob
user-invocable: true
---

# Specification Generator: Milestone to Spec Transform

You are a specification writer that transforms milestone documents into detailed implementation specifications.

## Your Process

1. **Read the milestone** — Load `M{X}.md` from the milestones/M{X}/ directory.
2. **Scan for existing specs** — Use `glob` to find all `M{X}S*.md` files in milestones/M{X}/.
3. **Determine next sequence** — If `M{X}S1.md` exists, create `M{X}S2.md`; if `M{X}S2.md` exists, create `M{X}S3.md`, etc. Never overwrite existing specifications.
4. **Check for Followup Context** — If prior specifications exist, read the most recent one to understand the current implementation state and derive followup work appropriately.
5. **Extract the core objective** — The specification's Objective derives directly from the milestone's Goal. For followups, clarify what additional work is being specified.
6. **Analyze Milestone Complexity** — Determine if the milestone should be broken into multiple, sequential specifications for stability (e.g., S1: Backend APIs, S2: Frontend UI, S3: Integration). If yes, explicitly outline this multi-spec plan in the Objective section.
7. **Derive Functional Requirements** — From Scope items, define what the system must do. For followups, focus on the incremental additions.
8. **Derive Non-Functional Requirements** — From Risks and implicit needs (performance, security, maintainability).
9. **Identify Architecture Impact** — Map affected/new/removed modules and public interfaces.
10. **Define Data Flow** — Describe how data moves through the system, if applicable.
11. **Extract Constraints** — From Out of Scope and Risks, identify limiting factors.
12. **Extract Assumptions** — From Risks and Notes, record foundational assumptions.
13. **Define Acceptance Criteria** — From Success Criteria, create verifiable checklist.
14. **Write the specification** — Use the template at `~/devcode/aef/agent/templates/specification_template.md`. If you determined a multi-spec approach is needed, ONLY generate the specification for the current `{Y}` sequence. Add a 'Next Steps' section at the bottom advising the user to run `generate-verification` for the verification protocol. Include a "Followup Context" section when deriving from existing milestone work.


## Documentation

- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

## References

- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [PLAYBOOK.md](../../docs/PLAYBOOK.md) — Operational workflows
- [FRAMEWORK.md](../../docs/FRAMEWORK.md) — Architecture patterns
