Viable long-term approach:

1.  Treat shared infra as parameterized by contract

- Every shared skill entry point should declare milestone_id explicitly.
- Shared paths/globs/error strings must use milestone_id; only tests/M{...} and
  milestones/M{...} content may be milestone-specific.

2.  Add a contamination guard

- Lightweight scanner over skills/, src/, shared core/, and tests/unit/.
- Flag hardcoded milestone tokens in shared infra: Path("milestones/M11"),
  glob("M11S\*.md"), read_milestone_file("M11"), discover_specifications("M11"),
  etc.
- Allowlist legitimately milestone-specific paths.

3.  Add an automatic remediation path

- Scripted rewrite for the known bad patterns back to parameterized form.
- Agent can run it pre-commit or before milestone closure.
- If contamination is detected, fail fast with a machine-fixable report.

4.  Make it part of the SDD workflow

- Run the guard after skill generation/implementation and again at close-milestone.
- If it fails, block closure and offer the auto-fix path.

If you want, I can implement this as:

- tools/guardrails/milestone_contamination_guard.py
- tools/guardrails/fix_milestone_contamination.py
- and a single workflow hook from manage-development / close-milestone.
