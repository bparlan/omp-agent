# AEF Generation Context

## Purpose

This document is context for improving the **existing AEF generation skills**. It is not a specification for generating new skills.

The immediate objective is to improve:

- `generate-specification`
- `generate-verification`
- `generate-tests`

and keep them consistent with the successful behavior established by the improved `/milestone` stage.

The target is practical: produce application-ready artifacts that allow the downstream pipeline to operate autonomously without silently reconstructing user intent.

## Current Generation Pipeline

The current conceptual flow is:

```text
bootstrap_project
      ↓
project knowledge / architecture context
      ↓
manage-roadmap
      ↓
milestone
      ↓
generate-specification
      ↓
generate-verification
      ↓
generate-tests
      ↓
evaluate-tests
      ↓
implementation
      ↓
evaluation / review
```

The project context includes established documentation such as:

- `ROADMAP.md`
- `MILESTONES.md`
- `PLAYBOOK.md`
- `SPEC.md`
- `TOOLING.md`
- `FRAMEWORK.md`
- `DATA.md`
- `CHANGELOG.md`
- `GAP_ANALYSIS.md`

The exact available project documents are evidence, not universal assumptions. Generation skills must remain project-agnostic.

## The Key Architectural Principle

Each stage refines an upstream contract.

It must not silently redefine upstream intent.

```text
project evidence + confirmed decisions
              ↓
          MILESTONE
              ↓
       SPECIFICATION
              ↓
        VERIFICATION
              ↓
            TESTS
              ↓
       IMPLEMENTATION
```

The milestone is the interactive requirements-convergence stage. Downstream stages are autonomous refinement stages.

## User-Interaction Boundary

The intended interaction boundary is:

```text
/milestone
    → MAY ask the user

downstream generation/evaluation stages
    → MUST NOT ask the user
```

If a downstream stage encounters a material ambiguity that cannot be resolved from the milestone, authoritative project evidence, or its own legitimate stage-level reasoning, it should:

```text
#NEEDS-CLARIFICATION
```

and halt rather than inventing a process, requirement, design decision, or expected behavior.

A halt is preferable to hallucinated continuity.

## What Should Transfer From Milestone

The following principles should generally transfer to downstream generation skills:

- evidence-first reasoning;
- explicit distinction between known, inferred, and unknown;
- anti-fabrication;
- contradiction detection;
- preservation of established constraints;
- implementation independence where appropriate;
- observable outcomes;
- traceability;
- downstream readiness;
- convergence;
- explicit failure rather than silent assumption;
- semantic consistency over token efficiency.

What should **not** automatically transfer is the milestone's user-questioning behavior.

The transferable principle is:

> Resolve ambiguity at the earliest appropriate stage. If the ambiguity belongs to milestone-level user intent, `/milestone` resolves it interactively. If a downstream stage cannot resolve a material issue from authoritative context, it fails explicitly.

## The Optimization Objective

When improving an existing generation skill, optimize for:

1. correctness of the resulting artifact;
2. fidelity to upstream intent;
3. usefulness to the next stage;
4. evidence grounding;
5. deterministic responsibility boundaries;
6. explicit handling of contradictions and unknowns;
7. mechanical traceability;
8. practical application-building value.

Do **not** optimize primarily for:

- line count;
- token count;
- apparent simplicity;
- filling every template field;
- producing an artifact without halting;
- making every stage conversational.

A shorter skill is only better when its behavioral guarantees remain intact.

## Current Improvement Goal

The milestone experiment demonstrated that a generation stage can become substantially more useful when it:

- investigates existing evidence;
- identifies material forks;
- distinguishes facts from assumptions;
- resolves material ambiguity at the appropriate boundary;
- produces a rich contract;
- prevents downstream reconstruction.

The next objective is to determine how these principles should be expressed in each existing downstream skill without making every skill behave like `/milestone`.

## Critical Rule

> **Do not make downstream generation skills behave like `/milestone`. Transfer the underlying engineering principles, not the interaction pattern.**

Each stage needs its own cognitive operating mode and responsibility boundary.
