# GEO-SEO Skill for Oh My Pi

GEO-first SEO analysis tool integrated into OMP infrastructure.

## Quick Start

### Full Audit
```bash
# Run via task tool with role
task(role: "GEO Auditor", assignment: "perform full GEO audit on https://example.com")
```

### Individual Commands

```bash
# Citability scoring
python3 ~/.omp/agent/skills/geo/scripts/citability_scorer.py https://example.com

# llms.txt validation/generation
python3 ~/.omp/agent/skills/geo/scripts/llmstxt_generator.py https://example.com validate
python3 ~/.omp/agent/skills/geo/scripts/llmstxt_generator.py https://example.com generate

# Brand mention scanning
python3 ~/.omp/agent/skills/geo/scripts/brand_scanner.py "Brand Name" domain.com
```

## Directory Structure

```
~/.omp/agent/skills/geo/
├── SKILL.md              # Main entry point
├── README.md             # This file
├── scripts/
│   ├── citability_scorer.py   # AI citation scoring
│   ├── brand_scanner.py       # Brand presence checking
│   └── llmstxt_generator.py   # llms.txt validation/generation
└── schema/
    ├── organization.json      # JSON-LD template
    ├── local-business.json    # LocalBusiness schema
    ├── article-author.json    # Article + Person schema
    ├── software-saas.json     # SaaS schema
    ├── product-ecommerce.json # Product schema
    └── website-searchaction.json # Website + SearchAction
```

## Tool Mapping

| Claude Code | OMP |
|-------------|-----|
| `WebFetch` | `browser` tool or `read` for URLs |
| `Grep` | `grep` tool |
| `Glob` | `glob` tool |
| Agents | `task` tool with `role` |

## Requirements

Python packages (install if needed):
```bash
pip install requests beautifulsoup4 lxml
```

## Scoring Methodology

| Category | Weight |
|----------|--------|
| AI Citability & Visibility | 25% |
| Brand Authority Signals | 20% |
| Content Quality & E-E-A-T | 20% |
| Technical Foundations | 15% |
| Structured Data | 10% |
| Platform Optimization | 10% |