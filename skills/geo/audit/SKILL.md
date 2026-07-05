---
name: geo-audit
description: Full GEO audit orchestration. Delegate via task tool.
allowed-tools: Read, Grep, Bash, Write
---

# GEO Audit - Agent Delegation Pattern

Use the `task` tool to run a full GEO audit in parallel:

```python
task(
    role="GEO Auditor",
    assignment: """
    Perform a comprehensive GEO audit for https://example.com.
    
    Steps:
    1. Fetch homepage and detect business type (SaaS, Local, E-commerce, Publisher, Agency)
    2. Crawl sitemap or internal links (max 50 pages)
    3. Run parallel subagent analysis via task tool:
       - role="GEO Visibility Analyst": citability, crawlers, llms.txt, brands
       - role="Technical GEO Auditor": technical SEO, SSR, Core Web Vitals
       - role="Content E-E-A-T Evaluator": content quality, author credentials
       - role="Schema Analyst": structured data detection/validation
    4. Aggregate scores and generate GEO-AUDIT-REPORT.md
    
    Output: Write report to current directory.
    """
)
```

## Score Aggregation

```
GEO_Score = (Citability * 0.25) + (Brand * 0.20) + (EEAT * 0.20) + (Technical * 0.15) + (Schema * 0.10) + (Platform * 0.10)
```

## Severity Classification

- **Critical**: All AI crawlers blocked, no SSR, 5xx errors, no structured data
- **High**: Key crawlers blocked (GPTBot, ClaudeBot), no llms.txt, missing Organization schema
- **Medium**: Partial crawler blocking, thin content, no author attribution
- **Low**: Minor schema errors, missing alt text, Open Graph issues