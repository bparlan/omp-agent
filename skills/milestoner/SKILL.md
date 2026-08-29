---
name: milestoner
version: 2.6.0-stable
description: Transform a rough feature idea into a complete milestone document through interactive requirements elicitation. Ensures strict, observable scope boundaries.
tools: [read, write, ask, edit, glob, bash, lsp, code-search, ast_edit, inspector, task]
user-invocable: true
---

## Core Principle

`/milestone` is an upstream compiler stage. Its output is consumed by another engineering agent. The milestone stage is not primarily a Markdown-generation task. It is a requirements-convergence task whose final output happens to be a canonical milestone document. The agent should optimize for **requirements fidelity and downstream specification readiness** rather than producing a plausible milestone quickly.

This is the **canonical, requirements-complete, specification-ready contract between human intent/project evidence and downstream autonomous engineering.**

---

#### 1. Enhanced System Awareness (AEF Integration)

Your skill now includes controlled infrastructure investigation capabilities that respect the requirements-elicitation contract while providing essential system awareness for creating realistic, achievable milestones:

##### 1.1 Safe Infrastructure Investigation (Contract-Respected)

**PROHIBITED (strictly forbidden):**
- Architecture changes or refactoring
- Implementation details that belong to downstream specification stage
- Premature design decisions that constrain implementation unnecessarily
- Creative interpretation that expands scope beyond user intent

**ALLOWED (evidence-based investigation within contract boundaries):**
- **Codebase Reality Check**: Understand what actually exists vs. what might be needed
- **Downstream Capability Assessment**: Understand what downstream skills can realistically deliver
- **Integration Binding Verification**: Validate that referenced interfaces, binaries, and fixtures actually exist
- **AEF Core Infrastructure Awareness**: Understand existing AEF core components that milestones might leverage
- **Historical Pattern Analysis**: Compare against similar completed milestones for realism
- **Feasibility Assessment**: Validate that milestone scope is achievable with existing infrastructure

**Controlled Investigation Capabilities:**
Your skill now has access to `code-search`, `ast_edit`, `inspector`, and `task` tools for safe repository exploration when:
- Validating that referenced integrations actually exist in the codebase
- Understanding existing module interfaces that specifications might need to interact with
- Assessing feasibility of proposed scope against existing codebase
- Comparing against similar completed milestones for realistic sizing
- Understanding AEF core infrastructure capabilities and limitations

##### 1.2 Enhanced Tooling Integration

**NEW TOOLS:**
- `code-search`: Semantic repository search for existing implementation patterns and conventions
- `ast_edit`: AST-aware pattern analysis for existing code structures
- `inspector`: Visual inspection QA for codebase quality
- `lsp`: Symbol-aware code intelligence for interface validation
- `task`: Subagent delegation for parallel investigation

**INTEGRATION CAPABILITIES:**
- Analyze existing code patterns to understand what's already implemented
- Discover existing module exports and public interfaces that specifications might need
- Identify existing fixture structures and dependencies
- Validate integration bindings against actual codebase
- Assess milestone feasibility against existing infrastructure

##### 1.3 AEF Core Infrastructure Awareness

**RECOGNIZED WORKING AEF CORE COMPONENTS:**
These are the current working AEF infrastructure components. Your skill should be aware of their existence and contracts when creating milestones that might leverage them:

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

**Downstream Skill Capabilities:**
Your milestone output must respect what downstream skills can actually deliver:

- `generate-spec`: Translates milestone into concrete Interface Contracts (CLI binaries, JSON schemas, config keys, file path mappings)
- `generate-verification`: Translates specification into testable assertions with explicit requirement traceability
- `generate-tests`: Generates deterministic, executable test scripts from verification contracts
- `implement-specification`: Implements logic to satisfy specification contracts; integrates with AEF core infrastructure
- `evaluate-implementation`: Executes tests, auto-fixes minor bugs, classifies failures
- `review-implementation`: Zero-trust reality audit of implementation against specification
- `evaluate-tests`: Pre-implementation baseline validation of test suites
- `investigate-issue`: Evidence-first investigation with failure classification and optional auto-fix
- `hotfix-focus`: Literal execution of checklist-driven changes
- `hotfix-issue`: Surgical bug fixes from investigation reports

**INTEGRATION RULES:**
- When milestones reference artifact systems, validate those references point to existing working infrastructure
- When milestones specify validation requirements, verify `core/validation.py` can satisfy them
- When milestones require type registration or resolution, verify `core/artifacts/registry.py` and `core/artifacts/resolution.py` support the required operations
- Do NOT assume downstream skills can deliver functionality not present in existing infrastructure
- Use `lsp` to verify referenced components exist before including them in milestone scope

##### 1.4 Enhanced Quality Gates

**MECHANICAL VALIDATION:**
- **Requirements Fidelity**: Verify milestone accurately captures user intent
- **Downstream Readiness**: Ensure milestone provides enough information for `generate-specification` to operate without additional intent-reconstruction
- **Feasibility**: Validate milestone scope is achievable with existing infrastructure
- **Integration Integrity**: Verify referenced integrations actually exist in evidence or are user-supplied

**SYSTEM AWARENESS CHECKS:**
- Verify milestone scope aligns with existing module interfaces
- Confirm milestone references existing integration bindings
- Ensure milestone respects existing code organization
- Validate milestone integrates correctly with AEF core infrastructure where relevant
- Ensure milestone does not invent interfaces or dependencies that don't exist

---

### 1. The Grill-Me Loop (Requirements Elicitation)

Before creating any milestone document, you MUST:

1. Perform code skeleton checks (`generate_skeletons`) to inspect integration boundaries and bindings.
   **Enhanced Validation:**
   - Use `lsp` to verify referenced interfaces exist in codebase
   - Use `code-search` to confirm integration bindings are real, not invented
   - Validate that all referenced binaries, fixtures, and interfaces actually exist

2. Active Challenge: Actively challenge assumptions, isolate scope boundaries, and define strict success criteria.
   **Enhanced Challenge:**
   - Use `code-search` to verify scope is achievable with existing infrastructure
   - Use `lsp` to confirm proposed scope aligns with existing module interfaces
   - Validate scope against AEF core infrastructure capabilities
   - Challenge any requirements that assume functionality not present in codebase

3. Resolve downstream ambiguities. Do not complete elicitation if material integration details or downstream decisions are deferred or omitted.
   **Enhanced Resolution:**
   - Use `lsp` to discover actual module interfaces before finalizing specifications
   - Use `code-search` to understand existing patterns that specifications must follow
   - Validate that all integration bindings are real and accessible
   - Ensure milestone does not defer material decisions to downstream stages

4. Structured Requirements Mapping: Generate a structured requirements mapping table as a mandatory post-condition.
   **Enhanced Mapping:**
   - Include validation results from system checks
   - Document AEF core integration status
   - Note any system-level observations or constraints

#### Interactive Workflow Triggers (Mandatory)

The milestoner skill MUST use the `ask` tool in these critical decision points:

1. **Milestone Confirmation:** After building the provisional requirements model and completing the "Active Challenge" phase, use `ask` to confirm milestone scope, goals, and constraints with the user:

| Option Label        | Action                                                      |
| :------------------ | :---------------------------------------------------------- |
| Confirm Scope       | Proceed with the current milestone scope as defined.        |
| Revise Requirements | Allow the user to specify necessary revisions or additions. |
| Custom              | Let me specify a custom decision.                           |

**Enhanced Confirmation:**
- Include system validation results in confirmation summary
- Highlight any AEF core integration opportunities or constraints
- Note any feasibility concerns discovered during investigation

2. **Spec Decomposition Approval:** After completing the milestone document structure, use `ask` to confirm the spec decomposition plan:

| Option Label          | Action                                            |
| :-------------------- | :------------------------------------------------ |
| Confirm Decomposition | Proceed with the current spec decomposition plan. |
| Modify Decomposition  | Allow the user to modify or add specifications.   |
| Custom                | Let me specify a custom decision.                 |

**Enhanced Approval:**
- Include validation that decomposition aligns with existing infrastructure
- Confirm each specification can be satisfied by downstream skills
- Highlight any AEF core integration points in decomposition

The `ask` tool usage is mandatory at these material decision points to ensure human oversight of requirements before moving downstream.

---

## Pipeline Contract & Sealing Principle

### Pipeline Contract

The milestone stage is the final interactive requirements stage. After the milestone is finalized, downstream stages should operate without routine user intervention.

**Enhanced Pipeline Awareness:**
- Understand that `generate-spec` needs concrete Interface Contracts (CLI binaries, JSON schemas, config keys, file path mappings)
- Understand that `generate-verification` needs testable assertions with explicit requirement traceability
- Understand that `generate-tests` needs deterministic, executable test scripts
- Understand that `implement-specification` integrates with AEF core infrastructure
- Design milestones that downstream skills can actually deliver

#### Responsibility Boundary

- **`/milestone` owns:** user intent, requirements clarification, scope, exclusions, architectural boundaries, material constraints, dependencies, observable behavior, acceptance conditions, and specification decomposition.
- **`/generate-specification` owns:** implementation-level design, technical decomposition, interfaces within the established milestone boundary, implementation constraints derived from project architecture, and specification-level functional requirements.
- **`/generate-verification` owns:** verification design, verification mapping, and evidence strategy.
- **`Later stages own:** implementation validation.

**Enhanced Boundary Respect:**
- Do not consume downstream specification stage's responsibility by prematurely designing implementation details
- Do not defer material decisions to downstream stages
- Provide enough information for downstream stages to operate without additional intent-reconstruction
- Respect what each downstream stage can actually deliver

### No Downstream Requirements Reconstruction

The milestone MUST NOT intentionally defer a material user decision to downstream stages. If the downstream specification agent would need to ask: "What did the user actually mean?", then the milestone stage failed to complete its requirements-elicitation responsibility.

**Enhanced Validation:**
- Use `lsp` to verify all referenced components exist before finalizing milestone
- Use `code-search` to confirm all integration bindings are real
- Validate that milestone provides enough detail for downstream specification generation
- Ensure no material decisions are deferred to downstream stages

### No Implementation Leakage

Conversely, the milestone MUST NOT consume the downstream specification stage's responsibility by prematurely designing implementation details unless those details are established project constraints.

**Enhanced Validation:**
- Use `code-search` to verify proposed implementation details are established project constraints, not invented details
- Use `lsp` to confirm implementation details align with existing interfaces
- Validate that milestone does not over-constrain implementation unnecessarily

### Sealing Principle

Once finalized, the milestone represents the agreed requirements contract. Downstream agents may interpret, decompose, implement, or verify it, and identify contradictions against code; but they should not silently redefine the user's intended requirements. If a downstream stage discovers a genuine contradiction that cannot be resolved from existing evidence, it should surface the contradiction as a blocking issue rather than silently inventing a new requirement.

**Enhanced Sealing:**
- Use `code-search` to verify milestone does not contradict existing codebase
- Use `lsp` to confirm milestone aligns with existing interfaces
- Validate that milestone does not invent requirements not present in user intent or project evidence

### Contract Category Preservation

The milestone MUST declare the contract category for every material interface or behavioral requirement. Allowed categories are:

- **Structured Schema Contract** — JSON/YAML schema, frontmatter schema, metadata schema
- **Function / API Contract** — callable interface with typed parameters and return values
- **CLI Executable Contract** — standalone binary or script invoked from shell, with exit codes and stdout/stderr
- **Filesystem State Contract** — observable files/directories/permissions after an operation
- **Skill Behavioral Contract** — observable outcomes after skill invocation, verified by filesystem/artifact state, not by process exit codes

The milestone MUST NOT defer contract-category decisions to downstream specification stages. If a requirement involves a `user-invocable: true` Skill, it MUST be classified as a Skill Behavioral Contract. No downstream specification may redefine a Skill as a CLI Executable Contract.

When the milestone describes mode-aware behavior for a Skill, it MUST specify the observable filesystem or artifact outcomes that constitute correct behavior. It MUST NOT specify process exit codes, stdout JSON, or CLI argument patterns for that Skill.

**Enhanced Contract Validation:**
- Use `lsp` to verify contract categories match actual module interfaces
- Use `code-search` to confirm CLI executable contracts match actual binaries
- Validate skill behavioral contracts against actual skill files
- Ensure contract categories are consistent with existing infrastructure

---

## Commands & Artifact Management

### No Downstream Requirements Reconstruction

The milestone MUST NOT intentionally defer a material user decision to downstream stages. If the downstream specification agent would need to ask: "What did the user actually mean?", then the milestone stage failed to complete its requirements-elicitation responsibility.

### No Implementation Leakage

Conversely, the milestone MUST NOT consume the downstream specification stage's responsibility by prematurely designing implementation details unless those details are established project constraints.

---

## Evidence-First Requirements Elicitation (Grill-Me Loop)

Before generating the canonical milestone document, the agent must inspect the available project evidence and interactively resolve material requirements with the user.

### Material Unknown Handling & The "Ask" Semantics

**When to Ask:** Ask when user intent, policy, scope, acceptance expectations, security posture, architectural boundaries, dependencies, observable behavior, or another material decision cannot be established from available evidence and could affect the milestone contract.

**Do NOT Ask:**

- Whenever something is simply unspecified.
- For implementation questions that belong to `generate-specification`.
- Using arbitrary question counts or mechanically walking through a questionnaire.

**Enhanced Evidence Inspection:**
- Use `lsp` to discover actual module interfaces before asking about integration
- Use `code-search` to find existing patterns before asking about implementation approach
- Use `inspector` to visually inspect existing code before asking about behavior
- Use `task` to delegate parallel evidence gathering
- Only ask when material decision cannot be established from available evidence

### Core Loop

1. Inspect available project evidence (documentation, roadmap, milestones, architecture, source code, schemas, tests, configuration, existing interfaces).
   **Enhanced Inspection:**
   - Use `lsp` to discover actual module interfaces and exports
   - Use `code-search` to find existing patterns and conventions
   - Use `glob` to locate actual test files and fixtures
   - Use `read` to examine existing integration bindings
   - Validate all evidence against current codebase state

2. **Provisional Requirements Model:** Build an internal provisional model covering intended outcome, motivation, scope, exclusions, dependencies, integrations, constraints, invariants, security/safety, important inputs/outputs, observable behavior, acceptance, specification boundaries, and verification-relevant conditions. This model does not need to be exposed as a separate artifact.
   **Enhanced Modeling:**
   - Validate all proposed integrations exist in codebase
   - Confirm all proposed dependencies are real and accessible
   - Ensure all proposed scope is achievable with existing infrastructure
   - Document AEF core integration opportunities and constraints

3. **Active Challenge:** Actively challenge the provisional model. Look for unsupported assumptions, contradictions, vague requirements, missing boundaries, accidental scope expansion, hidden dependencies, unclear ownership, undefined behavior, unverifiable success conditions, and requirements that downstream specification generation would have to reinterpret. Do not merely check whether required headings exist.
   **Enhanced Challenge:**
   - Use `code-search` to verify proposed scope is achievable
   - Use `lsp` to confirm proposed interfaces exist
   - Use `inspector` to validate proposed behavior against existing code
   - Challenge any requirements that assume functionality not present in codebase
   - Validate that all integration bindings are real, not invented

4. **Evidence-First:** Before asking any question: 1) inspect relevant project evidence; 2) determine whether the answer can be established; 3) only ask if user input remains necessary. Do not ask questions whose answers are already present in authoritative project evidence.
   **Enhanced Evidence-First:**
   - Use `task` to parallelize evidence gathering for complex questions
   - Use `code-search` to find authoritative project evidence
   - Use `lsp` to discover actual module capabilities
   - Only ask when material decision cannot be established from available evidence

5. If the answer depends on a material intent/policy/boundary decision, ask the user.

6. Incorporate the answer.

7. Re-evaluate the milestone as a whole.

8. Continue until downstream specification generation can proceed without material user clarification.

**Enhanced Loop:**
- Use `code-search` to validate all proposed requirements against existing codebase
- Use `lsp` to verify all proposed interfaces exist
- Use `inspector` to validate proposed behavior against existing implementation
- Ensure milestone provides enough information for downstream specification generation

### Questioning Strategy

- **Question Priority:** Prioritize questions by potential downstream impact. Ask first about uncertainties that could change: 1) milestone objective; 2) scope; 3) specification decomposition; 4) architectural boundaries; 5) security/safety; 6) externally observable behavior; 7) dependencies/integrations; 8) acceptance; 9) verification expectations. Do not spend user interaction on implementation details that belong downstream.

- **Avoid Over-Questioning:** Do not ask merely because a detail is unspecified, an implementation choice is open, multiple valid implementation strategies exist, or a section could contain more detail. The question must have material impact on requirements. Do not use fixed question counts or turn this into a questionnaire.

- **Challenge Contradictions:** Identify explicitly, explain consequences, and ask which source governs. Do not silently reconcile.

- **Challenge Vague Requirements:** Probe for observable requirements (e.g., instead of "handle errors properly," ask "What failure behavior is required...").

- **Drill-Down:** After each substantive user answer: update the requirements model, check whether the answer creates a new dependency or contradiction, reconsider previously resolved scope, and continue questioning if the answer materially changes the milestone. Do not simply append the answer to the document.

- **Use Adaptive Lenses:** Dynamically consider outcomes, constraints, boundaries, hidden assumptions, alternatives, reversibility, failure modes, stakeholders, security, data ownership, future compatibility, pre-mortems, and acceptance behavior.

- **Strawman Questions:** When a question is difficult to answer from an empty prompt, use a concise proposed interpretation (e.g., "My current interpretation is X because the architecture document establishes Y. If that is not intended, what should M1 do instead?"). Do not present the proposal as fact or bias the user when evidence does not support it.

- **Pushback:** Challenge proposed scope if it contradicts architecture, duplicates functionality, conflicts with the roadmap, creates unresolved dependencies, or introduces risky assumptions.

**Enhanced Questioning:**
- Use `code-search` to validate proposed scope against existing codebase
- Use `lsp` to verify proposed interfaces exist before asking about them
- Use `inspector` to understand existing behavior before proposing changes
- Use `task` to parallelize evidence gathering for complex decisions
- Ensure questions are informed by actual codebase state

### Known vs. Unknown Distinction

Distinguish between established project facts, explicit user requirements, derived constraints (acceptable only when logically following from established evidence), and unresolved material decisions (which require user input). No material requirement may be presented as fact if it is actually an assumption.

**Enhanced Distinction:**
- Use `code-search` to verify "established project facts" against actual codebase
- Use `lsp` to confirm "explicit user requirements" align with existing interfaces
- Use `read` to validate "derived constraints" against project evidence
- Clearly label unresolved material decisions requiring user input

---

## Specification-Readiness Contract

The milestone MUST NOT force empty sections to contain fabricated content. If a category is genuinely not applicable, state that it is not applicable; do not invent requirements to populate it. Material missing information must trigger evidence investigation or user clarification according to the existing evidence-first policy.

### Template Mapping

The milestone document MUST follow the template structure exactly. You MUST output this vertical Markdown table to document requirements mapping. Do NOT use multi-line row collapsing.

| Template Section            | Required Constraints                                                                                                                                                                                                                    |
| :-------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Milestone Contract**      | Generated from user input and project evidence. Captures goal, motivation, externally observable outcome, key constraints, important invariants, critical security/safety boundaries, and scope boundary. MUST NOT contain boilerplate. |
| **Goal**                    | Clear, one-sentence objective.                                                                                                                                                                                                          |
| **Motivation**              | Why it matters, and the consequences of inaction.                                                                                                                                                                                       |
| **Spec Decomposition Plan** | N bullet points listing every specification. generate-spec MUST follow this plan.                                                                                                                                                       |
| **Scope**                   | Defines what the milestone is responsible for making true, available, supported, preserved, or produced. May include implementation constraints when established requirements or bindings.                                              |
| **Out of Scope**            | Explicit exclusions to prevent scope creep.                                                                                                                                                                                             |
| **Success Criteria**        | Measurable checklist items defined as observable system states, artifacts, or behaviors. No subjective qualifiers.                                                                                                                      |
| **Integration Bindings**    | Declares existing binaries, fixtures, and interfaces this milestone consumes. Table format. Optional but recommended.                                                                                                                   |
| **Verification Strategy**   | Optional method hints for generate-verification (e.g., FR-1: SCRIPT_EXECUTION).                                                                                                                                                         |
| **Risks**                   | Material technical, architectural, operational, security, dependency, or failure risks affecting execution or verification.                                                                                                             |
| **Notes**                   | Optional implementation-independent observations.                                                                                                                                                                                       |

**Enhanced Template Validation:**
- Use `lsp` to verify all integration bindings exist in codebase
- Use `code-search` to confirm all referenced binaries/fixtures are real
- Validate that all contract categories match actual module interfaces
- Ensure milestone does not invent interfaces or dependencies

### Section Requirements

- **Scope Requirements:** Scope describes what the milestone is responsible for. It MUST NOT invent implementation choices merely to make the document appear concrete. The number and granularity of scope entries should emerge from the actual milestone complexity, without arbitrary counts.

- **Decomposition Requirements:** Each specification entry must establish its identifier, responsibility, boundary, expected outcome, relevant dependencies, and relevant constraints. It is the authoritative work plan for `generate-specification`. Do not force a predetermined number of specifications or artificially merge/split work.

- **Integration Bindings:** Where applicable, bindings identify existing interfaces, dependencies, inputs, outputs, ownership/boundaries, and constraints. Do not fabricate bindings.

**Enhanced Binding Validation:**
- Use `lsp` to verify all referenced interfaces exist
- Use `code-search` to confirm all referenced binaries/fixtures are real
- Use `read` to validate all referenced configuration files exist
- Ensure all integration bindings are verifiable in current codebase

- **Inputs & Outputs:** Material inputs, outputs, state transitions, and external exchanges must be captured where applicable, without duplicating information across sections.

- **Requirements Traceability:** Every significant requirement must have a clear home. Trace: `Goal → Scope → Specification → Success Criteria → Verification` where applicable.

- **Contradiction Detection:** Before finalizing, compare all repeated requirements (numeric thresholds, versions, identifiers, units, terminology, scope, security, read/write behavior, inclusions/exclusions). If contradictory project evidence exists, identify it and ask the user. Do not silently choose an interpretation.

**Enhanced Contradiction Detection:**
- Use `code-search` to find contradictory requirements in existing codebase
- Use `lsp` to verify proposed requirements don't conflict with existing interfaces
- Use `read` to compare against existing project evidence
- Identify and surface all contradictions before sealing milestone

- **Implementation Leakage & WHAT vs HOW:** Do not invent implementation decisions; preserve implementation details when they are established requirements, binding project conventions, mandated by an existing interface/dependency, or explicitly required by the user.

**Enhanced Leakage Prevention:**
- Use `code-search` to verify implementation details are established project constraints
- Use `lsp` to confirm implementation details align with existing interfaces
- Challenge any implementation details that are not established requirements

---

## Quality & Convergence Gates

Before reporting a successfully generated milestone, perform the following validation. Failure in any gate requires resolving the issue from evidence or asking the user; do not silently patch by guessing.

### Milestone Quality Gate

Validate the following:

1. **Structural & Contract Completeness:** Canonical sections exist, and the milestone communicates goal, motivation, scope, exclusions, decomposition, criteria, integrations, and constraints.
   **Enhanced Validation:**
   - Use `read` to verify all canonical sections are present
   - Use `lsp` to verify all integration bindings exist
   - Use `code-search` to confirm all referenced components are real

2. **Decomposition Completeness:** Every material deliverable is covered by a specification entry with a meaningful boundary, and no specification exists without reason.

3. **Success Criteria Quality:** Inspect every success criterion before sealing. If a criterion is subjective, vague, non-observable, non-verifiable, or dependent on an undefined interpretation, resolve it from project evidence or ask the user for a concrete acceptance condition. Do not silently invent an interpretation.

4. **Evidence & Scope Integrity:** No requirement is an unsupported assumption. No out-of-scope item appears as in-scope, and no future work is accidentally pulled in.
   **Enhanced Validation:**
   - Use `code-search` to verify all requirements are supported by project evidence
   - Use `lsp` to confirm all scope boundaries align with existing interfaces
   - Validate that no out-of-scope items are accidentally included

5. **Integration Integrity:** Referenced integrations actually exist in evidence or are user-supplied. Interfaces are not invented.
   **Enhanced Validation:**
   - Use `lsp` to verify all referenced interfaces exist in codebase
   - Use `code-search` to confirm all referenced binaries/fixtures are real
   - Use `glob` to validate all referenced files exist
   - Ensure no interfaces are invented

6. **Implementation Independence:** Do not invent implementation decisions; preserve implementation details when they are established requirements or binding project constraints.
   **Enhanced Validation:**
   - Use `code-search` to verify implementation details are established constraints
   - Use `lsp` to confirm implementation details align with existing interfaces
   - Challenge any invented implementation details

7. **Specification Readiness:** Output contains enough information for `generate-specification` to operate without additional intent-reconstruction.
   **Enhanced Validation:**
   - Use `lsp` to verify all necessary interface information is present
   - Use `code-search` to confirm all necessary patterns are documented
   - Validate that downstream `generate-specification` can operate without additional user input

### Requirements Convergence Gate

The agent may seal the milestone only when: **"No unresolved material question remains whose answer could change the milestone contract or require downstream user-intent reconstruction."** Do not stop merely because the template can be filled, the milestone looks complete, a plausible implementation can be imagined, or no obvious question comes to mind. Implementation-level questions do not block convergence.

Evaluate convergence across Intent, Scope, Decomposition, Dependencies, Constraints, Behavior, Verification, Contradictions, and Unknowns.

**Final Adversarial Test:** Before sealing, perform one adversarial pass: "What would make the specification-generation agent stop and ask the user?" If the answer is a material requirement question, resolve it now. If it is an implementation/design question, leave it to downstream specification generation. This is the final opportunity for human requirements input in the AEF pipeline.

**Enhanced Convergence Validation:**
- Use `code-search` to verify all requirements are achievable with existing infrastructure
- Use `lsp` to confirm all interfaces exist and are accessible
- Use `inspector` to validate proposed behavior against existing codebase
- Ensure no material questions remain unresolved

### Final Self-Review

Perform a semantic pass equivalent to: `Contract → Decomposition → Scope → Bindings → Criteria → Verification → Risks`. Confirm each stage is consistent with the previous one. Do not report success if an unresolved contradiction exists.

**Enhanced Self-Review:**
- Use `lsp` to verify all contracts align with existing interfaces
- Use `code-search` to confirm all bindings are real and accessible
- Use `read` to validate all criteria are observable and measurable
- Use `inspector` to validate proposed behavior against existing codebase
- Ensure milestone is complete, consistent, and ready for downstream processing

---

## Rule Classification and Enforcement

All rules within this skill are classified and enforced as follows:

- **Genuinely invariant:** Rules essential for process determinism and correctness (e.g., quality gates, artifact protocol). These are strictly enforced.
- **Recommended default:** Guidance that provides a sensible starting point (e.g., default milestone ID).
- **Context-dependent:** Rules that apply based on project evidence or user input (e.g., implementation leakage rules).
- **Harmful restriction:** Arbitrary limits (fixed counts) or conflated concepts detrimental to semantic clarity. These have been explicitly removed to ensure flexibility.

**Token-Efficiency Rule:** Explicitly prohibit optimizing the milestone for minimum token usage when doing so removes requirements, constraints, rationale, boundaries, or verification context. The preferred optimization is: **remove redundancy, not information.**

### Rule Precedence

Establish the following hierarchy to ensure deterministic interpretation:

1. Explicit user requirements and confirmed decisions.
2. Established project constraints and authoritative project evidence.
3. Milestone correctness and safety invariants.
4. Context-dependent guidance.
5. Formatting and stylistic defaults.

Do not allow a formatting or token-efficiency preference to override a substantive requirement. If two substantive sources conflict and authority cannot resolve the conflict, use the existing contradiction-resolution behavior and ask the user.

---

## Enhanced System-Specific Considerations

**AEF Core Infrastructure Integration:**
When creating milestones that might leverage AEF core components, your milestone MUST:

1. **Use Canonical Components**: Reference existing `core/artifacts/` and `core/validation.py` components when milestones involve artifact management
2. **Respect Existing Interfaces**: Ensure milestone scope aligns with existing module interfaces
3. **Integrate with Artifact System**: Verify milestone requirements can be satisfied by canonical validation and resolution APIs
4. **Maintain Compatibility**: Ensure milestone does not break existing AEF core functionality

**Working AEF Core Components Reference:**

**Validation Layer:**
- `core/validation.py`: `validate_metadata(artifact_path)`, `validate_artifact(metadata)`, `ValidationResult`, `ArtifactValidationResult`, `Validator`
- Reference these when milestones require artifact validation

**Artifact Metadata Layer:**
- `core/artifacts/metadata.py`: `extract_frontmatter(filepath)`, `parse_metadata(content)`, `get_metadata_from_file(file_path)`
- Reference these when milestones require frontmatter or metadata extraction

**Registry Layer:**
- `core/artifacts/registry.py`: `ArtifactRegistry`, `get_registry()`, `register_type()`, `get_storage_rule()`, `store_relationship()`, `get_relationships()`
- Reference these when milestones require type registration, storage rules, or relationship tracking

**Resolution Layer:**
- `core/artifacts/resolution.py`: `resolve_artifact(...)`, `construct_canonical_path(...)`
- `core/artifacts/resolve.py`: `main()` CLI entry point
- Reference these when milestones require artifact resolution or path construction

**Type System:**
- `core/artifacts/types.py`: `CanonicalArtifactType`, `get_artifact_type()`, `get_all_artifact_types()`, `get_type_definition()`, `get_all_type_definitions()`
- Reference these when milestones require artifact type definitions or type queries

**Error Handling:**
- `core/artifacts/errors.py`: `AmbiguousResolutionError` and related exceptions
- Reference these when milestones require error handling or failure modes

**Creation and Migration:**
- `core/artifacts/creation.py`: `create_artifact(...)`
- `core/artifacts/migration.py`: `migrate_legacy_artifact(...)`
- Reference these when milestones require artifact creation or legacy migration

**Required Investigation Methods:**
1. **Codebase Reality Check**: Verify what actually exists vs. what might be needed
2. **Downstream Capability Assessment**: Understand what downstream skills can realistically deliver
3. **Integration Binding Verification**: Validate that referenced interfaces, binaries, and fixtures actually exist
4. **Feasibility Assessment**: Validate that milestone scope is achievable with existing infrastructure
5. **Historical Pattern Analysis**: Compare against similar completed milestones for realism
6. **AEF Core Integration Verification**: Confirm milestone can leverage existing AEF core infrastructure

**Controlled Investigation Commands:**
```bash
# Verify integration bindings exist
glob "bin/**/*.py" && glob "tests/**/*.py" && glob "core/**/*.py"

# Discover module interfaces via lsp
lsp symbols core/artifacts/registry.py
lsp symbols core/validation.py

# Analyze existing implementation patterns
code-search "class.*Registry\|def.*validate\|def.*resolve"

# Verify AEF core component integration
code-search "from core.validation import\|from core.artifacts\."

# Validate live state claims
bash "git ls-files | grep -E 'core/artifacts|core/validation'"
```

This enhanced milestoner skill now provides comprehensive system awareness while preserving its core requirements-elicitation role, ensuring milestones are both user-intent-compliant and system-aligned with the existing working AEF infrastructure core and downstream skill capabilities.
