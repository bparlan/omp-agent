# AEF Generation Skill Improvement Principles

## Purpose

Use this document when improving an existing generation skill.

It is a refactoring and evaluation guide, not a template for creating new skills.

## 1. Preserve Behavior, Not Wording

A skill can become shorter without becoming better.

When optimizing:

- identify the behavioral contract first;
- preserve material guarantees;
- remove duplication only after semantic equivalence is established;
- avoid replacing precise rules with vague summaries.

The relevant unit is behavior, not sentence count.

## 2. Evidence Before Inference

Generation stages should establish what is known from authoritative evidence before deciding what to infer.

Distinguish:

- known fact;
- established project constraint;
- user-confirmed decision;
- reasonable technical inference;
- unresolved unknown.

Do not silently promote inference into fact.

## 3. Unknown Does Not Mean "Invent a Default"

A missing value can be:

- genuinely irrelevant;
- resolvable from evidence;
- a legitimate downstream design choice;
- a material unresolved requirement.

Only the last category requires an upstream clarification or downstream halt, depending on responsibility.

Do not fill template fields with fabricated content simply because the field exists.

## 4. Do Not Overuse "Ask"

The existence of an unknown does not automatically justify asking the user.

Use this decision process:

```text
Can authoritative evidence resolve it?
    ↓ yes → resolve from evidence

Is it a legitimate stage-level engineering choice?
    ↓ yes → decide within responsibility

Does it change upstream user intent?
    ↓ yes → milestone should resolve it

Can downstream resolve it without redefining intent?
    ↓ yes → continue

Otherwise
    ↓
#NEEDS-CLARIFICATION + halt
```

This prevents both hallucination and unnecessary interrogation.

## 5. Anti-Fabrication

Never create requirements, constraints, interfaces, acceptance criteria, or behavior merely to make an artifact look complete.

A category may legitimately be:

- not applicable;
- inherited;
- unresolved;
- delegated to a downstream stage.

Completeness means meaningful coverage, not populated headings.

## 6. Implementation Independence

Do not invent implementation decisions merely to make a contract concrete.

However, established implementation constraints must be preserved when they are:

- explicitly required;
- confirmed by the user;
- mandated by an existing interface;
- established by project architecture;
- materially binding project conventions.

The correct distinction is:

```text
invented implementation choice → forbidden
established implementation constraint → preserve
legitimate downstream design choice → decide downstream
```

## 7. Scope Semantics

Avoid arbitrary scope rules such as:

- exactly 2–5 deliverables;
- every scope item must avoid all implementation detail;
- arbitrary item counts.

Scope should describe what the stage/milestone is responsible for making:

- true;
- available;
- supported;
- preserved;
- produced.

Implementation constraints may appear when they are genuine requirements or established architectural bindings.

## 8. Contradiction Detection

Do not silently reconcile contradictory evidence.

When contradictions exist:

1. identify them;
2. determine whether authority/evidence weighting resolves them;
3. preserve the chosen resolution and rationale when material;
4. otherwise escalate according to the stage boundary.

Unrelated contradictions should not contaminate the current milestone/specification merely because they were discovered.

## 9. Observable Outcomes

Important requirements should eventually become observable.

Avoid vague criteria such as:

- works correctly;
- handles errors properly;
- is secure;
- performs well.

Translate them into meaningful observable conditions where the requirement permits it.

Do not invent metrics that were never required.

## 10. Convergence

A generation artifact is ready when the next stage does not need to reconstruct material upstream intent.

This does not mean every implementation detail must be predetermined.

The correct question is:

> What information does the next stage legitimately need to perform its responsibility without redefining upstream intent?

## 11. Token Efficiency

Token efficiency is subordinate to semantic integrity.

Good optimization:

- removes duplication;
- consolidates overlapping rules;
- eliminates harmful restrictions;
- improves precedence;
- makes instructions easier to execute.

Bad optimization:

- removes edge cases;
- collapses distinct responsibilities;
- replaces enforceable rules with slogans;
- suppresses useful context;
- encourages under-specification.

## 12. Avoid Arbitrary Rigidness

Be suspicious of instructions requiring arbitrary:

- counts;
- fixed numbers of questions;
- fixed numbers of risks;
- fixed section lengths;
- mandatory wording;
- mandatory technology choices.

A rule should exist because it protects a real behavioral invariant.

## 13. Stage-Specific Behavior

Shared principles do not imply identical behavior.

For example:

- milestone may interrogate user intent;
- specification should resolve technical design autonomously;
- verification should attack proofability;
- tests should attack executable evidence.

Transfer engineering principles, not surface behavior.

## 14. Mechanical Enforcement Is Preferable Where Available

If metadata, validators, artifact schemas, or other AEF mechanisms already enforce a rule, the skill should explain the intended behavior without redundantly recreating the entire enforcement mechanism.

Prompt rules and mechanical checks should reinforce one another.

## 15. Improve Existing Skills Incrementally

When modifying a production skill:

1. establish the current behavioral contract;
2. identify concrete weaknesses;
3. patch one coherent concern at a time;
4. run behavioral validation;
5. compare artifacts;
6. only then perform the next refactor.

Avoid broad rewrites unless the existing architecture is demonstrably unsalvageable.

## 16. Regression Principle

A successful optimization must preserve previously successful behaviors.

A shorter or cleaner skill is not a successful optimization if it produces a weaker downstream artifact.

The ultimate test is practical:

> Does the generation stage produce a more useful artifact for the next stage without introducing unsupported assumptions?
