# diagrammer Skill: Visual Architecture Synchronization

## Role in OMP AEF

`diagrammer` generates Mermaid diagrams as living snapshots of AEF's document flow, skill orchestration, and codebase architecture, grounded in codebase reality via code-search integration.

## Usage in Framework Skills

### When diagrammer is Used

| Trigger | Source | Action |
|---------|--------|--------|
| Structural changes | sync-documentation | Invoked for diagram regeneration |
| Pipeline updates | manage-development | Review workflow diagram alignment |
| New skills added | evolve-skills | Update skill orchestration views |

## Integration Points

### Diagram Generation Workflow

1. Ground in reality via code-search (`--skeletons` and `--search`)
2. Generate in 2-pass rule (nodes, then comments)
3. Save to `docs/diagrams/` directory

## Requirements

### Templates

- Output: `~/devcode/aef/agent/docs/diagrams/`

### Syntax Rules

- Arrows: `==>` (primary), `-.->` (secondary), `-->` (standard)
- One target per arrow
- Node IDs: `S_` (skills), `T_` (templates), `I_` (inputs), `O_` (outputs)
- Include ELK renderer init
- Layers stacked: Skills → Templates → Inputs → Outputs

## Best Practices

### Diagram Types

- **System Snapshot** — Current skill/template/input/output state
- **Skill-Centric View** — All artifacts for one skill
- **File-Flow** — Milestone artifact movement
- **Template Map** — Template usage across skills

## Output

### Diagrams Directory

```
docs/diagrams/
├── system_snapshot.mmd
├── skill_orchestration.mmd
└── template_map.mmd
```

## Behavior Rules

- Never write trailing comments
- Validate syntax before writing
- Include renderer init for all diagrams