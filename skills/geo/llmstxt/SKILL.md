---
name: geo-llmstxt
description: llms.txt analysis and generation. Validates or creates llms.txt files for AI crawler guidance.
allowed-tools:
  - Read
  - Bash
  - Write
---

# llms.txt Analysis & Generation

The llms.txt standard helps AI crawlers understand site structure.

## Location
- `/llms.txt` - concise version at root
- `/llms-full.txt` - detailed version (optional)

## Format Validation

1. First line: `# Site Name` (H1)
2. Optional: `> Brief description` (blockquote)
3. Sections: `## Section Name`
4. Links: `- [Title](url): Description`

## llms.txt Score

| Score | Criteria |
|-------|----------|
| 0 | Absent |
| 30 | Malformed format |
| 50 | Valid format, minimal content |
| 70+ | Comprehensive with key pages |

## Usage

```python
# Validate existing llms.txt
python3 ~/.omp/agent/skills/geo/scripts/llmstxt_generator.py https://example.com validate

# Generate llms.txt
python3 ~/.omp/agent/skills/geo/scripts/llmstxt_generator.py https://example.com generate
```

## Template Structure

```
# Site Name
> Brief description

## Main Pages
- [Page](url): Description

## Products & Services
- [Product](url)

## Contact
- Website: domain
- Email: contact@domain
```