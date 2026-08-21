# AEF Pipeline Responsibility Contract

## Purpose

This document defines responsibility boundaries for improving existing AEF generation skills.

The goal is to prevent stage overlap, downstream requirements reconstruction, and silent responsibility transfer.

## Stage Contract

| Stage | Operating mode | Primary responsibility | User interaction |
|---|---|---|---|
| `milestone` | Requirements Analyst | Resolve intent, scope, constraints, boundaries, and material unknowns | May ask |
| `generate-specification` | Systems Architect / Contract Decomposer | Transform milestone intent into implementable technical contracts | Must not ask |
| `generate-verification` | Adversarial Verification Engineer | Define how specification requirements become provable | Must not ask |
| `generate-tests` | Adversarial QA / Test Strategist | Produce executable evidence against verification/specification contracts | Must not ask |
| `evaluate-tests` | Independent Test Auditor | Challenge test quality, coverage, oracles, and false confidence | Must not ask |
| implementation | Engineering Executor | Implement the established contracts | Must not ask |
| evaluation/review | Adversarial Reviewer | Challenge implementation against upstream contracts | Must not ask |

## Milestone

Milestone owns:

- user intent;
- milestone objective;
- scope;
- exclusions;
- material requirements;
- architectural constraints that are already established;
- security and safety boundaries;
- meaningful acceptance conditions;
- specification decomposition boundaries;
- unresolved material questions.

It may investigate project evidence and ask the user when evidence cannot resolve a material requirement.

It seals the result before downstream processing.

## Generate-Specification

`generate-specification` owns technical refinement.

It may determine, where not already constrained:

- architecture;
- modules;
- interfaces;
- data structures;
- algorithms;
- technical contracts;
- error handling;
- implementation boundaries;
- technical dependencies;
- appropriate implementation strategy.

It must not silently redefine:

- product intent;
- milestone scope;
- business rules;
- user policy;
- security policy;
- acceptance expectations;
- externally meaningful behavior established upstream.

Recommended operating principle:

> Be opinionated inside established constraints and conservative outside them.

If a technical choice is genuinely open, make a justified engineering decision rather than asking the user.

If resolving the issue would require redefining upstream intent, emit `#NEEDS-CLARIFICATION` and halt.

## Generate-Verification

`generate-verification` owns proof.

Its core question is:

> What must be observably true for the specification to be considered satisfied?

It should derive:

- verification conditions;
- invariants;
- observable evidence;
- failure conditions;
- acceptance boundaries;
- verification methods where appropriate.

It should actively challenge specifications.

If a requirement cannot be meaningfully verified as written, it should not invent an oracle. It should fail with `#NEEDS-CLARIFICATION` when the defect cannot be resolved from authoritative context.

## Generate-Tests

`generate-tests` owns executable evidence.

Its core question is:

> What executable evidence can demonstrate the required behavior and expose meaningful failure?

It should consider:

- happy paths;
- boundary conditions;
- empty/null/zero cases;
- invalid inputs;
- state transitions;
- failure paths;
- integration failures;
- security-sensitive behavior;
- regression risks;
- test oracles.

It must not convert an ambiguous requirement into an invented expectation.

## Evaluate-Tests

`evaluate-tests` is deliberately separate.

Its purpose is independent challenge rather than self-certification.

It should evaluate whether tests:

- actually correspond to requirements;
- have meaningful oracles;
- cover important boundaries;
- can fail when the implementation is wrong;
- avoid false confidence;
- preserve traceability.

## Downstream Failure

Downstream autonomy does not mean forced completion.

The preferred behavior is:

```text
authoritative context sufficient
        ↓
continue

authoritative context insufficient
        ↓
#NEEDS-CLARIFICATION
        ↓
halt
```

Never:

```text
insufficient context
        ↓
guess
        ↓
continue
```

## Contract Refinement

Each stage may add technical precision appropriate to its responsibility.

It may not use refinement as a mechanism to redefine upstream intent.

A useful test is:

> Would this decision change what the user asked for, or only determine how the established requirement can be engineered?

If it changes what was requested, it belongs upstream.
If it determines how to implement the established requirement, it belongs downstream.

## Traceability

Every generated artifact must preserve its upstream lineage through the established metadata mechanism, including `derived_from`.

Prompt behavior should complement mechanical enforcement rather than replacing it.
