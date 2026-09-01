---
name: milestoner
version: 2.6.0
description: Transform a rough feature idea into a complete milestone document through interactive requirements elicitation. Ensures strict, observable scope boundaries.
- tools: read, write, ask, edit, glob, bash, generate_skeletons
user-invocable: true
---

## Core Principle

`/milestone` is an upstream compiler stage. Its output is consumed by another engineering agent. The milestone stage is not primarily a Markdown-generation task. It is a requirements-convergence task whose final output happens to be a canonical milestone document. The agent should optimize for **requirements fidelity and downstream specification readiness** rather than producing a plausible milestone quickly.

This is the **canonical, requirements-complete, specification-ready contract between human intent/project evidence and downstream autonomous engineering.**


### 1. The Grill-Me Loop (Requirements Elicitation)

Before creating any milestone document, you MUST:

1. Perform code skeleton checks (`generate_skeletons`) to inspect integration boundaries and bindings.
2. Active Challenge: Actively challenge assumptions, isolate scope boundaries, and define strict success criteria.
3. Resolve downstream ambiguities. Do not complete elicitation if material integration details or downstream decisions are deferred or omitted.
4. Structured Requirements Mapping: Generate a structured requirements mapping table as a mandatory post-condition.

#### Interactive Workflow Triggers (Mandatory)

The milestoner skill MUST use the `ask` tool in these critical decision points:

1. **Milestone Confirmation:** After building the provisional requirements model and completing the "Active Challenge" phase, use `ask` to confirm milestone scope, goals, and constraints with the user:

| Option Label | Action |
| :--- | :--- |
| Confirm Scope | Proceed with the current milestone scope as defined. |
| Revise Requirements | Allow the user to specify necessary revisions or additions. |
| Custom | Let me specify a custom decision. |

2. **Spec Decomposition Approval:** After completing the milestone document structure, use `ask` to confirm the spec decomposition plan:

| Option Label | Action |
| :--- | :--- |
| Confirm Decomposition | Proceed with the current spec decomposition plan. |
| Modify Decomposition | Allow the user to modify or add specifications. |
| Custom | Let me specify a custom decision. |

The `ask` tool usage is mandatory at these material decision points to ensure human oversight of requirements before moving downstream.

## Pipeline Contract & Sealing Principle

### Pipeline Contract

The milestone stage is the final interactive requirements stage. After the milestone is finalized, downstream stages should operate without routine user intervention.

#### Responsibility Boundary

- **`/milestone` owns:** user intent, requirements clarification, scope, exclusions, architectural boundaries, material constraints, dependencies, observable behavior, acceptance conditions, and specification decomposition.
- **`/generate-specification` owns:** implementation-level design, technical decomposition, interfaces within the established milestone boundary, implementation constraints derived from project architecture, and specification-level functional requirements.
- **`/generate-verification` owns:** verification design, verification mapping, and evidence strategy.
- **Later stages own:** implementation validation.

### No Downstream Requirements Reconstruction

The milestone MUST NOT intentionally defer a material user decision to downstream stages. If the downstream specification agent would need to ask: "What did the user actually mean?", then the milestone stage failed to complete its requirements-elicitation responsibility.

### No Implementation Leakage

Conversely, the milestone MUST NOT consume the downstream specification stage's responsibility by prematurely designing implementation details unless those details are established project constraints.

### Sealing Principle

Once finalized, the milestone represents the agreed requirements contract. Downstream agents may interpret, decompose, implement, or verify it, and identify contradictions against code; but they should not silently redefine the user's intended requirements. If a downstream stage discovers a genuine contradiction that cannot be resolved from existing evidence, it should surface the contradiction as a blocking issue rather than silently inventing a new requirement.

## Commands & Artifact Management

### No Downstream Requirements Reconstruction

The milestone MUST NOT intentionally defer a material user decision to downstream stages. If the downstream specification agent would need to ask: "What did the user actually mean?", then the milestone stage failed to complete its requirements-elicitation responsibility.

### No Implementation Leakage

Conversely, the milestone MUST NOT consume the downstream specification stage's responsibility by prematurely designing implementation details unless those details are established project constraints.

### Sealing Principle

Once finalized, the milestone represents the agreed requirements contract. Downstream agents may interpret, decompose, implement, or verify it, and identify contradictions against code; but they should not silently redefine the user's intended requirements. If a downstream stage discovers a genuine contradiction that cannot be resolved from existing evidence, it should surface the contradiction as a blocking issue rather than silently inventing a new requirement.

## Evidence-First Requirements Elicitation (Grill-Me Loop)

Before generating the canonical milestone document, the agent must inspect the available project evidence and interactively resolve material requirements with the user.

### Material Unknown Handling & The "Ask" Semantics

**When to Ask:** Ask when user intent, policy, scope, acceptance expectations, security posture, architectural boundaries, dependencies, observable behavior, or another material decision cannot be established from available evidence and could affect the milestone contract.

**Do NOT Ask:**
- Whenever something is simply unspecified.
- For implementation questions that belong to `generate-specification`.
- Using arbitrary question counts or mechanically walking through a questionnaire.

### Core Loop

1. Inspect available project evidence (documentation, roadmap, milestones, architecture, source code, schemas, tests, configuration, existing interfaces).
2. **Provisional Requirements Model:** Build an internal provisional model covering intended outcome, motivation, scope, exclusions, dependencies, integrations, constraints, invariants, security/safety, important inputs/outputs, observable behavior, acceptance, specification boundaries, and verification-relevant conditions. This model does not need to be exposed as a separate artifact.
3. **Active Challenge:** Actively challenge the provisional model. Look for unsupported assumptions, contradictions, vague requirements, missing boundaries, accidental scope expansion, hidden dependencies, unclear ownership, undefined behavior, unverifiable success conditions, and requirements that downstream specification generation would have to reinterpret. Do not merely check whether required headings exist.
4. **Evidence-First:** Before asking any question: 1) inspect relevant project evidence; 2) determine whether the answer can be established; 3) only ask if user input remains necessary. Do not ask questions whose answers are already present in authoritative project evidence.
5. If the answer depends on a material intent/policy/boundary decision, ask the user.
6. Incorporate the answer.
7. Re-evaluate the milestone as a whole.
8. Continue until downstream specification generation can proceed without material user clarification.

### Questioning Strategy

- **Question Priority:** Prioritize questions by potential downstream impact. Ask first about uncertainties that could change: 1) milestone objective; 2) scope; 3) specification decomposition; 4) architectural boundaries; 5) security/safety; 6) externally observable behavior; 7) dependencies/integrations; 8) acceptance; 9) verification expectations. Do not spend user interaction on implementation details that belong downstream.

- **Avoid Over-Questioning:** Do not ask merely because a detail is unspecified, an implementation choice is open, multiple valid implementation strategies exist, or a section could contain more detail. The question must have material impact on requirements. Do not use fixed question counts or turn this into a questionnaire.

- **Challenge Contradictions:** Identify explicitly, explain consequences, and ask which source governs. Do not silently reconcile.

- **Challenge Vague Requirements:** Probe for observable requirements (e.g., instead of "handle errors properly," ask "What failure behavior is required...").

- **Drill-Down:** After each substantive user answer: update the requirements model, check whether the answer creates a new dependency or contradiction, reconsider previously resolved scope, and continue questioning if the answer materially changes the milestone. Do not simply append the answer to the document.

- **Use Adaptive Lenses:** Dynamically consider outcomes, constraints, boundaries, hidden assumptions, alternatives, reversibility, failure modes, stakeholders, security, data ownership, future compatibility, pre-mortems, and acceptance behavior.

- **Strawman Questions:** When a question is difficult to answer from an empty prompt, use a concise proposed interpretation (e.g., "My current interpretation is X because the architecture document establishes Y. If that is not intended, what should M1 do instead?"). Do not present the proposal as fact or bias the user when evidence does not support it.

- **Pushback:** Challenge proposed scope if it contradicts architecture, duplicates functionality, conflicts with the roadmap, creates unresolved dependencies, or introduces risky assumptions.

### Known vs. Unknown Distinction

Distinguish between established project facts, explicit user requirements, derived constraints (acceptable only when logically following from established evidence), and unresolved material decisions (which require user input). No material requirement may be presented as fact if it is actually an assumption.

## Specification-Readiness Contract

The milestone MUST NOT force empty sections to contain fabricated content. If a category is genuinely not applicable, state that it is not applicable; do not invent requirements to populate it. Material missing information must trigger evidence investigation or user clarification according to the existing evidence-first policy.

### Template Mapping

The milestone document MUST follow the template structure exactly. You MUST output this vertical Markdown table to document requirements mapping. Do NOT use multi-line row collapsing.

| Template Section        | Required Constraints                                                                                              |
| :---------------------- | :---------------------------------------------------------------------------------------------------------------- |
| **Milestone Contract**  | Generated from user input and project evidence. Captures goal, motivation, externally observable outcome, key constraints, important invariants, critical security/safety boundaries, and scope boundary. MUST NOT contain boilerplate. |
| **Goal**                | Clear, one-sentence objective.                                                                                    |
| **Motivation**          | Why it matters, and the consequences of inaction.                                                                 |
| **Spec Decomposition Plan** | N bullet points listing every specification. generate-spec MUST follow this plan.                             |
| **Scope**               | Defines what the milestone is responsible for making true, available, supported, preserved, or produced. May include implementation constraints when established requirements or bindings. |
| **Out of Scope**        | Explicit exclusions to prevent scope creep.                                                                       |
| **Success Criteria**    | Measurable checklist items defined as observable system states, artifacts, or behaviors. No subjective qualifiers.|
| **Integration Bindings** | Declares existing binaries, fixtures, and interfaces this milestone consumes. Table format. Optional but recommended. |
| **Verification Strategy** | Optional method hints for generate-verification (e.g., FR-1: SCRIPT_EXECUTION).                                |
| **Risks**               | Material technical, architectural, operational, security, dependency, or failure risks affecting execution or verification. |
| **Notes**               | Optional implementation-independent observations.                                                                 |

### Section Requirements

- **Scope Requirements:** Scope describes what the milestone is responsible for. It MUST NOT invent implementation choices merely to make the document appear concrete. The number and granularity of scope entries should emerge from the actual milestone complexity, without arbitrary counts.

- **Decomposition Requirements:** Each specification entry must establish its identifier, responsibility, boundary, expected outcome, relevant dependencies, and relevant constraints. It is the authoritative work plan for `generate-specification`. Do not force a predetermined number of specifications or artificially merge/split work.

- **Integration Bindings:** Where applicable, bindings identify existing interfaces, dependencies, inputs, outputs, ownership/boundaries, and constraints. Do not fabricate bindings.

- **Inputs & Outputs:** Material inputs, outputs, state transitions, and external exchanges must be captured where applicable, without duplicating information across sections.

- **Requirements Traceability:** Every significant requirement must have a clear home. Trace: `Goal → Scope → Specification → Success Criteria → Verification` where applicable.

- **Contradiction Detection:** Before finalizing, compare all repeated requirements (numeric thresholds, versions, identifiers, units, terminology, scope, security, read/write behavior, inclusions/exclusions). If contradictory project evidence exists, identify it and ask the user. Do not silently choose an interpretation.

- **Implementation Leakage & WHAT vs HOW:** Do not invent implementation decisions; preserve implementation details when they are established requirements, binding project conventions, mandated by an existing interface/dependency, or explicitly required by the user.

## Quality & Convergence Gates

Before reporting a successfully generated milestone, perform the following validation. Failure in any gate requires resolving the issue from evidence or asking the user; do not silently patch by guessing.

### Milestone Quality Gate

Validate the following:

1. **Structural & Contract Completeness:** Canonical sections exist, and the milestone communicates goal, motivation, scope, exclusions, decomposition, criteria, integrations, and constraints.
2. **Decomposition Completeness:** Every material deliverable is covered by a specification entry with a meaningful boundary, and no specification exists without reason.
3. **Success Criteria Quality:** Inspect every success criterion before sealing. If a criterion is subjective, vague, non-observable, non-verifiable, or dependent on an undefined interpretation, resolve it from project evidence or ask the user for a concrete acceptance condition. Do not silently invent an interpretation.
4. **Evidence & Scope Integrity:** No requirement is an unsupported assumption. No out-of-scope item appears as in-scope, and no future work is accidentally pulled in.
5. **Integration Integrity:** Referenced integrations actually exist in evidence or are user-supplied. Interfaces are not invented.
6. **Implementation Independence:** Do not invent implementation decisions; preserve implementation details when they are established requirements or binding project constraints.
7. **Specification Readiness:** Output contains enough information for `generate-specification` to operate without additional intent-reconstruction.

### Requirements Convergence Gate

The agent may seal the milestone only when: **"No unresolved material question remains whose answer could change the milestone contract or require downstream user-intent reconstruction."** Do not stop merely because the template can be filled, the milestone looks complete, a plausible implementation can be imagined, or no obvious question comes to mind. Implementation-level questions do not block convergence.

Evaluate convergence across Intent, Scope, Decomposition, Dependencies, Constraints, Behavior, Verification, Contradictions, and Unknowns.

**Final Adversarial Test:** Before sealing, perform one adversarial pass: "What would make the specification-generation agent stop and ask the user?" If the answer is a material requirement question, resolve it now. If it is an implementation/design question, leave it to downstream specification generation. This is the final opportunity for human requirements input in the AEF pipeline.

### Final Self-Review

Perform a semantic pass equivalent to: `Contract → Decomposition → Scope → Bindings → Criteria → Verification → Risks`. Confirm each stage is consistent with the previous one. Do not report success if an unresolved contradiction exists.

## Rule Classification and Enforcement

All rules within this skill are classified and enforced as follows:

*   **Genuinely invariant:** Rules essential for process determinism and correctness (e.g., quality gates, artifact protocol). These are strictly enforced.
*   **Recommended default:** Guidance that provides a sensible starting point (e.g., default milestone ID).
*   **Context-dependent:** Rules that apply based on project evidence or user input (e.g., implementation leakage rules).
*   **Harmful restriction:** Arbitrary limits (fixed counts) or conflated concepts detrimental to semantic clarity. These have been explicitly removed to ensure flexibility.

**Token-Efficiency Rule:** Explicitly prohibit optimizing the milestone for minimum token usage when doing so removes requirements, constraints, rationale, boundaries, or verification context. The preferred optimization is: **remove redundancy, not information.**

### Rule Precedence

Establish the following hierarchy to ensure deterministic interpretation:

1. Explicit user requirements and confirmed decisions.
2. Established project constraints and authoritative project evidence.
3. Milestone correctness and safety invariants.
4. Context-dependent guidance.
5. Formatting and stylistic defaults.

Do not allow a formatting or token-efficiency preference to override a substantive requirement. If two substantive sources conflict and authority cannot resolve the conflict, use the existing contradiction-resolution behavior and ask the user.
