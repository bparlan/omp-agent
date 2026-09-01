---
id: M9
type: milestone
title: "M9 — AEF Artifact-System Integration & Project Workspace Alignment"
status: draft
template_version: 1.0.0
derived_from: []
---

# M9 — AEF Artifact-System Integration & Project Workspace Alignment

## Status

Proposed

## Objective

Integrate the canonical artifact architecture established by M9 into the existing AEF/OMP development infrastructure. This milestone ensures that AEF skills which create, locate, validate, or update artifacts operate consistently with the canonical artifact identity, type, metadata, lineage, storage, and legacy-compatibility rules defined by M9.

The milestone also establishes project-level workspace isolation so that AEF can be used both to develop AEF itself and to bootstrap and maintain independent application projects such as BariaDAO without leaking AEF-specific documentation, metadata, or development artifacts.

This milestone focuses on **artifact-system integration and workspace correctness**.

It does **not** redesign AEF's higher-level orchestration model.

---

## Architectural Context

M9 established the canonical artifact architecture.

The resulting infrastructure must now be adopted by the skills that interact with artifacts.

The canonical model is:

```
Project
  │
  ├── Project Configuration
  │     └── .omp/config.yml
  │
  ├── Canonical Artifacts
  │     ├── identity
  │     ├── type
  │     ├── metadata
  │     ├── lineage
  │     └── lifecycle state
  │
  ├── Artifact Registry / Type Definitions
  │
  ├── Artifact Resolver
  │
  └── Artifact Metadata Validator
```

Skills are consumers and producers of this model.

They must not independently invent:

* artifact IDs
* artifact types
* artifact storage locations
* metadata schemas
* frontmatter rules
* resolution precedence
* legacy handling
* project boundaries

Those concerns belong to the canonical artifact system.

---

# Scope

## In Scope

### 1. Artifact-System Adoption

Update existing artifact-producing and artifact-consuming skills to use the M9 canonical artifact model.

Affected skills include, at minimum:

* `bootstrap-project`
* `generate-spec`
* `generate-verification`
* `generate-tests`
* `implement-specification`
* `evaluate-implementation`
* `review-implementation`
* `sync-documentation`
* `archive-docs`
* `approve-specs`
* `code-search`
* `evolve-skills`
* `hotfix-focus`
* `hotfix-issue`
* `investigate-issue`
* `milestone`
* milestone creation/focus skills
* any skill that directly creates, resolves, validates, or archives canonical artifacts

The exact affected-skill inventory must be established during specification generation rather than assumed in advance.

### 2. Canonical Artifact Resolution

Skills must resolve artifacts through the canonical artifact-resolution mechanism defined by M9.

Skills must not rely on hardcoded assumptions such as:

```
milestones/M9/M9S1.md
milestones/M{X}/{artifact}.md
```

unless the canonical resolver itself explicitly defines that location.

The preferred interaction model is:

```
Skill
  ↓
Canonical Resolver
  ↓
Artifact Identity / Type / Metadata
  ↓
Resolved Physical Path
  ↓
Read or Write Artifact
```

The skill should reason from the artifact identity and metadata.

The skill should not independently reconstruct filesystem paths.

### 3. Canonical Artifact Creation

Any skill creating a canonical artifact must:

1. determine the artifact type;
2. assign or request a canonical artifact identity;
3. generate required metadata;
4. write canonical frontmatter;
5. place the artifact in its canonical storage location;
6. validate the resulting artifact;
7. report the created artifact identity and resolved path.

Creation must fail closed if the artifact cannot satisfy the canonical metadata contract.

A skill must not report successful creation when the artifact was only partially created or when metadata validation failed.

### 4. Metadata Validation

Artifact-producing skills must validate generated artifacts against the canonical metadata contract before reporting successful completion.

Validation must be performed through the canonical metadata-validation mechanism.

Individual skills must not maintain competing mandatory-field lists unless explicitly required by the artifact type registry.

The architecture must avoid this failure mode:

```
generate-spec
  └── custom metadata rules

generate-tests
  └── different custom metadata rules

milestone
  └── another metadata schema

validate_metadata.py
  └── fourth interpretation
```

The desired model is:

```
Canonical Artifact Contract
        │
        ├── Artifact Registry
        ├── Resolver
        └── Validator
                │
                ├── bootstrap-project
                ├── generate-spec
                ├── generate-verification
                ├── generate-tests
                ├── implement-specification
                └── sync-documentation
```

### 5. Project-Scoped Configuration

Introduce a project-level configuration mechanism based on:

```
.omp/config.yml
```

The configuration must define, at minimum, the project identity and development mode required by AEF infrastructure.

The exact schema must be defined by specification rather than hardcoded directly into this milestone.

The configuration must support at least:

```yaml
project_id:
project_slug:
mode:
```

Supported modes initially include:

```
framework
application
```

Additional modes must not be invented unless required by the specification.

### 6. Mode-Aware Bootstrapping

`bootstrap-project` must distinguish between at least:

```
framework
application
```

### Framework Mode

Used when developing AEF itself or another framework-like project.

Framework-specific documentation may be generated where explicitly required.

### Application Mode

Used for projects such as BariaDAO.

Application-mode bootstrapping must not blindly generate AEF-internal architectural documents such as:

```
FRAMEWORK.md
PLAYBOOK.md
DATA.md
```

unless the project configuration or specification explicitly requires them.

Instead, it must establish the minimum project-specific agent guidance required to safely work on the application.

The bootstrap process must preserve the application's own architecture and documentation conventions.

### 7. Application-Specific Agent Guidance

For application-mode projects, bootstrap must generate or install project-local agent guidance appropriate to the detected or declared technology stack, using a parameterized approach rather than hardcoded technology stacks.

For example, a Tailwind/DaisyUI application may require guardrails such as:

```
Do not modify, reorder, or remove layout or utility classes unless the active specification explicitly requires a visual or structural change.
```

However, such technology-specific rules must not be hardcoded into the universal bootstrap process.

The bootstrap architecture should support:

```
Project Mode
    +
Project Technology / Stack
    ↓
Appropriate Agent Guidance
```

The bootstrap system must not assume that every application is a Tailwind/DaisyUI project.

### 8. Documentation Synchronisation

`sync-documentation` must operate within the active project's workspace boundary.

It must resolve documentation artifacts through the canonical artifact system rather than assuming that every project contains the AEF repository's own documentation structure.

The skill must distinguish between:

```
AEF framework documentation
```

and:

```
Project documentation
```

Documentation synchronization must respect the project's configured mode (framework vs application) and canonical artifact architecture.

### 9. Milestone Artifact Integration

Milestone creation must produce canonical milestone artifacts using the M9 artifact contract, rejecting legacy filename-only documents.

New milestone artifacts must not be generated as legacy filename-only documents.

The milestone creator must:

* assign the canonical artifact identity;
* declare `type: milestone`;
* generate required metadata;
* validate metadata;
* resolve canonical storage;
* report the resulting artifact identity and resolved path.

The implementation must not assume that the filename alone establishes artifact identity.

### 10. Specification / Verification / Test Pipeline Integration

The following lifecycle must be supported:

```
Milestone
    ↓
Specification
    ↓
Verification Protocol
    ↓
Test Design
    ↓
Executable Tests
    ↓
Implementation
    ↓
Evaluation / Review
```

Each stage must consume the canonical artifact identity and metadata of the previous stage.

The skills must not infer artifact relationships solely from filenames.

Relationships such as:

```
derived_from
verifies
tests
implements
evaluates
reviews
```

must use the canonical relationship model defined by M9.

---

# Functional Requirements

## FR-1 — Canonical Artifact Contract Adoption

All affected artifact-producing and artifact-consuming skills must adopt the M9 canonical artifact model, rejecting independent schemas and decisions about artifact identity, type, metadata, lineage, storage, and legacy handling.

**Acceptance Criteria:**
- No affected skill independently defines a competing canonical artifact schema or metadata contract.
- Artifact type, identity, metadata, lineage, and storage decisions originate exclusively from the canonical artifact system (Artifact Registry, Resolver, Validator).
- Skills consume canonical artifact metadata rather than reconstructing semantics from filenames or paths.
- Skills maintain no skill-specific mandatory-field lists unless explicitly registered in the Artifact Registry.

## FR-2 — Canonical Artifact Resolution

Affected skills must resolve artifacts through the canonical artifact-resolution mechanism defined by M9, not through hardcoded assumptions or path patterns.

**Acceptance Criteria:**
- Skills do not hardcode milestone-specific artifact paths (e.g., `milestones/M9/M9S1.md`) as their primary resolution mechanism.
- Artifact resolution works when canonical artifacts are stored according to the M9 storage model regardless of location.
- Resolver failures are explicit and actionable (return structured error with artifact identity, attempted path, and failure reason).
- Ambiguous resolution does not silently select an arbitrary artifact (must surface ambiguity for human/agent intervention).

**Behavioral Specification:**
```
Skill
  ↓
Request Artifact (identity/type/context)
  ↓
Canonical Resolver (loads Registry + Validator + Storage rules)
  ↓
Return Artifact Identity/Type/Metadata
  ↓
Resolve Physical Path (via canonical storage model)
  ↓
Return Physical Path OR Error
  ↓
Skill reads/writes artifact via resolved path
```

**Ambiguous Resolution Behavior:**
```
Resolver receives ambiguous artifact request (multiple artifacts match criteria)
  ↓
Determine match criteria (identity, type, context, namespace, priority)
  ↓
If exactly one artifact matches:
  ↓
  Return artifact identity and resolved path
Else if multiple artifacts match:
  ↓
  Surface ambiguity with structured error:
    - artifact_id: list of matching artifact IDs
    - match_criteria: details about why each matched
    - user_instruction: guidance for resolving ambiguity (e.g., provide more specific identity, adjust type/context)
  ↓
  Do NOT automatically select or load an arbitrary artifact
  ↓
Skill receives ambiguous resolution error
  ↓
Either:
  - Provide more specific artifact identity/context to resolve
  - Or abort with explicit error message guiding user
```

**Error Response Format:**
```
AmbiguousResolutionError:
  error_type: "ambiguous_resolution"
  matching_artifacts:
    - artifact_id: "<id1>"
      type: "<type1>"
      match_reason: "<reason>"
    - artifact_id: "<id2>"
      type: "<type2>"
      match_reason: "<reason>"
  match_criteria:
    provided_identity: "<provided>"
    provided_type: "<provided>"
    provided_context: "<provided>"
  user_instruction: "Please provide more specific artifact identity or context. Available options: <id1>, <id2>, ... or adjust type/context criteria."
```

## FR-3 — Canonical Artifact Creation

All affected artifact-producing skills must create artifacts conforming to the canonical metadata contract, following a strict 7-step creation protocol.

**7-Step Creation Protocol:**
1. Determine the artifact type (from Artifact Registry or explicit declaration).
2. Assign or request canonical artifact identity (from Registry or generator).
3. Generate required metadata (per Artifact Registry schema).
4. Write canonical frontmatter (type, identity, metadata fields).
5. Place the artifact in its canonical storage location (per Registry storage rules).
6. Validate the resulting artifact (via canonical validator).
7. Report the created artifact identity and resolved path (or error if validation fails).

**Acceptance Criteria:**
Every successful artifact creation results in:
- canonical identity present in metadata;
- canonical type present in frontmatter and registry;
- required metadata fields populated and valid;
- valid frontmatter with correct YAML syntax and structure;
- canonical storage location (no fallback to arbitrary paths);
- successful metadata validation (all contract rules satisfied).

## FR-4 — Validation Before Completion

Artifact-producing skills must validate their generated output before reporting successful completion, rejecting partial or invalid artifacts as failures.

**Acceptance Criteria:**
- Invalid artifacts (validation failures) cause the producing skill to fail explicitly with error output.
- Partial artifact creation (e.g., missing frontmatter, invalid YAML) is not reported as successful.
- Validation is performed through the canonical validator (not custom checks per skill).
- Skills do not silently bypass validation (no `--skip-validation` flag unless it disables entire skill).

**Validation Gate Behavior:**
```
Skill executes artifact creation steps 1-7
  ↓
Before reporting success, validate artifact via canonical validator
  ↓
Validation result: PASS
  ↓
Report success with artifact identity and resolved path
  ↓
Validation result: FAIL
  ↓
Report error (validation details) and stop skill execution
  ↓
Do NOT report successful creation
```

## FR-5 — Project Configuration

`bootstrap-project` must create or update project configuration using the canonical `.omp/config.yml` model, treating configuration itself as a canonical artifact where applicable.

**Acceptance Criteria:**
- `.omp/config.yml` exists in project root;
- Configuration contains valid project configuration (project_id, project_slug, mode fields as specified in Registry schema);
- Configuration itself is treated according to canonical artifact/configuration rules where applicable (validation, lineage, storage).

**Supported Configuration Fields (per Registry schema, to be defined in M9S1 or extended later):**
- `project_id`: Unique project identifier (string, required).
- `project_slug`: Human-readable project identifier (string, required).
- `mode`: Development mode (framework | application, required).
- Optional fields as defined by Registry schema extensions.

## FR-6 — Mode-Aware Bootstrap

`bootstrap-project` must distinguish between framework mode and application mode, adjusting generated artifacts and documentation accordingly.

**Framework Mode Acceptance Criteria:**
- Preserves framework-oriented initialization behavior where appropriate (e.g., generating AEF framework documentation where explicitly required by specification).
- May generate AEF-specific architectural documents (FRAMEWORK.md, PLAYBOOK.md, DATA.md) only when explicitly required by the specification or project configuration.

**Application Mode Acceptance Criteria:**
- Does NOT generate irrelevant AEF-internal documentation by default (e.g., FRAMEWORK.md, PLAYBOOK.md, DATA.md unless explicitly required).
- Creates project-appropriate agent guidance (see FR-7).
- Preserves project-specific architecture and documentation conventions (no overwriting project conventions with AEF defaults).
- Establishes the canonical artifact infrastructure required by AEF (Artifact Registry, Resolver, Validator integration) without requiring project to adopt AEF-specific development workflows by default.

**Mode Selection Behavior:**
```
bootstrap-project receives project configuration
  ↓
If mode == 'framework':
  ↓
  Generate framework-specific artifacts and documentation where explicitly required
  ↓
  Install AEF agent guidance for framework development
  ↓
Else if mode == 'application':
  ↓
  Generate project-appropriate agent guidance only
  ↓
  Do NOT generate AEF-internal framework documentation by default
  ↓
  Preserve project architecture and conventions
  ↓
  Establish minimal AEF infrastructure (config + canonical components)
```

## FR-7 — Application-Specific Agent Guidance

For application-mode projects, `bootstrap-project` must generate or install project-local agent guidance appropriate to the detected or declared technology stack, using a parameterized approach rather than hardcoded technology stacks.

**Acceptance Criteria:**
- Bootstrap generates or installs project-local agent guidance appropriate to detected/declared technology stack (e.g., Tailwind/DaisyUI guardrails for web apps).
- Technology-specific rules are parameterized (not hardcoded in universal bootstrap process).
- The bootstrap architecture supports: Project Mode + Project Technology/Stack → Appropriate Agent Guidance.
- The system does NOT assume all application projects use a single technology stack (e.g., Tailwind/DaisyUI).

**Parameterized Guidance Model:**
```
bootstrap-project detects/declares technology stack (e.g., 'tailwind-daisyui')
  ↓
Determine appropriate agent guidance for stack (from parameter library or project configuration)
  ↓
Generate or install project-local guidance file (e.g., .agent/guidance/tailwind-daisyui.md)
  ↓
Guidance file contains stack-specific guardrails and conventions
  ↓
Subsequent AEF skills use this guidance file as constraint
```

**Example Guidance (parameterized, not hardcoded):**
```
Do not modify, reorder, or remove layout or utility classes unless the active specification explicitly requires a visual or structural change.
```

This example is part of a parameter library, not embedded in universal bootstrap logic.

## FR-8 — Documentation Synchronisation

`sync-documentation` must operate within the active project's workspace boundary.

**Acceptance Criteria:**
- `sync-documentation` resolves documentation artifacts through canonical resolution (not hardcoded paths).
- Skill distinguishes between AEF framework documentation (if in AEF project) and project documentation (if in application project).
- Skill does not inject AEF-specific documents into an application project merely because the skill itself was developed inside AEF.
- Documentation synchronization respects the project's configured mode (framework vs application) and canonical artifact architecture.

**Workspace Boundary Behavior:**
```
sync-documentation invoked
  ↓
Determine active project (from .omp/config.yml or context)
  ↓
Resolve project boundary (workspace root, allowed artifacts)
  ↓
Resolve documentation artifacts via canonical resolution
  ↓
If project is AEF framework:
  ↓
  Affect AEF framework documentation (FRAMEWORK.md, PLAYBOOK.md, DATA.md, SKILLS.md, AGENTS.md)
  ↓
Else if project is application:
  ↓
  Affect only project documentation (not AEF-specific docs)
  ↓
  Respect project conventions and architecture
```

## FR-9 — Milestone Artifact Integration

Milestone creation must produce canonical milestone artifacts using the M9 artifact contract.

New milestone artifacts must not be generated as legacy filename-only documents.

The milestone creator must:

* assign the canonical artifact identity;
* declare `type: milestone`;
* generate required metadata;
* validate metadata;
* resolve canonical storage;
* report the created artifact identity and resolved path.

The implementation must not assume that the filename alone establishes artifact identity.

## FR-10 — Pipeline Traceability

The specification → verification → test → implementation pipeline must use explicit canonical artifact relationships.

**Acceptance Criteria:**
The system can establish:

```
SPEC → VERIFICATION → TEST → IMPLEMENTATION
```

without relying exclusively on filename conventions.

## FR-11 — Legacy Compatibility

Existing legacy artifacts must remain readable according to M9's legacy compatibility rules.

**Acceptance Criteria:**
- Existing M1-M9 legacy artifacts are not mass-migrated automatically.
- Existing artifacts remain discoverable through the canonical resolution process where supported.
- New artifacts use canonical rules.
- Legacy artifacts and canonical artifacts can coexist safely.

## FR-12 — Generated Test Reliability

The verification/test generation pipeline must generate tests that are grounded in the current canonical specification and verification artifacts.

**Acceptance Criteria:**
Generated tests:

* reference the correct source specification;
* reference the correct verification protocol;
* test stated requirements rather than invented requirements;
* establish a valid initial failure path where applicable;
* do not validate documentation claims that are absent from the canonical specification;
* do not become specification validators accidentally;
* are executable in an isolated fixture environment;
* are persisted as canonical test artifacts.

The generator must not create tests whose assertions are based on guessed or hallucinated requirements.

## FR-13 — Artifact-Type Consistency

All pipeline stages must use canonical artifact types.

**Acceptance Criteria:**
The system must not produce ambiguous artifacts such as:

```
M9S4.md
M9S4V.md
M9S4T1.md
```

whose semantic meaning depends only on filename conventions.

The filename may remain human-readable, but the artifact's machine-readable type and identity must be explicit in canonical metadata.

---

# Negative Requirements

The implementation MUST NOT:

1. redesign AEF orchestration;
2. introduce an autonomous orchestration engine;
3. modify OMP internal agent implementations;
4. create a second artifact registry;
5. create a second metadata validator;
6. create skill-specific canonical path resolution;
7. require all historical artifacts to be migrated immediately;
8. mass-rewrite legacy milestone documents;
9. infer artifact type exclusively from filenames;
10. silently fabricate missing artifact relationships;
11. silently select among ambiguous artifact matches;
12. treat successful file creation as successful artifact creation without validation;
13. generate application projects with irrelevant AEF framework documentation by default;
14. assume all application projects use Tailwind or DaisyUI;
15. couple AEF's artifact model to a single project's technology stack.

---

# Non-Functional Requirements

### NFR-1 — Skill Compatibility

All 16+ affected skills must maintain backward compatibility with existing workflows where possible, introducing canonical integration as an enhancement, not a breaking change.

### NFR-2 — Error Clarity

All canonical integration failures must surface actionable error messages that include:
- Artifact identity (if resolution or creation failed)
- Expected vs actual state (if validation failed)
- Recommended next steps (if guidance needed)

### NFR-3 — Performance

Canonical resolution and validation must not introduce noticeable performance degradation for normal workflow operations (target: < 100ms for artifact resolution in typical cases).

### NFR-4 — Extensibility

The canonical artifact model must support future extensions (additional artifact types, modes, validation rules) without requiring rewrites of existing skills or migration of all existing artifacts.

### NFR-5 — Observability

Skills must log canonical integration activities (resolution attempts, validation results, mode selections) for debugging and auditing, but must not generate excessive logging in production use.

---

# Spec Decomposition Plan

This milestone will be decomposed into the following specifications:

* **M9S1** — Core artifact-system integration specification
* **M9S2** — Enhanced project configuration extension
* **M9S3** — Advanced validation and security rules
* **M9S4** — Mode-aware bootstrapping refinements
* **M9S5** — Documentation synchronization protocols

Each specification will establish explicit artifact types, resolution rules, and validation criteria.

---

# Scope

## In Scope

### Core Artifact Infrastructure
- Implementation of canonical artifact registry
- Canonical artifact resolution system
- Canonical metadata validation framework
- Integration with affected skills (16+ skills)
- Project configuration via `.omp/config.yml`
- Mode-aware project bootstrapping
- Application-specific agent guidance generation
- Documentation synchronization within project boundaries
- Canonical milestone creation
- Legacy artifact compatibility support
- Cross-project workspace isolation
- Specification → verification → test pipeline integration

### Project-Level Configuration
- Project identity (project_id, project_slug)
- Development mode selection (framework | application)
- Mode-specific artifact generation rules
- Technology stack parameter support

### Workspace Boundaries
- Framework project (AEF development) isolation
- Application project (BariaDAO) isolation
- Prevention of AEF documentation injection into applications
- Preservation of project-specific architecture

## Out of Scope

### Technical Areas
- AEF orchestration model redesign
- Autonomous workflow orchestration
- OMP internal agent implementation changes
- Migration of historical milestone artifacts
- Creation of secondary artifact registries
- Development of skill-specific resolution mechanisms

### Development Processes
- Future integration decisions deferred to M10+
- Legacy artifact migration automation
- Creation of new project modes beyond framework/application

### Performance Targets
- Implementation details that are not verifiable through tests
- Architecture optimization without functional improvements
- Internal refactoring without observable behavior changes

---

# Success Criteria

M9 is complete when:

1. **Contract Compliance**: All affected skills consume the M9 canonical artifact model
2. **Resolution Integration**: Canonical artifact resolution replaces skill-specific path guessing
3. **Creation Validation**: Artifact creation produces validated canonical artifacts
4. **Configuration Support**: `bootstrap-project` supports framework and application modes
5. **Project Config**: `.omp/config.yml` establishes project-scoped configuration
6. **Documentation Isolation**: Application projects remain isolated from AEF-specific documentation
7. **Milestone Creation**: New milestones are canonical artifacts with proper frontmatter
8. **Pipeline Traceability**: Specification → verification → test relationships are explicit
9. **Test Reliability**: Generated tests are traceable to canonical verification criteria
10. **Legacy Support**: Legacy artifacts remain readable with M9 compatibility
11. **Schema Purity**: No competing artifact registries or validators are introduced
12. **Migration Safety**: Existing legacy artifacts are not mass-migrated
13. **Test Isolation**: All M9 verification tests execute in isolated fixtures
14. **Future-Ready**: Implementation leaves system ready for future orchestration milestone
15. **Cross-Project Verification**: Both AEF framework and application project boundaries are enforced

---

# Integration Bindings

## Existing Infrastructure Dependencies

| Skill/Component | Existing Interface | Role in M9 |
|:---|:---|:---|
| `core/artifacts/resolution.py` | `resolve_artifact()` | Primary artifact resolution service |
| `core/artifacts/types.py` | `CanonicalArtifactType`, `get_artifact_type()` | Artifact type definitions |
| `core/validation.py` | `validate_metadata()` | Metadata validation service |
| `tools/omp-verify-metadata` | CLI tool | Metadata validation integration |
| `tools/omp-verify-traceability` | CLI tool | Relationship validation |

## Configuration Dependencies

### AEF Agent Configuration
- `.omp/config.yml` in agent root (project_id, mode)
- Skill-specific configuration paths

### Project Configuration
- `.omp/config.yml` in project root
- project_id, project_slug, mode fields

## Data Model Dependencies

### Artifact Registry
- Artifact type definitions in `core/artifacts/types.py`
- Legacy mappings in `resolution.py`
- Metadata validation rules in `core/validation.py`

### Validation Rules
- Required metadata fields per artifact type
- Frontmatter schema validation
- Storage location validation

## Artifacts Produced by M9

### Source Artifacts
- `.omp/config.yml` (project configuration artifact)
- `milestones/M9/M9S1.md` (specification)
- `milestones/M9/M9S1V.md` (verification protocol)
- `milestones/M9/M9S1T1.md` (test plan)
- `tests/M9/S1/` (generated test artifacts)

### Integration Points
- Updated skill SKILL.md files
- Modified AEF skill behavior
- Configuration schema extensions
- Validation rule additions

---

# Verification Strategy

Verification must validate the architecture at three levels:

## Level 1 — Artifact Contract

Verify:
- identity
- type
- metadata
- frontmatter
- relationships
- lifecycle state

## Level 2 — Skill Integration

Verify:
- bootstrap
- resolution
- creation
- validation
- documentation synchronization
- milestone generation
- specification generation
- verification generation
- test generation

## Level 3 — Cross-Project Isolation

Verify at minimum:

```
AEF framework project
        ↓
bootstrap
        ↓
framework mode
```

and:

```
BariaDAO application project
        ↓
bootstrap
        ↓
application mode
```

The verification environment must confirm that artifacts and documentation remain inside the intended project boundary.

---

# Risks

## Technical Risks

### Implementation Complexity
- **Risk**: Integrating canonical artifact system across 16+ skills requires significant coordination
- **Impact**: High - Could cause widespread disruption if not properly sequenced
- **Mitigation**: Follow implementation order, test each component in isolation

### Backward Compatibility
- **Risk**: Skills may break existing workflows during integration
- **Impact**: Medium - Could affect AEF development productivity
- **Mitigation**: Maintain existing interfaces where possible, enhance rather than replace

### Project Isolation
- **Risk**: AEF documentation may leak into application projects
- **Impact**: High - Could cause confusion and maintenance overhead
- **Mitigation**: Strict boundary enforcement, mode-aware processing

### Legacy Artifact Support
- **Risk**: Legacy artifacts may not be compatible with canonical resolver
- **Impact**: Medium - Could break existing milestone discovery
- **Mitigation**: Comprehensive legacy mapping, gradual migration path

## Operational Risks

### Configuration Errors
- **Risk**: Project configuration errors could break bootstrapping
- **Impact**: Medium - Could prevent project setup
- **Mitigation**: Schema validation, clear error messages

### Mode Misdetection
- **Risk**: Incorrect mode detection (framework vs application)
- **Impact**: Medium - Could cause inappropriate artifact generation
- **Mitigation**: Clear configuration interface, validation

### Skill Coordination
- **Risk**: Multiple skills modifying same artifacts could conflict
- **Impact**: High - Could cause race conditions
- **Mitigation**: Canonical resolution ensures single source of truth

## Mitigation Strategy

1. **Phased Implementation**: Follow the implementation order, testing each component
2. **Isolated Testing**: Use fixture environments to prevent workspace pollution
3. **Backward Compatibility**: Maintain existing interfaces where possible
4. **Clear Boundaries**: Enforce strict project workspace separation
5. **Comprehensive Testing**: Verify all 13 functional requirements through isolated tests
6. **Gradual Migration**: Support legacy artifacts alongside canonical ones
7. **Documentation Preservation**: Maintain project-specific documentation conventions

---

# Notes

1. This milestone establishes the foundation for AEF's canonical artifact system, enabling consistent artifact management across all AEF skills and projects.

2. The implementation follows a gradual integration approach, maintaining backward compatibility while introducing canonical artifact patterns.

3. Future milestones (M10+) may extend this infrastructure with additional artifact types, validation rules, and orchestration capabilities.

4. The canonical artifact model is designed to be extensible, supporting future project modes, technology stacks, and validation requirements without requiring system-wide rewrites.

5. All test fixtures and verification protocols are designed to be isolated from the active development environment to prevent accidental mutations.

6. The architecture emphasizes separation of concerns: skills focus on their domain logic while the canonical artifact system provides consistent interfaces and validation.

7. This milestone does not address AEF orchestration, which remains the focus of future milestones.

---

# Requirements Traceability

| Requirement | Scope | Success Criteria |
|:---|:---|:---|
| FR-1 through FR-13 | Core artifact infrastructure | All skills adopt canonical model |
| NFR-1 through NFR-5 | Non-functional constraints | Skills maintain compatibility, performance, observability |
| Out-of-scope items | Explicit exclusions | No premature implementation of deferred work |

---

# Completion Evidence

M9 completion requires:

- Changes to 16+ affected skills
- Updated infrastructure components
- Verification that all 13 FRs are satisfied
- Evidence of legacy artifact support
- Project isolation verification
- Cross-project boundary confirmation
- Test fixture validation

The completion report must identify:

* Changed skills and components
* Canonical artifact types exercised
* Test fixtures used
* Verification results
* Legacy compatibility evidence
* Project-isolation evidence
* Known limitations
* Explicitly deferred orchestration work

---

# Revision History

| Version | Date | Author | Changes |
|:---|:---|:---|:---|
| 1.0.0 | 2026-08-27 | Agent | Initial milestone document |
| 1.0.1 | 2026-08-27 | Agent | Added specification decomposition plan |
| 1.0.2 | 2026-08-27 | Agent | Added integration bindings table |
| 1.0.3 | 2026-08-27 | Agent | Enhanced risks section |
| 1.0.4 | 2026-08-27 | Agent | Added success criteria checklist |

---

# Template Version

template_version: 1.0.4
