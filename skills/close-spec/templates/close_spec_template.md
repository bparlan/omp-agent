---
id: CLOSE-M{X}S{Y}-{N}
type: closure
title: "Spec Closure Report for M{X}S{Y}"
milestone_id: M{X}
status: CLOSED  # or CLOSED_WITH_DEFECTS | REFUSED
derived_from:
  - M{X}
  - SPEC-M{X}S{Y}
  - VER-M{X}S{Y}V
  - TSET-M{X}S{Y}T{Z}
  - EVAL-{N_EVAL}
  - REVIEW-M{X}S{Y}
  # If fix cycle occurred:
  # - INV-{N_INV}
  # - HOT-{N_HOT}
  # - EVAL-{N_RE_EVAL}
  # - REVIEW-M{X}S{Y}-V{N_REVIEW}
supersedes: []  # e.g., [CLOSE-M{X}S{Y}-{N_PREVIOUS}] if this replaces an earlier closure
template_version: 1.0.0
---

# Spec Closure Report — M{X}S{Y}

**Closure ID:** CLOSE-M{X}S{Y}-{N}
**Status:** CLOSED | CLOSED_WITH_DEFECTS | REFUSED
**Date:** {YYYY-MM-DD}

---

## 1. Loop-Closure Assurance

### Investigation / Hotfix Detection
```
[evidence: list of investigation and hotfix reports found for this spec, or "none"]
```

### Post-Fix Re-Evaluation Evidence
```
[evidence: evaluation report filename and timestamp after the latest hotfix, or "none required — no fixes occurred"]
```

### Post-Fix Re-Review Evidence
```
[evidence: review report filename and timestamp after the latest evaluation, or "none required — no fixes occurred"]
```

### Assurance Statement
> **This spec has no unverified fixes.** Every fix applied through investigation/hotfix was re-evaluated by `evaluate-implementation` and re-reviewed by `review-implementation` before closure.
>
> OR
>
> **No fixes were applied during this spec's development cycle.** The standard spec → verification → tests → implementation → evaluation → review pipeline completed without deviation.

---

## 2. Mechanical Validation Results

### 2a. Lint Evaluation Gate
```
[command: python3 ~/devcode/aef/agent/bin/lint-evaluation-gate.py --spec M{X}S{Y}]
[exit code: N]
[stdout: captured output or "(empty)"]
[stderr: captured output or "(empty)"]
```

### 2b. Duplicate-ID / Schema Check
```
[command: python3 -c "
import yaml, sys, glob, os
from collections import Counter
paths = sorted(glob.glob('milestones/M{X}/M{X}S{Y}*.md'))
ids = []
errors = []
for p in paths:
    with open(p) as f:
        content = f.read()
    parts = content.split('---', 2)
    if len(parts) < 3:
        errors.append(f'{p}: no valid YAML frontmatter (less than 2 --- delimiters)')
        continue
    try:
        meta = yaml.safe_load(parts[1])
        if meta and 'id' in meta:
            ids.append((p, meta['id']))
        else:
            errors.append(f'{p}: missing id in frontmatter')
    except yaml.YAMLError as e:
        errors.append(f'{p}: YAML parse error: {e}')

counts = Counter(i for _, i in ids)
dupes = {k: v for k, v in counts.items() if v > 1}
if dupes:
    errors.append(f'Duplicate IDs found: {dupes}')
    for path, iid in ids:
        if iid in dupes:
            print(f'  {path} -> id: {iid}')
if errors:
    print('VALIDATION FAILURES:')
    for e in errors:
        print(f'  - {e}')
    sys.exit(1)
else:
    print('All frontmatter valid, no duplicate IDs.')
    for path, iid in ids:
        print(f'  {os.path.basename(path)} -> id: {iid}')
"]
[exit code: N]
[output: captured output or "(empty)"]
```

### 2c. Artifact Naming / Sequentialization Check

Verify that artifact filenames follow the canonical sequential pattern and do not collide:

- `M{X}S{Y}.md` — milestone spec
- `M{X}S{Y}V1.md`, `M{X}S{Y}V2.md` — verification artifacts
- `M{X}S{Y}T1.md`, `M{X}S{Y}T2.md` — test plans
- `M{X}S{Y}C1.md`, `M{X}S{Y}C2.md` — completion/evaluation/review artifacts

Reject bare repeated forms such as `M9S1C.md`, `VER-M9S1V.md`, `M9S1E.md`, or `M9S1R.md` when multiple artifacts of the same type exist, or when the same base name would otherwise collide with another artifact in the same spec sequence.


### 2d. Artifact Completeness Check
```
[command: python3 -c "
import yaml, glob, os
M = 'M{X}'
Y = '{Y}'
spec_file = f'milestones/{M}/{M}S{Y}.md'
ver_file = f'milestones/{M}/{M}S{Y}V.md'
# Find test plan
test_plan = None
for f in glob.glob(f'milestones/{M}/{M}S{Y}T*.md'):
    if f.endswith('T.md') or f.endswith('T[0-9].md'):
        # simple: take the first T file
        test_plan = f
        break
# Find completion
comp_file = None
for f in glob.glob(f'milestones/{M}/{M}S{Y}C*.md'):
    comp_file = f
    break
# Find evaluation
eval_file = None
for f in glob.glob(f'milestones/{M}/{M}S{Y}E*.md'):
    eval_file = f
    break
# Find review
review_file = None
for f in glob.glob(f'milestones/{M}/{M}S{Y}R*.md'):
    review_file = f
    break

missing = []
if not os.path.exists(spec_file):
    missing.append(f'{spec_file} (spec)')
if not os.path.exists(ver_file):
    missing.append(f'{ver_file} (verification)')
if not test_plan:
    missing.append(f'{M{X}S{Y}T*.md} (test plan)')
if not comp_file:
    missing.append(f'{M{X}S{Y}C*.md} (implementation)')
if not eval_file:
    missing.append(f'{M{X}S{Y}E*.md} (evaluation)')
if not review_file:
    missing.append(f'{M{X}S{Y}R*.md} (review)')

if missing:
    print('WARNING: Missing expected artifacts:')
    for m in missing:
        print(f'  - {m}')
else:
    print(f'All expected artifacts present for M{X}S{Y}.')
"]
[exit code: N]
```
M{X}/  (Milestone)
│
├── M{X}S{Y}.md              — SPEC-{Y}  (specification)
│   └── M{X}S{Y}V1.md         — VER-{Y}   (verification)
│       └── M{X}S{Y}T1.md  — TSET-{Y}  (test plan)
│           └── M{X}S{Y}T1E1.md     — EVAL-TEST-{N}  (test evaluation)
│               └── M{X}S{Y}C1.md  — COMP-{N}  (implementation)
│                   └── M{X}S{Y}E1.md  — EVAL-{N}  (evaluation)
│                       └── M{X}S{Y}R1.md  — REVIEW-M{X}S{Y}  (review)
│                           └── (fix cycle, if applicable)
│                               ├── M{X}S{Y}I{Z}.md  — INV-{N}  (investigation)
│                               ├── M{X}H{Z}.md       — HOT-{N}  (hotfix)
│                               ├── M{X}S{Y}E-V{N}.md — EVAL-{N}  (re-evaluation)
│                               └── M{X}S{Y}R-V{N}.md — REVIEW-M{X}S{Y}-V{N}  (re-review)
│
└── M{X}S{Y}CLOSE-{N}.md         — CLOSE-M{X}S{Y}-{N}  (closure)
```

### Full Artifact Table
| File | ID | Type | Status | derived_from | Filepath |
|---|---|---|---|---|---|
| (filename) | (id) | (type) | (status) | [sources] | (relative path) |

---

## 4. Status Assertion

**Spec M{X}S{Y} is [CLOSED | CLOSED_WITH_DEFECTS | REFUSED].**

- All specification requirements have been implemented, evaluated, and reviewed.
- [If CLOSED_WITH_DEFECTS]: The following known issues remain, but do not block closure: [list issues]
- [If REFUSED]: The loop-closure gate was not satisfied. See section 1 for details.

---

## 5. Raw Evidence

Every claim above is backed by the exact command that produced it and its captured output.

### Mandatory Format
```
[claim: <what this proves>]
$ <command>
Exit Code: <N>
stdout:
<captured stdout, or "(empty)">
stderr:
<captured stderr, or "(empty)">
```

### Constraints
- **EVERY** status assertion in section 2 and section 4 MUST have at least one corresponding raw evidence block in this section.
- A report with summary statements but no populated evidence blocks fails the evidence-floor gate.
- This section is additive to the structured findings above — both must be populated.