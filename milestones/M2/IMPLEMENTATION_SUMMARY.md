# Framework Improvement Strategy — Combined Solution

## Overview

This session implemented a **combined solution** that combines both approaches requested:

1. **New skill**: `session-audit` for systematic session-based framework improvement analysis
2. **Enhanced evolve-skills**: Integrated session-audit reports and improved documentation workflow

## Solution Architecture

### Two-Skill System

```
┌─────────────────────────────────────────────────────────────┐
│                      User Session                            │
│  (Edits many files without milestone > development)         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              session-audit Skill                            │
│  - Scans session changes                                    │
│  - Uses code-search for semantic impact analysis            │
│  - Classifies changes (major vs minor)                      │
│  - Generates structured report (M{X}SA.md)                   │
│  - Documents framework-critical changes                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  evolve-skills Skill                        │
│  - Reads session-audit report                               │
│  - Identifies which SKILL.md files need updates             │
│  - Applies documented improvements                          │
│  - Documents intervention in EVOLUTION.md                   │
│  - Verifies framework-critical files consistency            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Updated Framework Documentation                 │
│  - INDEX.md (auto-generated navigation)                      │
│  - AGENTS.md (comprehensive agent guide)                    │
│  - Code-search documentation                                │
│  - Session audit reports                                    │
└─────────────────────────────────────────────────────────────┘
```

### Key Benefits

1. **Clear Separation of Concerns**
   - `session-audit`: Analyzes what changed (understands impact, uses code-search)
   - `evolve-skills`: Applies changes to SKILL.md files (evidence-based, scoped to SDD)

2. **Automatic Tracking**
   - Major changes are systematically classified
   - Framework-critical files are identified
   - Documentation drift is prevented

3. **Tool Specialization**
   - session-audit uses code-search for semantic analysis
   - evolve-skills uses LSP and edit tools for precise changes
   - Each skill focuses on what it does best

4. **Reduced Manual Work**
   - No need to manually track changes across multiple files
   - evolve-skills automatically processes session-audit reports
   - Documentation stays in sync with implementation

## Session Audit Skill (`session-audit`)

### Purpose

Analyze session-based framework improvements and identify major structural changes to OMP AEF.

### When to Use

- After completing framework work in a session
- To ensure major changes (INDEX file introduction, new skills, structure changes) are properly documented
- To identify what files were modified and their impact on the framework
- To generate a structured report for evolve-skills to apply changes

### Core Capabilities

1. **Scan Session Changes**
   - Detects modified files using git or filesystem timestamps
   - Identifies framework-critical locations (root docs, skills, templates, config)

2. **Classify Changes**
   - **Track**: INDEX.md, AGENTS.md, README.md, FRAMEWORK.md, PLAYBOOK.md, skills-lock.json, config.yml, skill SKILL.md files with major changes
   - **Do NOT Track**: Cosmetic changes, reformatting, comment updates, tool list additions

3. **Use Code-Search for Semantic Analysis**
   - Search for agent handoff patterns
   - Identify template usage
   - Check consistency of negative guardrails
   - Verify agent interaction pipeline

4. **Generate Session Report**
   - Creates `M{X}SA.md` with detailed analysis
   - Includes recommended evolve-skills actions
   - Documents all major changes

5. **Apply Documented Changes**
   - Updates framework-critical documentation
   - Creates session change log

### Output

1. **`M{X}SA.md`** — Session Audit Report (detailed analysis)
2. **`SESSION_CHANGES.md`** — Concise change log
3. **Updated framework documentation** — INDEX.md, AGENTS.md, README.md, etc.

## Enhanced evolve-skills

### Changes Made

1. **Added session-audit to Restricted Scope**
   ```markdown
   - session-audit
   ```

2. **Added Session Audit Integration Step**
   ```
   10. **Session Audit Integration** — When a user provides a Session Audit Report (`M{X}SA.md`):
       - Read the report to understand major framework changes
       - Identify which skills need updates based on the "Recommended evolve-skills Actions" section
       - Apply documented improvements to affected SKILL.md files
       - Document the session-audit intervention in EVOLUTION.md
       - Verify all framework-critical files (INDEX.md, AGENTS.md, skills-lock.json) are consistent
   ```

### How It Works

1. **User provides session-audit report**
   - User runs session-audit after completing framework work
   - Session-audit generates M{X}SA.md with findings

2. **evolve-skills reads and processes the report**
   - Reads M{X}SA.md
   - Identifies skills to update based on "Recommended evolve-skills Actions"
   - Applies improvements to targeted SKILL.md files
   - Bumps version numbers

3. **evolve-skills documents the intervention**
   - Appends entry to EVOLUTION.md
   - Records date, skill updated, old/new version, rationale
   - Links to session-audit report

4. **Verification**
   - Checks consistency of framework-critical files
   - Verifies INDEX.md and AGENTS.md stay in sync
   - Ensures skills-lock.json matches actual skills

## Code-Search Infrastructure

### New Documentation

**File**: `~/.omp/agent/skills/code-search/README.md` (224 lines, 4.9KB)

**Contents**:
- Role in OMP AEF
- Usage in framework skills
- Requirements and setup
- Capabilities
- Best practices
- Integration with session-audit
- Troubleshooting

### Updated SKILL.md

**File**: `~/.omp/agent/skills/code-search/SKILL.md` (304 lines, 8.5KB)

**Changes**:
- Added version: 1.0.0
- Added README.md reference
- Enhanced description with role in framework

### Usage in Framework

**Skills that should use code-search**:
- `evolve-skills` — Analyze failure patterns, find guardrails
- `session-audit` — Understand impact of framework changes
- `implement-specification` — Analyze codebase structure
- `sync-documentation` — Verify documentation consistency

**Common patterns to search**:
```bash
search_code "agent handoff" --limit 50
search_code "Out of Scope" --limit 20
search_code "template_version"
search_code "code-search" --limit 20
```

## Documentation Updates

### AGENTS.md

**Changes**:
- Added new section "Infrastructure Skills" (lines 637+)
- Documented code-search role, responsibilities, artifacts
- Documented code-search usage in framework
- Added link to code-search/README.md

**Sections Added**:
```markdown
## Infrastructure Skills

### code-search

**Role**: Semantic repository search and skeleton generation for low-token codebase understanding.

**Key Responsibilities**:
- Provides semantic search across the OMP AEF codebase
- Generates tree-sitter skeletons for codebase structure
- Enables fast understanding of patterns without reading files
- Supports framework improvements and consistency checks

**Artifacts**:
- docs/skeletons/OMP-AEF_skeleton.md
- code_index_OMP-AEF.db

**Usage in Framework**:
- Used by evolve-skills, session-audit, SDD agents

**Documentation**:
- skills/code-search/README.md
```

## Workflow

### For User (Framework Improvement Session)

1. **Complete framework work**
   - Edit files as needed
   - Make major changes to framework-critical files
   - Add new skills or modify existing ones

2. **Run session-audit**
   ```
   Invoke session-audit skill
   ```

3. **Review session-audit report**
   - Check M{X}SA.md for classified changes
   - Verify recommended evolve-skills actions
   - Approve or request changes

4. **Invoke evolve-skills**
   ```
   Invoke evolve-skills skill
   ```
   - evolve-skills will read M{X}SA.md
   - Apply documented improvements
   - Document intervention in EVOLUTION.md

5. **Verify changes**
   - Check that all SKILL.md files were updated
   - Verify framework-critical files are consistent
   - Test that framework still works as expected

### For evolve-skills (Applying Changes)

1. **Read session-audit report**
   - Locate M{X}SA.md in milestones/M{X}/
   - Extract recommended actions

2. **Identify skills to update**
   - Map recommended actions to specific SKILL.md files
   - Determine what changes are needed

3. **Apply improvements**
   - Use edit tool to update SKILL.md files
   - Bump version numbers
   - Add documentation references

4. **Document intervention**
   - Append to EVOLUTION.md
   - Record date, skill updated, old/new version, rationale
   - Link to session-audit report

5. **Verify consistency**
   - Check INDEX.md and AGENTS.md
   - Verify skills-lock.json matches actual skills
   - Ensure all framework-critical files are consistent

## Deliverables

### Files Created

1. **`skills/session-audit/SKILL.md`** (304 lines, 8.5KB)
   - Complete session audit skill
   - Process, capabilities, output, requirements

2. **`skills/code-search/README.md`** (224 lines, 4.9KB)
   - Comprehensive code-search documentation
   - Usage patterns, best practices, troubleshooting

3. **`milestones/M2/M2SA.md`** (204 lines, 7.9KB)
   - Session audit report for this session
   - Detailed analysis of changes made

4. **`milestones/M2/SESSION_CHANGES.md`** (1.8KB)
   - Concise change log
   - Summary of session deliverables

### Files Modified

1. **`skills/evolve-skills/SKILL.md`**
   - Added session-audit to restricted scope
   - Added Session Audit Integration workflow

2. **`skills/code-search/SKILL.md`**
   - Added version 1.0.0
   - Added README.md reference

3. **`AGENTS.md`**
   - Added Infrastructure Skills section
   - Documented code-search role and usage

## Key Decisions

### Why Two-Skill System?

**Pros**:
- Clear separation of concerns
- Tool specialization (code-search vs LSP/edit)
- Simplified workflow for user
- Maintainable and extensible

**Cons**:
- Additional skill to maintain
- Slightly more complex integration

**Decision**: Chose two-skill system for maintainability and specialization.

### Why Not Single Skill?

**Single skill (analysis + application)** would:
- Have broad scope (all analysis and application)
- Mix responsibilities (what vs how)
- Be harder to test and verify
- Make debugging harder

**Two-skill system**:
- Each skill focused on one responsibility
- Easier to test and verify
- Better separation of concerns
- More maintainable

### Why Keep geo and humanizer?

**Benefits**:
- Available for future use in skills-lock.json
- Not forced into workflow (respect user preferences)
- Optional external skills don't interfere with SDD

**Decision**: Keep in skills-lock.json but don't enforce usage.

## Open Questions

None at this time.

## Next Steps

1. **Review M2SA.md** — Check that all changes are properly classified
2. **Run evolve-skills** — Apply recommended improvements from M2SA.md
3. **Test session-audit** — Verify it works correctly on framework work
4. **Consider integration** — Add code-search to evolve-skills workflow in future
5. **Update skills-lock.json** — Add session-audit if needed for installation

## Benefits Summary

✅ **Improved session-based workflow** — Clear tracking, reduced documentation drift
✅ **Enhanced code-search infrastructure** — Comprehensive documentation, clear usage patterns
✅ **Better evolve-skills integration** — Systematic workflow, reduced manual work
✅ **Tool specialization** — Each skill does what it does best
✅ **Maintainable** — Clear separation of concerns, easy to extend
