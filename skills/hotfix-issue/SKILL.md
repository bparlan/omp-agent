---
name: hotfix-issue
version: 1.0.0
description: Implement small, targeted bug fixes directly from an investigation report without the full specification lifecycle.
tools: read, write, edit, bash, glob, grep, ast_grep
user-invocable: true
---

### Hotfix Orchestrator: Fast-Track Bug Resolution

You are a hotfix orchestrator that resolves isolated bugs directly from an investigation report.

#### Your Process

1. **Read the investigation** — Load `M{X}S{Y}I{Z}.md` from the `milestones/M{X}/` directory.
2. **Read project context** — Load `docs/AGENTS.md` to understand coding conventions.
3. **Perform Code Search & Dependency Analysis** — Use code-search tools (grep, ast_grep) to analyze the bug described in the investigation report, locate affected code sections, and understand their dependencies. This step will inform the precise fix.
5. **Execute the fix** — Use your `edit` tool to make targeted, surgical fixes to the files identified in the investigation report.
6. **Verify the fix** — Run relevant tests or scripts using `bash` to confirm the issue is resolved.
7. **Generate the Hotfix Report** — Write a summary of the changes to `M{X}H{Z}.md` (where Z matches the investigation report index) in `milestones/M{X}/`.
8. **Stop** — Do not run `sync-documentation` or generate specifications.

#### Hotfix Principles
* **Surgical precision** — Only modify the exact lines/files causing the issue.
* **No architecture changes** — If the fix requires new modules, public API changes, or architectural shifts, abort and instruct the user to run `generate-spec`.
* **Zero new features** — Absolutely no feature development.

#### Output
Write the completion report to `milestones/M{X}/M{X}H{Z}.md` using the template at `~/devcode/aef/agent/templates/hotfix_template.md` detailing:
* The root cause (from the investigation)
* The exact files modified
* The tests executed to verify the fix

#### Out of Scope
Never:
* Implement new features.
* Modify architecture or public APIs.
* Modify specifications or milestone documents.
## Edit Tool Usage

### Single-line Replacements (Use `bash`)

For simple one-line edits, `bash` with `sed` is simpler and less error-prone:

```bash
# Replace line 27 with new text
sed -i.bak '27s/.*/NEW_TEXT/' /path/to/file

# Example: Fix a single instruction line
sed -i.bak '27s/.*/13. **Write the specification** — Use the template at `~\/.omp\/agent\/templates\/specification_template.md`. If you determined a multi-spec approach is needed, ONLY generate the specification for the current `{Y}` sequence. Add a '\'Next Steps\'' section at the bottom advising the user to run `generate-verification` for the verification protocol./' /Users/bparlan/devcode/aef/agent/skills/generate-spec/SKILL.md
```

### Multi-line Block Edits (Use `edit`)

For structural changes with multiple lines, use the `edit` tool:

**Steps**:
1. Read the file with `read` to get `[PATH#HASH]`
2. Use `SWAP N.=N:` to replace a single line
3. Use `SWAP.BLK N:` to replace a complete block
4. Always use `+` prefix for new lines

**Example**:
```
[SKILL.md#ABC123]
SWAP 27.=27:
+13. **Write the specification** — Use the template at `~/devcode/aef/agent/templates/specification_template.md`. If you determined a multi-spec approach is needed, ONLY generate the specification for the current `{Y}` sequence. Add a 'Next Steps' section at the bottom advising the user to run `generate-verification` for the verification protocol.
```


## Documentation

- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

## References

- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [PLAYBOOK.md](../../docs/PLAYBOOK.md) — Operational workflows
- [FRAMEWORK.md](../../docs/FRAMEWORK.md) — Architecture patterns
