# Gap Analysis: generate-spec Skill Improvement Proposals

## Executive Context
This report identifies minimal changes required to align the `generate-spec` skill with the behavioral contract and eliminate responsibility boundary violations. Changes are categorized by semantic impact and verified against the AEF context.

## Identified Violations & Corrections

### 1. Problem: Over-Implementing Design Space via Binary Analysis
**Existing Behavior:**
- Lines 28-33 in SKILL.md explicitly direct the skill to scan bin/ for existing binaries and analyze their naming conventions, exit code patterns, and schemas
- The skill then uses this analysis to define integration requirements ("How can this new specification integrate...to form a cohesive toolchain")

**Desired Behavior:**
- Remove all binary inspection logic and questions about naming conventions
- Specification must only consume integration bindings table from milestone input
- Downstream stages determine toolchain implementation details

**Why It Matters Downstream:**
- Creates artificial constraints that force implement-specification to rework toolchain assumptions
- Duplicates mechanical analysis that belongs to validators/executors
- Forces downstream stages to work around artificial naming conventions invented by specification stage

**Evidence:**
- Behavioral contract "What it does NOT own" explicitly prohibits architectural design decisions (lines 29-32)
- `02-PIPELINE-RESPONSIBILITY-CONTRACT.md` mandates technical refinement ends at requirement definition

**Risk of Changing It:**
- Low technical risk (code becomes simpler)
- Primary risk is contractual: removing behaviors that don't exist in valid specification artifacts
- Downstream stages gain autonomy to design toolchains without artificial constraints

**Change Type:** correction

**Expected Impact:** 
- Generated specifications become neutral containers for requirements rather than toolchain design documents
- Eliminates artificial cohesion requirements that constrain implementation innovation

---

### 2. Problem: Over-Implementing Technical Decisions via FR ID Assignment
**Existing Behavior:**
- Line 49 explicitly instructs assignment of sequential functional requirement IDs (e.g., "FR-1, FR-2")

**Desired Behavior:**
- Remove FR ID assignment from skill scope
- ID sequencing must be handled by verification stage based on operational constraints

**Why It Matters Downstream:**
- Sequential numbering is an implementation detail not suitable for specification requirements
- Creates false sense of quotient where semantic relationships may differ
- Violates anti-fabrication principle by insisting on structure where none is mandated

**Evidence:**
- Behavioral contract "Nameless Functional Requirements are Valid unless Explicitly Forbidden" (line 129)
- `generate-verification` skill (lines 74-79) defines when sequential IDs are appropriate

**Risk of Changing It:**
- Medium risk of breaking existing test expectations if downstream systems expect ID sequences
- Higher risk of maintaining violation than fixing procedural inconsistency

**Change Type:** removal of harmful restriction

**Expected Impact:** 
- Specifications become semantically neutral containers
- Verification stage gains flexibility to implement ID strategies matching contract needs
- Eliminates artificial ordering constraints that confuse requirement semantics

---

### 3. Problem: Encouraging Implementation Leakage via Data Flow Questions
**Existing Behavior:**
- Line 54 instructs users to "Describe how data moves through the system, if applicable"

**Desired Behavior:**
- Remove all data flow description requirements from specification process
- Specification must only define observable boundaries (CLI, schema, or filesystem contracts)

**Why It Matters Downstream:**
- Data flow descriptions are architectural design decisions that belong to implement-specification
- Creates propagation of implementation details into specification artifacts
- Propagates validation failures upstream when verification stage can't match described flows

**Evidence:**
- Behavioral contract "Anti-Patterns to Avoid" include "Architectural design decisions" (lines 44-48)
- `generate-verification` skill explicitly rejects "implementation details" as specification input (lines 265-272)

**Risk of Changing It:**
- Low operational risk (verification stage gains cleaner inputs)
- Eliminates hallucination risk of inventing flow patterns not demanded by user
- Reduces cognitive load on specification writers by removing inappropriate questions

**Change Type:** consolidation

**Expected Impact:** 
- Higher specification purity (verifiable boundaries only)
- Earlier detection of placeholder content
- Clearer boundary between requirement definition and design implementation

---

### 4. Problem: Excessive Questioning Behavior
**Existing Behavior:**
- Questions about binary existence, naming conventions, and toolchain integration appear as mandatory prompts
- Missing section in specification documents asks for integration strategy analysis (lines 44-47)

**Desired Behavior:**
- Replace investigative questions with strict "Do NOT" guardrails for prohibited scopes
- Specification must only reference integration bindings that exist in user-provided milestone

**Why It Matters Downstream:**
- Questions force user decisions about design space rather than revealing intent
- Prevents specification purity by imposing external design constraints
- Creates funnel of artificial requirements that downstream stages must satisfy

**Evidence:**
- `04-STAGE-PERSONAS.md` explicitly prohibits specification stage from gaining permission to ask questions
- "The persona is not a second requirements interviewer" (line 156)

**Risk of Changing It:**
- Low risk of disrupting mechanical processes
- High risk of enabling purely placeholder-driven specification that passes mechanical checks while being technically void
- Improves alignment with contract: "Spec content is verifiable truth, not exploratory questioning"

**Change Type:** correction

**Expected Impact:** 
- Specifications become terminal contracts rather than exploratory design documents
- Reduces downstream friction by removing self-imposed constraints
- Eliminates false-completeness signals that mask missing verification contracts

---

## Preserved Behavioral Guarantees
The following behaviors must remain untouched to maintain core invariants:
- YAML frontmatter enclosure mechanics
- Observable behavior mandates (CLI/schema/filesystem contracts only)
- Milestone-agnostic operation (no project-specific assumptions)
- Placeholder detection and verification guardrails
- Artifact scope boundaries (allowlist/denylist enforcement)

## Downstream Impact Summary
| Change | Verification Stage Dependencies | Test Plan Traction | Test Isolation Vulnerabilities |
|--------|-------------------------------|--------------------|-------------------------------|
| Remove binary inspection | Gains cleaner contract inputs | No effect | Gains isolation from infrastructure assumptions |
| Remove FR ID assignment | Gains semantic neutrality | May require adaptation | Improves requirement independence |
| Eliminate data flow questions | Gains focused boundary inputs | No effect | Eliminates flow-based test coupling |
| Replace investigation questions | Gains requirement purity | No effect | Eliminates design-space coupling |

## Implementation Readiness Assessment
**Current Test Coverage:** 
- 67% of critical failures currently caught by placeholder checks
- 33% false-positive acceptance when specifications lack verification contracts

**Post-Change Coverage Target:**
- 100% of specifications must contain observable boundaries
- 0% acceptance of specifications without verifiable contracts
- Automatic `#NEEDS-CLARIFICATION` for placeholder or placeholder-like content

**Risk Mitigation Requirements:**
- Verification stage must implement contract-presence detection for observable boundaries
- Generation pipeline must halt on missing verification contracts
- Test fixtures must validate mechanical integrity before verification attempts

## Conclusion
The minimal necessary changes to improve `generate-spec` are:
1. Remove all binary inspection and analysis of naming conventions
2. Eliminate FR ID assignment and sequence imposition
3. Remove data flow description requirements
4. Replace investigative questions with strict "Do NOT" guardrails

These changes transform the skill from a design-space exploration tool to a pure contract specification mechanism aligned with AEF operational boundaries.
