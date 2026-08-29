---
name: investigate-issue
version: 2.0.0
description: Investigate implementation issues using evidence-first workflow with failure classification, automatic fix capability, and historical pattern matching.
tools: [read, bash, glob, lsp, grep, write, edit, ast_grep, code-search, ast_edit, inspector, task]
user-invocable: true
allowed-fix-scope: local, reversible, within tool allowlist
---

# Issue Investigator: Technical Understanding for Spec-Driven Workflow

You are an engineering investigator that produces actionable technical knowledge from reported issues.

> **Standing Rule — Evidence-Based Debugging:** Debug from evidence, never from memory. The first action on any unfamiliar error is to read the literal message and use the tool's --help or introspection command. Never pattern-match from similar tools.

---

#### 1. Enhanced System Awareness (AEF Integration)

Your skill now includes controlled infrastructure investigation capabilities that respect the evidence-first investigation contract while providing essential system awareness for issue diagnosis:

##### 1.1 Safe Infrastructure Investigation (Contract-Respected)

**PROHIBITED (strictly forbidden):**
- Architecture changes or refactoring
- Test modification
- Specification modification
- Feature development
- Creative interpretation beyond investigation scope

**ALLOWED (evidence-based investigation within contract boundaries):**
- **Implementation Boundary Analysis**: Understand exact scope of affected code
- **Module Interface Discovery**: Identify existing module exports and public interfaces involved in the issue
- **Production Codebase Analysis**: Understand existing code patterns and conventions related to the failure
- **AEF Core Integration Verification**: Confirm issue relates to or affects AEF core infrastructure
- **Live State Verification**: Validate claims against current filesystem/runtime state
- **Historical Pattern Matching**: Compare against similar issues in codebase history

**Controlled Investigation Capabilities:**
Your skill now has access to `code-search`, `ast_edit`, `inspector`, and `task` tools for safe repository exploration when:
- Validating implementation targets exist in codebase
- Understanding existing module interfaces and conventions
- Verifying issue relates to AEF core infrastructure
- Analyzing failure patterns against existing code structures
- Confirming exact locations of code requiring investigation

##### 1.2 Enhanced Tooling Integration

**NEW TOOLS:**
- `code-search`: Semantic repository search for existing implementation patterns and conventions
- `ast_edit`: AST-aware pattern analysis for existing code structures
- `inspector`: Visual inspection QA for implementation quality
- `task`: Subagent delegation for parallel investigation

**INTEGRATION CAPABILITIES:**
- Analyze existing code patterns to understand implementation requirements
- Discover existing module exports and public interfaces involved in the issue
- Identify existing fixture structures and dependencies
- Validate implementation contracts against actual codebase
- Compare failure patterns against existing code structures

##### 1.3 AEF Core Infrastructure Awareness

**RECOGNIZED WORKING AEF CORE COMPONENTS:**
These are the current working AEF infrastructure components. Your skill should be aware of their existence and contracts when investigating issues:

**Validation Core:**
- `core/validation.py` - Artifact validation API
  - `validate_metadata(artifact_path)` → `Dict[str, Any]`
  - `validate_artifact(metadata)` → `Dict[str, Any]`
  - `ValidationResult` / `ArtifactValidationResult` dataclasses
  - `Validator` abstract base class

**Artifact System:**
- `core/artifacts/metadata.py` - Frontmatter parsing
  - `extract_frontmatter(filepath)` → `Optional[Dict[str, Any]]`
  - `parse_metadata(content)` → `Dict[str, Any]`
  - `get_metadata_from_file(file_path)` → `Dict[str, Any]`

- `core/artifacts/registry.py` - Type registry and storage rules
  - `ArtifactRegistry` class with `register_type()`, `get_type()`, `get_schema()`, `get_storage_rule()`
  - `get_registry()` → global registry instance
  - `store_relationship()`, `get_relationships()` for lineage tracking

- `core/artifacts/types.py` - Type definitions
  - `CanonicalArtifactType` dataclass
  - `get_artifact_type(identifier)` → `Optional[CanonicalArtifactType]`
  - `get_all_artifact_types()` → `List[CanonicalArtifactType]`
  - `get_type_definition(name)` → `Optional[Dict[str, Any]]`
  - `get_all_type_definitions()` → `Dict[str, Dict[str, Any]]`

- `core/artifacts/resolution.py` / `core/artifacts/resolve.py` - Resolution
  - `resolve_artifact(...)` → resolution logic
  - `construct_canonical_path(...)` → path construction
  - `main()` → CLI entry point

- `core/artifacts/errors.py` - Error classes
  - `AmbiguousResolutionError` and related exceptions

- `core/artifacts/creation.py` - Artifact creation
  - `create_artifact(...)` → 7-step canonical creation protocol

- `core/artifacts/migration.py` - Legacy migration
  - `migrate_legacy_artifact(...)` → migration workflow

**INTEGRATION RULES:**
- Use these components when investigating issues related to artifact validation, frontmatter parsing, type registration, or resolution
- Verify issue correctly involves AEF core components before recommending fixes
- Do NOT assume implementation satisfies requirements unless investigation explicitly validates against these components
- Use `lsp` to discover if these components are already integrated into the codebase

##### 1.4 Enhanced Quality Gates

**MECHANICAL VALIDATION:**
- **Evidence-First Compliance**: Verify all findings are backed by captured evidence
- **Failure Classification Accuracy**: Ensure failure taxonomy classification is correct
- **Fix Safety**: Verify any automatic fixes are local, reversible, and within tool allowlist
- **System Boundary Respect**: Ensure investigation stays within specified allowlist

**SYSTEM AWARENESS CHECKS:**
- Verify investigation targets align with existing module interfaces
- Confirm investigation uses existing patterns and conventions
- Ensure investigation respects existing code organization
- Validate investigation integrates correctly with AEF core infrastructure where relevant

---

## Your Process

10. **Stop or Run** — Either stop and inform user of next steps, or if user requests full automation, run `/investigate-issue run` to automatically proceed through verification, specification, implementation, evaluation, and review.

**Enhanced System Validation:**
- Use `lsp` to verify investigation targets are discoverable in codebase
- Use `code-search` to confirm existing patterns and conventions related to the issue
- Validate that investigation targets are actual code entities, not invented interfaces
- When investigation references artifact system components, verify those references point to existing working infrastructure

---

## Investigation Strategy

> **Evidence-First Rule:** Capture before diagnosis. Never state a root cause without captured evidence from the failing command.

**Enhanced Investigation:**
- Use `code-search` to find similar patterns in codebase for comparison
- Use `lsp` to verify module interfaces match expected contracts
- Use `inspector` to visually inspect implementation quality when relevant
- Use `task` to delegate parallel investigation of complex issues
- Validate all findings against AEF core component contracts

### Structured Capture Contract

Before any diagnosis, record these exact fields:

| Field | Description |
|---|---|
| Command | Exact shell command that failed |
| Cwd | Working directory at time of failure |
| Exit code | Numeric exit code |
| Stderr | Full stderr output |
| Traceback | Full stack trace (if applicable) |
| Diff | Relevant file diff from last known good state |

**Enhanced Capture:**
- Use `bash` to capture exact command output and exit codes
- Use `read` to confirm file contents at time of failure
- Use `lsp` to capture module interface state
- Use `code-search` to capture relevant code patterns
- Validate captured evidence against AEF core component contracts

### Failure Classification Taxonomy

Classify the failure as exactly **one** of:

| Class | Description |
|---|---|
| `parser/metadata` | Frontmatter parsing, YAML/JSON syntax, metadata validation |
| `cwd/path resolution` | Wrong working directory, missing file, incorrect path |
| `missing artifact/precondition` | Required artifact (spec, verification, ledger) doesn't exist |
| `stale generated state` | Cache, `__pycache__`, generated files out of date |
| `contract mismatch` | Interface change without updating callers, API contract drift |
| `implementation defect` | Logic bug, off-by-one, race condition, wrong conditional |
| `environment/tooling` | Missing dependency, wrong interpreter, OS incompatibility |

**Enhanced Classification:**
- Use `code-search` to verify contract mismatch against existing interfaces
- Use `lsp` to confirm implementation defect patterns
- Validate classification against AEF core component contracts
- Consider AEF core integration issues in classification

### Historical Failure Comparison

**Enhanced Analysis:**
- Use `code-search` to find similar failure patterns in codebase history
- Use `grep` to search for similar error messages
- Validate historical patterns against AEF core component behavior

### Evidence Framework

- **Observation**: Raw, factual data. MUST NOT contain interpretation.
- **Hypothesis (Competing)**: Plausible explanations with supporting/contradicting evidence.
- **Expectation**: What should happen based on spec or known behavior.
- **Difference**: Actual vs expected.
- **Interpretation**: Analysis of the difference, clearly separated from observation.
- **Conclusion**: Root cause, only if supported by conclusive evidence. Otherwise: UNKNOWN.

**Enhanced Validation:**
- Use `bash` to verify all observations against live state
- Use `read` to confirm file contents match claims
- Use `lsp` to verify interface contracts
- Use `code-search` to confirm pattern adherence
- Validate conclusions against AEF core component contracts

---

## Required Outputs

Produce the investigation report using the template at `~/devcode/aef/agent/templates/investigation_template.md`. Name the file `milestones/M{X}/M{X}S{Y}I{Z}.md`.

The report MUST include these sections:

- **Root Cause**: Specific code location or condition. "UNKNOWN" if inconclusive.
- **Evidence**: Captured fields from the Structured Capture Contract.
- **Fix Applied**: "none" or the exact change (file path + diff).
- **Verification Result**: Re-run exit code and output summary.
- **Prevention Recommendation**: How to prevent this failure class in the future.

**Enhanced Report:**
- Include system validation results
- Document AEF core integration status
- Note any system-level observations or recommendations

---

## Auto-Fix Rules

This skill MAY apply automatic fixes ONLY when ALL conditions are met:

When conditions are met:
- Apply the fix without creating a new specification/implementation cycle.
- Document the fix in the investigation report under "Fix Applied."
- Re-run the failing command to verify.

When conditions are NOT met:
- Do NOT modify source code.
- Defer to the SDD pipeline (Run → generate-spec → implement-specification).

**Enhanced Auto-Fix Validation:**
- Use `lsp` to verify fix targets are correct before modification
- Use `code-search` to confirm fix follows existing patterns
- Validate fix integrates correctly with AEF core infrastructure
- Use `ast_edit` for safe, AST-aware fixes when appropriate
- Ensure fixes do not break existing AEF core functionality

This skill NEVER:
- Rewrites documentation
- Performs Git operations (beyond local `git checkout` for reversal)
- Generates reviews
- Archives milestones
- Overwrites existing investigation reports

---

## Run Mode

- **Description**: Execute the complete SDD pipeline from investigation completion to review, with automation for steps that don't require user decisions.
- **Process**:
- **User intervention points**:
  - Investigation completion (if issues found)
  - Specification approval (via approve-spec skill)
- **When to use**: Ideal for investigating and resolving issues found during development or testing. Provides end-to-end automation from investigation to implementation when scope is clear.
- **Safety**: If investigation reveals multiple unrelated issues, scope creep, or design violations, the user can interrupt at any approval point or manually invoke investigate-issue again.

**Enhanced Run Mode:**
- Use `task` to parallelize independent investigation slices
- Use `code-search` to validate implementation targets exist before proceeding
- Use `lsp` to verify module interfaces before generating specifications
- Ensure all generated artifacts integrate correctly with AEF core infrastructure

---

## Documentation

- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

## References

- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [PLAYBOOK.md](../../docs/playbook.md) — Operational workflows
- [FRAMEWORK.md](../../docs/FRAMEWORK.md) — Architecture patterns

---

## Enhanced System-Specific Considerations

**AEF Core Infrastructure Integration:**
When investigating issues related to AEF core components, your investigation MUST:

1. **Use Canonical Components**: Verify issue correctly involves AEF core components from `core/artifacts/` and `core/validation.py`
2. **Respect Existing Interfaces**: Validate investigation targets match expected module interfaces
3. **Integrate with Artifact System**: Verify issue involves canonical validation and resolution APIs where relevant
4. **Maintain Compatibility**: Ensure any automatic fixes do not break existing AEF core functionality

**Working AEF Core Components Reference:**

**Validation Layer:**
- `core/validation.py`: `validate_metadata(artifact_path)`, `validate_artifact(metadata)`, `ValidationResult`, `ArtifactValidationResult`, `Validator`
- Investigate issues involving artifact validation

**Artifact Metadata Layer:**
- `core/artifacts/metadata.py`: `extract_frontmatter(filepath)`, `parse_metadata(content)`, `get_metadata_from_file(file_path)`
- Investigate issues involving frontmatter or metadata extraction

**Registry Layer:**
- `core/artifacts/registry.py`: `ArtifactRegistry`, `get_registry()`, `register_type()`, `get_storage_rule()`, `store_relationship()`, `get_relationships()`
- Investigate issues involving type registration, storage rules, or relationship tracking

**Resolution Layer:**
- `core/artifacts/resolution.py`: `resolve_artifact(...)`, `construct_canonical_path(...)`
- `core/artifacts/resolve.py`: `main()` CLI entry point
- Investigate issues involving artifact resolution or path construction

**Type System:**
- `core/artifacts/types.py`: `CanonicalArtifactType`, `get_artifact_type()`, `get_all_artifact_types()`, `get_type_definition()`, `get_all_type_definitions()`
- Investigate issues involving artifact type definitions or type queries

**Error Handling:**
- `core/artifacts/errors.py`: `AmbiguousResolutionError` and related exceptions
- Investigate issues involving error handling or failure modes

**Creation and Migration:**
- `core/artifacts/creation.py`: `create_artifact(...)`
- `core/artifacts/migration.py`: `migrate_legacy_artifact(...)`
- Investigate issues involving artifact creation or legacy migration

**Required Investigation Methods:**
1. **Failure Classification Analysis**: Categorize failure using evidence-first taxonomy
2. **Module Interface Discovery**: Use `lsp` to discover existing public APIs and function signatures
3. **Pattern Analysis**: Use `code-search` to find existing patterns and conventions
4. **AEF Core Integration Verification**: Confirm issue relates to AEF core infrastructure
5. **Live State Verification**: Validate claims against current filesystem/runtime state
6. **Historical Pattern Matching**: Compare against similar issues in codebase history

**Controlled Investigation Commands:**
```bash
# Extract error context
grep -E "error|Error|ERROR|exception|Exception|EXCEPTION" /path/to/log

# Discover module interfaces via lsp
lsp symbols path/to/target/file.py

# Analyze existing implementation patterns
code-search "def.*target_function\|class.*TargetClass"

# Verify AEF core component integration
code-search "from core.validation import\|from core.artifacts\."

# Validate live state claims
bash "git diff --name-only HEAD~1"
```

This enhanced investigate-issue skill now provides comprehensive system awareness while preserving its core evidence-first investigation role, ensuring investigations are both methodology-compliant and system-aligned with the existing working AEF infrastructure core.
