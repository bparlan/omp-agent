# OMP Framework Playbook

This playbook provides guidance on running, testing, and deploying components within the OhMyPi (OMP) Framework, and outlines common operational procedures.

## Running the Framework

The primary mechanism for running OMP workflows involves initiating specific Python scripts that orchestrate agent actions. The main entry point for many operations, such as starting a workflow, is often:

```bash
./start_omp_workflow.sh
```

Individual agent skills and workflows can be executed directly via Python scripts (e.g., `python skills/some_skill.py` or `python implement_workflow.py`), though this should typically be managed by higher-level orchestration tools like the `task` tool.

## Testing and Verification

OMP emphasizes a **Spec-Driven Development** lifecycle, with verification integrated into the process:

1.  **Specification (`generate-spec`)**: The output of this stage is the core input for the next.
2.  **Verification Planning (`generate-verification`)**: Defines how correctness will be evaluated.
3.  **Implementation (`implement-specification`)**: Code is built against the specification.
4.  **Review (`review-implementation`)**: Completed implementations are audited against the specification and verification plan.

Explicit automated test suites (e.g., `pytest`, `unittest`) were not prominently identified in the repository structure. Verification relies heavily on the `review-implementation` stage and the adherence to the defined specification artifacts.

## Deployment

Deployment procedures are not explicitly detailed in the foundational documents. However, based on the framework's structure, deployment would likely involve:

-   Ensuring all necessary Python dependencies are installed.
-   Configuring any external services or APIs required by agents (e.g., LLM providers, search services).
-   Executing the appropriate workflow scripts to set up and run the desired agentic processes.

## Common Operational Procedures

-   **Bootstrap Project**: Use the `bootstrap-project` skill to initialize the framework in a new repository or after major architectural changes. This includes generating core documentation files.
-   **Managing Agent Workflows**: Utilize the `task` tool for delegating work to subagents in parallel. Monitor background tasks using the `job` tool.
-   **Inter-Agent Communication**: Use `irc` for direct messaging between agents, especially for coordination or status updates.
-   **Maintaining Documentation**: Adhere to the principle of artifact persistence. All changes, decisions, and specifications should be documented in Markdown files within the `docs/` directory or related artifact locations.
-   **Debugging Agent Issues**: Leverage the `debug` tool and `eval` for inspecting state and diagnosing problems within agent logic or tool execution.

## Every Session

Run the following workflow at the beginning of each OMP session to establish context and ensure everything is up to date:

1. **Review Session Audit Reports** — Use `glob` to find all Session Audit Reports: `glob path="milestones/ -name "*SA*.md"`. Read the most recent SA to understand recent failures and recommended improvements.

2. **Run evolve-skills** — Execute `evolve-skills` to analyze SAs and automatically update SKILL.md files based on recommended improvements. This ensures your agent knows the latest friction points.

3. **Run skills-auditor** — Execute `python skills-auditor.py audit` to check the health of all evolve-skills dependencies. Review `evolve-skills/health/*.yaml` reports for any critical or high-priority issues.

4. **Check Milestones** — Use `glob` to find active milestones: `glob path="milestones/ -type d -maxdepth 1"`. Identify which milestone you're working on and check its current status.

5. **Read Active Milestone** — Read the milestone document to understand current scope and requirements.

6. **Initialize Workflow** — Begin work on the milestone following the Spec-Driven Development lifecycle:
   - Generate specification (if needed)
   - Create verification plan
   - Implement specification
   - Review implementation

**Why this matters**:
- Ensures all agent skills are updated with the latest knowledge
- Prevents working on outdated SKILL.md files
- Helps identify potential issues before they become blockers
- Maintains consistency across the framework
## Session Audit, Evolve-Skills, and Skills-Auditor Integration

### Session Audit System

**Purpose**: Captures any session (milestone, hotfix, manual edits, external reports) into Session Audit Reports (M{X}SA{Y}.md) that drive documentation updates, skill evolution, and quality monitoring.

**What it captures**:
- Framework changes (framework-critical vs cosmetic)
- Recommended actions for evolve-skills
- Issue classification and recommendations
- Ingestion entries for manage-roadmap

**Outputs per session**:
- `M{X}SA{Y}.md` — Main session audit report
- `SESSION_CHANGES.md` — Detailed change log
- `CHANGELOG_ENTRIES.md` — Standard format changelog (Added/Changed/Fixed)
- `MILESTONE_UPDATES.md` — Progress tracking with task breakdown
- `INGEST_ENTRIES.md` — List of new/modified files ready for ingestion

**Session types detected**:
1. **Milestone Session**: Triggered by milestone mentions
2. **Hotfix Session**: Triggered by hotfix/hotfix-focus/bug fix mentions
3. **Manual Edit Session**: Triggered by file modifications
4. **External Report Session**: Triggered by external document references
5. **Ad-Hoc Session**: No specific trigger detected

**Integration with evolve-skills**:
- session-audit automatically recommends prompt improvements after each session
- evolve-skills analyzes SA documents and updates SKILL.md files
- Changes require per-skill approval via evolve-skills

**Integration with manage-roadmap**:
- session-audit generates INGEST_ENTRIES.md
- manage-roadmap processes ingestion entries after user permission

### Evolve-Skills Skill

**Purpose**: Analyzes recent project artifacts (M{X}SA{Y}.md, Review Reports, Completion Reports) to learn from mistakes, identify workflow inefficiencies, and automatically update/version SKILL.md files.

**Key Responsibilities**:
- Read all SA documents chronologically for each milestone
- Identify failure patterns, inefficiencies, and areas for improvement
- Draft targeted prompt improvements for each skill
- Apply updates to SKILL.md files with incremented version numbers
- Document evolution in EVOLUTION.md
- Process TEMP milestones before formal milestones

**Artifacts Modified**:
- `skills/*/SKILL.md` files (with incremented version numbers)
- `skills/evolve-skills/EVOLUTION.md` ledger

**Workflow**:
1. Read SA documents and classify changes (framework-critical vs cosmetic)
2. Analyze for failure patterns and recommended improvements
3. Draft prompt improvements for each affected skill
4. Show diffs for each change
5. Ask user for per-skill approval
6. Apply approved changes

**Out of Scope**:
- Creating new features
- Running implementation workflows
- Creating new templates

### Skills-Auditor Health Dashboard

**Purpose**: Automated quality monitoring for evolve-skills dependencies, ensuring all skills meet required standards.

**What it audits**:
- Version consistency (version in frontmatter vs. content)
- User-invocable flag presence
- Required tools (read, edit) availability
- Description quality (minimum 10 characters)
- Dependencies list presence
- Out-of-scope declarations

**Priority calculation**:
- **HIGH**: Critical functionality with issues
- **MEDIUM**: Important but not critical
- **LOW**: All checks pass

**Status values**:
- **HEALTHY**: No issues found
- **NEEDS_IMPROVEMENT**: Minor issues, no blocking problems
- **CRITICAL**: Major issues requiring immediate attention

**Health dashboard commands**:

```bash
# Run full audit of all 13 skills
cd skills/evolve-skills
python3 skills-auditor.py audit

# Display color-coded dashboard
python3 skills-auditor.py list

# Audit specific skill
python3 skills-auditor.py audit --skill <skill-name>

# List all skills with health status
python3 skills-auditor.py list
```

**Health report structure** (evolve-skills/health/{skill-name}.yaml):
```yaml
skill: <skill-name>
version: "1.0.0"
last_audited: "2026-07-23"
priority: "LOW"
priority_reason: "0 HIGH issues, 0 MEDIUM issues"
issues:
  - type: <issue-type>
    description: <description>
    severity: <severity>
recommendations:
  - <recommendation-1>
  - <recommendation-2>
status: healthy
```

**Critical skills examples**:
- `bootstrap-project`: Required tools (read, edit)
- `generate-spec`: Required tools (read, edit)
- `generate-verification`: Required tools (read, edit)
- `investigate-issue`: Required tools (read, edit)
- `review-implementation`: Required tools (read, edit)

**Dashboard output**:
- Color-coded status: RED (CRITICAL), YELLOW (NEEDS_IMPROVEMENT), GREEN (HEALTHY)
- Priority and issue counts per skill
- Detailed health reports in YAML format
- Last audited date for each skill

**Integration with session-audit**:
- session-audit automatically triggers skills-auditor audit after generating SA report
- Recommended evolve-skills actions often include health fixes
- Health dashboard used during every session to ensure framework quality

## Every Session
