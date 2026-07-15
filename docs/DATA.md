# OMP Framework Data Schema and Flow

## Data Handled by Agents

Agents within the OMP Framework process various forms of data, primarily in the context of their strategic and execution tasks:

-   **Artifacts**: The core data model of the OMP framework. This includes specifications, milestone documents, code skeletons, review reports, and any other generated Markdown or script files. These are treated as immutable, persistent data.
-   **Agent State**: Transient state information that agents might maintain during their execution. This is managed carefully to ensure determinism and avoid context loss.
-   **External Data**: Agents may interact with external data sources (e.g., APIs, databases, search results) as part of their tasks. The handling of this data is defined by the specific agent's strategy and the tools it utilizes.

## Database Schema

No specific database schemas (e.g., SQL, NoSQL) for core framework operations were identified during the initial bootstrap analysis. The framework prioritizes artifact persistence in human-readable formats (Markdown, JSON, etc.) over rigid database schemas for its primary knowledge representation.

## Data Flow Patterns

Data flows through the OMP system primarily via:

1.  **Sequential Artifact Transformation**: Data (e.g., a milestone definition) is transformed through the 5-stage Spec-Driven Development lifecycle, producing new, more detailed artifacts at each stage.
2.  **Agent-Tool Interaction**: Agents pass data (e.g., queries, instructions, code snippets) to tools for execution, and tools return results or modified data.
3.  **Inter-Agent Communication**: Agents can exchange data via the `irc` tool.

## Artifact Persistence

The framework's emphasis on artifact persistence means that structured data is often serialized into Markdown files. For instance, specifications, roadmaps, and agent prompts are stored as text files, ensuring human readability and traceability. This approach minimizes reliance on complex, opaque data stores for core knowledge management.
