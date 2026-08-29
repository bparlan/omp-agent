# OMP/AEF Infrastructure Audit & Structural Alignment Report

## Executive Summary
This report provides a rigorous, critical, and evidence-based architectural checkup of the **OhMyPi (OMP) Agentic Engineering Framework (AEF)** infrastructure. It evaluates how the pipeline upgrades introduced in **Report 05** and **Report 06** (specifically the 12-stage state machine, automated repair loops, and close-milestone validation) have impacted historical core development skills, helper scripts, and templates.

Through detailed static analysis and metadata sweeps, we have identified several **prompt-driven contradictions**, **unresolved deadlocks**, and **strict parser collisions** that currently cause the pipeline to "fail-closed" or deadlock.

This document provides:
1. A clear mapping of the upgraded 12-stage SDD State Machine.
2. A critical evaluation of alignment gaps across core development, post-evaluation, and loop-closure skills.
3. A detailed diagnosis of Python plumbing bugs (regex format constraints, YAML scanner crashes, and double-escaping errors).
4. Critical architectural questions to align our next steps.
5. A concrete, tactical stabilization roadmap to reach a 100% stable, hands-free development environment.

---

## 1. The Upgraded SDD State Machine

Following the upgrades in Report 05 and Report 06, the Spec-Driven Development (SDD) pipeline was expanded from an 11-stage process to a **12-stage sequential state machine** [3, 76, 624-626]. This upgrade introduced automated lint gates, post-evaluation routing, horizontal repair loops, and loop-closure validation [3, 5, 6].

### The 12-Stage Lifecycle Sequence
The canonical, sequential progression of a milestone is defined as follows [3, 76, 626]:
1. **`milestone`** $\rightarrow$ Elicits requirements interactively, creates the authoritative contract `M{X}.md` [State: `PLANNING_READY`] [914, 956].
2. **`generate-spec`** $\rightarrow$ Translates milestone intent into verifiable specifications `M{X}S{Y}.md` with stable Semantic FR IDs [State: `SPEC_GENERATED`] [921, 956].
3. **`generate-verification`** $\rightarrow$ Translates specifications into a verification protocol `M{X}S{Y}V.md` [State: `VERIFICATION_GENERATED`] [933, 956].
4. **`generate-tests`** $\rightarrow$ Translates verification protocol into executable test scripts under `tests/M{X}/` and initializes the test plan ledger `M{X}S{Y}T{Z}.md` [State: `TESTS_GENERATED`] [934-936, 956].
5. **`evaluate-tests` (Phase 1 Baseline)** $\rightarrow$ Executes generated tests against a blank/empty codebase to verify shebang compliance, check for NUL bytes, detect "False-Pass" leaks, and certify a "Red" TDD baseline [State: `TESTS_VERIFIED`] [587, 592, 952].
6. **`approve-spec` (Approval Gate)** $\rightarrow$ Presents baseline results and stamps explicit human approval `* [x] Approved for implementation by user` under `#### User Approval` inside `M{X}S{Y}.md` [State: `APPROVED_FOR_IMPLEMENTATION`] [680, 956].
7. **`implement-specification`** $\rightarrow$ Translates specification into production code and generates completion report `M{X}S{Y}C.md` with captured raw evidence [State: `IMPLEMENTING`] [660, 664, 956].
8. **`evaluate-implementation` (Phase 2 Optimizer)** $\rightarrow$ Runs tests against implementation, triggers the auto-optimizer loop to fix minor logic typos, and generates evaluation report `M{X}S{Y}E.md` with YAML "Structured Findings" [State: `EVALUATED_OK`] [521, 524, 956].
9. **`review-implementation`** $\rightarrow$ Runs independent zero-trust reality audits of implementation, generates review report `M{X}S{Y}R.md` [State: `REVIEWED_OK`] [878, 881, 956].
10. **`sync-documentation`** $\rightarrow$ Integrates review changes into ROADMAP, CHANGELOG, and indices [State: `SYNCED`] [926, 956].
11. **`close-milestone` (Terminal Gate)** $\rightarrow$ Audits loop-closure (ensuring all fixes were evaluated/reviewed), checks duplicates, parses completeness, and writes closure artifact `M{X}CLOSE-{N}.md` [State: `CLOSED` / `CLOSED_WITH_DEFECTS`] [292-297, 831].
12. **`archive-milestone` / `archive-docs`** (Optional) $\rightarrow$ Cleans up active folders and archives completed documents to `milestones/archive/` [State: `ARCHIVED`] [258, 259, 956].

### The Horizontal Post-Evaluation Auto-Repair Loop
A core addition to the orchestration engine is the horizontal fix-and-re-evaluation loop triggered when `evaluate-implementation` exits with `EXIT_CODE=1` (valid failures remain) [5, 627, 628]:
```
                   [evaluate-implementation] (EXIT_CODE=1)
                              |
                     (Classify Failures)
                              |
             +----------------+----------------+
             |                                 |
      [MINOR DEFECT]                   [COMPLEX ISSUE]
             |                                 |
       /hotfix-issue                  /investigate-issue
             |                                 |
     (Surgical Patch)                (Root Cause Analysis)
             |                                 |
             |                         (Changes Required?)
             |                         |                 |
             |                        YES               NO
             |                         |                 |
             |                         v                 |
             |                (Return to Spec Gate)      |
             |                         |                 |
             +-------------------------+-----------------+
                                       |
                                       v
                           [evaluate-implementation]
```
To prevent infinite loops, the orchestrator enforces a repair limit (`MAX_AUTO_REPAIR_CYCLES`, default 2-3 attempts) per task before escalating to `HUMAN_ESCALATION` [5, 78, 630].

---

## 2. Gaps & Misalignments in Core Development Skills

Despite the rigor of the 12-stage state machine, several older skills were designed under pre-upgrade assumptions. This creates critical operational deadlocks.

### A. The "False-Green" / Brownfield Paradox (`evaluate-tests`)
*   **The Problem:** The Phase 1 precheck auditor (`evaluate-tests`) is designed to fail-closed and throw `EXIT_CODE=2` if any functional code test (`IMPLEMENTATION_CHECK`) passes cleanly with exit code `0` before coding begins, classifying it as a "TDD False-Pass Leak" (due to a circular mock or empty assertion) [128, 588].
*   **The Conflict:** When starting milestone work on a **brownfield codebase** (where the target binary or class has already been partially implemented or exists from prior sequences), the test naturally passes with exit code `0` [128, 588]. Under old rules, this legitimate pass locks the precheck gate [128, 588].
*   **The Solution:** The updated `evaluate-tests` (v1.2.0) and `implement-specification` (v1.3.0) skills were modified to support the **`VALID_BROWNFIELD_PASS`** exception [588, 664]. When a pre-implementation test passes cleanly, the auditor must inspect the filesystem; if the implementation binary is physically present on standard disk and contains non-trivial logic, it is certified as a valid brownfield pass, unblocking the pipeline [128, 588]. However, many templates and manual checklists in older milestones are still unaligned with this exception.

### B. The Shebang-Comment Header Collision (`generate-tests` vs `evaluate-tests`)
*   **The Problem:** The `generate-tests` skill (v2.0.0-stable) historically mandated that *every* test file must start with `# {Verification IDs: ...}` comments on Line 1 to support raw metadata scanning [8, 640]. However, `evaluate-tests` strictly mandates that all executable Python and shell scripts must contain a valid shebang line (`#!/bin/bash` or `#!/usr/bin/env python3`) on **line 1** to prevent interpreter mismatches [87, 128, 552, 588].
*   **The Conflict:** Pushing the shebang line to Line 2 causes `evaluate-tests` (and standard shell environments) to flag the script as `INVALID_TEST` (missing shebang on Line 1), locking the baseline validation [127, 128, 587, 588].
*   **The Solution:** The `generate-tests` skill was bumped to **v3.7.0-stable** to enforce placing the language-appropriate shebang strictly on Line 1, and the traceability comments on subsequent lines [522].

### C. Stale "Ghost" Entries in the Test Ledger (`M{X}S{Y}T{Z}.md`)
*   **The Problem:** During active iteration, test scripts are frequently renamed, deleted, or converted (e.g., from `.sh` to `.py`) [51, 638]. Under older implementations, `generate-tests` would append or merge new test cases into the test plan ledger (`milestones/M{X}/M{X}S{Y}T{Z}.md`) [51, 640].
*   **The Conflict:** Obsolete test files remain documented in the ledger's traceability table [51, 640]. When `evaluate-tests` or `evaluate-implementation` parses the ledger, they attempt to locate and execute these non-existent "ghost" scripts, triggering immediate validation and persistence gate failures [51, 118, 127].
*   **The Solution:** Mandate a strict **Ledger Truncation Rule** where `generate-tests` completely overwrites or truncates the test plan ledger file upon initialization, mapping only successfully generated, validated, and physically written test scripts [51, 640]. We must also run `omp-sanitize-tests-v3.py` to prune stale ledger rows from active test plans [9].

---

## 3. Gaps in Post-Evaluation & Loop Closure Processes

The post-evaluation phase introduces several advanced artifacts, but their integration with older support skills is currently broken.

### A. Non-Parseable Metadata in Support Artifacts (`hotfix-issue` & `investigate-issue`)
*   **The Problem:** The loop-closure gatekeeper (`close-milestone`) and the metadata validator (`validate_metadata.py`) strictly enforce valid YAML frontmatter blocks containing `id`, `type`, `milestone_id`, and `derived_from` fields on *all* milestone documents [8, 71, 836].
*   **The Conflict:** Older versions of the `hotfix-issue` and `investigate-issue` skills write unstructured, pre-metadata markdown files (e.g., `M10H1.md`) with **zero YAML frontmatter** [70, 72]. During the mechanical audit phase of `close-milestone`, these files trigger parse errors, forcing the milestone closure into a permanent `CLOSED_WITH_DEFECTS` status [71, 73, 836, 839].
*   **The Solution:** Update `hotfix-issue` and `investigate-issue` SKILL files and their associated templates (`hotfix_template.md` and `investigation_template.md`) to strictly enforce writing valid YAML frontmatter at generation time [99, 120, 575, 576].

### B. The `review-implementation` Dead-End Gap
*   **The Problem:** Under the upgraded state machine, if `evaluate-implementation` fails (exit code 1), the orchestrator automatically routes to `hotfix-issue` or `investigate-issue` [5, 627, 628].
*   **The Conflict:** If evaluation passes but the Zero-Trust Review Agent (`review-implementation`) exits with `EXIT_CODE=1` (identifying core specification non-compliance, missing security rules, or undocumented technical debt), **there is no defined handoff or automated loop** [68, 69, 533]. The pipeline simply halts, leaving the milestone in limbo [68, 69, 533].
*   **The Solution:** Expand `manage-development`'s state machine to support a secondary horizontal repair loop: when `review-implementation` reports a `CONTRACT_FAILURE` or critical specification mismatch, it must trigger `investigate-issue` to trace the compliance gap and route back through `implement-specification`.

### C. The Documentation Sync Stage-Ordering Anomaly
*   **The Problem:** In the upgraded pipeline, `sync-documentation` is defined as Stage 10, and `close-milestone` is defined as Stage 11 [76, 626].
*   **The Conflict:** `sync-documentation` is responsible for updating ROADMAP, CHANGELOG, and indexing documents based on completed work [926]. However, running this *before* `close-milestone` means we are updating project documentation before the loop-closure audit has certified the milestone's completion [6, 76, 292, 626]. If `close-milestone` subsequently fails or issues a `REFUSED` status, the canonical documents have already been synced as completed [6, 71, 839]. Furthermore, `sync-documentation` completely misses the closure report `M{X}CLOSE-{N}.md` because it runs before the closure report is even generated [6, 71, 838].
*   **The Solution:** Re-order the strategic lifecycle sequence: `close-milestone` must run first as Stage 10. Once loop-closure is certified and `M{X}CLOSE-{N}.md` is physically saved, `sync-documentation` should execute as Stage 11, distilling both the review report and the authoritative closure report into long-lived documentation.

---

## 4. Technical Validation Bottlenecks (Python Plumbery)

Our mechanical checkup of the Python scripts in `/workspace/artifacts/` has revealed two major, active bugs that will crash the development workspace:

### A. Syntax Error in `validate_metadata-v3.py` (ACTIVE BUG)
During our compilation sweep, the latest version of the metadata validator (`validate_metadata-v3.py`) crashed on line 99 with a fatal SyntaxError:
```text
  File "/workspace/artifacts/validate_metadata-v3.py", line 99
    print(f\\\"Metadata OK: {filepath} ({data['id']} - {data['type']})\\\")
            ^
SyntaxError: unexpected character after line continuation character
```
*   **The Cause:** This is a classic **JSON Double-Escaping Bug** [12, 638]. When the script was written or transferred, double quotes were converted into backslash-escaped quotes `\\\"`, and the backslashes themselves were escaped, creating `f\\\"`. Python interprets `f\\` as a line continuation character followed by an illegal character `\\\"`.
*   **The Impact:** This syntax error completely disables metadata validation in Sequence 11.
*   **The Cure:** Replace `validate_metadata-v3.py` with a cleanly formatted, syntax-valid script utilizing standard quotes (identical to `validate_metadata-stable-v2.py`).

### B. Broken YAML Parsing in `test-evaluation_template.md` (ACTIVE BUG)
When executing static analysis on the transition templates, we discovered that `test-evaluation_template.md` throws a PyYAML crash:
```text
Error reading test-evaluation_template.md: while parsing a flow sequence
  in "<unicode string>", line 7, column 15:
    derived_from: [SPEC-{Y}, VER-{Y}, TSET-{Z}]
                  ^
expected ',' or ']', but got '{'
```
*   **The Cause:** PyYAML safe loading treats curly braces `{}` as inline dictionary initializers. Inside a flow sequence `[...]`, writing unquoted placeholders like `SPEC-{Y}` violates the YAML standard.
*   **The Impact:** Any downstream validator or orchestrator trying to load this template safely will immediately crash, locking the pre-implementation baseline.
*   **The Cure:** The placeholders inside the flow sequence must be double-quoted in the template file: `derived_from: [\"SPEC-{Y}\", \"VER-{Y}\", \"TSET-{Z}\"]`.

### C. Missing Core Types in `validate_metadata-stable-v2.py`
*   **The Problem:** The metadata validator `validate_metadata-stable-v2.py` restricts valid document types to: `['specification', 'verification', 'test_set', 'completion', 'evaluation', 'review', 'milestone']` [13, 603].
*   **The Conflict:** Report 05 and Report 06 officially registered additional pipeline artifacts: `investigation` (`M10S1I1.md`), `session_audit` (`M10SA1.md`), and `findings` (`M10S1_FINDINGS.md`) [34, 583]. Running `validate_metadata-stable-v2.py` against these valid artifacts will fail, locking the pipeline [34, 583].
*   **The Cure:** Update `validate_metadata.py` to register the new types in its valid list: `['specification', 'verification', 'test_set', 'completion', 'evaluation', 'review', 'milestone', 'investigation', 'session_audit', 'findings']` [34, 583].

### D. The Repo-Namespace Colon Validation Failure (`aef:SPEC-M10S4`)
*   **The Problem:** Report 04 established that multi-project repositories may adopt a repo-namespace prefix (e.g., `aef:SPEC-M10S4` or `baria:COMP-M8S2`) to prevent duplicate ID collisions across repositories in a shared workspace [8, 597].
*   **The Conflict:** The regex constraint inside `validate_metadata.py` is hardcoded as `^[A-Z]+-[A-Z0-9]+$` [12, 601]. The colon `:` character is not part of the alphanumeric char class [12, 601]. Therefore, any valid, namespaced artifact ID is rejected by the validator [12, 601].
*   **The Cure:** Update the ID validation regex inside the metadata validator to optionally support an alphanumeric namespace prefix followed by a colon: `^(?:[a-z0-9]+:)?[A-Z]+-[A-Z0-9]+$`.

---

## 5. Architectural Discovery Questions

To reach the most stable, bulletproof infrastructure for app development, we must align on some key architectural preferences. Please review these three questions:

1.  **Strict Namespacing vs. Milestone Isolation:** Do you intend to enforce the repo-prefixed namespacing scheme (e.g. `aef:SPEC-M10S10`) across all projects, or should we align on standard milestone-qualified IDs (e.g. `SPEC-M10S10`)? Standardizing on standard milestone-qualified IDs simplifies downstream tools, but namespacing provides complete isolation across multi-repository workspaces.
2.  **Autonomous Review Repair Loop:** Do you want us to design and implement an autonomous repair loop for Stage 9 (`review-implementation` failures)? If yes, we can configure `manage-development` to route review failures to `investigate-issue` and trigger an automated edit cycle, matching our evaluation failure workflow.
3.  **The Positioning of `sync-documentation`:** Do you approve re-ordering Stage 10 and 11, placing `close-milestone` first as Stage 10 and `sync-documentation` second as Stage 11? This ensures the long-lived documentation captures the certified closure state and includes the generated closure artifact.

---

## 6. Tactical Stabilization Roadmap

To resolve these contradictions and establish a highly stable development framework, we propose the following concrete, step-by-step roadmap:

### Step 1: Repair the Active Python Validator (`validate_metadata.py`)
*   **Action:** Re-write the master `validate_metadata.py` file to replace the broken v3 file.
*   **Enhancements:**
    *   Fix the escaped quote syntax error [99, 127].
    *   Add BOM-stripping support to gracefully handle UTF-8 byte-order-marks [98, 638].
    *   Support flag-filtering (strip out option flags `--spec` and `--verification` to prevent argv collisions) [7, 602].
    *   Register the newly adopted transition types: `investigation`, `session_audit`, and `findings` [34, 583].
    *   Update the ID validation regex to safely support repo-prefixed namespace colons: `^(?:[a-z0-9]+:)?[A-Z]+-[A-Z0-9]+$` [12, 601].

### Step 2: Fix the Transition Templates
*   **Action:** Update `templates/test-evaluation_template.md` to:
    *   Quote the placeholder variables inside the flow sequence: `derived_from: ["SPEC-{Y}", "VER-{Y}", "TSET-{Z}"]` to prevent PyYAML loading crashes.
    *   Normalize `type: test_evaluation` to the canonical single-word enum `type: evaluation` to pass metadata schema checks [583, 600].
*   **Action:** Update `templates/completion_template.md` and `templates/evaluation_template.md` to include robust formatting rules for the `## Raw Evidence` section [9, 18, 578].

### Step 3: Upgrade `hotfix-issue` and `investigate-issue` Skills
*   **Action:** Modify the skills to ensure their generated reports (`milestones/M{X}/M{X}H{Z}.md` and `milestones/M{X}/M{X}S{Y}I{Z}.md`) write complete, valid YAML frontmatter blocks upon file creation [70, 72]. This satisfies `close-milestone` loop-closure audits and prevents `CLOSED_WITH_DEFECTS` status [71, 836].

### Step 4: Align `manage-development` and `close-milestone` Sequencing
*   **Action:** Re-order stages 10 and 11 inside `manage-development/SKILL.md` to place `close-milestone` before `sync-documentation` [6, 76, 626]. Update the orchestrator's state transitions to ensure that documentation sync operates on a certified, closed milestone.

---

### Applied Citations & Grounding Index
This audit and analysis are strictly grounded in the provided OMP documentation:
*   **Pipeline and Stages:** `manage-development/SKILL.md` (v2.2.0) [3, 75], `close-milestone/SKILL.md` [6, 292], `review-implementation` [878, 1108].
*   **The Mechanism and Evidence Contract:** `OhMyPi Agentic Engineering Framework` [998, 1004], `completion_template` and `evaluation_template` [544, 584, 586].
*   **Historical Gaps and Issues:** `omp-context-audit.md` [Issue A-G] [638], `validate_metadata.py` discrepancies [12, 13, 602, 603], `clean_skills.py` [21, 1073], `heal_test_scripts_v8.py` [31, 1073].
