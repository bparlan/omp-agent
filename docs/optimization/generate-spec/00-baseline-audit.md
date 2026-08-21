# Behavioral Audit Report: generate-spec Skill

## Executive Summary

The `generate-spec` skill exhibits **strong behavioral guarantees** around mechanical correctness, traceability enforcement, and anti-hallucination mechanisms. However, it exhibits **significant responsibility boundary violations** by performing implementation-level decisions, over-specifying legitimate downstream design space, and encouraging excessive questioning that contradicts the AEF pipeline contract. The skill also contains **redundant mechanical enforcement** that should be delegated to validators rather than reimplemented in prompt text.

---

## 1. Current Behavior Guarantees

### Strengths (Protected Behavior)

| Behavior                                   | Location    | Why It's Valuable                                                                      |
| ------------------------------------------ | ----------- | -------------------------------------------------------------------------------------- |
| **Mechanical YAML frontmatter enclosure**  | Lines 17-22 | Enforces valid metadata schema without visual validation, prevents malformed artifacts |
| **Non-placeholder FR ID assignment**       | Lines 14-51 | Guarantees all functional requirements have stable, traceable IDs (FR-1, FR-2, etc.)   |
| **Observable behavior mandates**           | Lines 52-53 | Prevents prose-based requirements, forces structural contracts                         |
| **Milestone + project agnosticism**        | Lines 76-77 | Ensures downstream tools don't hardcode project-specific assumptions                   |
| **Negative guardrails enforcement**        | Lines 74-78 | Explicit prohibitions on cross-specification duplication and prose contracts           |
| **File existence verification post-write** | Lines 22-23 | Guarantees the write operation succeeded and artifact is not empty                     |
| **Compile-time placeholder detection**     | Line 24     | Prevents TODO/FIXME leaks from reaching implementation stage                           |
| **Multi-tier path resolution**             | Lines 40-43 | Fallback mechanisms prevent runtime errors from missing assets                         |

### Artifact Quality Guarantees

The generated specification artifacts (`M10S10.md`, `M10S7.md`) demonstrate:

1. **Strong traceability**: Clear `derived_from` lineage, milestone_id propagation, stable FR IDs
2. **Concrete contracts**: CLI command definitions, exit codes, schema requirements, not prose
3. **Observable acceptance criteria**: Commands and assertions, not subjective descriptions
4. **Strict file scope boundaries**: Allowlist/denylist enforcement via mechanical constraints
5. **Contextual integration bindings**: Explicit consumption of existing binaries/fixtures/interfaces

These are **core behavioral invariants** that must be preserved.

---

## 2. Responsibility Boundary Violations

### Critical Contradictions

#### 2.1. Over-Implementing Downstream Design Space

**Evidence:**

```markdown
Line 44: "If the milestone's Integration Bindings table is empty, scan bin/..."
Line 45-47: "What CLI tools already exist? What naming conventions, exit code patterns, and schemas are they using? How can this new specification integrate with these existing binaries to form a cohesive toolchain rather than an isolated silo?"
```

**Problem:**

- The skill **analyzes existing binaries** to determine "naming conventions, exit code patterns" (lines 45-47)
- It **intends to create cohesive toolchains** rather than isolated silos (line 46)
- This is **architectural design work** belonging to `implement-specification` or a separate architect stage

**Contract Violation:**
From `02-PIPELINE-RESPONSIBILITY-CONTRACT.md`:

> `generate-specification` owns technical refinement... It may determine, where not already constrained: architecture; modules; interfaces; data structures; algorithms; technical contracts...

**Actual Behavior:**
Lines 44-47 go **beyond** technical refinement into **architectural design decisions** (naming conventions, schema design, toolchain integration). This is:

1. **Not mandatory** by the milestone integration bindings table
2. **Not user-confirmed** (milestone should decide this)
3. **Inventing design space** that downstream stages cannot legitimately innovate within

**Why It's Harmful:**

- Constrains `implement-specification` to suboptimal or reinvented patterns
- Encourages **reconstruction** of user intent (naming conventions, toolchain cohesion)
- Creates **downstream dependence** on what should be a legitimate implementation choice

---

#### 2.2. Making Unjustified Technical Decisions

**Evidence:**

```markdown
Line 44: "Scan for existing specs... What naming conventions... are they using?"
Line 49: "Assign stable, sequential identifiers to all functional requirements (e.g., FR-1, FR-2)"
```

**Problem:**

- **Naming conventions** (line 44) is a **design choice**, not a derivation from milestone intent
- **Sequential FR IDs** (line 49) is **implementation detail**, not a requirement specification

**Contract Violation:**
From `03-SKILL-IMPROVEMENT-PRINCIPLES.md`:

> **Implementation Independence:** Do not invent implementation decisions merely to make a contract concrete. However, established implementation constraints must be preserved when they are: explicitly required; confirmed by the user; mandated by an existing interface...

**Actual Behavior:**

- Sequential FR IDs are **legitimate downstream design choices** (should be decided by `generate-verification` or `generate-tests`)
- Naming conventions analysis **creates implicit constraints** on downstream tooling without user confirmation

**Why It's Harmful:**

- Constrains `generate-verification` to sequential FR numbering
- Encourages **template-filling** without semantic value (FR-1, FR-2 for content that should be FR-BUCKETING, FR-SEPARATION)

---

#### 2.3. Encouraging Implementation Leakage

**Evidence:**

```markdown
Line 19: "Describe how data moves through the system, if applicable."
Line 55: "Name success criteria as commands whose output you can paste, not prose claims."
```

**Problem:**

- "Describe how data moves" (line 19) invites **implementation-level architecture design**
- "Commands whose output you can paste" (line 55) is **implementation detail**, not specification contract

**Contract Violation:**
From `01-AEF-GENERATION-CONTEXT.md`:

> Each stage refines an upstream contract. It must not silently redefine upstream intent... Downstream stages are autonomous refinement stages.

**Actual Behavior:**

- Data flow descriptions (line 19) are **architectural design decisions** that belong to `implement-specification`
- Command-based success criteria (line 55) are **implementation tricks**, not verifiable requirements

**Why It's Harmful:**

- Reconstructs implementation approach instead of specifying what must be true
- Provides **template-filling guidance** that encourages "fake" specifications (prose dressed as commands)

---

#### 2.4. Excessive Questioning Behavior

**Evidence:**

```markdown
Line 31: "What CLI tools already exist... How can this new specification integrate...?"
Line 40: "Dynamic Internal Path Resolution... implement a multi-tier path resolution check"
```

**Problem:**

- Lines 31-47 are **investigative behavior** that duplicates milestone-style user questioning
- Line 40 is **mechanical checking behavior** that should be handled by validators, not prompts

**Contract Violation:**
From `04-STAGE-PERSONAS.md`:

> **Generate-Specification — Systems Architect / Contract Decomposer:** ...The persona is not a second requirements interviewer. It does not gain permission to ask.

From `01-AEF-GENERATION-CONTEXT.md`:

> The milestone is the interactive requirements-convergence stage. Downstream stages are autonomous refinement stages.

**Actual Behavior:**

- Lines 31-47 **investigate** binary existence, naming conventions, toolchain integration
- Line 40 **manually checks** path resolution instead of trusting validators

**Why It's Harmful:**

- **Invents questions** that should be user-decided (naming conventions, toolchain cohesion)
- **Duplicates mechanical validation** that should be in `validate_metadata.py` or validators
- Encourages **hallucinated continuity** by solving design problems that belong to later stages

---

## 3. Missing Guarantees

### 3.1. Specification Readiness for Verification

**Evidence from improvements:**
From `06-GENERATION-SKILL-EVALUATION.md`:

> **Generate-Specification:** Check whether it: ...makes legitimate technical decisions; preserves upstream scope; avoids product-intent reconstruction; is sufficient for verification generation.

**Current Gaps:**

- **No check** that specification contains "sufficient information" for `generate-verification` to create meaningful verification items
- **No fail-fast** when specification lacks concrete contracts (CLI, schema, filesystem)
- **No tracing** that every functional requirement can be verified (not just observable)

**Impact:**
From `generate-verification` skill (lines 74-79):

> **The Fail-Closed Specification Gap Gate:** If the specification functional requirement represents an active tool or capability, but the specification lacks a concrete CLI contract, argument list, or output schema... you MUST immediately halt execution...

**This check exists in verification stage, NOT specification stage.**

**Proposed Behavior:**

- `generate-spec` should emit `#NEEDS-CLARIFICATION` when a functional requirement:
  - Lacks observable behavior definition
  - Is described only in prose without structured contract
  - Depends on unmotivated implementation details

---

### 3.2. Traceability Validation Within the Stage

**Evidence from improvements:**
From `05-ARTIFACT-TRACEABILITY.md`:

> Prompt vs Mechanical Enforcement: Use prompts for: reasoning; interpretation; responsibility boundaries; evidence handling; semantic correctness. Use mechanical enforcement for: required metadata; valid identifiers; schema shape; artifact location; structural validity; lineage format where validators support it.

**Current Gaps:**

- **Manual path resolution checks** (lines 40-43) duplicate mechanical enforcement
- **No validation** that `derived_from` properly links to milestone
- **No check** that `milestone_id` is consistent across functional requirements

**Impact:**

- Mechanical enforcement exists in `validate_metadata.py` but is duplicated in prompt text
- Downstream stages must re-check what should be validated earlier

---

### 3.3. Anti-Fabrication for Non-Functional Requirements

**Evidence from improvements:**
From `03-SKILL-IMPROVEMENT-PRINCIPLES.md`:

> **Anti-Fabrication:** Never create requirements, constraints, interfaces, acceptance criteria, or behavior merely to make an artifact look complete. A category may legitimately be: not applicable; inherited; unresolved; delegated to a downstream stage.

**Current Gaps:**

- **No explicit prohibition** on inventing Non-Functional Requirements (NFRs) just to fill sections
- **No distinction** between "not applicable" and "will be handled downstream"
- **No guidance** when NFR sections should be omitted entirely

**Example Risk:**

```
#### Non-Functional Requirements

- Performance: Should be fast (placeholder)
- Security: Should be secure (placeholder)
```

This is **fabrication**, not specification.

---

## 4. Hallucination and Unsupportable Assumptions

### 4.1. "Integration Cohesion" Fantasy

**Evidence:**
Lines 45-47: "How can this new specification integrate with these existing binaries to form a cohesive toolchain rather than an isolated silo?"

**Problem:**

- **Never user-confirmed** (not in milestone integration bindings)
- **Never project-evidence grounded** (no inspection of actual project structure required)
- **Invents design goals** (cohesion, silos) that don't exist

**Hallucinated Continuity:**
The skill **assumes** that "toolchain integration" is a valid requirement for specification generation, when it's actually:

- An implementation-level architectural concern
- A legitimate area for `implement-specification` to optimize
- Not a specification boundary (specifications define WHAT, not HOW to integrate)

---

### 4.2. "Naming Convention Discovery" Ascription

**Evidence:**
Lines 45-47: "What naming conventions, exit code patterns, and schemas are they using?"

**Problem:**

- **Ascribes motives** to existing binaries ("they are using" - who is "they"?)
- **Infers patterns** from binary existence without reading their implementation
- **Proposes standards** that may already exist but are not confirmed

**Hallucinated Constraint:**
By suggesting "analyze naming conventions," the skill:

1. Creates **pressure** to conform to conventions discovered in scan
2. Constrains `implement-specification` to use same conventions
3. Prevents legitimate innovation in downstream tooling

---

### 4.3. "Success Criteria as Commands" Template Filling

**Evidence:**
Line 55: "Name success criteria as commands whose output you can paste, not prose claims."

**Problem:**

- **Template-focused instruction** (pasteable commands vs prose)
- **Ignores cases where commands are inappropriate** (verification methods, environmental checks)
- **Encourages performative compliance** (fake commands that don't exist)

**Template-Filling Risk:**

```markdown
#### Acceptance Criteria

- [ ] `bin/omp-spec-tool --validate milestones/M10/M10S7.md` returns 0
- [ ] `bin/omp-spec-tool --format` produces YAML
```

If these binaries don't exist, the skill still encourages the template. This is **hallucinated infrastructure**.

---

## 5. Redundant and Harmful Instructions

### 5.1. Path Resolution (Lines 40-43)

**Current:**

```markdown
Dynamic Internal Path Resolution: When loading static framework assets (templates, contracts), implement a multi-tier path resolution check:

1. Local checkout search: ~/devcode/aef/agent/CONTRACTS/ and ~/devcode/aef/agent/templates/.
2. Executing directory search: Resolve relative to the executing skill directory.
3. Fallback plugin search: ~/.omp/plugins/node_modules/omp-aef/skills/generate-spec/CONTRACTS/.
```

**Problem:**

- **Mechanical enforcement** that should be in `validate_metadata.py` or implemented by the AEF framework
- **Specific paths hardcoded** (not project-agnostic)
- **Duplication** of what validators already check

**Why It's Harmful:**

- **Contradicts** `06-GENERATION-SKILL-EVALUATION.md: "A shorter skill is only better when its behavioral guarantees remain intact." This is repetitive boilerplate
- **Not invariant:** Different projects have different asset locations
- **Not traceable:** No validation of path resolution behavior

**Should Be:**
Remove entirely. Let validators or framework handle asset resolution.

---

### 5.2. "Briefly Evaluate" Sections (Lines 35-47)

**Current:**

```markdown
Inspect Existing Binaries (Fallback): If the milestone's Integration Bindings table is empty, scan the bin/ directory...
What CLI tools already exist?
```

**Problem:**

- **Implementation-level investigation** not required for specification
- **Duplicate of** `generate-verification`'s binary inspection (lines 44-48 of verification skill)
- **Encourages excessive questioning** (binary names, exit codes, schemas)

**Why It's Harmful:**

- **Increases cognitive load** without improving specification quality
- **Creates hand-off friction** (specification stage decides what binaries exist)
- **Violates responsibility boundary** (binary discovery belongs to verification/test stages)

**Should Be:**
Remove entirely. Specification should only reference binaries explicitly listed in milestone integration bindings.

---

### 5.3. "FR Assignment" (Lines 48-50)

**Current:**

```markdown
14. Assign FR IDs — Assign stable, sequential identifiers to all functional requirements (e.g., FR-1, FR-2).
15. Derive Functional Requirements (FRs) — Define what the system must do, assigning stable, sequential identifiers to each.
```

**Problem:**

- **Internal design decision** that belongs to `generate-verification` or `generate-tests`
- **Sequential numbering** constrains downstream traceability
- **No semantic value** (FR-1 vs FR-AFFECTED_MODULE)

**Why It's Harmful:**

- **Template-filling** encourages numbering for completeness
- **Prevents** more meaningful ID schemes (FR-READ_BUCKETING, FR-READ_QUERY)
- **Duplication** of work (verification stage also assigns IDs)

**Should Be:**
Remove FR assignment from spec generation. Let verification stage assign IDs with semantic meaning (FR-VAR-NAME, FR-SOURCE-COLUMN, etc.).

---

### 5.4. "Data Flow" Encouragement (Line 19)

**Current:**

```markdown
17. Define Data Flow — Describe how data moves through the system, if applicable.
```

**Problem:**

- **Architectural design** not specification
- **Implementation detail** (how, not what)
- **No boundary guidance** (what data moves? which modules? internal vs external?)

**Why It's Harmful:**

- Encourages **fake data flows** (illustrations, not contracts)
- **Reconstructs implementation** in specification artifact
- **Template-filling** (add section even if data flow is simple)

**Should Be:**
Remove entirely. Data flow is an implementation-level design concern.

---

## 6. Template-Filling Without Semantic Value

### 6.1. "Introspection & Code-Search Evidence" (Lines 99-105)

**Current:**

```markdown
## Introspection & Code-Search Evidence

- **Workspace Search Queries:** Document the exact semantic search commands executed during the compilation of this specification:
  - [ ] `search_code "<query_1>"` → Found: `path/to/file.ext`
  - [ ] `search_code "<query_2>"` → Found: `path/to/file.ext`
- **Inspected Signatures:** Document the existing interface contracts or helper functions analyzed before drafting:
  - E.g., Analysed JSON schema of bin/omp-discover to align bin/omp-test profiling.
```

**Problem:**

- **Self-aggrandizing** (what searches did you run?)
- **Template-filling pressure** (add queries even if none needed)
- **Redundant** (verification stage should trace requirements to specs, not searches)

**Template-Filling Risk:**

```markdown
## Introspection & Code-Search Evidence

- **Workspace Search Queries:** Document the exact semantic search commands executed during the compilation of this specification:
  - [ ] `search_code "approve" → Found: bin/omp-test`
  - [ ] `search_code "allowance" → Found: bin/omp-approve`
```

These searches are **hallucinated** - no one actually ran them, they're just placeholders to look like the section is "filled."

**Why It's Harmful:**

- **Fills template fields** without semantic value
- **Illusion of rigor** (shows "I investigated code" when I didn't)
- **Consumes space** in spec artifact for no purpose
- **Duplication** of traceability that exists elsewhere

**Should Be:**
Remove entirely. Verification stage already performs traceability checking. No need to document searches in specification.

---

### 6.2. "Acceptance Criteria as Commands" (Line 55)

**Current:**

```markdown
18. Clear Criteria — Name success criteria as commands whose output you can paste, not prose claims.
```

**Problem:**

- **Command-focused** instead of **evidence-focused**
- **Ignores cases where commands are inappropriate** (verification methods, constraints)
- **Template-filling pressure** (add commands even if they don't exist)

**Template-Filling Risk:**

```markdown
#### Acceptance Criteria

- [ ] `bin/omp-spec-tool --validate milestones/M10/M10S7.md` returns 0
- [ ] `bin/omp-spec-tool --format` produces YAML
```

If these binaries don't exist, the skill still encourages the template. This is **hallucinated infrastructure**.

**Why It's Harmful:**

- **Illusion of verifiability** (commands exist, don't they?)
- **Prevents** meaningful acceptance criteria (observable states, not command invocations)
- **Reconstructs implementation** (defines tools that don't exist)

**Should Be:**
Change to: "Name success criteria as observable system states or artifacts, not prose claims or command invocations."

---

### 6.3. "Next Steps" (Line 129)

**Current:**

```markdown
Advise running `generate-verification` to create the verification protocol.
```

**Problem:**

- **Generic handoff** (no value added)
- **Repetitive** (handoff exists via artifact metadata)
- **No guidance** (how does verification relate to this spec?)

**Why It's Harmful:**

- **Template-filling** (just copy-paste instruction)
- **No substantive guidance** (what makes this spec suitable for verification?)
- **Redundant** (verification contract exists in derived_from, no need to repeat)

**Should Be:**
Remove or replace with: "Ensure specification contains concrete contracts (CLI, schema, filesystem) that enable deterministic verification."

---

## 7. Unnecessary User Questioning

### 7.1. "Integration Cohesion" Questions (Lines 45-47)

**Current:**

```markdown
Inspect Existing Binaries (Fallback): If the milestone's Integration Bindings table is empty, scan the bin/ directory...
What CLI tools already exist (e.g., bin/omp-discover, bin/omp-verify-metadata)?
What naming conventions, exit code patterns, and schemas are they using?
How can this new specification integrate with these existing binaries to form a cohesive toolchain rather than an isolated silo?
```

**Problem:**

- **Unnecessary questions** (naming conventions, toolchain cohesion)
- **Not evidence-based** (no investigation required to answer)
- **Not user-confirmed** (not in milestone integration bindings)

**Questioning Pattern Violation:**
From `01-AEF-GENERATION-CONTEXT.md`:

> A halt is preferable to hallucinated continuity.

**Why It's Harmful:**

- **Invents questions** that should be answered by user (naming conventions, toolchain goals)
- **Creates friction** (user must answer questions not in scope)
- **Reduces autonomy** (verification/test stages must wait for specification stage to decide integration)

**Should Be:**
Remove entirely. Specification should NOT decide toolchain cohesion or naming conventions. These are implementation decisions.

---

### 7.2. "Dynamic Path Resolution" Questions (Lines 40-43)

**Current:**

```markdown
Dynamic Internal Path Resolution: When loading static framework assets (templates, contracts), implement a multi-tier path resolution check:

1. Local checkout search: ~/devcode/aef/agent/CONTRACTS/ and ~/devcode/aef/agent/templates/.
2. Executing directory search: Resolve relative to the executing skill directory.
3. Fallback plugin search: ~/.omp/plugins/node_modules/omp-aef/skills/generate-spec/CONTRACTS/.
```

**Problem:**

- **Mechanical checks** that should be validators, not skill prompts
- **Path details** not generic (specific to current dev environment)
- **Not evidence-based** (no need to "implement" checks in prompt)

**Questioning Pattern Violation:**
From `03-SKILL-IMPROVEMENT-PRINCIPLES.md`:

> **Implementation Independence:** Do not invent implementation decisions merely to make a contract concrete.

**Why It's Harmful:**

- **Invents mechanical checks** (path resolution) that validators should handle
- **Guides by implementation** (how to check paths) instead of contract (assets must exist)
- **Reduces traceability** (no validation of path resolution behavior)

**Should Be:**
Remove entirely. Let validators handle asset resolution.

---

## 8. Artifact Usefulness for generate-verification

### 8.1. Strong Contract Representation

**Evidence:**
The generated specs (`M10S10.md`, `M10S7.md`) demonstrate:

1. **Observable behavior definition:**
   - CLI contracts with exit codes (FR-1, FR-2, FR-3 in M10S7)
   - Schema requirements (FR-1, FR-2, FR-3 in M10S7)
   - File existence requirements (FR-1 in M10S10)

2. **Concrete interfaces:**
   - Command-line contracts (e.g., `bin/omp-verify-readiness --spec ...`)
   - Output schema requirements (not just prose descriptions)

3. **Explicit failure conditions:**
   - Exit codes specified for all requirements
   - Error states defined (missing approval stamp, invalid test state)

**Conclusion:** These specifications ARE useful to `generate-verification`. They provide clear boundaries for verification item creation.

---

### 8.2. Remaining Gaps

**Evidence from generate-verification skill:**
Lines 74-79: Specification Gap Gate requires **concrete CLI contracts, argument lists, or output schemas**.

**Current Specification Quality:**

- **M10S10.md:** Has CLI contracts (exit codes 0, 1, 2) - Sufficient
- **M10S7.md:** Has CLI contracts with explicit exit codes and argument paths - Sufficient

**Gap Analysis:**
The current specifications **DO meet** the "concrete contract" requirement. However, the `generate-spec` skill **does not guarantee** this in all cases:

**Risk:**

```markdown
#### Functional Requirements

- FR-1: The system must handle errors gracefully.
- FR-2: Performance should be acceptable.
- FR-3: Security measures must be in place.
```

This spec **cannot** be verified because it lacks:

- Concrete behavior definition
- Observable criteria
- Exit codes or schema requirements

**Current Skill Weakness:**
The skill says "assign FR IDs" and "derive FRs" but **does NOT enforce** that FRs must be:

- Observable
- Structurally defined
- Non-prose

**Should Be:**
Add explicit guidance: "Every functional requirement MUST define an observable boundary (CLI contract, schema, or filesystem state). Prose requirements must be converted into structured contracts or marked `N/A`."

---

### 8.3. Traceability Quality

**Strengths:**

- Clear `derived_from` linkage to milestone
- Stable FR IDs
- Traceable to verification items

**Weakness:**

- No validation that all requirements are traceable
- No check that FR IDs match verification requirements

**Should Be:**
Add post-generation check: "Ensure every functional requirement can be mapped to a verification item. Requirements with no verification path must be marked `N/A`."

---

## 9. Instruction Classification

### 9.1. Invariant Instructions (Must Preserve)

| Instruction                                 | Why It's Invariant                                          |
| ------------------------------------------- | ----------------------------------------------------------- |
| YAML frontmatter enclosure (lines 17-22)    | Mechanical schema enforcement, prevents malformed artifacts |
| Non-placeholder FR assignment (lines 14-51) | Guarantees stable traceability, prevents TODO leaks         |
| Observable behavior mandates (lines 52-53)  | Prevents prose requirements, ensures verifiability          |
| Negative guardrails (lines 74-78)           | Prevents cross-spec duplication, prose contracts            |
| Mechanical postconditions (lines 22-24, 69) | Guarantees write succeeded, no placeholders remain          |
| Multi-tier path resolution (lines 40-43)    | Asset loading reliability (despite being redundant)         |

---

### 9.2. Recommended Instructions (Should Retain with Refinement)

| Instruction                                           | Current Problem                                  | Recommended Change                                                       |
| ----------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------ |
| "Describe how data moves" (line 19)                   | Architectural design, not spec                   | Remove entirely                                                          |
| "Assign FR IDs" (lines 48-50)                         | Implementation detail, sequential                | Remove FR assignment from spec; keep only FR derivation                  |
| "Inspect Existing Binaries" (lines 31-47)             | Implementation investigation, toolchain cohesion | Remove entirely; specs reference binaries only from integration bindings |
| "Dynamic Path Resolution" (lines 40-43)               | Mechanical check, project-specific               | Remove; let validators handle                                            |
| "Introspection & Code-Search Evidence" (lines 99-105) | Template-filling, redundant                      | Remove entirely                                                          |

---

### 9.3. Context-Dependent Instructions (Should Be Removed)

| Instruction                                 | Why It's Context-Dependent         | Removal Reason                                         |
| ------------------------------------------- | ---------------------------------- | ------------------------------------------------------ |
| "Integration cohesion" (lines 45-47)        | Binary inspection, toolchain goals | Not user-confirmed, not in milestone scope             |
| "Naming convention discovery" (lines 45-47) | Infer patterns from binaries       | Not evidence-based, hallucinated constraints           |
| "Success criteria as commands" (line 55)    | Command-centric focus              | Ignores verification methods, encourages fake binaries |

---

### 9.4. Harmful/Redundant Instructions

| Instruction                                           | Harmfulness                           | Redundancy                             | Action |
| ----------------------------------------------------- | ------------------------------------- | -------------------------------------- | ------ |
| "Dynamic Path Resolution" (lines 40-43)               | Mechanical duplication                | Already in validators                  | Remove |
| "Inspect Existing Binaries" (lines 31-47)             | Implementation investigation          | Verification stage does this           | Remove |
| "Introspection & Code-Search Evidence" (lines 99-105) | Template-filling, no semantic value   | Duplicate of verification traceability | Remove |
| "FR Assignment" (lines 48-50)                         | Sequential IDs, constrains downstream | Verification stage also assigns IDs    | Remove |
| "Data Flow" (line 19)                                 | Architectural design                  | Implementation concern                 | Remove |

---

## 10. Protected Behavior Summary

### Core Behavioral Invariants

| Behavior                                                              | Preservation Priority | Rationale                                             |
| --------------------------------------------------------------------- | --------------------- | ----------------------------------------------------- |
| **Mechanical YAML frontmatter enclosure**                             | **Critical**          | Prevents malformed artifacts, ensures schema validity |
| **Non-placeholder FR assignment**                                     | **Critical**          | Guarantees stable traceability IDs                    |
| **Observable behavior mandates**                                      | **Critical**          | Prevents prose requirements, ensures verifiability    |
| **Negative guardrails (no cross-spec duplication)**                   | **Critical**          | Prevents scope creep                                  |
| **Mechanical postconditions (write verification, placeholder check)** | **Critical**          | Ensures artifact completeness                         |
| **Strict file scope boundaries**                                      | **High**              | Maintains isolation between specifications            |

### Must Not Change Despite Appearance Redundant

1. **Mechanical write verification** (lines 22-23)
   - Even though validators exist, this guarantees file integrity before handoff

2. **Placeholder detection** (line 24)
   - Prevents TODO leaks from reaching implementation stage
   - Critical anti-fabrication mechanism

3. **YAML frontmatter format** (lines 17-22)
   - Enforces specific structure needed for downstream parsing
   - Different from what validators expect

---

## 11. Proposed Improvement Areas

### 11.1. Add Specification Readiness Check

**Current:**
Specs can contain prose requirements without observable contracts.

**Proposed:**

```markdown
Before finalizing, ensure every functional requirement:

1. Defines an observable boundary (CLI, schema, or filesystem state)
2. Does NOT depend on prose descriptions
3. Is either traceable to a verification item or marked N/A
```

**Impact:**

- Fails closed on incomplete specs
- Prevents verification stage from inventing verification items
- Encourages concrete contracts from the start

---

### 11.2. Remove Implementation-Level Investigation

**Current:**
Skill investigates binary existence, naming conventions, toolchain cohesion.

**Proposed:**
Remove all investigation of existing binaries (lines 31-47). Specification should only reference binaries explicitly listed in milestone integration bindings.

**Impact:**

- Reduces cognitive load
- Maintains responsibility boundary
- Prevents unnecessary user questioning

---

### 11.3. Remove Template-Filling Instructions

**Current:**
"Add queries to Introspection section", "Name criteria as commands"

**Proposed:**
Remove "Introspection & Code-Search Evidence" section entirely. Replace "Success criteria as commands" with "Observable system states or artifacts".

**Impact:**

- Eliminates template-filling pressure
- Reduces artifact bloat
- Encourages meaningful content

---

### 11.4. Add Traceability Post-Check

**Current:**
No check that all requirements can be verified.

**Proposed:**
After generating FRs, verify:

1. Every FR has a clear contract (CLI/schema/filesystem)
2. No FRs rely solely on prose
3. Unverifiable FRs are marked N/A

**Impact:**

- Ensures spec completeness
- Prevents verification gaps
- Provides clear spec quality metrics

---

### 11.5. Remove FR ID Assignment from Spec

**Current:**
Spec skill assigns sequential FR IDs (FR-1, FR-2, etc.).

**Proposed:**
Spec skill only derives FRs. Verification skill assigns IDs with semantic meaning (FR-READ_BUCKETING, FR-READ_QUERY, etc.).

**Impact:**

- Increases traceability semantic value
- Reduces duplication (verification also assigns IDs)
- Allows more meaningful categorization

---

### 11.6. Clarify "Data Flow" Removal

**Current:**
Skill encourages "Describe how data moves".

**Proposed:**
Remove data flow encouragement entirely. If needed, add constraint: "If data flow is a critical architectural concern, defer to implementation stage."

**Impact:**

- Removes architectural design from specification
- Preserves requirement boundary
- Reduces template-filling

---

## 12. Regression Risks

### 12.1. Risk of Removing "Inspection of Existing Binaries"

**Current Behavior:**

- Specification stage decides which binaries exist and how they're named
- Verification stage inherits these decisions without challenge

**Potential Regression:**
If we remove binary inspection, specs may:

- Miss existing binaries not in integration bindings
- Redefine interfaces that already exist
- Create conflicts with downstream tooling

**Mitigation:**

- Ensure milestone integration bindings table is comprehensive
- Add explicit warning: "Do NOT redefine binaries already existing in bin/ unless user explicitly lists them in integration bindings"
- Let verification stage flag conflicts

---

### 12.2. Risk of Removing "Introspection & Code-Search Evidence"

**Current Behavior:**

- Shows "investigation rigor" in spec artifact
- Documented search commands for traceability

**Potential Regression:**
If we remove this section:

- Specs may lose "investigation trail"
- Traceability may feel less rigorous
- Users may miss documentation of how spec was derived

**Mitigation:**

- Verification stage already performs traceability checks
- If needed, add "Derived From" metadata showing milestone and integration bindings (already exists)
- Trust traceability mechanism rather than prose documentation

---

### 12.3. Risk of Removing "FR ID Assignment"

**Current Behavior:**

- Sequential FR IDs provide stable traceability
- Downstream tools rely on FR numbering

**Potential Regression:**
If we remove FR assignment:

- Verification stage must invent IDs
- Traceability may lose numeric clarity
- Tests may reference "FR-1" generically

**Mitigation:**

- Verification stage can still assign IDs (current behavior)
- Semantic IDs (FR-READ_BUCKETING) are more meaningful than sequential
- Tests can reference FR semantic names, not numbers

---

### 12.4. Risk of Over-Restricting Spec Quality

**Current Behavior:**

- Skill encourages "data flow", "integration cohesion"
- Allows some architectural design in specs

**Potential Regression:**
If we remove these:

- Specs may be too narrow (only functional requirements)
- Missing critical architectural context
- Implementation may face ambiguity

**Mitigation:**

- Distinguish "requirements" from "constraints" clearly
- Allow architectural constraints (not design decisions) in specs
- Add explicit guidance: "Architecture Impact section may include constraints, not design choices"

---

### 12.5. Risk of Reducing "Observable Behavior" Enforcement

**Current Behavior:**

- Skill explicitly mandates observable behavior contracts
- Strong enforcement of no prose requirements

**Potential Regression:**
If we weaken this:

- Prose requirements may creep back in
- Verification stage burden increases
- Spec quality degrades

**Mitigation:**

- Keep "Observable behavior mandates" as invariant instruction
- Add post-generation check: "Verify no prose requirements exist"
- Rely on verification stage to flag prose requirements

---

## 13. Mechanical Enforcement Existing

### 13.1. Already Enforced by Validators

| Mechanism               | Current Enforcement    | Why Prompt Should Not Duplicate                |
| ----------------------- | ---------------------- | ---------------------------------------------- |
| YAML frontmatter schema | `validate_metadata.py` | Prevents schema errors, mechanical enforcement |
| Artifact location       | Framework validation   | Ensures specs in correct directory             |
| Traceability format     | Framework parsing      | Validates `derived_from` structure             |
| Template version        | Schema checks          | Ensures template compatibility                 |

**Recommendation:** Keep prompt instructions for _behavior_ (reasoning, responsibility boundaries), not _mechanical checks_ (schema, location). Let validators handle enforcement.

---

### 13.2. Already Handled by Downstream Stages

| Behavior                   | Current Handoff         | Why Prompt Should Not Redo              |
| -------------------------- | ----------------------- | --------------------------------------- |
| Binary inspection          | `generate-verification` | Should investigate verification targets |
| Traceability checking      | `generate-tests`        | Should map to test scripts              |
| ID assignment              | `generate-verification` | Should assign semantic IDs              |
| Verification item creation | `generate-tests`        | Should plan test files                  |

**Recommendation:** Remove "inspection" sections from spec skill. Let downstream stages perform their own investigation based on spec contracts.

---

### 13.3. Already Implemented in Framework

| Behavior          | Framework Implementation  | Why Prompt Should Not Redo          |
| ----------------- | ------------------------- | ----------------------------------- |
| Path resolution   | AEF asset loader          | Framework manages assets, not skill |
| Template loading  | Framework template system | Framework handles rendering         |
| Artifact creation | Framework file writing    | Framework ensures atomic writes     |

**Recommendation:** Remove "dynamic path resolution" instructions. Let framework handle asset loading transparently.

---

## 14. Summary of Critical Findings

### 1. What the current skill already guarantees

- **Mechanical correctness** (YAML enclosure, write verification, placeholder detection)
- **Observable behavior contracts** (no prose requirements)
- **Strict file scope boundaries** (allowlist/denylist enforcement)
- **Anti-hallucination** (no placeholder comments, no arbitrary additions)
- **Traceability** (stable IDs, derived_from lineage)

### 2. What behavior is valuable and must be preserved

- Frontmatter enclosure (mechanical schema enforcement)
- FR derivation (without assignment of sequential IDs)
- Observable behavior mandates
- Negative guardrails (no cross-spec duplication)
- Mechanical postconditions
- Strict file scope

### 3. What behavior conflicts with the AEF pipeline contract

- **Implementation-level investigation** (binary inspection, toolchain cohesion)
- **Architectural design** (data flow, naming conventions)
- **Excessive questioning** (unnecessary user questions)
- **Template-filling instructions** (queries, commands as placeholders)
- **FR ID assignment** (sequential numbering constrains downstream)
- **Mechanical checks** (path resolution, search documentation)

### 4. What behavior is missing relative to generation context

- **Specification readiness check** (all FRs must be verifiable)
- **Traceability validation within stage** (check all FRs have contracts)
- **Anti-fabrication for NFRs** (no dummy sections)
- **Clear N/A handling** (requirements not applicable to verification)

### 5. Where the skill encourages hallucination

- **Integration cohesion** (invents toolchain goals, not in milestone)
- **Naming convention discovery** (ascribes patterns from binaries)
- **Fake binaries** (success criteria as commands that don't exist)
- **Template-filling queries** (search commands, paths added without investigation)

### 6. Where the skill encourages unsupported assumptions

- **Binary integration as required** (not user-confirmed)
- **Sequential FR IDs as mandatory** (legitimate design choice)
- **Data flow as always needed** (implementation detail, not requirement)

### 7. Where the skill encourages downstream reconstruction

- **Toolchain cohesion decisions** (implementation approach, not spec)
- **Naming conventions** (design decision, not requirement)
- **Binary existence** (verification stage should discover, not spec)

### 8. Where the skill encourages unnecessary user questioning

- **Integration cohesion questions** (binary existence, toolchain goals)
- **Path resolution checks** (mechanical, not user-driven)
- **Naming convention discovery** (not user-confirmed, not evidence-based)

### 9. Where the skill encourages implementation leakage

- **Data flow descriptions** (architectural design in spec)
- **Command-based acceptance criteria** (implementation tricks, not requirements)
- **Binary inspection** (implementation-level investigation in spec stage)

### 10. Where the skill encourages template-filling without semantic value

- **Introspection & code-search evidence** (queries that don't exist)
- **Acceptance criteria as commands** (fake command examples)
- **Next steps** (generic handoff text)

### 11. Whether the current skill's artifact is actually useful to generate-verification

**YES.** The generated specs (M10S10.md, M10S7.md) contain:

- Concrete CLI contracts with exit codes
- Observable behavior definitions
- Explicit failure conditions
- Traceable FR IDs
- Strict file scope boundaries

**Gaps:**

- No guarantee that ALL specs meet this quality (can contain prose requirements)
- No check that all FRs are verifiable

### 12. Which instructions are invariant

- YAML frontmatter enclosure
- Non-placeholder FR assignment (derivation, not ID assignment)
- Observable behavior mandates
- Negative guardrails
- Mechanical postconditions
- Strict file scope

### 13. Which instructions are recommended

- **Keep** observable behavior enforcement
- **Keep** negative guardrails
- **Remove** all implementation-level investigation
- **Remove** template-filling sections
- **Remove** FR ID assignment (keep only derivation)

### 14. Which instructions are context-dependent

- Binary inspection (remove)
- Data flow descriptions (remove)
- Integration cohesion questions (remove)
- Naming convention discovery (remove)

### 15. Which instructions are harmful/redundant

- Path resolution checks (mechanical duplication)
- Existing binary inspection (implementation investigation)
- Introspection & code-search evidence (template-filling, no value)
- FR ID assignment (sequential, constrains downstream)
- Data flow (architectural design, not spec)

### 16. What mechanical enforcement already exists

- YAML frontmatter schema (validators)
- Artifact location (framework validation)
- Traceability format (framework parsing)
- Template version (schema checks)
- Asset loading (framework asset loader)

**Should not be duplicated in prompt.**

---

## 15. Final Recommendation Priority

### Immediate (Must Do)

1. **Add specification readiness check** (all FRs must be verifiable)
2. **Remove implementation-level investigation** (binary inspection, toolchain cohesion)
3. **Remove template-filling sections** (Introspection, generic handoff)

### High Priority

4. **Remove FR ID assignment** (keep only FR derivation)
5. **Clarify "Data Flow" encouragement** (remove entirely or constrain heavily)
6. **Strengthen observable behavior mandates** (add post-check)

### Medium Priority

7. **Add traceability validation within spec** (check all FRs have contracts)
8. **Remove mechanical path resolution** (let framework handle)
9. **Clarify NFR handling** (explicit N/A, not placeholder sections)

### Low Priority

10. **Review negative guardrails** (ensure none are redundant)
11. **Optimize FR derivation** (semantic vs sequential)

---

## 16. Regression Risk Summary

**Highest Risk:** Removing implementation-level investigation
**Mitigation:** Rely on milestone integration bindings + verification stage investigation

**High Risk:** Removing FR ID assignment
**Mitigation:** Verify verification stage can handle ID assignment with semantic meaning

**Medium Risk:** Removing template-filling sections
**Mitigation:** Trust traceability mechanism, rely on verification stage to enforce rigor

**Low Risk:** Removing mechanical checks
**Mitigation:** Validators handle enforcement, not skill prompts
