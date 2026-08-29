# AEF Skill / Artifact Integration Template

Use this document as the canonical process and checklist whenever a new skill, closure artifact, or SDD lifecycle extension is added to AEF. It captures the broader system-awareness workflow, the exact validation gates, and the mechanical steps that keep the framework, plugin, docs, and ledger in sync.

---

## 1. Trigger Conditions

Apply this integration workflow when any of the following occur:

- A new skill is introduced (`skills/<skill-name>/SKILL.md`).
- A new artifact type or artifact-naming convention is added to the SDD lifecycle (for example, `M{X}S{Y}CLOSE-{N}.md`).
- An existing skill's lifecycle responsibilities change (for example, `close-milestone` moving from per-spec closure to milestone-only closure).
- A skill version, description, or routing rule changes in a way that affects pipeline behavior.

Do **not** apply this template to ad-hoc documentation edits or cosmetic markdown updates.

---

## 2. AEF Broader System Awareness Workflow

Before writing or editing anything, validate the broader system context. Treat the framework as an interconnected whole: skills, artifacts, docs, ledgers, and templates must all agree.

### 2.1 Skill Inventory & Dependencies

1. List every skill that may reference, invoke, or be affected by the new/changed skill.
2. Map the dependency graph:
   - Which skills call the new skill directly?
   - Which artifacts does the new skill read or write?
   - Which templates does the new skill consume?
3. Validate that the dependency targets exist and are stable. If a referenced file is missing or provisional, halt until it exists.

### 2.2 Artifact-Naming & ID Conventions

1. Confirm the new artifact's filename pattern matches existing minting rules.
   - No semantic qualifiers (`-FINAL`, `-V2`, `-CORRECTED`).
   - Filename must map cleanly to its YAML `id` field.
   - Sequential counters start at `1` and increment per scope.
2. Validate that the new artifact type does not collide with existing patterns in the same milestone directory.
3. Document the artifact in every place that enumerates artifact types (skill docs, ledger descriptions, template headers).

### 2.3 Pipeline Routing & State Machine Impact

1. Determine whether the new skill introduces new states or transitions in the SDD state machine.
2. Update every skill that owns adjacent states to ensure consistent routing rules.
3. Validate that the new state does not create parallel execution paths that bypass sequential guards.
4. Record the updated state machine in the orchestrating skill's documentation.

### 2.4 Pre-flight Integrity & Validation Gates

1. Confirm the new skill or artifact passes the same mechanical checks as existing ones:
   - Valid YAML frontmatter.
   - Required keys present (`id`, `type`, `title`, `milestone_id`, `status`, `derived_from`, `template_version`).
   - No duplicate IDs within the milestone directory.
   - Shebang/syntax checks for executable artifacts.
2. Identify whether the new skill introduces new validation gates (for example, a per-spec closure gate before milestone closure).

### 2.5 Human Interaction & Escalation Contracts

1. Decide where the new skill must use `ask` versus auto-invocation.
   - Material decisions that affect scope, approval, or closure must use `ask`.
   - Mechanical transitions that follow deterministic rules may auto-invoke the next skill.
2. Document the escalation path if the new skill fails:
   - Does it halt?
   - Does it route to `investigate-issue` or `hotfix-issue`?
   - Does it return control to the user?

---

## 3. Integration Implementation Checklist

Use this checklist for every new skill/artifact integration. Mark each item complete before declaring integration done.

### 3.1 Skill Definition

- [ ] Create or update `skills/<skill-name>/SKILL.md` with:
  - YAML frontmatter: `name`, `version`, `description`, `tools`, `user-invocable`.
  - Clear mandate: what the skill owns and what it explicitly does not own.
  - Step-by-step process with mechanical validation commands.
  - ID minting rules if the skill creates artifacts.
  - Negative guardrails that prevent scope creep.
  - References to templates and related skills.
- [ ] Add or update templates under `skills/<skill-name>/templates/`.
- [ ] Update the skill description and version if existing responsibilities change.

### 3.2 Artifact Validation

- [ ] Confirm every new artifact filename pattern is documented.
- [ ] Confirm YAML frontmatter schemas are valid and parseable.
- [ ] Confirm the new artifact integrates into the milestone completeness check in `close-milestone` or the new per-spec closure skill.
- [ ] Confirm the new artifact is included in the lineage-tracing DAG for both spec-level and milestone-level closure.

### 3.3 Ledger Registration

- [ ] Update `skills/skills-ledger.json`:
  - Add the new skill entry with name, description, version, status, last_modified, and version_validation rules.
  - Update any existing skill entries whose version, description, or validation rules changed.
  - Update `metadata.last_updated` to the current timestamp.
- [ ] Replicate the same ledger update in the plugin copy at `/Users/bparlan/.omp/plugins/node_modules/omp-aef/skills/skills-ledger.json`.

### 3.4 Documentation Sync

- [ ] Update `docs/SKILLS.md` to include the new skill or changed skill description.
- [ ] Update interaction flow diagrams or textual flows to reflect the new routing.
- [ ] Update `INDEX.md` or roadmap docs if they enumerate skill counts or categories.
- [ ] Confirm the new skill's purpose, key responsibilities, artifacts generated, out-of-scope items, and location are all present.

### 3.5 Routing & Orchestration Updates

- [ ] Update `manage-development/SKILL.md` to include the new skill in its state machine if the new skill is part of the SDD lifecycle.
- [ ] Update adjacent skills that invoke or are invoked by the new skill.
- [ ] Confirm the new artifact integrates into the milestone completeness check in `close-milestone` or the new per-spec closure skill.
- [ ] Confirm the new artifact is included in the lineage-tracing DAG for both spec-level and milestone-level closure.
- [ ] **Filename sequentialization rule:** Canonical artifact filenames MUST use sequential counters starting at `1` for the first artifact of each type within a spec. Reject bare repeated forms such as `M9S1C.md`, `VER-M9S1V.md`, `M9S1E.md`, or `M9S1R.md` when multiple artifacts of the same type exist, or when the same base name would otherwise collide with another artifact in the same spec sequence.

### 3.6 Verification Gates

- [ ] Run syntax validation on all modified skill markdown and templates.
- [ ] Run JSON schema validation on updated `skills-ledger.json`.
- [ ] Run YAML frontmatter validation on any new templates.
- [ ] Confirm no duplicate IDs, no stale references, and no orphaned template variables.

---

## 4. Example: close-spec Integration

This section records the exact integration work completed for the `close-spec` skill so future integrations can follow the same pattern.

### 4.1 What Changed

- Added new skill `close-spec` with SKILL.md and template.
- Updated `manage-development` to route to `close-spec` after `review-implementation`.
- Updated `close-milestone` to gate on all specs having individual `close-spec` artifacts.
- Bumped `close-milestone` to `1.1.0-stable`.
- Bumped `manage-development` to `2.4.0-stable`.
- Registered `close-spec` in both repo and plugin `skills-ledger.json`.
- Updated `docs/SKILLS.md` with `close-spec` section and revised `manage-development` flow.

### 4.2 Validation Commands

```bash
# Verify skill files exist
ls skills/close-spec/SKILL.md
ls /Users/bparlan/.omp/plugins/node_modules/omp-aef/skills/close-spec/SKILL.md

# Verify ledger registration
python3 -c "import json; d=json.load(open('skills/skills-ledger.json')); print('close-spec' in d['skills'])"
python3 -c "import json; d=json.load(open('/Users/bparlan/.omp/plugins/node_modules/omp-aef/skills/skills-ledger.json')); print('close-spec' in d['skills'])"

# Verify docs mention new skill
grep -n "close-spec" docs/SKILLS.md
```

### 4.3 Resulting Pipeline Flow

```
Spec Sequence M{X}S{Y}
  ├── generate-spec
  ├── generate-verification
  ├── generate-tests
  ├── evaluate-tests
  ├── approve-spec
  ├── implement-specification
  ├── evaluate-implementation
  │     ├── PASS → review-implementation
  │     └── FAIL → hotfix-issue / investigate-issue → re-evaluate
  ├── review-implementation
  ├── close-spec
  └── handoff: next spec

Milestone M{X}
  ├── repeat for each spec
  ├── close-milestone   # only when all specs closed
  └── sync-documentation
```

---

## 5. Healthcheck-Ready Notes

When the `healthcheck` skill is rebuilt, it should use this template to validate that:

- Every skill directory has a valid `SKILL.md` with required frontmatter.
- Every skill listed in `skills-ledger.json` exists on disk with matching name and version.
- Every template referenced by a skill exists and is non-empty.
- Every artifact pattern documented in a skill matches actual generated filenames in `milestones/`.
- The interaction flow documented in `docs/SKILLS.md` matches the routing logic in `manage-development/SKILL.md`.

This template is the source of truth for “what does complete integration look like.”
