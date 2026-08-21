# Red Team Report: Adversarial Review of `generate-spec` Skill

## Overview
This report identifies conceptual failure modes in the current `generate-spec` skill implementation as defined in `SKILL.md`, its associated behavioral contract (`01-behavioral-contract.md`), and modification plan (`03-modification-plan.md`). For each failure mode, we quote the relevant rule, explain the breach, and propose the smallest corrective change.

---

## Failure 1 – Reconstructs User Intent (Rule: “Derive Functional Requirements (FRs) — Define what the system must do.”)

- **Quoted Rule**: *“Every functional requirement MUST define an observable boundary — specify either: a) A CLI Executable Contract, b) A Structured Schema Contract, or c) A Filesystem State Contract.”*
- **Failure**: The skill often infers user intent from indirect milestone language and formulates FRs that are not directly traceable to explicit milestone text. This reconstructs intent rather than extracting only what is explicitly stated.
- **Correction**: Require each FR to be directly quoted or explicitly referenced from a specific milestone clause, using a citation marker (e.g., `[FR-1:Milestone§2.3]`).

---

## Failure 2 – Asks the User Unnecessarily (Rule: “Do NOT ask questions about design space.”)

- **Quoted Rule**: *“Do NOT ask questions about design space. Specification must only reference integration bindings that exist in user‑provided milestone.”*
- **Failure**: The skill’s fallback clause triggers a `#NEEDS-CLARIFICATION` request whenever the Integration Bindings table is ambiguous, even when the ambiguity is resolvable from existing milestone context.
- **Correction**: Only emit `#NEEDS-CLARIFICATION` when the milestone explicitly lacks a required binding; otherwise derive the requirement from the available text.

---

## Failure 3 – Hallucinates Missing Requirements (Rule: “If the milestone lacks concrete definitions, you MUST halt immediately, emit a `#NEEDS-CLARIFICATION` marker, and request user input.”)

- **Quoted Rule**: *“If the milestone lacks concrete definitions, you MUST halt immediately, emit a `#NEEDS-CLARIFICATION` marker, and request user input.”*
- **Failure**: In practice the skill sometimes generates placeholder‑style FRs (e.g., “TBD: implement X”) before halting, effectively hallucinating a requirement to satisfy template structure.
- **Correction**: Enforce a strict pre‑generation check that all required integration bindings are fully defined; if any are missing, terminate generation immediately without producing any FR text.

---

## Failure 4 – Treats Technical Inference as Established Fact (Rule: “Every functional requirement must define an observable boundary.”)

- **Quoted Rule**: *“You are STRICTLY PROHIBITED from outputting requirements with generic placeholders (e.g., `(Placeholder: ...)` or `(to be defined)`).”*
- **Failure**: The skill may infer a CLI contract from a binary name mentioned in the milestone (e.g., assuming `process-rewards` exists) and declare it as a concrete Executable Contract without explicit milestone confirmation.
- **Correction**: Replace inferred contracts with a clear “Inferred Contract – requires verification” flag, or demand an explicit milestone statement defining the contract.

---

## Failure 5 – Leaves Design Specified Too Lightly (Rule: “No Prose Contracts: Never write a requirement that forces downstream verification to use grep or text‑matching.”)

- **Quoted Rule**: *“Never write a requirement that forces downstream verification to use grep or text‑matching (unless explicitly defining a literal template boilerplate).”*
- **Failure**: Some generated specifications include vague prose such as “the system shall handle user data responsibly,” which cannot be mechanically verified.
- **Correction**: Restrict all FRs to the three concrete contract types (CLI, Schema, Filesystem) and provide a verifiable predicate (e.g., “`process-rewards --allocate <amount>` returns exit code 0”).

---

## Failure 6 – Produces a Specification That Verification Cannot Meaningfully Verify (Rule: “Acceptance Criteria must be verifiable via framework validators, referencing FR titles or module boundaries.”)

- **Quoted Rule**: *“Acceptance Criteria must be verifiable via framework validators, referencing FR titles or module boundaries. Do NOT use command invocations.”*
- **Failure**: Acceptance criteria sometimes reference generic module names (e.g., “Auth‑Service”) without specifying a validator or observable artifact, making automated verification impossible.
- **Correction**: Tie each Acceptance Criterion to a concrete validator: a schema file, an executable contract, or a filesystem state check with a precise path and expected content.

---

## Failure 7 – Overfills Templates with Generic Prose (Rule: “No Sequential Duplication or Cross‑Contamination.”)

- **Quoted Rule**: *“Never redefine, duplicate, or re‑specify functional CLI arguments or outputs for tools that have already been implemented, evaluated, and reviewed in previous sequences.”*
- **Failure**: Generated specs frequently reuse boilerplate sections verbatim from prior specifications, leading to duplicated prose that adds no new requirement.
- **Correction**: Enforce a per‑spec template purge: strip all previously used text and require each section to be regenerated based solely on the current milestone’s content.

---

## Failure 8 – Violates Upstream/Downstream Responsibility (Rule: “Traceability Lineage: Every specification artifact must include a `derived_from` field linking to the milestone ID.”)

- **Quoted Rule**: *“Every specification artifact must include a `derived_from` field linking to the milestone ID.”*
- **Failure**: In some generated front‑matter blocks the `derived_from` field is omitted or incorrectly populated, breaking the traceability link required for downstream verification.
- **Correction**: Automatically inject a validated `derived_from` entry immediately before writing the file, and run a post‑write check to ensure the field is present and correctly formatted.

---

## Failure 9 – Loses Artifact Traceability (Rule: “Artifact Completeness: The generated file must include all required sections (YAML frontmatter, Objective, Functional Requirements, Architecture Impact with allowlist/denylist, Acceptance Criteria, Next Steps).”)

- **Quoted Rule**: *“The specification must contain a valid YAML frontmatter enclosed in `---` delimiters with required fields (`id`, `type`, `title`, `milestone_id`, `status`, `derived_from`, `template_version`).”*
- **Failure**: Some generated specifications omit the `Objective` or `Architecture Impact` sections when the milestone lacks explicit language, resulting in incomplete artifacts.
- **Correction**: Mandate that every required section header must be present; if the milestone does not provide content, insert a `#NEEDS-CLARIFICATION` marker rather than omitting the section.

---

## Failure 10 – Produces an Apparently Valid but Semantically Weak Specification (Rule: “The specification must be machine‑readable and directly consumable by the `generate-verification` stage.”)

- **Quoted Rule**: *“The specification must be machine‑readable and directly consumable by the `generate-verification` stage.”*
- **Failure**: The generated YAML sometimes contains placeholder values (e.g., `status: draft`) that are not replaced, leading to a file that parses but fails verification due to missing substantive contracts.
- **Correction**: Validate the final YAML against a schema that requires non‑placeholder values for all mandatory fields before allowing file write.

---

### Summary of Recommendations
- Insert explicit citation markers for each FR.
- Remove automatic clarification prompts unless a binding is truly undefined.
- Enforce a pre‑generation “all bindings defined” check.
- Flag inferred contracts rather than asserting them.
- Ban vague prose; restrict to observable contract forms.
- Bind acceptance criteria to concrete validators.
- Prevent reuse of boilerplate across specs.
- Auto‑populate and verify `derived_from` and other required front‑matter fields.
- Validate final YAML against a strict schema before write.

*Prepared by the adversarial review team for the `generate-spec` skill.*