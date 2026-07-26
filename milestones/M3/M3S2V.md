# Verification M3S2V

| Property         | Value        |
| ---------------- | ------------ |
| Document Type    | Verification |
| Identifier       | M3S2V        |
| Derived From     | M3S2         |
| template_version | 1.1.0        |

## Success Criteria

- [ ] `docs/FRAMEWORK.md` contains a "The Uncertainty Marker" section defining `#NEEDS-CLARIFICATION: <specific missing fact>` with the HALT-on-guessing rule.
- [ ] `AGENTS.md` contains both the Uncertainty Marker rule and the Mechanical Tooling Stack mandate.
- [ ] `skills/implement-specification/SKILL.md` references `#NEEDS-CLARIFICATION` in its "When uncertain" section.
- [ ] `skills/review-implementation/SKILL.md` begins with "Assume the prior report is wrong until proven otherwise. Verify every claim against the live state."
- [ ] `templates/review_template.md` has a "Live State Verification" section with claim/command/observed-state template.
- [ ] `skills/investigate-issue/SKILL.md` begins with "Debug from evidence, never from memory. The first action on any unfamiliar error is to read the literal message and use the tool's --help or introspection command."
- [ ] `skills/evaluate-implementation/SKILL.md` begins with the same evidence-based debugging rule.
- [ ] `templates/completion_template.md` has a "## Raw Evidence" section with the evidence template.
- [ ] `templates/evaluation_template.md` has a "## Raw Evidence" section with the evidence template.
- [ ] `bin/ground-truth-check.sh` exists, is executable, and supports: `file-exists`, `git-status`, `command-exists`, `dir-exists`, `file-contains`. Running with `--help` or no args prints usage.
- [ ] `skills/bootstrap-project/SKILL.md` includes a step to define the four-category Mechanical Tooling Stack.
- [ ] No specific tooling brands are hardcoded — only categories (environment manager, linter/formatter, pre-commit framework, type checker).
- [ ] `bin/ground-truth-check.sh` contains zero write operations (no `>`, `>>`, `mv`, `cp`, `rm`, `mkdir`, `touch`, `chmod`, `chown`).

---

## Followup Reuse

### Derivation References

- M3S2 (specification)
- M3S1V (prior verification — orthogonal scope, Ladybug graph pipeline)
- M3S1R (review — identified critical gaps in M3S1, not applicable here)

### Reusable Items from M3S1V

- **Diff-Scope Verification pattern**: The `git diff --name-only` pre-merge check from M3S1V's Automated Validation is conceptually relevant to M3S2's ground-truth `git-status` command validation. The pattern of mechanically comparing diff output against an allowlist is reusable.
- **File existence check pattern**: M3S1V's `test -f` check pattern (`test -f <path> && echo "SUCCESS"`) is directly reusable for M3S2's ground-truth `file-exists` command.
- none — 100% of M3S1V's content is Ladybug-specific (CLI installation, graph schema, Cypher queries, parser correctness, pilot validation). These are orthogonal to M3S2's documentation + shell utility scope.

### New Verification Required

All verification items are specific to M3S2's six FRs: Uncertainty Marker (FR-1), Zero-Trust Review (FR-2), Evidence-Based Debugging (FR-3), Raw Evidence Mandate (FR-4), Ground-Truth Helper (FR-5), Mechanical Tooling Stack (FR-6).

---

## Functional Validation

### FR-1: Uncertainty Marker (`#NEEDS-CLARIFICATION`)

**Validation Method:** File content grep + structural read of three target files.

**Test Steps:**
1. Run `grep -n '#NEEDS-CLARIFICATION' docs/FRAMEWORK.md` — confirm the marker literal exists.
2. Read `docs/FRAMEWORK.md` and verify the "The Uncertainty Marker" section is present as a new section under Architectural Patterns (between Spec-Driven Development and Agent-Tool Separation).
3. Read the section content — confirm it defines: _"If an agent's confidence in a fact is below 'I could paste the command that proves this,' it MUST either run the command immediately to prove it, or emit `#NEEDS-CLARIFICATION: <specific missing fact>` and HALT."_
4. Run `grep -rn '#NEEDS-CLARIFICATION' AGENTS.md` — confirm the marker is present.
5. Read `skills/implement-specification/SKILL.md` — confirm the "When uncertain" section contains the `#NEEDS-CLARIFICATION` marker definition.

**Expected Output:**
- `grep` returns at least one match per target file.
- The architectural section is structurally placed between existing "Spec-Driven Development" and "Agent-Tool Separation" sections.
- The HALT-on-guessing rule is explicitly stated.

**Failure Criteria:**
- `grep` returns no matches in any target file.
- The marker appears quoted or wrapped (e.g., backtick-quoted as code) in a way that prevents literal `grep '#NEEDS-CLARIFICATION'` from matching.
- The HALT requirement is softened (e.g., "should" instead of "MUST").
- Guessing is not explicitly forbidden.

---

### FR-2: Zero-Trust Review Pass

**Validation Method:** File content read + structural verification of two target files.

**Test Steps:**
1. Read `skills/review-implementation/SKILL.md` lines 1-20 — confirm the file begins with the standing rule: _"Assume the prior report is wrong until proven otherwise. Verify every claim against the live state using bash or read commands."_
2. Verify the same rule is also present in the "Review Analysis Rules" section further in the document.
3. Read `templates/review_template.md` — confirm a "## Live State Verification" section exists, located after the "Specification Compliance" / compliance matrix section and before "Architecture Assessment".
4. Verify the Live State Verification section contains a template for: claim being verified, command used, actual state observed.

**Expected Output:**
- The standing rule is the first non-metadata content in the SKILL.md.
- The rule also exists in the analysis rules section.
- The review template has a structured Live State Verification section with claim/command/observed-state fields.

**Failure Criteria:**
- The rule appears anywhere other than the very beginning of the process (after YAML frontmatter and title).
- The rule is conditional (e.g., "If time permits, verify...").
- The review template lacks the Live State Verification section.
- The Live State Verification section contains only a heading with no structured template.

---

### FR-3: Evidence-Based Debugging Mandate

**Validation Method:** File content read of two target files.

**Test Steps:**
1. Read `skills/investigate-issue/SKILL.md` lines 1-20 — confirm the file begins with: _"Debug from evidence, never from memory. The first action on any unfamiliar error is to read the literal message and use the tool's --help or introspection command. Never pattern-match from similar tools."_
2. Verify the same rule is also present in the "Investigation Strategy" section.
3. Read `skills/evaluate-implementation/SKILL.md` lines 1-20 — confirm the file begins with the same evidence-based debugging rule.

**Expected Output:**
- Both SKILL.md files begin with the evidence-based debugging standing rule.
- The rule also appears in investigate-issue's Investigation Strategy section.

**Failure Criteria:**
- The rule is missing from either file's opening.
- The rule is placed after other content (not the first substantive text).
- The rule says "consider" or "prefer" instead of "never" for pattern-matching.
- The rule does not explicitly mention `--help` or introspection commands.

---

### FR-4: Raw Evidence Mandate

**Validation Method:** File content read of two target templates.

**Test Steps:**
1. Read `templates/completion_template.md` — confirm a "## Raw Evidence" section exists after the existing "## Technical Debt incurred" section.
2. Verify the section contains: _"Every 'done' claim must ship with the exact terminal command and raw output that proves it succeeded."_ followed by the bullet template: `- [ ] <requirement>: \`<command>\` → <raw output>`.
3. Repeat steps 1-2 for `templates/evaluation_template.md`.

**Expected Output:**
- Both templates have a "## Raw Evidence" section as the last substantive section.
- The section header and content match the specification.
- The bullet template is present with the exact format specified.

**Failure Criteria:**
- The section is missing from either template.
- The section appears before "Technical Debt incurred" in the completion template.
- The evidence requirement is generic (e.g., "attach evidence") without specifying "exact terminal command and raw output."
- The bullet template lacks the `command → raw output` structure.

---

### FR-5: Ground-Truth Helper Utility

**Validation Method:** File existence + script execution + content audit.

**Test Steps:**
1. Verify `bin/ground-truth-check.sh` exists: `test -f bin/ground-truth-check.sh && echo "EXISTS"`.
2. Verify it is executable: `test -x bin/ground-truth-check.sh && echo "EXECUTABLE"`.
3. Run `bin/ground-truth-check.sh --help` — confirm usage synopsis is printed.
4. Run `bin/ground-truth-check.sh` (no args) — confirm usage synopsis is printed (no crash).
5. Run `bin/ground-truth-check.sh file-exists bin/ground-truth-check.sh` — confirm output contains "PASS" and exit code is 0.
6. Run `bin/ground-truth-check.sh file-exists /nonexistent/path` — confirm output contains "FAIL" and exit code is 1.
7. Run `bin/ground-truth-check.sh dir-exists /tmp` — confirm "PASS" and exit code 0.
8. Run `bin/ground-truth-check.sh dir-exists /nonexistent` — confirm "FAIL" and exit code 1.
9. Run `bin/ground-truth-check.sh command-exists ls` — confirm "PASS" and exit code 0.
10. Run `bin/ground-truth-check.sh command-exists nonexistentxyz123` — confirm "FAIL" and exit code 1.
11. Run `bin/ground-truth-check.sh file-contains bin/ground-truth-check.sh "PASS"` — confirm "PASS" and exit code 0.
12. Run `bin/ground-truth-check.sh file-contains bin/ground-truth-check.sh "UNLIKELY_STRING_ZZZ"` — confirm "FAIL" and exit code 1.
13. Run `bin/ground-truth-check.sh git-status bin/` — confirm "PASS" or "FAIL" with exit code 0 (git status is purely informational; no git diff check required for pass/fail).
14. Read the script header — confirm it contains documentation for agent use.
15. Read the entire script — grep for write operations: `grep -n -- '>\||>>\|mv\|cp\|rm\|mkdir\|touch\|chmod\|chown' bin/ground-truth-check.sh`. Confirm zero matches.

**Expected Output:**
- All commands produce correct PASS/FAIL output.
- Exit codes: PASS → 0, FAIL → 1.
- `--help` and no-args both print usage without side effects.
- No write operations present in the script body.
- Header documents agent-facing usage patterns.

**Failure Criteria:**
- Script does not exist or is not executable.
- Any command crashes instead of producing PASS/FAIL output.
- Exit code is wrong for any command.
- `--help` or no-args produces a crash instead of usage.
- Any write operation (`>`, `>>`, `mv`, `cp`, `rm`, `mkdir`, `touch`, `chmod`, `chown`) appears outside comments.
- Script uses Python, Node.js, or any non-POSIX dependency.

---

### FR-6: Mechanical Tooling Stack Mandate

**Validation Method:** File content read of two target files.

**Test Steps:**
1. Read `skills/bootstrap-project/SKILL.md` — locate the "Your Process" numbered steps sequence (steps 1-11 currently).
2. Verify a step exists between "Create missing documents" (step 7) and "Create root-level entry points" (step 8) that defines the Mechanical Tooling Stack.
3. Read the step content — confirm it mandates the four categories: Environment Manager, Fast Linter/Formatter, Pre-commit Framework, Type Checker.
4. Read `AGENTS.md` — find the "Mechanical Tooling Stack" section under Core Concepts (after Agent Handoffs).
5. Verify the section describes the same four categories with the rule that every bootstrapped project must document its chosen stack.
6. Confirm no specific brand names appear (no `mise`, `ruff`, `pre-commit`, `mypy`, or similar).

**Expected Output:**
- Both files contain the Mechanical Tooling Stack mandate with all four categories.
- The bootstrap-project step is correctly positioned in the process sequence.
- No brand names are hardcoded.

**Failure Criteria:**
- The step is missing from bootstrap-project's process.
- The step appears before or replacing existing steps instead of being inserted between steps 7 and 8.
- Any of the four categories is missing.
- A specific brand name is used as a requirement (e.g., "must use mise") instead of the category.
- The AGENTS.md section is missing or incomplete.

---

## Edge Cases

- **Ground-truth script: empty argument** — Running `bin/ground-truth-check.sh file-exists` without a path argument. Script should print usage/error, not crash or hang.
- **Ground-truth script: invalid command** — Running `bin/ground-truth-check.sh nonexistent-cmd /tmp`. Script should print usage/error, not silently succeed.
- **Ground-truth script: special characters in pattern** — Running `file-contains <path> ".*"` (regex metacharacters). Script must treat the pattern as a literal string (as `grep -F` would), not interpret it as regex.
- **Ground-truth script: binary file** — Running `file-contains <path>` on a binary file. Script should not hang, corrupt output, or crash.
- **Ground-truth script: git-status in non-git directory** — Running `git-status /tmp` (no git repository). Script should output FAIL and exit code 1 gracefully.
- **Ground-truth script: path with spaces** — Running `file-exists "path/with spaces/file.txt"`. Script must handle quoted paths correctly.
- **Uncertainty marker marginalia** — All variants like `#NEEDS-CLARIFICATION:` (trailing colon without fact), `#NEEDS-CLARIFICATION` (no colon), `NEEDS-CLARIFICATION` (no hash) must NOT be considered valid markers. Only the full literal `#NEEDS-CLARIFICATION: <specific missing fact>` is valid.
- **Zero-trust review: no claims to verify** — When running review on a spec with zero implementable claims (unlikely edge). The reviewer must note "No claims to verify" rather than skipping the section.
- **Raw evidence: empty implementation** — When there are no "done" claims. The Raw Evidence section should contain "N/A" or equivalent, not be omitted entirely.
- **Evidence-based debugging: error with no --help** — The rule must still direct agents to `read` the error message literally. The `--help` invocation is a guide, not a universal requirement.
- **Mechanical tooling stack: single-language project** — The mandate must work for any language (Python, Node.js, Rust, etc.). Categories must remain language-agnostic.
- **Mechanical tooling stack: no package manager** — The "environment manager" category must be defined broadly enough to cover projects without a standard package manager (e.g., Go, Rust with rustup).

---

## Failure Scenarios

### Uncertainty Marker Violations

- **Scenario**: Agent continues generating output after emitting `#NEEDS-CLARIFICATION` instead of halting.
  - **Detection**: grep for `#NEEDS-CLARIFICATION` followed by additional agent output (not halt).
  - **Validation**: The FRAMEWORK.md and AGENTS.md definitions must use MUST-level language (RFC 2119) for the HALT requirement. Review reports must flag any continuation after marker emission as a critical violation.

- **Scenario**: Agent guesses instead of emitting the marker.
  - **Detection**: Implementation review identifies claims made without evidence.
  - **Validation**: The spec explicitly forbids guessing. Review reports must flag guessed claims.

### Zero-Trust Review Failures

- **Scenario**: Reviewer reads the completion report's self-assessment without independently verifying.
  - **Detection**: The Live State Verification section is empty or references "per completion report."
  - **Validation**: Review template requires listing specific verification commands run and their output. Empty or self-referential entries are a compliance failure.

- **Scenario**: Reviewer skips live-state verification due to time pressure.
  - **Detection**: Live State Verification section missing or contains placeholder text.
  - **Validation**: The SKILL.md's standing rule is mandatory (MUST-level). Missing verification is a critical finding in the review.

### Evidence-Based Debugging Failures

- **Scenario**: On an unfamiliar error, the agent attempts to pattern-match from memory instead of reading the error message.
  - **Detection**: Investigation report references "I've seen this before" or "this looks like" without first showing the error text.
  - **Validation**: The standing rule is at the top of the process. Any deviation is flagged in the review.

- **Scenario**: Error message is read but the agent jumps to conclusions without using `--help` or introspection.
  - **Detection**: Investigation report lacks evidence of `--help` or introspection command usage on first encounter with an unfamiliar tool.
  - **Validation**: Evaluate-implementation must flag missing evidence of command introspection.

### Raw Evidence Mandate Violations

- **Scenario**: Completion report claims "done" without providing the exact command and raw output.
  - **Detection**: The Raw Evidence section is missing, partially filled, or contains paraphrased results instead of raw output.
  - **Validation**: Review report must flag any completed requirement lacking raw evidence.

- **Scenario**: Evaluation report claims tests passed without providing the test command and its output.
  - **Detection**: Raw Evidence section references "tests passed" without the exact shell command and stdout/stderr.
  - **Validation**: Review report must flag any evaluation claim lacking raw evidence.

### Ground-Truth Script Failures

- **Scenario**: Script accidentally introduces a side effect (writes a temp file, modifies permissions, creates a directory).
  - **Detection**: Audit the script for any write operations (`>`, `>>`, `| tee`, `dd`, `install`).
  - **Validation**: The acceptance criteria audit confirms zero write operations. Any write operation is a critical failure.

- **Scenario**: Script crashes on malformed input (e.g., binary file, path with null bytes).
  - **Detection**: Test with edge case inputs.
  - **Validation**: All edge case tests produce PASS/FAIL output, never crash.

### Mechanical Tooling Stack Violations

- **Scenario**: bootstrap-project creates milestones and documentation but skips the tooling stack step.
  - **Detection**: The step between "Create missing documents" and "Create root-level entry points" is missing or empty.
  - **Validation**: Review of bootstrap-project's implementation notes the missing step.

- **Scenario**: A specific brand is hardcoded (e.g., "Use ruff for linting").
  - **Detection**: Grep for known brand names (`mise`, `ruff`, `pre-commit`, `mypy`, `pylint`, `flake8`, `black`, `isort`, `eslint`, `prettier`, `biome`, `poetry`, `pipenv`, `venv`).
  - **Validation**: Any brand-specific requirement is a specification violation per NFR-4.

---

## Regression Checklist

### AEF Documents (Unchanged Files)

- [ ] No modifications to `milestones/` directory files (any change is out-of-scope).
- [ ] No modifications to `tests/` directory.
- [ ] No modifications to `skills/code-search/`, `skills/graph-context/`, `skills/session-audit/`, `skills/evolve-skills/` directories.
- [ ] No modification to any HTML, CSS, or JSON files.
- [ ] No SDD pipeline sequence alteration — all changes are additive documentation updates or new files.

### Existing Template Structure

- [ ] `templates/completion_template.md` — All pre-existing sections (Files Modified, Tests Executed, Edge Cases Handled, Technical Debt incurred) remain intact and unmodified. Only the new "Raw Evidence" section is appended.
- [ ] `templates/evaluation_template.md` — All pre-existing sections (Test Execution Summary, Passed Tests, Failed Tests, Bugs Auto-Resolved, Remaining Structural Failures, Next Steps) remain intact and unmodified. Only the new "Raw Evidence" section is appended.
- [ ] `templates/review_template.md` — All pre-existing sections (Executive Summary, Implementation Summary, Reality vs Plan, Specification Compliance, Verification Results, Architecture Assessment, Edge Cases, Technical Debt, Recommendations, Revision Summary) remain intact and unmodified. Only the new "Live State Verification" section is inserted.

### Existing SKILL.md Process Sequences

- [ ] `skills/review-implementation/SKILL.md` — All existing process steps 1-10 remain intact. Only the standing rule is prepended and the rule added to Review Analysis Rules.
- [ ] `skills/investigate-issue/SKILL.md` — All existing process steps 1-8 remain intact. Only the standing rule is prepended and the rule added to Investigation Strategy.
- [ ] `skills/evaluate-implementation/SKILL.md` — All existing process steps 1-6 remain intact. Only the standing rule is prepended.
- [ ] `skills/bootstrap-project/SKILL.md` — All existing process steps 1-11 remain intact. Only a new step is inserted between existing steps 7 and 8.
- [ ] `skills/implement-specification/SKILL.md` — All existing content remains intact. Only the "When uncertain" section gains the uncertainty marker rule.

### Existing Framework Documents

- [ ] `docs/FRAMEWORK.md` — All existing architectural patterns (Spec-Driven Development, Agent-Tool Separation, Hierarchical Control System, Artifact Persistence) and Infrastructure Skills sections remain intact. Only the new "The Uncertainty Marker" section is inserted.
- [ ] `AGENTS.md` — All existing agent role descriptions, handoffs, and process definitions remain intact. Only the new Uncertainty Marker rule and Mechanical Tooling Stack section are added.

---

## Manual Validation

1. **Structured Documentation Review for FR-1**:
   - Read `docs/FRAMEWORK.md` end-to-end, verifying "The Uncertainty Marker" section is seamlessly integrated between "Spec-Driven Development" and "Agent-Tool Separation."
   - Verify the surrounding section flow is coherent.
   - Confirm the language matches the RFC 2119 MUST-level requirements: the specification says "MUST either...or emit...and HALT" and "Guessing is strictly forbidden."

2. **Zero-Trust Review Simulation**:
   - Take a hypothetical completion report and simulate a zero-trust review.
   - Confirm the Live State Verification section in `templates/review_template.md` provides enough structure to independently verify each claim.
   - Assess whether the template alone is sufficient, or if the SKILL.md needs additional guidance on how to operate in a "separate context."

3. **Evidence-Based Debugging Readability**:
   - Read both `skills/investigate-issue/SKILL.md` and `skills/evaluate-implementation/SKILL.md` from an agent's perspective.
   - Confirm the standing rule is prominent enough that an agent cannot miss it.
   - Verify the rule does not conflict with other existing process steps.

4. **Cross-Reference the Ground-Truth Script**:
   - Run all 12 test cases from FR-5 Functional Validation manually.
   - Confirm the output formatting is consistent (e.g., always `PASS:` or `FAIL:` prefix).
   - Verify the usage text is informative enough for both human and agent readers.

5. **Tooling Stack Agnosticism Check**:
   - Read the bootstrap-project step and AGENTS.md section.
   - Confirm that someone reading this section could correctly implement it for any language/ecosystem (Python, Node.js, Rust, Go) without contacting the author.

6. **Template Upgrade Consistency**:
   - Read both `completion_template.md` and `evaluation_template.md` side-by-side.
   - Confirm the Raw Evidence section is at the same position and uses the same language in both templates.

---

## Automated Validation

#### Diff-Scope Verification (Pre-Merge Check)

This mechanical check MUST be executed by `evaluate-implementation` before tests are considered passed.

- **Command:** `git diff --name-only`
- **Assertion:** The output of this command MUST strictly match the "Allowlist" defined in M3S2 Specification. If any file appears in the diff that is not on the Allowlist, the test automatically FAILS. The agent must revert the out-of-scope file before proceeding.

**Allowlist (Files permitted to change):**
- `docs/FRAMEWORK.md`
- `AGENTS.md`
- `skills/implement-specification/SKILL.md`
- `skills/review-implementation/SKILL.md`
- `templates/review_template.md`
- `skills/investigate-issue/SKILL.md`
- `skills/evaluate-implementation/SKILL.md`
- `templates/completion_template.md`
- `templates/evaluation_template.md`
- `bin/ground-truth-check.sh` (new file)
- `skills/bootstrap-project/SKILL.md`

**Failure Criteria:**
- Any file outside allowlist appears in git diff.
- Out-of-scope files committed or staged.

---

#### FR-1: Uncertainty Marker — Grep Check

**Command:**
```bash
grep -F '#NEEDS-CLARIFICATION' docs/FRAMEWORK.md AGENTS.md skills/implement-specification/SKILL.md
```

**Assertion:** Every target file contains the literal string `#NEEDS-CLARIFICATION`.

**Failure Criteria:**
- Any target file has zero matches.
- The marker is only in comments (grep with context flags to confirm).

---

#### FR-2: Zero-Trust Rule — Header Check

**Command:**
```bash
head -5 skills/review-implementation/SKILL.md | grep -F "Assume the prior report is wrong"
```

**Assertion:** The standing rule is within the first 5 lines of content (after YAML frontmatter).

**Failure Criteria:**
- Rule not found in first 5 content lines.
- Rule text is different from specification.

---

#### FR-2: Live State Verification — Section Header Check

**Command:**
```bash
grep -F '## Live State Verification' templates/review_template.md
```

**Assertion:** Section header exists.

**Failure Criteria:**
- Section header not found.

---

#### FR-3: Evidence-Based Debugging — Header Check (both files)

**Command:**
```bash
head -5 skills/investigate-issue/SKILL.md | grep -F "Debug from evidence"
head -5 skills/evaluate-implementation/SKILL.md | grep -F "Debug from evidence"
```

**Assertion:** Both files contain the evidence-based debugging rule within the first 5 content lines.

**Failure Criteria:**
- Rule missing from either file.
- Rule text differs from specification.

---

#### FR-4: Raw Evidence — Section Header Check (both templates)

**Command:**
```bash
grep -F '## Raw Evidence' templates/completion_template.md templates/evaluation_template.md
```

**Assertion:** Both templates contain the Raw Evidence section header.

**Failure Criteria:**
- Section header missing from either template.

---

#### FR-5: Ground-Truth Script — Existence and Executability

**Command:**
```bash
test -f bin/ground-truth-check.sh && echo "FILE_EXISTS"
test -x bin/ground-truth-check.sh && echo "IS_EXECUTABLE"
```

**Assertion:** Both checks pass.

**Failure Criteria:**
- File does not exist.
- File is not executable.

---

#### FR-5: Ground-Truth Script — Write Operation Audit

**Command:**
```bash
grep -cPn -- '>[>]?|mv[[:space:]]|cp[[:space:]]|rm[[:space:]]|mkdir[[:space:]]|touch[[:space:]]|chmod|chown|install[[:space:]]' bin/ground-truth-check.sh || echo "CLEAN"
```

**Assertion:** The grep finds zero write operation patterns (excluding comments and string literals). Output should be "CLEAN".

**Failure Criteria:**
- Any write operation pattern is found outside a quoted string, here-doc, or comment.
- See specific acceptance criterion: `bin/ground-truth-check.sh` contains zero write operations.

---

#### FR-6: Mechanical Tooling Stack — Category Check

**Command:**
```bash
grep -i 'environment manager' skills/bootstrap-project/SKILL.md AGENTS.md
grep -i 'linter.*formatter\|fast.*lint\|formatter' skills/bootstrap-project/SKILL.md AGENTS.md
grep -i 'pre-commit\|precommit' skills/bootstrap-project/SKILL.md AGENTS.md
grep -i 'type checker\|type.*check' skills/bootstrap-project/SKILL.md AGENTS.md
```

**Assertion:** Each category appears in at least one of the target files.

**Failure Criteria:**
- Any category is entirely absent.
- Only one file contains a category (should appear in both or at minimum in bootstrap-project).

---

#### FR-6: Brand Name Audit

**Command:**
```bash
grep -ins -- 'mise\|ruff\|poetry\|black\|isort\|flake8\|pylint\|eslint\|prettier\|biome\|mypy\|pipenv\|venv\|golangci-lint\|clippy' skills/bootstrap-project/SKILL.md AGENTS.md || echo "NO_BRANDS_FOUND"
```

**Assertion:** No specific brand names appear in the target files.

**Failure Criteria:**
- Any brand name appears as a requirement (not as an example in a parenthetical note).
- A brand name is listed as "must use X."

---

## Expected Outcomes

**Observable Success Indicators:**

1. **Uncertainty Marker Adoption**: A reviewer or agent can run `grep -rn '#NEEDS-CLARIFICATION'` across the entire AEF repo and find the marker defined in FRAMEWORK.md, AGENTS.md, and implement-specification/SKILL.md.

2. **Zero-Trust Review Culture**: Any review generated with the updated `review_template.md` contains a populated Live State Verification section showing which claims were independently verified, with what commands, and what was observed.

3. **Evidence-First Debugging**: Investigation reports and evaluation reports will all begin with the literal error message or `--help` output, not with "I've seen this before" or memory-based diagnosis.

4. **Raw Evidence as Cultural Norm**: Completion and evaluation reports always include the exact shell command and its raw stdout/stderr for every claim made. A report without this section is structurally incomplete.

5. **Ground-Truth Utility Ready**: `bin/ground-truth-check.sh` is a single POSIX shell file, executable, self-documenting, and provides 5 commands for low-friction live-state verification by both agents and humans. It has zero side effects.

6. **Mechanical Tooling as Standard Practice**: Every bootstrapped project via `bootstrap-project` will produce documentation defining its tooling stack with the four categories (environment manager, fast linter/formatter, pre-commit framework, type checker), without being tied to specific brands.

---

## Next Steps

Advise running `generate-tests` to create executable test scripts and then `implement-specification` to execute the implementation.
