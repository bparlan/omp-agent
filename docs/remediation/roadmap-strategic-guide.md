# OMP Strategic Roadmap & Architecture Design Guide

This guide establishes the strategic groundwork, design patterns, and phased prompts required to run highly effective `manage-roadmap` sessions within the OhMyPi (OMP) Agentic Engineering Framework (AEF).

Use this document to prime your strategic agents so they design your application's architecture, documentation, and milestones in a way that downstream tactical and implementation agents can execute with zero ambiguity, zero context thrashing, and high success rates [344, 381].

---

## 1. The Dual-Layer Architecture: Strategy vs. Execution

To maintain absolute system hygiene and avoid agentic chaos, you must enforce the framework's core **Dual-Layer Management Architecture** [387]:

*   **The Strategic Layer (`manage-roadmap`):** This is where you, acting as the Product Manager, define the **"What and Why"** [387, 535]. You establish the high-level business goals, use-case scenarios, non-negotiable tech stacks, architectural constraints, and the **Spec Decomposition Plan** [2014, 535].
*   **The Tactical Layer (`manage-development`):** This is the automated Spec-Driven Development (SDD) assembly line that handles the **"How"** [387, 411]. It reads your approved milestones (`M{X}.md`) and sequences them through contiguous code, test, and evaluation cycles [411].

> **Core Rule:** Never allow tactical code implementation details to leak into strategic roadmap planning, and never let the strategic roadmap manager guess or implement code logic [33, 533].

---

## 2. Agentic-Friendly Architecture: The Three-Layer Registry Pattern

To ensure that autonomous coding agents can modify your application without introducing regressions or colliding with other components, structure your repository around the AEF's canonical **Three-Layer Registry Pattern** [207, 214]:

```
PROJECT_ROOT/
├── data/                    # Layer 1: Data (JSON/YAML/SQLite) [218, 220]
│   └── config.json          # Persistent source of truth [220]
├── src/                     # Layer 3: Logic (Python/JS/TS) [218, 220]
│   ├── main.py              # Backend entry points [220]
│   └── utils/               # Modular features & helper utilities [220]
├── web/                     # Layer 2: View (HTML/CSS/JS) [218, 220]
│   ├── index.html           # Logic-less templates [219, 220]
│   └── static/              # Raw static assets [220]
├── templates/               # Backup and template-source directories [220]
├── tests/                   # TDD-compliant test suites [220]
├── docs/                    # Centralized markdown documentation [218, 220]
│   ├── milestones/          # Active spec/verification/evaluation artifacts [220]
│   └── skeletons/           # Structural code signatures [220]
└── README.md                # General entry point [220]
```

### Layer Separation Rules [219]
1.  **No Direct Imports Between Layer 1 (Data) and Layer 2/3:** Layer 1 data files must always be loaded and parsed through Layer 3 backend loaders. No UI file should directly read or write JSON/YAML databases.
2.  **Layer 2 (View) Must Be Logic-Less:** Keep your HTML/CSS templates free of embedded python, complex JavaScript execution, or state mutations. Let Layer 3 inject static strings or handle layout changes dynamically through well-defined API boundaries.
3.  **Strict File Scope Allowlist:** When a development cycle begins, the specification MUST list the exact files permitted to change in its `Strict File Scope (Allowlist)` [49]. Edits outside the allowlist are treated as critical integrity failures and blocked [49, 1722].

---

## 3. The Prompt Engineering Playbook for Roadmaps

Drawing from elite agentic engineering practices, follow these four strategic directives to structure your roadmap and milestones [256, 447]:

### Directive 1: Vision-to-Decomposition (Start High, Drill Deep) [258]
Do not try to write 100-line specifications yourself. Instead, feed the strategic agent a concise 5-line objective brief explaining the feature, use-case, and user target [258, 263]. Instruct the agent to expand this brief into a formal, structured milestone proposal [258]. Iterate on the plan and success criteria first, then seal it before a single line of code is touched [259, 261].

### Directive 2: Establish Three-Tier Boundaries upfront [288]
Your milestones and specifications must explicitly document agent behavioral boundaries [266]. Structure them into a strict three-tier system:
*   **✅ ALWAYS DO:** Autonomous actions the agent should execute immediately without asking (e.g., "Always write unit tests for new API utilities," "Always format code before committing") [288].
*   **⚠️ ASK FIRST:** Actions requiring explicit user validation (e.g., "Ask first before altering database schemas," "Ask first before adding an external npm/pip package") [288].
*   **🚫 NEVER DO:** Hard, non-negotiable stops (e.g., "Never modify layout structure unless specified," "Never commit raw API keys or secrets") [289].

### Directive 3: Enforce Observable Success Criteria (Purity over Prose) [345-346]
Subjective criteria (e.g., "The UI should look modern," "The server must handle errors gracefully") cause downstream testing agents to flail or invent fake test assertions [345].
*   Every success criterion MUST reference an **observable system state or artifact** [2015, 346].
*   Translate prose goals into concrete interface boundaries: CLI commands with explicit exit codes, strict JSON output schemas, or specific file creations [49, 346].

### Directive 4: Avoid Task Overloading (Modular Milestone Splits) [190, 276]
Do not pack an entire application rewrite into a single milestone [276]. A healthy milestone contains **2 to 5 concrete, isolated deliverables** [537]. If a milestone has more than 5 deliverables, instruct `manage-roadmap` to split it into contiguous sequential specifications (e.g., `M1S1`, `M1S2`, `M1S3`) [1806, 2014].

---

## 4. Establishing a Verifiable `MILESTONES.md`

Your `docs/MILESTONES.md` file tracks project-wide historical integrity [442, 534]. Ensure that it adheres to this strict markdown layout:

```markdown
# Project Milestones Registry

This registry tracks the status and canonical closure artifacts of all project development cycles.

## Active Milestones
*   - [M1] - Core Data Store & API Registry (active)
*   - [M2] - Frontend View Integration (active)

## Archived Milestones
*   - [M0] - Project Bootstrap & Tooling Verification (archived) ──> milestones/archive/M0/
```

---

## 5. Phased Prompts for Your `manage-roadmap` Session

Copy-paste these sequential prompts into your active `manage-roadmap` session to steer the planning process step-by-step:

### Phase 1: Ingesting the Use-Case and Tech Stack
```text
You are operating under the Technical Product Manager persona for the "manage-roadmap" skill.
I want to establish the groundwork for my application's architecture and roadmap.

Here is the high-level vision of the application:
[PASTE APP VISION / SCENARIO / DESCRIPTION HERE]

Our chosen technical stack is:
[PASTE TECH STACK / LANGUAGES / FRAMEWORKS HERE]

Please analyze this vision. Map out how we will decompose this application according to the Three-Layer Registry Pattern:
- Layer 1 (Data): What persistent data, schemas, or JSON configurations do we need?
- Layer 2 (View): What logic-less HTML/CSS/template files represent our UI?
- Layer 3 (Logic): What backend scripts, controllers, or modules handle the execution?

Output your architectural mapping clearly, then list any immediate ambiguities or details we must clarify before proposing a milestone plan.
```

### Phase 2: Defining the Three-Tier Boundaries & Integration Bindings
```text
Now that we have mapped the Three-Layer structure, let's establish the guardrails and boundaries for our development team (the downstream AEF agents).

Based on our architectural mapping, let's document:
1. Integration Bindings: Detail any pre-existing binaries we must consume, static test fixtures we need to prepare, or expected output schemas.
2. The Three-Tier Boundaries:
   - What should downstream agents ALWAYS DO autonomously?
   - What must they ASK FIRST before modifying?
   - What are they strictly FORBIDDEN from doing (NEVER DO)?

Draft these boundaries and bindings. Ensure that all success criteria are written as observable system states or physical artifacts, rather than vague prose or command invocations. Present the draft for my review.
```

### Phase 3: Milestone Planning & Decomposition
```text
Let's decompose this roadmap into highly focused, contiguous milestones to prevent context thrashing during development.

Review the scope we've defined. I want us to plan exactly N milestones. Each milestone must contain:
1. A single, concise Goal and Motivation.
2. A Spec Decomposition Plan outlining the exact sequence of specifications (e.g. S1, S2) that will make up this milestone.
3. A scoped list of 2 to 5 deliverables.
4. Clear Success Criteria mapped to observable filesystem states or exit codes.

Propose the Milestone Registry entries and draft the complete `M1.md` milestone file using our canonical milestone template. Do not write any code or specs yet—let's finalize and approve the milestone plan first.
```

### Phase 4: Final Verification and Sealing
```text
Please review our drafted `M1.md` document against our quality checklist:
- Does it contain valid YAML frontmatter?
- Are there zero placeholder markers (TODO, FIXME, placeholder) left in the text?
- Are all success criteria programmatically verifiable without relying on string-matching or english prose checks?

If yes, write the finalized milestone file to `milestones/M1/M1.md` and append its active entry to `docs/MILESTONES.md`. Once written, output your standard completion and handoff instructions so we can hand over to `manage-development` and trigger our first development cycle.
```
