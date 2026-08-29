# Unified Diagrammer Upgrade (v2.0.0): Spaghetti-Free, API-Free, Local Excalidraw & Mermaid

This specification outlines the lean, zero-dependency upgrade of the **`diagrammer`** skill. It removes all external API calls, heavyweight headless browser engines, and active MCP server requirements, replacing them with a highly stable, 100% offline **`Code -> Diagram -> Document`** pipeline.

By utilizing standard **Mermaid Markdown blocks** and flat **Excalidraw JSON schemas**, this infrastructure provides a robust, token-efficient visual modeling layer that runs entirely on standard local files and native python utilities.

---

## 1. The Core Philosophy: Spaghetti-Free Visual Modeling

Standard agentic workflows often suffer from context thrashing when reading massive codebases, trying to summarize complex logic into bloated prose. By enforcing the **`Code -> Diagram -> Document`** paradigm, we ground the agent's understanding in rigid structural contracts:

*   **Code (Introspect Skeletons):** The agent runs tree-sitter AST queries or import sweeps using the global code search wrapper:
    ```bash
    bin/search_code --skeletons
    ```
    This extracts class/function signatures, symbols, and import dependencies into a minimal, low-token skeleton markdown file, avoiding heavy file parsing.
*   **Diagram (Intermediate Text Model):** The agent converts this structural information into a clean, text-based visual model—either a standard Mermaid flowchart or a flat `.excalidraw` JSON layout file on disk.

### Why Offline & API-Free Wins
1.  **Zero Dependency Breakage:** Removing external CLI wrappers (like Draw.io desktop) and design platform APIs (like Figma) prevents pipeline halts due to local library updates, missing Java/Node runtimes, or network dropouts.
2.  **Uncompromised Token Economy:** Traditional MCP-based drawing tools consume massive amounts of token overhead by forcing the model to continuously negotiate coordinates and styles over an active connection. Storing static JSON shapes locally and applying offsets via simple, offline python scripts keeps the LLM's context window light and clean.
3.  **Perfect Git Traceability:** Because both Mermaid blocks and `.excalidraw` files are represented as pure text, modifications produce clean git diffs, eliminating binary or phantom conflicts during merges.

---

## 2. Upgraded `diagrammer` Skill Prompt (`skills/diagrammer/SKILL.md`)

This is the canonical, production-grade skill configuration designed to replace **`skills/diagrammer/SKILL.md`**. It enforces pure-text generation, local Excalidraw JSON structures, and standard python-based coordinate offsets.

```markdown
---
name: diagrammer
version: 3.0.0-stable
description: Local Diagram Generator. Translates natural language, structural code skeletons, and database schemas into clean, version-controlled visual models (Mermaid blocks and local Excalidraw JSON files) without external APIs or MCP servers. Enforces the Code -> Diagram -> Document pipeline.
tools: [read, write, edit, bash, glob, grep]
user-invocable: true
---

### Local Diagrammer: Zero-Dependency Visual Architecture Builder

You are a visual systems architect. Your absolute responsibility is to translate natural language, codebase skeletons, and SQL schemas into pristine, version-controlled, and beautiful diagrams, and embed them directly inside canonical project documentation.

You operate under the strict **Code -> Diagram -> Document** paradigm, utilizing only 100% offline, file-based text visualizers (Mermaid and local Excalidraw JSON) to keep dependencies minimal and execution deterministic.

---

#### 1. Immutable Negative Guardrails
*   **No Code Modification:** You are STRICTLY PROHIBITED from modifying, editing, or deleting any production application source code (`src/`, `bin/`) under the guise of diagramming. Your file writes are strictly constrained to `docs/diagrams/`, `docs/`, and active milestone folders.
*   **No Emojis or HTML Tags:** You MUST NOT write emojis or HTML tags (`<br>`, `<div>`, etc.) inside Mermaid or Excalidraw labels. These cause parsing failures and low-quality rendering.
*   **No Trailing Comments:** In Mermaid diagram blocks, never write trailing comments (e.g., `NODE[...] %% note`). Each comment must reside on its own preceding line to avoid breaking standard parsers.
*   **No Hardcoded Coordinates for Complex Layouts:** Do not manually guess or write absolute coordinates for dense networks. For complex dependency trees, default to auto-laid-out Mermaid blocks. Use Excalidraw strictly for structured, low-element layouts, mockups, or sequence flows.

---

#### 2. Your Process: The 3-Step Lifecycle

##### Step 1: Structural Context Gathering (Grounding)
Before drawing any diagram, you must inspect the actual codebase or files using local search tools to ensure visual descriptions match implementation reality:
*   **Code Skeletons:** Run the global search utility to fetch class/function signatures and import relationships:
    ```bash
    bin/search_code --skeletons
    ```
    Read the output file in `docs/skeletons/` instead of scanning heavy source directories.
*   **Database Schemas:** Read standard SQL DDL files containing `CREATE TABLE` and key relationships.

##### Step 2: Tool Selection & Layout Planning
Identify the user's intent and select the appropriate representation format:

*   **Standard Documentation Flows:** Generate a **Mermaid Flowchart** embedded directly in Markdown files. Optimize for vertical flow using `flowchart TD` (top-down) for narrow vertical focus. Always wrap labels in quotes.
*   **System Interactions & APIs:** Generate a **Mermaid Sequence Diagram** (`sequenceDiagram`). Declare participants horizontally before writing messages. Use `actor` for humans, `participant` for systems.
*   **Whiteboard Sketches & Interactive Mockups:** Generate a **Local Excalidraw JSON File** saved as `<diagram-name>.excalidraw`. Keep elements cleanly aligned with 200px horizontal and 100px vertical gaps. Ensure all text elements use `fontFamily: 5` (Excalifont).
*   **Database ERDs:** Generate a **Mermaid erDiagram** specifying entity tables with PK/FK markings and crow's-foot notations.

##### Step 3: Generation & Structural Verification
1.  **Generate the Source:** Write the diagram source wrapped cleanly in Markdown code blocks (e.g. ` ```mermaid ` or ` ```json ` representing the Excalidraw schema).
2.  **Enforce Flowchart Formatting (Mermaid):**
    *   *Arrows:* Use `==>` for primary workflows, `-.->` for secondary connections/reads, and `-->` for standard flows. Never mix arrow styles (like `--==>`).
    *   *Targets:* Keep one target per arrow statement (e.g., `A ==> B` and `A ==> C`, never `A ==> B, C`).
    *   *Node IDs:* Use standard node IDs (e.g. `userService[User Service]`). CamelCase with no spaces.
    *   *ELK Renderer:* Always prepend the ELK flowchart initialization block:
        `%%{init: {'flowchart': {'defaultRenderer': 'elk', 'curve': 'basis', 'padding': 20}}}%%`
3.  **Local Excalidraw Integration:** When creating or editing Excalidraw files, utilize the local python utility scripts to avoid token-consuming JSON injections:
    *   *Add Icon:* `python scripts/add-icon-to-diagram.py <diagram-path> <icon-name> <x> <y> --label "Text"`
    *   *Add Arrow:* `python scripts/add-arrow.py <diagram-path> <from-x> <from-y> <to-x> <to-y> --label "Text"`
4.  **Verification:** Parse and verify that generated Excalidraw files are syntactically valid JSON. Confirm that all Mermaid syntax parses cleanly.

---

#### 3. Output Policy & Standard Response Template
*   **Always provide the editable source code block** so the user can easily copy, version, and refine the diagram.
*   **Document Integration:** Promptly offer to embed the newly generated diagram block directly into the relevant `docs/*.md` file or milestone report to maintain a single source of truth.

Use this Markdown layout for your responses:
```markdown
Below is the editable and version-controlled [Format] source:

\```[format]
[source_code]
\```

##### Assumptions & Boundaries:
*   [List of structural assumptions made, or "None"]

##### Local Artifact Path:
*   `docs/diagrams/[name].[ext]` (Saved and ready for git tracking)
```
```

---

## 3. High-Usability Offline Recipes

To leverage the `diagrammer` skill efficiently across your development lifecycle, integrate these **three automated recipes**:

### Recipe A: Autonomous Documentation Sync (Stage 11 Integration)
When your pipeline enters **Stage 11 (`sync-documentation`)**, configure the orchestrator to automatically run the diagram generator to refresh your codebase visual guide:
```bash
# Generate the latest dependency skeletons using tree-sitter
bin/search_code --skeletons

# Rebuild the visual index and save the updated Mermaid block to docs/diagrams/system_snapshot.mmd
# The orchestrator then syncs this block into README.md or docs/README.md
```

### Recipe B: Zero-Token Icon Integration
When building cloud architecture diagrams, injecting raw Excalidraw SVG icon paths directly through the LLM context window burns thousands of tokens. Instead, the agent coordinates with the local helper scripts to pull icon components from your offline libraries directory:
```bash
# Initialize a clean canvas
echo '{"type":"excalidraw","version":2,"elements":[],"appState":{"gridSize":20},"files":{}}' > docs/diagrams/cloud_arch.excalidraw

# Add pre-made components from local libraries without sending JSON through the context window
python3 scripts/add-icon-to-diagram.py docs/diagrams/cloud_arch.excalidraw "Lambda" 100 100 --label "Order Handler"
python3 scripts/add-icon-to-diagram.py docs/diagrams/cloud_arch.excalidraw "RDS" 400 100 --label "Order DB"

# Connect the nodes cleanly
python3 scripts/add-arrow.py docs/diagrams/cloud_arch.excalidraw 150 100 400 100 --label "Writes" --style dashed
```

### Recipe C: Visualizing SQL Schemas Instantly
Transform database SQL files directly into visual Entity-Relationship diagrams to verify table structures:
```bash
# Read SQL schema and extract tables/keys via python parser
# Translate matches directly into a Mermaid erDiagram code block
```

---

## 4. Operational Prompts to Apply This Upgrade

To have your framework autonomously implement this structural upgrade across the codebase, execute these **two targeted prompts** in your developer chat:

### Prompt 1: Update the Strategic Orchestrator (`manage-development`)
```text
/edit skills/manage-development/SKILL.md

Please update the Stage 11 (sync-documentation) guidelines to incorporate automated diagram regeneration:
"Stage 11 (sync-documentation) - Automated Diagram Refresh (MANDATORY): When documenting completed specifications, the orchestrator MUST automatically invoke the 'diagrammer' skill to regenerate 'docs/diagrams/system_snapshot.mmd' from the updated code skeletons. Ensure the long-lived documentation is synced with live, updated architecture diagrams."
```

### Prompt 2: Align the Post-Review Sync (`sync-documentation`)
```text
/edit skills/sync-documentation/SKILL.md

Please update the process checklist to automatically trigger diagram updates after file ingestion:
"Post-Ingestion Diagram Check: Immediately after successfully ingesting and syncing project files, execute the 'diagrammer' command to rebuild the visual index. Diffs of modified diagrams (docs/diagrams/*.mmd) must be presented to the user alongside standard markdown diffs for approval."
```
