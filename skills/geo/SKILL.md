---
name: geo
description: >
  GEO-first SEO analysis tool. Optimizes websites for AI-powered search engines
  (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews) while maintaining
  traditional SEO foundations. Performs full GEO audits, citability scoring,
  AI crawler analysis, llms.txt generation, brand mention scanning, platform-specific
  optimization, schema markup, technical SEO, content quality (E-E-A-T), and
  client-ready GEO report generation. Use when user says "geo", "seo", "audit",
  "AI search", "AI visibility", "optimize", "citability", "llms.txt", "schema",
  "brand mentions", or any URL for analysis.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# GEO-SEO Analysis Tool — Oh My Pi Skill (July 2026)

> **Philosophy:** GEO-first, SEO-supported. AI search is eating traditional search.
> This tool optimizes for where traffic is going, not where it was.

---

## How to Use

Invoke via `task` tool with appropriate role for parallel analysis.

### Quick Commands

| Command | What It Does |
|---------|-------------|
| `geo audit <url>` | Full GEO + SEO audit with parallel subagents |
| `geo citability <url>` | Score content for AI citation readiness |
| `geo crawlers <url>` | Check AI crawler access (robots.txt) |
| `geo llmstxt <url>` | Analyze or generate llms.txt |
| `geo brands <url>` | Scan brand mentions across AI-cited platforms |
| `geo schema <url>` | Structured data analysis & generation |
| `geo technical <url>` | Technical SEO audit |
| `geo content <url>` | Content quality & E-E-A-T assessment |

---

## Architecture (OMP Adaptation)

```
~/.omp/agent/skills/geo/
├── SKILL.md              # This file - main orchestrator
├── scripts/
│   ├── citability_scorer.py   # AI citation readiness scoring
│   ├── brand_scanner.py       # Brand mention detection
│   └── llmstxt_generator.py   # llms.txt validation & generation
├── schema/
│   ├── organization.json
│   ├── local-business.json
│   ├── article-author.json
│   ├── software-saas.json
│   └── product-ecommerce.json
└── README.md             # Usage examples
```

**Note:** OMP uses `task` tool for parallel subagent execution instead of Claude Code's agent files.

---

## Quick Start Examples

```
# Full GEO audit of a website
task(role: "GEO Auditor", assignment: "perform full GEO audit on https://example.com")

# Check if AI bots can see your site
python3 ~/.omp/agent/skills/geo/scripts/citability_scorer.py https://example.com

# Score a specific page for AI citability
python3 ~/.omp/agent/skills/geo/scripts/citability_scorer.py https://example.com/blog/post

# Generate an llms.txt file for your site
python3 ~/.omp/agent/skills/geo/scripts/llmstxt_generator.py https://example.com generate

# Scan for brand mentions
python3 ~/.omp/agent/skills/geo/scripts/brand_scanner.py "Brand Name" domain.com
```

---

## Scoring Methodology

| Category | Weight |
|----------|--------|
| AI Citability & Visibility | 25% |
| Brand Authority Signals | 20% |
| Content Quality & E-E-A-T | 20% |
| Technical Foundations | 15% |
| Structured Data | 10% |
| Platform Optimization | 10% |

---

## Tool Mapping (OMP vs Claude Code)

| Claude Code | OMP |
|-------------|-----|
| `WebFetch` | `read` (URLs) or `browser` |
| `Grep` | `grep` tool |
| `Glob` | `glob` tool |
| Agent files | `task` tool with `role` |
| `~/.claude/skills/` | `~/.omp/agent/skills/` |

---

## Data Storage

Audit results are written to the current working directory as markdown files:
- `GEO-AUDIT-REPORT.md`
- `GEO-CITABILITY-SCORE.md`
- `llms.txt` (generated)

Historical tracking via `~/.omp/agent/state/state.json` when enabled.