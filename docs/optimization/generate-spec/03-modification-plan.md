# Phased Modification Plan for generate-spec Skill

## Phase 1: Eliminate Binary Analysis

**Behavioral Objective:**
Remove all binary inspection and naming convention analysis from specification generation. The skill must only consume integration bindings from the milestone input.

**Affected Sections:**
- Lines 28-33 in SKILL.md (`bin/` scanning, naming convention analysis, toolchain integration questions)
- Step 2 in "Your Process" (Integration Bindings Table handling)
- Step 3 in "Your Process" (Inspect Existing Binaries - Fallback)

**Rules Removed:**
- Step 3 entirely: "Inspect Existing Binaries (Fallback)" with sub-bullets about CLI tools, naming conventions, exit code patterns, and toolchain integration
- Step 2's clause: "If the milestone's Integration Bindings table is empty, scan the `bin/` directory..."
- Questions about "What CLI tools already exist?", "What naming conventions...?", "How can this new specification integrate with these existing binaries...?"

**Rules Added:**
- "Do NOT analyze bin/ directory contents"
- "Do NOT inquire about binary naming conventions"
- "Do NOT analyze exit code patterns from binaries"
- "Do NOT define toolchain integration strategies"
- "Specification MUST only consume integration bindings explicitly listed in the milestone's Integration Bindings table"

**Rules Modified:**
- Step 2: Remove fallback to bin/ scanning; if Integration Bindings table is empty, specification proceeds with only milestone-declared bindings

**Rules Consolidated:**
- None (this phase removes, does not consolidate)

**Existing Behavior Explicitly Protected:**
- YAML frontmatter enclosure mechanics (lines 17-24)
- Observable behavior mandates (CLI/schema/filesystem contracts only) (line 13)
- Milestone-agnostic operation (line 76 in behavioral contract)
- Placeholder detection and verification guardrails (lines 69, 22-23)
- Artifact scope boundaries (allowlist/denylist enforcement) (lines 15-16, 141-147)

**Regression Risk:**
- Low technical risk (code becomes simpler)
- Primary risk is contractual: removing behaviors that don't exist in valid specification artifacts
- Downstream stages gain autonomy to design toolchains without artificial constraints

**Validation Required After Phase:**
- Generate a test specification from a milestone with empty Integration Bindings table
- Verify no binary-related queries appear in the output
- Verify placeholder check still triggers on incomplete specifications
- Verify YAML frontmatter is correctly generated

---

## Phase 2: Eliminate FR ID Assignment

**Behavioral Objective:**
Remove sequential FR ID assignment (FR-1, FR-2, etc.) from specification generation. FR ID strategy must be deferred to the verification stage.

**Affected Sections:**
- Line 49 in SKILL.md: "Assign FR IDs — Assign stable, sequential identifiers to all functional requirements (e.g., FR-1, FR-2)"
- Line 50 in SKILL.md: "Derive Functional Requirements (FRs) — Define what the system must do, assigning stable, sequential identifiers to each"
- Lines 226-227 in behavioral contract: "Do NOT assign sequential FR IDs (implementation detail)"
- Line 248 in behavioral contract: "Stable FR IDs (sequential or semantic, but consistent)" — must be interpreted as "verification stage assigns"

**Rules Removed:**
- Sequential FR ID assignment (FR-1, FR-2, FR-3...)
- Logic that derives FR IDs from requirement order
- Requirement that every FR must have a sequential numeric ID

**Rules Added:**
- "FR IDs must be managed by the verification stage"
- "Functional requirements must be identified by descriptive, stable titles without implicit sequencing"
- "The specification must not impose an ID sequencing strategy"

**Rules Modified:**
- Step 14 (Assign FR IDs): Remove entirely
- Step 15 (Derive Functional Requirements): Remove "assigning stable, sequential identifiers to each"; replace with "Each functional requirement MUST define an observable boundary..."

**Rules Consolidated:**
- Combine Step 14 and Step 15 into a single step: "Derive Functional Requirements — Define what the system must do. Each requirement MUST define an observable boundary (CLI, schema, or filesystem contract)."

**Existing Behavior Explicitly Protected:**
- Observable behavior mandates for functional requirements (Step 15, lines 51-53)
- Prohibition on placeholders in requirements (Step 15, line 51)
- Traceability lineage (`derived_from`) (line 25 in behavioral contract)
- Requirement that FRs define observable boundaries (lines 129-134 in behavioral contract)

**Regression Risk:**
- Medium risk of breaking existing test expectations if downstream systems expect ID sequences
- Higher risk of maintaining violation than fixing procedural inconsistency
- May require adaptation in verification stage

**Validation Required After Phase:**
- Generate a test specification
- Verify no FR- prefixed IDs appear in functional requirements
- Verify all functional requirements still define observable boundaries
- Verify traceability through requirement titles rather than FR IDs

---

## Phase 3: Eliminate Data Flow Questions

**Behavioral Objective:**
Remove data flow description requirements from specification generation. Focus exclusively on observable boundaries (CLI, schema, filesystem contracts).

**Affected Sections:**
- Line 54 in SKILL.md: "Define Data Flow — Describe how data moves through the system, if applicable"
- Lines 149-152 in behavioral contract: Data Flow Section marked "NOT RECOMMENDED"
- Lines 79-80 in gap analysis: Data flow description is architectural design

**Rules Removed:**
- "Describe how data moves through the system, if applicable"
- All questions about data transformation pathways
- The entire Data Flow section from the specification template output

**Rules Added:**
- "Specification must only define observable boundaries (CLI Executable Contract, Structured Schema Contract, or Filesystem State Contract)"
- "Data flow descriptions are architectural design decisions, not specification requirements"
- "If data flow section is included in template, it MUST describe interface boundaries and data transformations (requirement boundary), NOT implementation data movement"

**Rules Modified:**
- Step 17 (Define Data Flow): Remove entirely or convert to "Define Interface Boundaries — Specify the contract boundaries between components"

**Rules Consolidated:**
- Consolidate data flow concerns into Functional Requirements section: each FR defines its own interface boundary

**Existing Behavior Explicitly Protected:**
- Observable behavior mandates (lines 129-134 in behavioral contract)
- CLI Executable Contracts, Structured Schema Contracts, Filesystem State Contracts (lines 130-132)
- Strict File Scope Allowlist/Denylist (lines 141-147)
- Acceptance criteria as observable system states (lines 172-175)

**Regression Risk:**
- Low operational risk (verification stage gains cleaner inputs)
- Eliminates hallucination risk of inventing flow patterns not demanded by user
- Reduces cognitive load on specification writers by removing inappropriate questions

**Validation Required After Phase:**
- Generate a test specification
- Verify no "data flow" section exists in output (or if present, only describes interface boundaries)
- Verify all functional requirements define observable boundaries
- Verify acceptance criteria reference module boundaries or FR titles, not command invocations

---

## Phase 4: Replace Investigative Questions with Guardrails

**Behavioral Objective:**
Replace investigative questions with strict "Do NOT" guardrails for prohibited scopes. Specification must only reference integration bindings that exist in user-provided milestone.

**Affected Sections:**
- Lines 44-47 in SKILL.md: Missing section asking for integration strategy analysis (gap analysis lines 104-105)
- Line 103 in gap analysis: "Questions about binary existence, naming conventions, and toolchain integration appear as mandatory prompts"
- Lines 116-117 in gap analysis: "04-STAGE-PERSONAS.md explicitly prohibits specification stage from gaining permission to ask questions"

**Rules Removed:**
- All investigative questions about binary existence
- Questions about naming conventions
- Questions about toolchain integration
- Questions that force user decisions about design space
- "How can this new specification integrate with these existing binaries to form a cohesive toolchain rather than an isolated silo?"

**Rules Added:**
- "Do NOT ask questions about design space"
- "Specification must only reference integration bindings that exist in user-provided milestone"
- "Do NOT add integration cohesion questions (e.g., 'How can this integrate with existing binaries?')"
- "Do NOT analyze naming conventions from binaries"
- "Do NOT define data flow descriptions"
- "Do NOT add template-filling sections (introspection queries, fake search commands)"

**Rules Modified:**
- Step 6 (Specification Generation Template): Ensure template doesn't contain investigative prompts
- Step 12 (Follow Spec Decomposition Plan): Emphasize that scope is limited to plan's enumerated artifacts

**Rules Consolidated:**
- Consolidate all negative guardrails into a single "Out of Scope / Do NOT" section in the skill
- Move specific prohibitions from scattered steps into a unified negative guardrails list

**Existing Behavior Explicitly Protected:**
- Milestone integration bindings consumption (Step 2)
- Strict file scope boundaries (Step 16)
- Placeholder detection and verification guardrails (Step 22)
- Artifact scope boundaries (allowlist/denylist enforcement)
- YAML frontmatter enclosure mechanics
- Observable behavior mandates

**Regression Risk:**
- Low risk of disrupting mechanical processes
- High risk of enabling purely placeholder-driven specification that passes mechanical checks while being technically void
- Improves alignment with contract: "Spec content is verifiable truth, not exploratory questioning"

**Validation Required After Phase:**
- Generate a test specification
- Verify no investigative questions appear in the output
- Verify all requirements reference milestone integration bindings
- Verify negative guardrails section is present and comprehensive
- Verify placeholder check still triggers on incomplete specifications
