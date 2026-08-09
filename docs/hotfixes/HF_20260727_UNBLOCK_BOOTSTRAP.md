[~/devcode/aef/templates/hotfix_focus_template.md#75E1]
### Hotfix Focus Report UNBLOCK_BOOTSTRAP
| Property | Value |
| ------ | ------ |
| Document Type | Hotfix Focus |
| Identifier | HF_20260727_UNBLOCK_BOOTSTRAP |
| Date | 2026-07-27 |
| Documentation Impact | MODERATE |
| template_version | 1.0.0 |

--------------------------------------------------------------------------------

#### Literal Checklist Executed
- Unblock bootstrap by correcting the `skills/*/SKILL.md` modification rule.
- Fix the contradiction between `FRAMEWORK_SKILL_DEFINITION` allowance and the "Out of Scope" list in `skills/bootstrap-project/SKILL.md`.

--------------------------------------------------------------------------------

#### Mechanical Code Changes
- File modified: `skills/bootstrap-project/SKILL.md`
- Literal changes:
  - Deleted lines 188-219, which included "Never:", "## Edit Tool Usage", and the "Edit Tool Usage" section.
  - Inserted the following text after line 187: "**Exception:** Modifications to `skills/*/SKILL.md` files are permitted when they are explicitly designated as `FRAMEWORK_SKILL_DEFINITION`s for the current milestone."
