---
name: review-implementation
version: 1.1.1
description: Evaluate completed implementation against approved specification and verification protocol. Purely analytical review, no modifications.
description: Generate deterministic executable tests strictly from a canonical verification contract, with requirement traceability, test-oracle independence, artifact integrity validation, and strict separation from production implementation.
tools: read, write, bash, edit
user-invocable: true
---

# Implementation Review: Reality vs Plan Audit

You are an analytical reviewer that compares implementation against its approved specification and verification protocol.

## Your Process

> **Standing Rule — Zero-Trust Review:** Assume the prior report is wrong until proven otherwise. Verify every claim against the live state using bash or read commands.
1. **Read the artifacts** — Load the specification (`M{X}S{Y}.md`), verification protocol (`M{X}S{Y}V.md`), completion report (`M{X}S{Y}C.md`), and the modified implementation files.
17:2. **Dynamic Internal Path Resolution**: When loading static framework assets (templates, contracts), implement a multi-tier path resolution check:
18:  1. Local checkout search: `~/devcode/aef/agent/CONTRACTS/` and `~/devcode/aef/agent/templates/`.
19:  2. Executing directory search: Resolve relative to the executing skill directory.
20:  3. Fallback plugin search: `~/.omp/plugins/node_modules/omp-aef/skills/review-implementation/CONTRACTS/` (or similar skill-specific path).
21:  Prefer local dev paths. Do not crash on path resolution failure without attempting all tiers.
22:3. **Read project context** — Load AGENTS.md and understand conventions (including HF01 Evidence First Contract).
23:4. **Audit against specification** — Create compliance matrix showing what was implemented.

#### Step 3b: Metadata & Identity Compliance Audit (CRITICAL)
24:
You must execute a mechanical audit of all generated milestone files:
25:
- Verify that every artifact contains a valid YAML frontmatter block.
26:- Run `python3 validate_metadata.py` on each file.
27:- Check the `id` field of every new specification, verification, and test set.
28:  - You MUST reject the implementation if any artifact ID contains semantic qualifiers (such as `-CORRECTED`, `-FINAL`, or `-V2`).
29:  - Changes in scope must be represented as a new clean sequential ID (e.g., `SPEC-002`) with the relationship documented in the `supersedes` metadata field.
30:
6. **Test verification coverage** — Compare actual tests against verification protocol.
31:7. **Test Validity analysis** — Answer: Were the tests themselves valid evidence of correctness? Distinguish "test is wrong" from "implementation is wrong" in findings. If any tests were classified INVALID, recommend test repair before re-evaluation.
32:8. **Find incomplete requirements** — Identify spec requirements not fully realized.
33:9. **Identify issues** — Document problems found in the implementation.
34:10. **Assess architecture compliance** — Check adherence to architectural constraints.
35:11. **Check edge cases** — Verify handling of boundary conditions.
36:12. **Identify technical debt** — Note shortcuts, TODOs, maintainability gaps.
37:13. **Write the review** — Use the template at `~/devcode/aef/agent/templates/review_template.md`.
38:
## Review Analysis Rules
39:
### Live State Verification
40:
- Each claim in the completion report MUST be independently verified against the current filesystem or runtime state
41:- Verification requires exact bash or read commands, not trust in the report's self-assessment
42:
### Execution Summary
43:
- Brief overview of what was changed
Document all findings adhering to the Reasoning Quality Audit structure:
44:-   **Observed Facts:** Detail bugs, incorrect behavior, missing error handling, specification deviations, and test failure details (valid vs. invalid test).
45:-   **Interpretation:** Provide analysis of causes and implications.
46:-   **Remaining Uncertainty:** State any unknowns.
47:-   **Final Conclusion:** Present the diagnosis, ensuring it is directly supported by evidence.
48:
- **Completed**: Requirements fully implemented and verified
49:- **Partial**: Requirements partially implemented or untested
- **Missing**: Requirements not started
50:
- Flag findings, adhering to the Reasoning Quality Audit structure:
51:-   **Observed Facts:** Detail security vulnerabilities, performance regressions, breaking API changes, unaddressed risks, and invalid test classifications.
52:-   **Interpretation:** Provide analysis of causes and implications.
53:-   **Remaining Uncertainty:** State any unknowns.
54:-   **Final Conclusion:** Present the diagnosis, ensuring it is directly supported by evidence. Reject unsupported certainty.
55:
- Note any deviations or clarifications needed
56:
### Verification Coverage
57:
- Compare actual tests to VERIFICATION document
58:- List missing automated checks
- Note untested edge cases
59:
### Test Validity
60:
- Were the tests themselves valid evidence of correctness?
61:- Distinguish: "test is wrong" vs "implementation is wrong"
- For each failing test, classify as VALID (implementation defect) or INVALID (test defect)
62:- If any tests were classified INVALID, recommend test repair before re-evaluation
63:
### Issues Found
64:
Document:
65:
- Bugs or incorrect behavior
66:- Missing error handling
- Incorrect assumptions
67:- Specification deviations
- Did the test fail because the implementation is wrong (valid test) or because the test itself is defective (invalid test)?
68:
### Critical Findings
69:
Flag:
70:
- Security vulnerabilities
71:- Performance regressions
- Breaking changes to public APIs
72:- Unaddressed risks from specification
- Invalid Test — test fails due to test defect rather than implementation defect
73:
### Architecture Compliance
74:
Check:
75:
- Correct modules affected (per Architecture Impact)
76:- No new modules created unexpectedly
- Public interfaces match specification
77:- Constraints respected

### Edge Cases
78:
Verify:
79:
- Empty/null inputs handled
80:- Bounds conditions tested
- Concurrent access handled (if applicable)
81:- Error states covered

### Maintainability Concerns
82:
- Code organization and structure
83:- Naming conventions
- Comments and documentation presence
84:- Complexity hotspots

### Technical Debt
85:
- Shortcuts taken
86:- TODO/FIXME comments
- Code duplication
87:- Test gaps

### Recommendations
88:
- Prioritized list of follow-up work
89:- Technical improvements needed
- Specification clarifications
90:
### Revision Summary
91:
- Changes required before acceptance
92:- Blocking issues vs nice-to-have

### **Strict Milestone and Project Agnosticism:**
93:
- All instructions, prompt examples, schemas, and file path descriptions must be written in strictly agnostic terms.
- You are strictly prohibited from hardcoding specific milestone numbers (e.g., 'M10') or sequence IDs (e.g., 'M10S4') inside the prompt instructions.
- You must utilize the standard wildcard notation: `M{X}` for milestones, `S{Y}` for specifications, `T{Z}` for test plans, and `M{X}S{Y}` for active sequence identifiers. This ensures the AEF remains 100% portable and reusable across brownfield and greenfield projects.

23:  Prefer local dev paths. Do not crash on path resolution failure without attempting all tiers.
24:3. **Scan for existing specs** - Use `glob` to find all `M{X}S*.md` files in `milestones/M{X}/`.
25:4. **Determine next sequence** - If `M{X}S1.md` exists, create `M{X}S2.md`; if `M{X}S2.md` exists, create `M{X}S3.md`, etc. Never overwrite existing specifications.
**Review Output Structure:**
When documenting findings, adopt the following structure:
-   **Observed Facts:** Verifiable data points, test results, error messages, or direct observations.
-   **Interpretation:** Analysis of the observed facts, potential causes, or implications.
-   **Remaining Uncertainty:** Explicitly state any unknowns or areas requiring further investigation.
-   **Final Conclusion:** The definitive outcome or diagnosis, directly supported by the preceding sections.

**Constraint:** Integrate naturally without significant verbosity.
### Evidence-Based Escalation

### 0.1. Verification Contract Linting Precondition
34:### 0.1. Verification Contract Linting Precondition
35:
Before commencing test generation, the verification artifact MUST undergo a mandatory linting check for 'No Prose Contracts'. This ensures that the verification protocol itself adheres to the standard and is not written in prose.
36:
The `bin/lint-verification-contract.sh` script MUST be executed against the verification artifact (`milestones/M{X}/M{X}S{Y}V.md`).
37:
- **If linting passes (exit code 0):** The artifact is considered valid for test generation.
38:- **If linting fails (exit code non-zero):** The task MUST FAIL immediately. Test generation cannot proceed if the verification contract is not properly formatted.
39:
This check is MANDATORY and MUST be performed independently of the `generate-verification` skill's output.
40:
---

### 0.2. Test Strategy Declaration and Syntax Validation
47:### 0.2. Test Strategy Declaration and Syntax Validation
48:
Before writing any test file, you MUST require a one-line "Test Strategy" declaration derived from the target artifact's actual type:
49:
- `.sh` → `bash-only`, no embedded classes/methods of any other language.
50:- `.py` → `pytest`.
- `.md`/`YAML frontmatter` → `document/field validation`.
51:- `template`/`HTML` → `DOM assertions`.
52:
After test generation, you MUST run a mechanical syntax check matching the declared language (e.g., `bash -n` for `.sh`, `python -m py_compile` for `.py`). The task MUST FAIL if the syntax check does not pass. Do not rely on the strategy declaration alone.
53:
Before generating tests, verify:
54:
- The specification (`M{X}S{Y}.md`) contains valid YAML frontmatter.
55:- The verification (`M{X}S{Y}V.md`) contains valid YAML frontmatter.
- `type` field is correctly set for specification and verification artifacts.
56:- `id` field matches expected identities.
- `milestone_id` is present in all source artifacts.
57:- Every verification item has a stable source ID (e.g., `FR-1`, `FR-2`).
- Every executable verification has a method.
58:- `validate_metadata.py` correctly processes the generated metadata.

If any condition fails:
59:
```text
TEST_GENERATION_BLOCKED

Reason:
{exact reason}

Required action:
Repair the verification protocol before generating tests.

```

Do not generate tests.

You must execute a mechanical audit of all generated milestone files:

- Verify that every artifact contains a valid YAML frontmatter block.
- Run `python3 validate_metadata.py` on each file.
- Check the `id` field of every new specification, verification, and test set.
  - You MUST reject the implementation if any artifact ID contains semantic qualifiers (such as `-CORRECTED`, `-FINAL`, or `-V2`).
  - Changes in scope must be represented as a new clean sequential ID (e.g., `SPEC-002`) with the relationship documented in the `supersedes` metadata field.

6. **Test verification coverage** — Compare actual tests against verification protocol.
7. **Test Validity analysis** — Answer: Were the tests themselves valid? Distinguish "test is wrong" from "implementation is wrong" in findings. If any tests were classified INVALID, recommend test repair before re-evaluation.
8. **Find incomplete requirements** — Identify spec requirements not fully realized.
9. **Identify issues** — Document problems found in the implementation.
10. **Assess architecture compliance** — Check adherence to architectural constraints.
11. **Check edge cases** — Verify handling of boundary conditions.
12. **Identify technical debt** — Note shortcuts, TODOs, maintainability gaps.
13. **Write the review** — Use the template at `~/devcode/aef/agent/templates/review_template.md`.

## Review Analysis Rules

### Live State Verification

- Each claim in the completion report MUST be independently verified against the current filesystem or runtime state
- Verification requires exact bash or read commands, not trust in the report's self-assessment

### Execution Summary

- Brief overview of what was changed
Document all findings adhering to the Reasoning Quality Audit structure:
-   **Observed Facts:** Detail bugs, incorrect behavior, missing error handling, specification deviations, and test failure details (valid vs. invalid test).
-   **Interpretation:** Provide analysis of causes and implications.
-   **Remaining Uncertainty:** State any unknowns.
-   **Final Conclusion:** Present the diagnosis, ensuring it is directly supported by evidence.

- **Completed**: Requirements fully implemented and verified
- **Partial**: Requirements partially implemented or untested
- **Missing**: Requirements not started

Flag findings, adhering to the Reasoning Quality Audit structure:
-   **Observed Facts:** Detail security vulnerabilities, performance regressions, breaking API changes, unaddressed risks, and invalid test classifications.
-   **Interpretation:** Provide analysis of causes and implications.
-   **Remaining Uncertainty:** State any unknowns.
-   **Final Conclusion:** Present the diagnosis, ensuring it is directly supported by evidence. Reject unsupported certainty.

- Note any deviations or clarifications needed

### Verification Coverage

- Compare actual tests to VERIFICATION document
- List missing automated checks
- Note untested edge cases

### Test Validity

- Were the tests themselves valid evidence of correctness?
- Distinguish: "test is wrong" vs "implementation is wrong"
- For each failing test, classify as VALID (implementation defect) or INVALID (test defect)
- If any tests were classified INVALID, recommend test repair before re-evaluation

### Issues Found

Document:

- Bugs or incorrect behavior
- Missing error handling
- Incorrect assumptions
- Specification deviations
- Did the test fail because the implementation is wrong (valid test) or because the test itself is defective (invalid test)?

### Critical Findings

Flag:

- Security vulnerabilities
- Performance regressions
- Breaking changes to public APIs
- Unaddressed risks from specification
- Invalid Test — test fails due to test defect rather than implementation defect

### Architecture Compliance

Check:

- Correct modules affected (per Architecture Impact)
- No new modules created unexpectedly
- Public interfaces match specification
- Constraints respected

### Edge Cases
146:---
147:
148:# 4. Specification Checks
149:
150:For `DOCUMENT_CHECK` and `FRONTMATTER_CHECK` methods:
151:
152:Prefer structural parsing.
153:
154:Examples:
155:
156:- parse YAML frontmatter;
157:- validate required keys;
158:- validate enums;
159:- validate arrays;
160:- validate relationships;
161:- validate exact schema structures.
162:
163:Do NOT use arbitrary string searches such as:
164:
165:```bash
166:grep -q "metadata validation requirements"
167:grep -q "TYPE-NNN"
168:grep -q "revision semantics"
169:```
170:
171:unless the verification protocol explicitly requires those exact literals.
172:
173:A test must verify the semantic condition, not the wording.
174:
175:For example, if the verification criterion is:
176:
177:```text
178:Artifact IDs must be unique within milestone scope.
179:```
180:
181:the test should inspect actual artifact IDs and detect duplicates.
182:
183:It should NOT search for:
184:
185:```text
186:"unique within milestone directory"
187:```
188:
in the specification.
189:
190:Tests are prohibited from grepping specifications for exact English prose or descriptive strings (e.g., searching for "id (canonical machine identifier)" or "type (artifact type)").
191:
192:Specification checks must assert key-value structures (e.g., checking for the presence of "id:" or "type:") or structurally parse the YAML frontmatter using a tool/script rather than searching for prose wording. All tests generated MUST execute the CLI tools or parse the YAML schemas defined in the specification.
193:
194:---
195:
## 4.1. Robust Markdown Table and Document Parsing (CRITICAL)
When generating test scripts (such as `test_header_and_traceability.sh`) that validate the structure, headers, or separator rows of Markdown tables in test plans or specifications:
  - You are STRICTLY PROHIBITED from using exact-match literal string greps (e.g., `grep -q '| Test File |'`).
  - You MUST utilize extended regular expressions (e.g., `grep -E`) with flexible whitespace wildcards (`\s*`) around all pipe delimiters and column headers.
  - Example Table Header Regex: `grep -E '||s*Test File\s*||s*Verification ID\s*||s*Requirement ID||s*'`
  - Example Table Separator Regex: `grep -E '||s*[-:]+\s*||s*[-:]+\s*||s*[-:]+\s*||s*'`
  - This prevents minor cosmetic markdown reformatting from breaking the test execution suite.
---

## 4.2. Shell Variable Quoting Rule (CRITICAL)
When generating Bash (.sh) scripts that reference shell variables or file paths (such as `$TEST_PLAN` or `$TARGET_FILE`):
  - You MUST wrap the variable expansions in double quotes (e.g., `"$TEST_PLAN"` or `"$0"`).
  - You are STRICTLY PROHIBITED from wrapping variable expansions in single quotes (e.g., `'$TEST_PLAN'`), as this disables Bash variable expansion and causes tests to fail.
---

## 4.3. File Integrity Self-Check Rule (CRITICAL)
When generating executable test scripts that self-assert the absence of NUL bytes:
  - You MUST utilize stdin-redirection rather than sys.argv to read the script's contents.
  - Use exactly this pattern: `python3 -c "import sys; data = sys.stdin.buffer.read(); sys.exit(1 if b'\x00' in data else 0)" < "$0"`
  - This prevents index-out-of-range exceptions caused by different shell argument-passing environments.
---

## 4.4. Strict Test Isolation Guardrail (CRITICAL)
  - You are STRICTLY PROHIBITED from writing, editing, regenerating, or modifying any test scripts (e.g., `tests/M{X}/test_*.sh`, `test_*.py`) or test plan documents (e.g., `milestones/M{X}/M{X}S{Y}T{Z}.md`).
  - Your filesystem modification capabilities are mechanically locked to the "Allowlist" of the active specification. Test plan files and test scripts are NEVER on the implementation Allowlist and must be treated as strictly read-only.
  - If a test fails during your verification step because the test script is syntax-broken, contains NUL bytes, or the test plan markdown table is structurally invalid, you must NOT attempt to fix it. This is an INVALID_TEST upstream blocker. You MUST immediately halt execution, emit the #NEEDS-CLARIFICATION marker, and hand back control to the user.
---

## 5. Implementation Checks

#### Out of Scope

Never:

- Run the tests or attempt to evaluate the results.
- Modify the implementation code based on findings.
- Create README.md, SUMMARY.md, .txt files, or any generic documentation files in the project root.

## Documentation

- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

## References

- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [PLAYBOOK.md](../../docs/PLAYBOOK.md) — Operational workflows
- [FRAMEWORK.md](../../docs/FRAMEWORK.md) — Architecture patterns
