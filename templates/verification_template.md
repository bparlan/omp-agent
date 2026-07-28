---
id: VER-000
type: verification
title: Template Verification Protocol
milestone_id: M0
status: draft
derived_from: []
template_version: 1.1.0
---

## Success Criteria

- ...

---

## Followup Reuse

_(Include for followup specifications)_

### Reusable Items from Prior Verifications

- Regression items: ...
- Automated test patterns: ...
- Edge cases: ...
- Failure scenarios: ...

### New Verification Required

- Items specific to this followup scope: ...

---

## Functional Validation

- ...

---

## Edge Cases

- ...

---

## Failure Scenarios

- ...

---

## Regression Checklist

- ...

---

## Manual Validation

1.
2.

---

## Automated Validation

#### Diff-Scope Verification (Pre-Merge Check)

_This mechanical check must be executed by `evaluate-implementation` before tests are considered passed._

- **Command:** `git diff --name-only`
- **Assertion:** The output of this command MUST strictly match the "Allowlist" defined in the Specification. If any file appears in the diff that is not on the Allowlist, the test automatically FAILS. The agent must revert the out-of-scope file before proceeding.

* Existing tests
* New tests
* Commands

---

## Expected Outcomes

Describe observable success.
