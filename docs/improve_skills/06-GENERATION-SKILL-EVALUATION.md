# AEF Generation Skill Evaluation

## Purpose

Use this document to evaluate improvements to existing generation skills.

It is intended for practical regression analysis before and after modifying:

- `generate-specification`
- `generate-verification`
- `generate-tests`

## Core Evaluation Question

Do not ask only:

> Is the generated artifact complete?

Ask:

> Is the generated artifact more useful to the next autonomous stage, without inventing unsupported requirements or decisions?

## Evaluation Dimensions

### 1. Upstream Fidelity

Does the artifact preserve:

- user-confirmed intent;
- milestone scope;
- exclusions;
- established constraints;
- security boundaries;
- important behavior?

### 2. Evidence Grounding

Can material decisions be traced to:

- upstream artifact;
- authoritative project evidence;
- legitimate stage-level technical reasoning?

### 3. Anti-Fabrication

Did the stage invent:

- requirements;
- behavior;
- acceptance criteria;
- interfaces;
- constraints;
- technology decisions that were not justified?

### 4. Responsibility Boundary

Did the stage perform its own responsibility without:

- redefining upstream intent;
- doing work belonging to another stage;
- pushing its own responsibility downstream?

### 5. Downstream Readiness

Can the next stage proceed without reconstructing material information?

If not, classify the missing information:

- legitimate downstream design choice;
- missing project evidence;
- upstream contract defect;
- true unresolved requirement.

Do not treat all missing detail as a defect.

### 6. Contradiction Handling

Did the stage:

- detect material contradictions;
- resolve them when authority/evidence permits;
- preserve important unresolved contradictions;
- avoid silently selecting arbitrary interpretations?

### 7. Failure Behavior

When the artifact cannot be correctly produced, did the skill:

- fail explicitly;
- emit the established `#NEEDS-CLARIFICATION` state where appropriate;
- avoid hallucinating continuity?

### 8. Traceability

Does the artifact preserve valid upstream lineage through the existing metadata and `derived_from` mechanism?

### 9. Observable Quality

Are important claims:

- observable;
- verifiable;
- concrete enough for the next stage?

### 10. Information Density

Does the artifact contain useful information rather than:

- boilerplate;
- repeated prose;
- empty categories;
- generic statements?

## Stage-Specific Evaluation

### Generate-Specification

Check whether it:

- converts milestone responsibilities into technical contracts;
- establishes useful interfaces and boundaries;
- makes legitimate technical decisions;
- preserves upstream scope;
- avoids product-intent reconstruction;
- is sufficient for verification generation.

### Generate-Verification

Check whether it:

- identifies what must be proven;
- defines meaningful observables;
- exposes specification weaknesses;
- covers invariants and failure conditions;
- refuses untestable claims;
- provides useful input to test generation.

### Generate-Tests

Check whether it:

- maps to verification/specification requirements;
- contains meaningful oracles;
- attacks boundaries and failure paths;
- avoids happy-path-only testing;
- can fail when implementation is wrong;
- provides useful input to independent test evaluation.

## Adversarial Downstream Simulation

For every improvement, simulate the next stage.

Ask:

> What would the next agent still have to reconstruct?

Then classify each finding.

If the answer is material upstream intent, repair the upstream skill.

If the answer is legitimate technical design, do not over-constrain the upstream skill.

If the answer is an ambiguity that cannot be resolved, the appropriate behavior is explicit failure rather than invention.

## Regression Testing

Compare before/after artifacts.

Look specifically for:

- information lost during optimization;
- newly invented decisions;
- weaker boundaries;
- weaker traceability;
- reduced verification readiness;
- increased generic prose;
- excessive questioning;
- insufficient questioning where the stage is allowed to question;
- new dependence on hidden supportive context.

## M1 as an Empirical Reference

The improved M1 milestone is useful as a case study because it demonstrates:

- evidence-first investigation;
- targeted resolution of material forks;
- explicit contradiction handling;
- richer decomposition;
- strong integration bindings;
- observable success criteria;
- downstream convergence.

It should be treated as empirical evidence, not as a universal template for every generation stage.

## Optimization Acceptance

An optimization should be accepted only when:

1. existing successful behavior remains intact;
2. identified weaknesses are measurably reduced;
3. downstream artifact quality improves or remains stable;
4. no unsupported assumptions are introduced;
5. the stage remains within its responsibility boundary.

Line-count reduction is not an acceptance criterion.
