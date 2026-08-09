[~/devcode/aef/templates/hotfix_focus_template.md#75E1]
### Hotfix Focus Report GENERATE_TESTS_FIX
| Property | Value |
| ------ | ------ |
| Document Type | Hotfix Focus |
| Identifier | HF_20260727_GENERATE_TESTS_FIX |
| Date | 2026-07-27 |
| Documentation Impact | MODERATE |
| template_version | 1.0.0 |

--------------------------------------------------------------------------------

#### Literal Checklist Executed
- Apply the same hotfix logic to `skills/generate-tests/SKILL.md`.
- Correct the contradiction between `FRAMEWORK_SKILL_DEFINITION` allowance and the "Out of Scope" list in `skills/generate-tests/SKILL.md`.

--------------------------------------------------------------------------------

#### Mechanical Code Changes
- File modified: `skills/generate-tests/SKILL.md`
- Literal changes:
  - Deleted lines 219-220, which included "Never:" and "## Edit Tool Usage".
  - Deleted lines 222-251 (the entire "Edit Tool Usage" section).
  - Inserted the following text after line 218: "**Exception:** Modifications to `skills/*/SKILL.md` files are permitted when they are explicitly designated as `FRAMEWORK_SKILL_DEFINITION`s for the current milestone."
