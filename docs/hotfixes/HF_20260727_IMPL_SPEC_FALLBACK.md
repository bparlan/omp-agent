[~/devcode/aef/templates/hotfix_focus_template.md#75E1]
### Hotfix Focus Report IMPL_SPEC_FALLBACK
| Property | Value |
| ------ | ------ |
| Document Type | Hotfix Focus |
| Identifier | HF_20260727_IMPL_SPEC_FALLBACK |
| Date | 2026-07-27 |
| Documentation Impact | MINOR |
| template_version | 1.0.0 |

--------------------------------------------------------------------------------

#### Literal Checklist Executed
*(Update Step 4 in skills/implement-specification/SKILL.md to provide a built-in fallback: If lsp is unavailable, you MUST fallback to using code-search, ast_grep, or grep to map the codebase.)*

--------------------------------------------------------------------------------

#### Mechanical Code Changes
*(File: `skills/implement-specification/SKILL.md`
Change: Updated line 29 to include fallback instructions for code inspection.
Original: `4. Inspect existing code — Use `lsp` to find affected modules and existing implementations.`
Modified: `4. Inspect existing code — Use `lsp` to find affected modules and existing implementations. If lsp is unavailable, you MUST fallback to using code-search, ast_grep, or grep to map the codebase.`)*
