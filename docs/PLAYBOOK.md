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
