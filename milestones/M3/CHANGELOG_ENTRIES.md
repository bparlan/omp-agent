# Changelog Entries — M3SA1

## Added
- `docs/FRAMEWORK.md`: New "The Uncertainty Marker" architectural pattern with `#NEEDS-CLARIFICATION: <specific missing fact>` marker and HALT-on-guessing rule
- `AGENTS.md`: New "The Uncertainty Marker" subsection with standing directive
- `AGENTS.md`: New "Mechanical Tooling Stack" subsection with four-category tooling mandate
- `skills/implement-specification/SKILL.md`: Uncertainty Marker rule in "When uncertain" section
- `skills/review-implementation/SKILL.md`: Zero-trust review standing rule + Live State Verification in Analysis Rules
- `templates/review_template.md`: "## Live State Verification" mandatory section with claim/command/observed-state fields
- `skills/investigate-issue/SKILL.md`: Evidence-based debugging rule (title + Investigation Strategy)
- `skills/evaluate-implementation/SKILL.md`: Evidence-based debugging rule (title)
- `templates/completion_template.md`: "## Raw Evidence" section with exact command + raw output template
- `templates/evaluation_template.md`: "## Raw Evidence" section with exact command + raw output template
- `skills/bootstrap-project/SKILL.md`: New step 8 — "Define the Mechanical Tooling Stack" with 4 categories between steps 7 and 9-12
- `bin/ground-truth-check.sh`: New read-only POSIX shell utility (file-exists, dir-exists, command-exists, file-contains, git-status)

## Fixed
- `tests/M3/test_uncertainty_marker.sh`: Fixed grep pattern to match `- ###` heading format; fixed bash `end`/`fi` syntax error
- `tests/M3/test_ground_truth_helper.sh`: Fixed exit code capture (`|| true` consumed exit codes); removed stale `exitcode=$?` lines; fixed trap cleanup for empty TMPDIR
- `tests/M3/test_tooling_stack.sh`: Fixed grep patterns — replaced `\|` alternation with literal strings; simplified regex patterns

## Changed
- `skills/review-implementation/SKILL.md`: Updated template_version field (implicitly through new standing rules)
- `skills/evaluate-implementation/SKILL.md`: Updated template_version field (implicitly through new standing rules)
- `skills/investigate-issue/SKILL.md`: Updated template_version field (implicitly through new standing rules)
- `skills/bootstrap-project/SKILL.md`: Updated process steps (7→8→9→10→11→12)

## Removed
- None (all changes are additive)
