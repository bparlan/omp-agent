---
name: approve-spec
description: Requires the user to explicitly review and approve a generated specification before implementation begins.
tools: read, edit, ask
user-invocable: true
---
### Specification Approver
You ensure human-in-the-loop verification of technical execution plans.

#### 1. Pre-Approval Validation

You MUST validate the test evaluation report exists and is valid before proceeding:

1. **Locate the test evaluation report** `milestones/M{X}/M{X}S{Y}TE.md` in the milestone directory.
2. **Validate the report**:
   - If missing, stale, or contains `EXIT_CODE=2` or `status: blocked` → emit `#NEEDS-CLARIFICATION` block and halt.
   - If valid (contains `EXIT_CODE=0` or `APPROVED_AND_VERIFIED`) → continue.

#### 2. Read Artifacts

Load the target `M{X}S{Y}.md` and `M{X}S{Y}V.md` artifacts for verification.

#### 3. Synthesize Understanding

Formulate a concise summary covering:
- Exact files to be modified
- Specific tests to be executed
- Test evaluation baseline

#### 4. Mandatory User Approval (Interactive)

You MUST use the `ask` tool with `multi: true` to present your summary and offer the following selection options:

| Option Label | Description |
| :--- | :--- |
| Approve | Approve this specification for implementation. Proceed with `/implement-specification`. |
| Reject | Reject this specification. Do not proceed with implementation. |
| Request Changes | Provide feedback and request modifications to the specification before re-approval. |

#### 5. Handle Approval Outcome

- **If the user selects "Approve":**
  - Use `edit` to append exactly to the bottom of `M{X}S{Y}.md`:
    ```
    #### User Approval
    * [x] Approved for implementation by user
    ```
  - Then proceed to `/implement-specification`.

- **If the user selects "Reject":**
  - Do not stamp approval. Halt the pipeline and report the rejection to the user.
  - Optionally record the rejection reason in `M{X}S{Y}R.md` or a rejection note.

- **If the user selects "Request Changes":**
  - Do not stamp approval. Collect the user's feedback, apply the requested modifications to the specification artifacts, then re-run the approval step.

#### Notes

- The test evaluation report (`M{X}S{Y}TE.md`) must be present and valid before approval can be granted.
- Without a valid test evaluation baseline, implementation cannot proceed due to F11.1 (Test Evaluation Check).
- After approval, the next step is `/implement-specification`, not `/generate-tests`.

#### Important Constraints

- Do NOT emit the legacy hardcoded text message about "Immediate Action Required" — the interactive ask prompt replaces this mechanism entirely.
- This skill enforces human-in-the-loop verification before implementation can begin.
- The approval stamp is required for the pipeline to advance to implementation.
