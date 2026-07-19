# OMP AEF Framework Health Report

**Date**: 2026-07-18
**Scan Type**: Comprehensive Documentation Structure Analysis
**Status**: Critical Issues Detected

---

## Executive Summary

The OMP Agentic Engineering Framework has **5 critical issues** that require immediate attention. The framework documentation structure is inconsistent, with naming conflicts, missing files, and duplicate documentation that affects usability and maintainability.

---

## Critical Issues (5)

### 1. **SKILL.md vs SKILLS.md Naming Conflict**
- **Severity**: CRITICAL
- **Impact**: Confusion between individual skill files and comprehensive catalog
- **Details**:
  - `skills/*/SKILL.md` (lowercase) — Individual skill definitions
  - `docs/SKILLS.md` (uppercase) — Comprehensive skill catalog
- **Files Affected**:
  - All 21 skills in `skills/` directory use `SKILL.md`
  - `docs/SKILLS.md` is uppercase catalog
- **Recommendation**: Rename `docs/SKILLS.md` to `docs/skills.md` for consistency

### 2. **Skills Missing README.md Files**
- **Severity**: CRITICAL
- **Impact**: No entry points for external tools or users to understand individual skills
- **Details**:
  - 17 of 21 skills lack README.md files
  - 3 skills have README.md (code-search, geo, last30days)
  - Skills affected:
    - archive-milestone
    - bootstrap-project
    - brave-search
    - careful
    - evaluate-implementation
    - evolve-skills
    - generate-spec
    - generate-tests
    - generate-verification
    - hotfix-issue
    - humanizer
    - implement-specification
    - investigate-issue
    - manage-development
    - manage-roadmap
    - milestone
    - review-implementation
    - safe-update
    - session-audit
    - sync-documentation
- **Recommendation**: Create README.md for all 21 skills with consistent structure

### 3. **Duplicate INDEX.md Files**
- **Severity**: CRITICAL
- **Impact**: Confusion about which INDEX.md is authoritative
- **Details**:
  - `INDEX.md` (root, 61 lines) — Quick navigation hub
  - `docs/INDEX.md` (243 lines) — Complete skill catalog
- **Files Affected**:
  - `INDEX.md` (root)
  - `docs/INDEX.md`
- **Recommendation**: Remove `docs/INDEX.md` and redirect all references to root INDEX.md

### 4. **Skill Count Inconsistency**
- **Severity**: CRITICAL
- **Impact**: Documentation references wrong numbers
- **Details**:
  - AGENTS.md: 35 skills (3 strategic + 7 core + 7 support + 18 other = 35)
  - INDEX.md (root): 22 skills (13 active + 9 missing)
  - INDEX.md (docs): 35 skills
  - SKILLS.md: 35 skills
- **Files Affected**:
  - `AGENTS.md`
  - `INDEX.md` (root)
- **Recommendation**: Update INDEX.md (root) to reflect correct count (35 skills)

### 5. **Inconsistent Reference Patterns**
- **Severity**: CRITICAL
- **Impact**: Users don't know where to look for skill information
- **Details**:
  - Some docs reference `skills/*/SKILL.md` (individual files)
  - Some docs reference `docs/SKILLS.md` (catalog)
  - No unified guidance on when to use which
- **Files Affected**:
  - `AGENTS.md`
  - `INDEX.md` (root)
  - `INDEX.md` (docs)
- **Recommendation**: Add clear guidance in INDEX.md about reference patterns

---

## Major Issues (3)

### 6. **AGENTS.md Structure**
- **Severity**: MAJOR
- **Impact**: AGENTS.md references docs/SKILLS.md but main catalog is in docs/INDEX.md
- **Details**:
  - AGENTS.md references `docs/SKILLS.md` (line 102)
  - docs/INDEX.md is the main catalog (243 lines)
  - SKILLS.md (uppercase) is less prominent in docs/INDEX.md
- **Files Affected**:
  - `AGENTS.md`
  - `docs/INDEX.md`
- **Recommendation**: Update AGENTS.md to reference docs/INDEX.md instead of docs/SKILLS.md

### 7. **Reference Patterns Inconsistent**
- **Severity**: MAJOR
- **Impact**: Users unsure where to find skill information
- **Details**:
  - Some docs: "See SKILL.md in skills/*/"
  - Some docs: "See docs/SKILLS.md"
  - No clear distinction between:
    - Individual skill details (skills/*/SKILL.md)
    - Comprehensive catalog (docs/skills.md)
    - Quick reference (INDEX.md)
- **Recommendation**: Add reference pattern guide in INDEX.md

### 8. **README.md Structure Inconsistency**
- **Severity**: MAJOR
- **Impact**: Inconsistent user experience when reading skill documentation
- **Details**:
  - code-search/README.md: Comprehensive with examples
  - geo/README.md: Basic overview
  - last30days/README.md: Basic overview
  - No standard structure across all README.md files
- **Files Affected**:
  - skills/code-search/README.md
  - skills/geo/README.md
  - skills/last30days/README.md
- **Recommendation**: Create README.md template and standardize all skill directories

---

## Minor Issues (4)

### 9. **Missing References to docs/SKILLS.md**
- **Severity**: MINOR
- **Impact**: Skills lack links to comprehensive catalog
- **Files Affected**:
  - skills/code-search/README.md
  - skills/geo/README.md
  - skills/last30days/README.md
  - skills/sync-documentation/SKILL.md
  - skills/evolve-skills/SKILL.md
  - skills/session-audit/SKILL.md
  - skills/manage-roadmap/SKILL.md
  - skills/bootstrap-project/SKILL.md
- **Recommendation**: Add "See docs/skills.md for comprehensive catalog" links

### 10. **No README.md in skills/ Directory**
- **Severity**: MINOR
- **Impact**: No overview of skills directory structure
- **Files Affected**:
  - `skills/` (root of skills directory)
- **Recommendation**: Create `skills/README.md` with overview of all skills

### 11. **Skill README.md Content Variation**
- **Severity**: MINOR
- **Impact**: Inconsistent documentation quality across skills
- **Details**:
  - Some have full descriptions
  - Some have minimal content
  - No clear standard
- **Recommendation**: Create README.md template with required sections

### 12. **Negative Guardrails Not Prominent**
- **Severity**: MINOR
- **Impact**: Out of Scope sections vary in visibility
- **Details**:
  - Some skills have prominent "Out of Scope" sections
  - Some have hidden them
  - No standard format
- **Recommendation**: Standardize Out of Scope section format

---

## Reference Analysis

### Files Currently Referencing SKILLS.md
1. **docs/SKILLS.md** — Primary skill catalog (554 lines)
2. **docs/INDEX.md** — References skills (lines 11-76)
3. **INDEX.md** (root) — References SKILLS.md (lines 9, 35-36, 49-50)
4. **AGENTS.md** — References SKILLS.md (lines 80, 90, 103-104)

### Files Missing References to docs/SKILLS.md
1. skills/code-search/README.md
2. skills/geo/README.md
3. skills/last30days/README.md
4. skills/sync-documentation/SKILL.md
5. skills/evolve-skills/SKILL.md
6. skills/session-audit/SKILL.md
7. skills/manage-roadmap/SKILL.md
8. skills/bootstrap-project/SKILL.md

### Skill Directories Without README.md
- archive-milestone
- bootstrap-project
- brave-search
- careful
- evaluate-implementation
- evolve-skills
- generate-spec
- generate-tests
- generate-verification
- hotfix-issue
- humanizer
- implement-specification
- investigate-issue
- manage-development
- manage-roadmap
- milestone
- review-implementation
- safe-update
- session-audit
- sync-documentation

---

## Recommended Actions

### Priority 1 (Fix Immediately)
1. ✅ Rename `docs/SKILLS.md` to `docs/skills.md` (lowercase)
2. ✅ Remove `docs/INDEX.md` and update all references
3. ✅ Create README.md for all 21 skills (standardized template)

### Priority 2 (Fix Soon)
4. ✅ Update INDEX.md (root) to reflect 35 skills
5. ✅ Update AGENTS.md to reference docs/INDEX.md instead of docs/SKILLS.md
6. ✅ Add reference pattern guide to INDEX.md

### Priority 3 (Clean Up)
7. ✅ Create `skills/README.md` for skills directory overview
8. ✅ Standardize Out of Scope sections
9. ✅ Add consistent links to docs/skills.md from all skill files

---

## Documentation Structure After Fixes

```
~/devcode/aef/agent/
├── AGENTS.md (110 lines) — Lightweight navigation hub
├── INDEX.md (61 lines) — Quick reference (authoritative)
├── skills/
│   ├── README.md — Skills directory overview
│   ├── archive-milestone/
│   │   ├── SKILL.md
│   │   └── README.md
│   ├── bootstrap-project/
│   │   ├── SKILL.md
│   │   └── README.md
│   ├── [other 19 skills]
│   │   ├── SKILL.md
│   │   └── README.md
│   └── code-search/
│       ├── SKILL.md
│       └── README.md
└── docs/
    ├── ROADMAP.md
    ├── SPEC.md
    ├── DATA.md
    ├── MILESTONES.md
    ├── PLAYBOOK.md
    ├── FRAMEWORK.md
    ├── EXPERIENCES.md
    ├── INGEST_ENTRIES.md
    ├── INFRASTRUCTURE_FIXES.md
    ├── INDEX.md (remove - duplicate)
    └── skills.md (renamed from SKILLS.md) — Comprehensive catalog
```

---

## Conclusion

The OMP AEF framework has **significant structural inconsistencies** that need to be addressed before the framework can be considered stable and maintainable. The most critical issues are:

1. **Naming conflicts** between `SKILL.md` and `SKILLS.md`
2. **Missing README.md files** for 21 skills
3. **Duplicate INDEX.md files**
4. **Incorrect skill counts** in documentation

Immediate action on Priority 1 items is required to establish a consistent, stable infrastructure.

---

**Next Steps**:
1. Implement Priority 1 fixes
2. Run consistency scan again
3. Verify all references work correctly
4. Test with external tools (if available)
