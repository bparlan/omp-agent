---
name: geo-schema
description: Schema markup analysis and generation. Detects, validates, and generates JSON-LD structured data.
allowed-tools:
  - Read
  - Grep
  - Bash
  - Write
---

# Schema Markup Analysis

## Critical Schema Types for GEO

| Type | Best For |
|------|----------|
| Organization | All businesses |
| LocalBusiness | Service businesses |
| Article + Person | Publishers, blogs |
| SoftwareApplication | SaaS |
| Product | E-commerce |
| FAQ | Answer pages |
| HowTo | Tutorials, guides |

## Templates Available

- `~/.omp/agent/skills/geo/schema/organization.json`
- `~/.omp/agent/skills/geo/schema/local-business.json`
- `~/.omp/agent/skills/geo/schema/article-author.json`
- `~/.omp/agent/skills/geo/schema/software-saas.json`
- `~/.omp/agent/skills/geo/schema/product-ecommerce.json`
- `~/.omp/agent/skills/geo/schema/website-searchaction.json`

## Usage

```python
# Check existing schema
grep(pattern: "@context.*schema.org", paths: ["path/to/file"])

# Generate from templates
# Edit the template JSON files with your data
```

## Validation Checklist

- [ ] @context points to https://schema.org
- [ ] @type is valid schema type
- [ ] sameAs includes Wikipedia, Wikidata, social profiles
- [ ] JSON-LD in <script> tag or .json file