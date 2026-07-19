---
name: ruff-superficial-fix-loop
description: "Prevent Ruff from repeatedly applying superficial line-length fixes without overall issue reduction."
condition: ["tool:bash('ruff --fix')", "ruff.*fix.*(line-length|shorten).*and.*(static|no change|loop)"]
scope: "tool:bash(*ruff*)"
---

When running Ruff fixes, prioritize changes that reduce the overall issue count. If fixes primarily target line length or code shortening and do not lead to a significant decrease in the total number of issues, pause that specific fix strategy and investigate other linting rules or potential underlying issues. Avoid repetitive application of superficial fixes that do not contribute to comprehensive code quality improvements.