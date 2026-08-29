## EXPERIENCES

- generate-tests/SKILL.md - Output Path Correction: Updated lines 18 and 28 to reflect
  the correct output path for test artifacts as milestones/M{X}/M{X}S{Y}T{Z}.md.
- implement-specification/SKILL.md - Process & Output Correction: Modified line 33 to
  advise evaluate-implementation as the next step and corrected lines 92-93 to specify
  the completion report path as M{X}S{Y}C.md in milestones/M{X}/.
- milestone/SKILL.md - Skill Clarification: Updated lines 26-29 and 90-95 to clarify
  the preservation of existing documents, data evaluation, and the process of generating
  milestone documents from templates.
- evolve-skills/SKILL.md - Documentation Enhancement: Integrated "Edit Tool Usage"
  instructions for consistent guidance on code editing practices.
- sync-documentation/SKILL.md - Documentation Enhancement: Integrated "Edit Tool
  Usage" instructions for consistent guidance on code editing practices.
- hotfix-issue/SKILL.md - Documentation Enhancement: Integrated "Edit Tool Usage"
  instructions for consistent guidance on code editing practices.
- evaluate-implementation/SKILL.md - Documentation Enhancement: Integrated "Edit Tool
  Usage" instructions for consistent guidance on code editing practices.
- bootstrap-project/SKILL.md - Documentation Enhancement: Integrated "Edit Tool Usage"
  instructions for consistent guidance on code editing practices.
- manage-roadmap/SKILL.md - Documentation Enhancement: Integrated "Edit Tool Usage"
  instructions for consistent guidance on code editing practices.
- manage-development/SKILL.md - Agentic Behavior Enhancement: Modified lines 22 and 25
  to make the skill fully agentic by automating skill invocation and updating the "Out
  of Scope" section to reflect autonomous execution.
- generate-tests/SKILL.md - Template and Artifact Clarification: Added details on
  template usage (referencing ~/devcode/aef/agent/templates/test_template.md) and clarified
  artifact reporting.
- ~/devcode/aef/agent/templates/test_template.md - Template Creation: Created the
  test_template.md file with a Python pytest structure for standardized test script
  generation.
- Template Version Stamping - Failed Task: Repeated attempts were made to add
  template_version: 1.0.0 to template files using sed, but these failed due to
  persistent newline escaping issues in bash. The process was halted due to a
  tool_call_loop_detected error. No successful edits were made for this specific task.
- evolve-skills/SKILL.md - Health Audit Layer: Successfully implemented automated health monitoring for evolve-skills dependencies, discovering and fixing critical issues in 5 skills (missing edit tool in frontmatter).

- `bin/_frontmatter.py` - BOM Handling: M7.md (and potentially other files) has a UTF-8 BOM prefix (`\ufeff`) that prevented `extract_frontmatter()` from matching the `^---` regex. Fixed by adding BOM stripping before regex matching. Discovered during M7S3 review-implementation phase.

- AEF — Skills-as-Tools Re-evaluation (User Note 2026-08-27): The AGENTS.md
  classification that skills are "NOT programmatic tools" is too rigid. Skills
  like `session-audit` and `close-milestone` produce structured artifacts with
  high data value — their output feeds back into `evolve-skills` for continuous
  framework improvement. Proposal: treat certain skills (session-audit,
  close-milestone, archive-docs, sync-documentation) as "agent-invocable tools"
  in addition to human-invoked commands, allowing the framework to autonomously
  capture lessons, close milestones, and evolve itself. Further exploration
  needed — not yet assigned to a milestone.

- M11 — AEF Orchestration Concurrency Controls (Proposed 2026-08-27):
  Problem: manage-development and manage-roadmap fail when subagent count
  exceeds capacity. User suspects a "max 3 subagent" rule would resolve
  cascading failures.
  Scope: Hard subagent limits in manage-development and manage-roadmap;
  skill-invocation boundaries; backpressure/routing when limit is hit.
  Extends M10's safe-to-proceed philosophy to the execution engine.
  Status: Not yet started — user will initiate after M9 context.
- YAML `&` Anchor Operator: `milestones/M7/M7S3E.md` had `title: Evaluation Report for M7S3: Legacy Compatibility & Transition` — the `&` is a YAML anchor operator, causing `validate_metadata.py` to fail silently. Fixed by quoting the title string. Discovered during M7S3 evaluation phase.