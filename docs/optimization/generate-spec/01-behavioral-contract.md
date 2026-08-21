# Behavioral Contract: generate-specification Skill

**Template Version:** 1.0.0
**Status:** Defined from baseline audit
**Date:** 2026-08-17

---

## Executive Summary

This contract defines the responsibility, behavioral guarantees, and boundaries for the `generate-specification` skill. It separates **existing behavior**, **required behavior**, and **proposed behavior** to guide skill evolution while preserving critical invariants.

---

## 1. Responsibility

### 1.1. Core Responsibility

The `generate-specification` stage owns **technical refinement of milestone-derived requirements into mechanically verifiable implementation specifications**.

**What it explicitly owns:**
- Translating milestone intent into **observable behavioral contracts** (CLI, schema, filesystem state)
- Enforcing **strict file scope boundaries** (allowlist/denylist enforcement)
- Preventing **placeholder and TODO leaks** from reaching implementation
- Maintaining **upstream traceability** through derived_from lineage
- Validating **observable behavior mandates** (no prose requirements)

**What it does NOT own:**
- Architectural design decisions (naming conventions, toolchain cohesion)
- Implementation investigation (binary inspection, exit code patterns)
- Mechanical validation that validators should handle (schema validation, path resolution)
- Downstream tooling choices (verification strategy, test structure)

### 1.2. Mental Model

**Systems Architect / Contract Decomposer Persona:**

- **Objective:** Define WHAT the system must do, not HOW it must do it
- **Boundary:** Functional requirements, not implementation details
- **Verification:** Every requirement must be mechanically verifiable
- **Continuity:** Inherit from milestone integration bindings, not invent from scratch
- **Isolation:** Specifications are independent artifacts, not toolchain designs

**Anti-Patterns to Avoid:**
- Prose requirements (e.g., "system must handle errors gracefully")
- Placeholder descriptions (e.g., "(to be defined)", "(placeholder)")
- Implementation tricks (e.g., command invocations, grep-based checks)
- Template-filling (e.g., adding sections without semantic content)
- Reconstruction of user intent (e.g., inferring toolchain cohesion)

---

## 2. Inputs

### 2.1. Authoritative Information Consumed

**Primary Input:**
- **Milestone Document:** `M{X}.md` from `milestones/M{X}/` directory

**Required Derived Information:**
- **Integration Bindings Table:** From milestone's `## Integration Bindings` section
  - Binary, fixture, and interface dependencies explicitly listed by milestone
  - Authority: Milestone integration bindings (not skill-investigation)

**Optional Inherited Information:**
- **Prior Specifications:** From `milestones/M{X}/M{X}S{Y-1}.md` (for followup context)
- **Spec Decomposition Plan:** From milestone's `## Spec Decomposition Plan`
  - Declares exact N specifications in sequence
  - Limits scope to plan's enumerated artifacts

### 2.2. Template Assets

**Required Template:**
- `templates/specification_template.md` from generate-spec skill directory

**Constraint:**
- Template must contain valid frontmatter with `id`, `type`, `title`, `milestone_id`, `status`, `derived_from`, `template_version` fields

### 2.3. Framework Artifacts

**Implicitly Available:**
- AEF asset loader (framework handles path resolution)
- Template rendering system (framework handles template loading)
- Validator infrastructure (framework enforces schema, location, traceability)

**NOT Provided:**
- No binary inspection capability (spec should not investigate bin/)
- No code-search tool access (not used for this stage)
- No framework-specific path resolution checks (validators handle this)

---

## 3. Outputs

### 3.1. Primary Output Artifact

**File Location:** `milestones/M{X}/M{X}S{Y}.md`

**Artifact Structure:**
1. **YAML Frontmatter (REQUIRED)**
   - Strictly enclosed in `---` delimiters
   - Fields: `id`, `type`, `title`, `milestone_id`, `status`, `derived_from`, `template_version`
   - Format:
     ```yaml
     ---
     id: SPEC-M{X}S{Y}
     type: specification
     title: "[Title]"
     milestone_id: M{X}
     status: draft
     derived_from:
       - M{X}
     template_version: 1.2.2
     ---
     ```

2. **Objective Section**
   - Short summary of specification scope
   - Reference to milestone integration bindings
   - Multi-spec plan (if applicable)

3. **Followup Context (if applicable)**
   - Derived From: milestone and prior specification
   - Prior Work Completed: summary of implementation
   - Remaining Gaps: what work from milestone remains incomplete

4. **Functional Requirements Section**
   - List of mechanical, verifiable requirements
   - Each requirement MUST define:
     - CLI Executable Contract (flags/args/exit codes) OR
     - Structured Schema Contract (non-negotiable keys) OR
     - Filesystem State Contract (file paths, state transitions)
   - Requirements MUST NOT be prose descriptions
   - Requirements MUST NOT include placeholders

5. **Non-Functional Requirements Section**
   - Only if genuinely applicable (not fabricated for template-filling)
   - Prefer "not applicable" over generic placeholders

6. **Architecture Impact Section**
   - **Strict File Scope (Allowlist & Denylist):**
     - Allowlist: Files permitted to change
     - Denylist: Files do NOT touch (e.g., all HTML/CSS, all JSON if view-only)
   - Affected Modules: Modules with modified interfaces
   - New Modules: Newly introduced modules
   - Removed Modules: Modules deprecated or removed
   - Public Interfaces: Entry points, APIs, CLI commands

7. **Data Flow Section**
   - **NOT RECOMMENDED** (architectural design, not specification)
   - If included, MUST NOT describe "how data moves" (implementation detail)
   - MUST describe interface boundaries and data transformations (requirement boundary)

8. **Implementation Tasks Section**
   - Mechanical list of implementation steps
   - MUST reference functional requirements
   - MUST be aligned with spec decomposition plan

9. **Introspection & Code-Search Evidence Section**
   - **NOT REQUIRED** (template-filling, redundant with verification stage traceability)
   - If present, MUST NOT hallucinate non-existent search commands

10. **Constraints Section**
    - Out of Scope explicit prohibitions (from milestone)
    - Risk factors (from milestone)
    - Technical constraints (from milestone)

11. **Assumptions Section**
    - Explicit assumptions with evidence (from milestone)
    - NOT placeholder statements

12. **Acceptance Criteria Section**
    - Observable system states or artifacts, NOT command invocations
    - MUST be verifiable via framework validators
    - MUST reference FR IDs or module boundaries

13. **Next Steps Section**
    - Advice to run `generate-verification` (if concrete contracts exist)
    - MUST NOT be generic placeholder text

### 3.2. Handoff Protocol

**Post-Generation Actions (REQUIRED):**
1. **Physical Write:** Use `write` tool to save spec to `milestones/M{X}/M{X}S{Y}.md`
2. **Write Verification:** Run `head -n 10 milestones/M{X}/M{X}S{Y}.md` to verify file exists and is not empty
3. **Placeholder Check:** Search for `placeholder`, `TODO`, `FIXME`, `to be defined` in output buffer
4. **If Placeholder Found:** Halt, emit `#NEEDS-CLARIFICATION: Incomplete specification contains placeholder markers`, request user input
5. **If Placeholder Not Found:** Output plain text: `[SPECIFICATION_GENERATION_COMPLETE] Task complete. Next Step: Please run /generate-verification to continue.`

**Failure Conditions (HALT):**
- Milestone integration bindings table is empty AND spec decomposition plan references binaries not in bin/ (specification cannot be mechanically verified)
- Functional requirements contain prose descriptions (no observable boundary)
- Functional requirements contain placeholders (e.g., "(to be defined)")
- Output buffer is empty after write
- Cannot determine next sequence number (existing spec already exists at max Y)

---

## 4. Upstream Authority

### 4.1. What It Inherits (Must Preserve)

**From Milestone:**
- Integration bindings (binaries, fixtures, interfaces)
- Out of scope definitions
- Risk factors
- Assumptions
- Spec decomposition plan (exact N specifications)

**From Prior Specifications:**
- Followup context (what was done, what remains)
- Module boundaries and interfaces already defined
- Existing contracts in same milestone

### 4.2. What It Must Not Redefine

**Boundaries:**
- **Not an architectural design stage** — cannot decide toolchain cohesion, naming conventions, exit code patterns
- **Not an investigation stage** — cannot inspect bin/, cannot discover binary existence
- **Not a reconstruction stage** — cannot infer user intent from implementation (e.g., naming conventions)

**Specific Prohibitions:**
- Do NOT add integration cohesion questions (e.g., "How can this integrate with existing binaries?")
- Do NOT analyze naming conventions from binaries (e.g., "What naming conventions are they using?")
- Do NOT define data flow descriptions (architectural design)
- Do NOT assign sequential FR IDs (implementation detail)
- Do NOT add template-filling sections (introspection queries, fake search commands)
- Do NOT prescribe command-based acceptance criteria (implementation tricks)

**Constraint from `02-PIPELINE-RESPONSIBILITY-CONTRACT.md`:**
> `generate-specification` owns technical refinement... It may determine, where not already constrained: architecture; modules; interfaces; data structures; algorithms; technical contracts...

**Interpretation:** Technical refinement ends at requirement definition. Architectural design is downstream (implement-specification). Module boundaries are constraints, not design choices.

---

## 5. Downstream Contract

### 5.1. What `generate-verification` Must Be Able To Rely On

**Required Artifacts:**
1. **Observable Behavioral Contracts:**
   - CLI contracts with explicit flags/args/exit codes
   - Structured schemas with non-negotiable keys
   - Filesystem state requirements with explicit paths and states

2. **Traceability:**
   - Stable FR IDs (sequential or semantic, but consistent)
   - `derived_from` lineage linking to milestone
   - Reference to integration bindings table

3. **Strict File Scope:**
   - Allowlist/denylist definitions (what files can be modified)
   - Affected/new/removed module lists
   - Public interface definitions

4. **Failure Conditions:**
   - Explicit exit codes or error states
   - Revert criteria
   - Exception cases

**Required Condition for Verification Generation:**
Every functional requirement MUST define an observable boundary. Requirements that are only prose descriptions MUST be marked `N/A` (not applicable to verification).

### 5.2. What `generate-verification` Will NOT Expect From This Stage

**Not Provided:**
- Binary investigation results (what binaries exist, naming conventions)
- Exit code patterns (how tools should behave)
- Toolchain integration strategies (how tools work together)
- Implementation details (how data flows through modules)
- Verification strategies (how to test requirements)
- Test file structures (test organization)

**Why This Boundary Exists:**
Verification stage owns its own investigation based on spec contracts. It is not blocked by implementation details from earlier stages.

---

## 6. Allowed Reasoning

### 6.1. Legitimate Inference (Evidence-Based)

**From Milestone Integration Bindings:**
- Which binaries/fixeds/interfaces are required
- Which files/modules are affected (from spec decomposition plan)
- Which sections are out of scope (from milestone's "Out of Scope" definition)

**From Spec Decomposition Plan:**
- Exact number of specifications to generate
- Sequence of spec artifacts (S1, S2, S3...)
- Module boundaries per specification

**From Prior Specifications:**
- What interfaces already exist (to avoid redefinition)
- What work from milestone is already complete

**From Template:**
- Required section structure (Objective, Functional Requirements, Architecture Impact, etc.)
- Field names and formats (id, type, title, milestone_id, status, derived_from, template_version)

### 6.2. Legitimate Decision-Making (Not Implementation)

**Contract Refinement:**
- Determining whether a functional requirement maps to CLI, schema, or filesystem contract
- Converting prose descriptions into structured contracts
- Mapping milestone sections to spec sections (Objective, Functional Requirements, Constraints, etc.)

**Scope Alignment:**
- Ensuring spec covers exactly what milestone decomposition plan declares
- Rejecting requirements outside spec decomposition plan
- Marking requirements as N/A if not applicable to verification

**Boundary Definition:**
- Defining allowlist/denylist based on integration bindings and module lists
- Identifying affected/new/removed modules based on spec decomposition
- Defining public interfaces based on milestone integration bindings

**Failure Condition Definition:**
- Defining explicit exit codes based on milestone risks
- Defining error states based on integration binding expectations
- Defining revert criteria based on out-of-scope sections

**NOT Allowed (Implementation Decisions):**
- Choosing between multiple architectural approaches
- Designing verification strategies
- Selecting test frameworks or tools
- Determining how modules should be implemented
- Choosing naming conventions for toolchain
- Defining exit code patterns (validation decides this)

---

## 7. Forbidden Reasoning

### 7.1. Absolute Prohibitions

**NO Prose Requirements:**
- "The system must handle errors gracefully"
- "Performance should be acceptable"
- "Security measures must be in place"

**NO Placeholders:**
- "(Placeholder: exit code definitions)"
- "(to be defined)"
- "(implementation to be defined)"

**NO Implementation Investigation:**
- "What naming conventions are they using?" (from binary existence)
- "How can this integrate with existing binaries to form a cohesive toolchain?"
- "What exit code patterns do existing tools use?"

**NO Template-Filling:**
- Adding "Introspection & Code-Search Evidence" with fake search commands
- Adding "Acceptance Criteria" with command invocations that don't exist
- Adding sections without semantic content

**NO Architectural Design:**
- "Describe how data moves through the system"
- "Design toolchain integration strategy"
- "Define exit code patterns for all tools"

**NO Reconstruction of User Intent:**
- Inferring toolchain cohesion from binary names
- Assuming specific naming conventions from binary existence
- Deciding integration goals not in milestone

### 7.2. Evidence-Based Rejection

**If Milestone Integration Bindings Table is Empty AND Spec Decomposition Plan References Binaries:**
- Halt and emit `#NEEDS-CLARIFICATION: Specification requires binaries not defined in milestone integration bindings. Define explicit dependencies in integration bindings table.`
- Do NOT scan bin/ directory
- Do NOT infer binary existence

**If Functional Requirement Lacks Observable Boundary:**
- Halt and emit `#NEEDS-CLARIFICATION: Functional requirement lacks observable behavior contract. Rewrite requirement as CLI contract, schema definition, or filesystem state, or mark N/A.`
- Do NOT proceed to next requirement
- Do NOT fabricate placeholders

**If Placeholder Found in Output:**
- Halt and emit `#NEEDS-CLARIFICATION: Incomplete specification contains placeholder markers. Remove placeholders and define concrete contracts.`
- Do NOT output handoff message
- Do NOT mark spec complete

---

## 8. Unknown Handling

### 8.1. When Information is Missing

**If Integration Bindings Table is Missing from Milestone:**
- Check if spec decomposition plan includes binaries (FR-1: "System must call bin/omp-discover")
- If yes: Halt with `#NEEDS-CLARIFICATION: Specification references binaries not defined in milestone integration bindings. Define integration bindings table in milestone.`
- If no: Continue (spec may be implementation-agnostic)

**If Spec Decomposition Plan Ambiguous:**
- Halt with `#NEEDS-CLARIFICATION: Spec decomposition plan unclear about N specifications. Define exact sequence (M{X}S1, M{X}S2, ..., M{X}SN) with clear scope per specification.`
- Do NOT guess sequence
- Do NOT assume more specs than declared

**If Prior Specification Missing but Required by Followup Context:**
- Halt with `#NEEDS-CLARIFICATION: Followup context requires prior specification (M{X}S{Y-1}) but file not found. Ensure specification sequence is contiguous.`
- Do NOT skip specification
- Do NOT reconstruct prior work

**If Template Version Not Specified:**
- Halt with `#NEEDS-CLARIFICATION: Template version not specified. Must provide template_version in milestone or skill configuration.`
- Do NOT use default version
- Do NOT assume version compatibility

### 8.2. When Information is Insufficient for Verification

**If Functional Requirement Cannot Be Verified:**
- Halt and emit `#NEEDS-CLARIFICATION: Functional requirement lacks observable boundary. Rewrite as CLI contract, schema definition, or filesystem state.`
- Do NOT proceed with unverified requirements
- Do NOT mark N/A without explicit statement of inapplicability

**If Non-Functional Requirement Appears Fabricated:**
- Halt and emit `#NEEDS-CLARIFICATION: Non-functional requirement appears fabricated. If truly applicable, provide evidence from milestone. If not applicable, mark N/A and explain.`
- Do NOT accept generic placeholders
- Do NOT fabricate for template-filling

---

## 9. Contradiction Handling

### 9.1. When Evidence Conflicts

**Milestone Integration Bindings vs Spec Decomposition Plan:**
- Priority: **Spec Decomposition Plan**
- Action: Halt with `#NEEDS-CLARIFICATION: Spec decomposition plan references binaries not in milestone integration bindings. Define explicit dependencies.`
- Rationale: Decomposition plan defines scope, integration bindings define authorization

**Spec Decomposition Plan vs Prior Specification:**
- Priority: **Spec Decomposition Plan** (only for first spec, prior spec for followup specs)
- Action: Halt with `#NEEDS-CLARIFICATION: Spec decomposition plan declares N specifications but existing artifacts cover more. Refine plan to match actual artifacts.`
- Rationale: Decomposition plan is ground truth for artifact count

**Functional Requirement vs Out of Scope Section:**
- Priority: **Out of Scope Section**
- Action: Mark requirement `N/A` and explicitly reference out-of-scope section from milestone
- Rationale: Out-of-scope section has higher authority than inferred requirements

**Template Requirements vs Constraint:**
- Priority: **Constraint from Audit/Skill Improvements**
- Action: Follow constraint, not template instruction
- Rationale: Template provides structure, constraints define boundaries

### 9.2. When User Input Required

**If Functional Requirement Ambiguous:**
- Emit `#NEEDS-CLARIFICATION: Functional requirement ambiguous. Example: "System must handle errors gracefully." Define concrete error handling contract (exit codes, recovery paths).`

**If Spec Decomposition Plan Incomplete:**
- Emit `#NEEDS-CLARIFICATION: Spec decomposition plan incomplete. Example: Declares M5S1, M5S2, but unclear scope. Define concrete scope boundaries per specification.`

**If Integration Bindings Ambiguous:**
- Emit `#NEEDS-CLARIFICATION: Integration bindings table incomplete. Example: References bin/omp-tool but no schema or CLI definition provided. Define explicit contract.`
- Do NOT scan bin/ directory
- Do NOT infer contract from binary existence

**If Template-Provided Guidance Conflicts with Constraints:**
- Emit `#NEEDS-CLARIFICATION: Template instruction conflicts with skill constraints. Example: "Describe data flow" conflicts with architectural design prohibition. Follow constraint, not template instruction.`
- Do NOT follow template instruction
- Do NOT fabricate content

---

## 10. Traceability

### 10.1. Lineage Preservation

**Upstream Tracing:**
- `derived_from: [M{X}]` — Links spec to milestone
- `derived_from: [M{X}, M{X}S{Y-1}]` — Links followup spec to prior spec
- Reference integration bindings table in Objective section
- Reference out-of-scope section in Constraints section

**Downstream Tracing:**
- Every functional requirement MUST be traceable to:
  - Milestone section (from which it was derived)
  - Spec decomposition plan sequence (S{Y})
  - Integration binding (if tool/interface referenced)

**FR ID Assignment:**
- Assign stable, semantic identifiers if beneficial (e.g., FR-READ_BUCKETING, FR-READ_QUERY)
- OR assign sequential identifiers if semantic naming is unclear (FR-1, FR-2)
- Consistency is key — if using sequential, use throughout specification
- Verification stage may reassign IDs with semantic meaning

**Traceability Validation:**
- Ensure every functional requirement has FR ID
- Ensure FR IDs are referenced in acceptance criteria
- Ensure acceptance criteria reference FR IDs or module boundaries
- Ensure no requirements are orphaned (no ID, no trace)

### 10.2. Evidence Requirements

**From Milestone:**
- Integration bindings table content
- Spec decomposition plan sequence
- Out of scope definitions
- Risk factors
- Assumptions

**From Prior Specifications (if applicable):**
- Interfaces already defined
- Modules already created
- Work already completed

**NOT Required:**
- Code inspection results
- Binary investigation findings
- Search query logs
- Manual path resolution checks

---

## 11. Quality Invariants

### 11.1. Mechanical Correctness (Always True)

**Frontmatter Enclosure:**
- Every spec MUST begin with `---` enclosure
- YAML schema MUST be valid
- `template_version` MUST match template file version

**Artifact Completeness:**
- File MUST exist after write
- File MUST not be empty
- No placeholders (placeholder, TODO, FIXME, to be defined) allowed

**Observable Behavior:**
- Every functional requirement MUST define an observable boundary
- No prose-only requirements allowed
- No "generic" requirements allowed

**File Scope Boundaries:**
- Allowlist MUST define permitted file modifications
- Denylist MUST define prohibited file modifications
- Architecture Impact section MUST reference allowlist/denylist

### 11.2. Semantic Correctness (Always True)

**Requirement Quality:**
- Requirements MUST be verifiable
- Requirements MUST be traceable
- Requirements MUST be consistent with milestone
- Requirements MUST NOT duplicate prior specs (negative guardrail)

**Anti-Fabrication:**
- NO requirements fabricated just to fill sections
- NFRs ONLY if genuinely applicable (not just "add NFRs")
- Acceptance criteria ONLY if verifiable

**Responsibility Boundaries:**
- Specifications MUST NOT include architectural design
- Specifications MUST NOT include implementation investigation
- Specifications MUST NOT include template-filling sections

### 11.3. Traceability Invariants (Always True)

**Lineage:**
- `derived_from` MUST list milestone(s)
- Every functional requirement MUST have ID
- Every acceptance criterion MUST reference FR ID or module boundary

**Consistency:**
- Spec ID format MUST be `SPEC-M{X}S{Y}`
- Milestone ID MUST match specification title milestone
- Template version MUST match template file version

---

## 12. Failure Conditions

### 12.1. Halting Conditions (Critical Failures)

**Block Generation, Do Not Proceed:**

1. **Missing Integration Bindings for Binaries**
   - Evidence: Spec decomposition plan references binaries, integration bindings table is empty
   - Action: Halt with `#NEEDS-CLARIFICATION: Specification requires binaries not defined in milestone integration bindings. Define explicit dependencies.`
   - Reason: Specification cannot be mechanically verified without binary contract

2. **Placeholder in Output**
   - Evidence: Output buffer contains `placeholder`, `TODO`, `FIXME`, `to be defined`
   - Action: Halt with `#NEEDS-CLARIFICATION: Incomplete specification contains placeholder markers. Remove placeholders and define concrete contracts.`
   - Reason: Placeholder leaks into implementation stage (anti-hallucination)

3. **Prose Functional Requirements**
   - Evidence: Functional requirement lacks CLI contract, schema definition, or filesystem state
   - Action: Halt with `#NEEDS-CLARIFICATION: Functional requirement lacks observable boundary. Rewrite as CLI contract, schema definition, or filesystem state.`
   - Reason: Specification not verifiable

4. **Spec Sequence Mismatch**
   - Evidence: Declared N specifications but existing artifacts exceed N, or missing spec in sequence
   - Action: Halt with `#NEEDS-CLARIFICATION: Spec decomposition plan declares N specifications but actual artifacts differ. Refine plan to match actual artifacts.`
   - Reason: Duplicate or missing artifacts violate spec decomposition plan

5. **Template Version Mismatch**
   - Evidence: `template_version` not specified in frontmatter or does not match template file
   - Action: Halt with `#NEEDS-CLARIFICATION: Template version not specified or does not match template file. Define template_version.`
   - Reason: Template version is required for validation

### 12.2. Warnings (Non-Critical, Continue But Flag)

**Flag but Do Not Halt:**

1. **Template-Filling Sections**
   - Evidence: "Introspection & Code-Search Evidence" section present with fake search commands
   - Action: Emit warning, optionally remove section or add note that queries are placeholders
   - Reason: Redundant with verification stage traceability

2. **Generic NFRs**
   - Evidence: Non-Functional Requirements section contains generic placeholders like "Performance: Should be fast"
   - Action: Emit warning, suggest marking as N/A if not applicable
   - Reason: Fabrication, not specification

3. **Command-Based Acceptance Criteria**
   - Evidence: Acceptance criteria reference command invocations (e.g., `bin/omp-tool --validate`)
   - Action: Emit warning, suggest converting to observable system states
   - Reason: Implementation trick, not verifiable requirement

### 12.3. Continuation Conditions (Proceed Normally)

**Safe to Continue:**

1. **No Integration Bindings for Binaries**
   - Evidence: Integration bindings table empty AND spec decomposition plan does NOT reference binaries
   - Action: Proceed (spec is implementation-agnostic)

2. **Followup Context Without Prior Specification**
   - Evidence: Followup context requires prior spec but file not found
   - Action: Emit warning, proceed using available context (milestone only)

3. **Unknown Template Version**
   - Evidence: Template version not specified but template exists
   - Action: Emit warning, use latest template version
   - Reason: Framework handles version compatibility

---

## 13. Stage Persona

### 13.1. Cognitive Operating Mode

**Systems Architect / Contract Decomposer:**

- **Focus:** Define WHAT, not HOW
- **Standard:** Mechanical verifiability, not prose fluency
- **Boundary:** Functional requirements, not implementation details
- **Verification:** Every requirement must be checkable
- **Continuity:** Inherit from milestone, not invent from scratch
- **Isolation:** Specifications are independent, not toolchain designs

**Anti-Patterns to Avoid:**

- **Over-Designing:** Don't add architectural decisions (naming conventions, toolchain cohesion)
- **Over-Investigating:** Don't inspect binaries, don't scan code
- **Over-Questioning:** Don't ask user questions (integration cohesion, naming conventions)
- **Over-Filling:** Don't add sections without semantic content

### 13.2. Mental Checklist Before Generation

**Requirements Phase:**
- [ ] Did I read milestone integration bindings table?
- [ ] Did I read milestone spec decomposition plan?
- [ ] Did I check for prior specification (followup context)?
- [ ] Did I ensure spec sequence is contiguous and within plan?
- [ ] Did I strip visual dividers from template?
- [ ] Did I construct YAML frontmatter with proper enclosure?
- [ ] Did I assign FR IDs (sequential or semantic)?
- [ ] Did I derive functional requirements with observable boundaries?
- [ ] Did I check each requirement for placeholders?
- [ ] Did I define architecture impact with allowlist/denylist?

**Pre-Output Phase:**
- [ ] Did I physically write the file?
- [ ] Did I verify file exists (head -n 10)?
- [ ] Did I search for placeholders in output buffer?
- [ ] Did I output handoff message if no placeholders found?

**If ANY Check Fails:**
- HALT and emit `#NEEDS-CLARIFICATION` with specific failure
- Do NOT proceed to output
- Do NOT mark task complete

---

## 14. Behavioral Taxonomy

### 14.1. Existing Behavior (Preserve)

**Mechanical Invariants:**
- YAML frontmatter enclosure (lines 17-22)
- Non-placeholder FR assignment (derivation, not ID assignment)
- Observable behavior mandates (lines 52-53)
- Negative guardrails (lines 74-78)
- Mechanical postconditions (lines 22-24, 69)
- Strict file scope boundaries (allowlist/denylist enforcement)

**Artifact Quality Guarantees:**
- Strong traceability (derived_from lineage, stable FR IDs)
- Concrete contracts (CLI, schema, filesystem)
- Observable acceptance criteria (commands/assertions)
- Strict file scope boundaries (allowlist/denylist enforcement)
- Contextual integration bindings (consumption of milestone integration bindings)

### 14.2. Required Behavior (Must Exist)

**From AEF Contract:**
- Observable behavioral contracts (CLI, schema, filesystem state)
- No prose requirements
- No placeholder descriptions
- Strict file scope boundaries
- Upstream traceability (derived_from lineage)
- Mechanical verifiability (every requirement must be checkable)

**From Audit Recommendations:**
- Specification readiness check (all FRs must be verifiable)
- No implementation-level investigation (binary inspection, toolchain cohesion)
- No template-filling sections (introspection queries, fake commands)
- Remove FR ID assignment (keep only FR derivation)
- Clarify data flow removal (architectural design, not spec)
- Strengthen observable behavior mandates (add post-check)
- Add traceability validation within spec (check all FRs have contracts)

### 14.3. Proposed Behavior (Future Direction)

**Remove Implementation Leakage:**
- Remove "Inspect Existing Binaries" (lines 31-47)
- Remove "Dynamic Path Resolution" (lines 40-43)
- Remove "Introspection & Code-Search Evidence" (lines 99-105)
- Remove "FR Assignment" (lines 48-50)
- Remove "Data Flow" encouragement (line 19)

**Add Specification Readiness:**
- Add explicit check: "Every functional requirement MUST define an observable boundary"
- Add post-generation check: "Verify all FRs are verifiable (CLI/schema/filesystem)"
- Add NFR handling: "Explicitly mark N/A if not applicable, do not fabricate"

**Refine Output:**
- Change "Success criteria as commands" to "Observable system states or artifacts"
- Clarify "Next Steps" to ensure specification contains concrete contracts
- Remove generic handoff text in favor of concrete guidance

---

## 15. Evidence Contract

### 15.1. What Must Be Observed

**Before Generation:**
- [ ] Milestone document loaded (M{X}.md)
- [ ] Milestone integration bindings table read
- [ ] Spec decomposition plan read
- [ ] Prior specification read (if followup context exists)
- [ ] Template loaded and dividers stripped

**During Generation:**
- [ ] YAML frontmatter constructed with proper enclosure
- [ ] Objective section derived from milestone integration bindings
- [ ] Followup context populated (if applicable)
- [ ] Functional requirements derived with observable boundaries
- [ ] Architecture impact defined with allowlist/denylist
- [ ] Acceptance criteria defined with FR references

**After Generation:**
- [ ] File physically written to milestones/M{X}/M{X}S{Y}.md
- [ ] File existence verified (head -n 10)
- [ ] No placeholders found in output buffer
- [ ] Handoff message output

### 15.2. What Must NOT Be Observed

**Do NOT Observe:**
- Binary existence (do NOT scan bin/)
- Naming conventions (do NOT infer from binaries)
- Exit code patterns (do NOT design for toolchain)
- Toolchain cohesion (do NOT decide integration strategy)
- Code search queries (do NOT hallucinate searches)
- Path resolution (do NOT manually check paths)

**If These Are Observed, Contract Violation:**
- Halt and emit `#NEEDS-CLARIFICATION` with specific failure
- Do NOT proceed with implementation details
- Do NOT output handoff message

---

## 16. Regression Risk Assessment

### 16.1. High-Risk Changes

**Removing Implementation-Level Investigation (binary inspection, toolchain cohesion):**
- **Risk:** Specs may miss existing binaries not in integration bindings
- **Mitigation:** Rely on milestone integration bindings table, not skill investigation
- **Fallback:** Verification stage can flag conflicts

**Removing FR ID Assignment (sequential numbering):**
- **Risk:** Verification stage must invent IDs
- **Mitigation:** Verification stage already assigns IDs with semantic meaning
- **Fallback:** Use FR semantic names, not numbers, in test scripts

### 16.2. Medium-Risk Changes

**Removing Template-Filling Sections (introspection, fake queries):**
- **Risk:** Specs may lose "investigation trail" documentation
- **Mitigation:** Traceability exists via derived_from and FR IDs, not prose documentation
- **Fallback:** Verify stage performs traceability checks

**Removing "Data Flow" Encouragement:**
- **Risk:** Specs may lack architectural context
- **Mitigation:** Constraints and architecture impact sections cover boundaries, not detailed flows
- **Fallback:** Implementation stage can add data flow if needed

### 16.3. Low-Risk Changes

**Removing Mechanical Path Resolution:**
- **Risk:** Asset loading failures at runtime
- **Mitigation:** Framework asset loader handles path resolution transparently
- **Fallback:** Validators catch asset loading errors

---

## 17. Summary of Behavioral Invariants

### Must Preserve (Critical)

1. **Mechanical YAML frontmatter enclosure** — Prevents malformed artifacts
2. **Observable behavior mandates** — Prevents prose requirements
3. **Non-placeholder FR derivation** — Guarantees stable traceability
4. **Negative guardrails enforcement** — Prevents cross-spec duplication
5. **Mechanical postconditions** — Ensures write succeeded, no placeholders
6. **Strict file scope boundaries** — Maintains isolation between specs

### Must Implement (Required)

1. **Specification readiness check** — All FRs must be verifiable
2. **No implementation investigation** — Specs should not inspect binaries
3. **No template-filling** — Sections must have semantic content
4. **Remove FR ID assignment** — Keep only FR derivation
5. **No architectural design** — Specs define WHAT, not HOW

### Must Remove (Harmful)

1. **Binary inspection** — Implementation investigation not in scope
2. **Path resolution checks** — Mechanical enforcement belongs to validators
3. **Introspection sections** — Template-filling, redundant with verification
4. **FR ID assignment** — Sequential IDs constrain downstream
5. **Data flow descriptions** — Architectural design, not specification

---

## Appendix A: Example Contract Transitions

### Example 1: Milestone with Integration Bindings

**Input:**
- `milestones/M10/M10.md`
- Integration bindings: `bin/omp-discover`, `bin/omp-verify-metadata`
- Spec decomposition plan: 3 specifications (M10S1, M10S2, M10S3)

**Existing Behavior:**
- Reads integration bindings table
- Scans bin/ directory for binary names and schemas
- Determines naming conventions and exit code patterns
- Defines toolchain cohesion strategy
- Assigns sequential FR IDs (FR-1, FR-2, ...)

**Required Behavior:**
- Reads integration bindings table
- Derives functional requirements with observable contracts
- Defines architecture impact with allowlist/denylist
- Assigns FR IDs (sequential or semantic)
- Hints at data flow, naming conventions, toolchain cohesion

**Proposed Behavior:**
- Reads integration bindings table
- Derives functional requirements with observable contracts
- Defines architecture impact with allowlist/denylist
- Removes FR ID assignment (keep only derivation)
- Removes investigation of bin/ (integration bindings is authoritative source)
- Removes data flow encouragement
- Hints at data flow constraints, not design

### Example 2: Followup Specification

**Input:**
- `milestones/M10/M10S2.md`
- Prior spec: M10S1.md (already implemented)

**Existing Behavior:**
- Reads M10S1.md
- Uses prior spec to understand current implementation state
- Refines requirements to match implementation
- May add "Followup Context" section

**Required Behavior:**
- Reads prior specification
- Uses prior work completed to inform current scope
- Defines remaining gaps from original milestone
- Ensures no duplication of already implemented specs

**Proposed Behavior:**
- Reads prior specification
- Defines remaining gaps from original milestone
- Ensures no duplication (negative guardrail)
- Refines scope based on implementation, not redefined intent

---

## Appendix B: Failure Mode Examples

### Example 1: Placeholder Leak

**Input:**
- Milestone M5 defines FR-1: "System must validate user input"
- Integration bindings: none
- Spec decomposition plan: M5S1

**Current Behavior (Risk):**
```markdown
#### Functional Requirements

- FR-1: System must validate user input. (Placeholder: define exit codes and validation logic)
```

**Required Behavior:**
```markdown
#### Functional Requirements

- FR-1: System MUST return exit code 0 on valid input, 1 on invalid input, 2 on system error.
```

**Failure Condition:**
- Halt with `#NEEDS-CLARIFICATION: Incomplete specification contains placeholder markers. Remove placeholders and define concrete contracts.`

### Example 2: Prose Requirement

**Input:**
- Milestone M5S1 requires error handling

**Current Behavior (Risk):**
```markdown
#### Functional Requirements

- FR-1: The system must handle errors gracefully.
```

**Required Behavior:**
```markdown
#### Functional Requirements

- FR-1: System MUST return exit code 0 on success, 1 on validation failure, 2 on system error, with detailed error message in stderr.
```

**Failure Condition:**
- Halt with `#NEEDS-CLARIFICATION: Functional requirement lacks observable boundary. Rewrite as CLI contract, schema definition, or filesystem state.`

### Example 3: Missing Integration Bindings

**Input:**
- Milestone M10 defines FR-1: "System must call bin/omp-discover"
- Integration bindings table: empty
- Spec decomposition plan: M10S1

**Current Behavior (Risk):**
- Scans bin/ directory, discovers bin/omp-discover
- Infers exit code patterns, schema
- Defines spec based on discovered binary

**Required Behavior:**
- Halt with `#NEEDS-CLARIFICATION: Specification requires binaries not defined in milestone integration bindings. Define explicit dependencies.`
- Do NOT scan bin/ directory
- Do NOT infer binary behavior

### Example 4: Template-Filling

**Input:**
- Milestone M5S1 requires file validation

**Current Behavior (Risk):**
```markdown
## Introspection & Code-Search Evidence

- **Workspace Search Queries:**
  - `search_code "validate"` → Found: bin/omp-validate
  - `search_code "file parsing"` → Found: src/file-parser.js
```

**Required Behavior:**
- Remove "Introspection & Code-Search Evidence" section entirely
- No fake search commands

**Failure Condition:**
- Halt with `#NEEDS-CLARIFICATION: Incomplete specification contains placeholder markers.` (if placeholders found)

### Example 5: FR ID Assignment Conflict

**Input:**
- Milestone M10S2 requires caching functionality

**Current Behavior (Risk):**
- Assigns FR-5 to caching requirement
- Sequential ID may not map to semantic meaning
- Verification stage must reassign IDs

**Required Behavior:**
- Derive FRs, do NOT assign sequential IDs
- Verification stage assigns IDs with semantic meaning (FR-CACHE-INVALIDATE, etc.)

**Proposed Behavior:**
- Derive FRs, let verification stage assign semantic IDs
- More meaningful traceability

---

**Document End**
