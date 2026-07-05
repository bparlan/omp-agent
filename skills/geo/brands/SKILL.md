---
name: geo-brands
description: Brand mention scanning across AI-cited platforms. Checks Wikipedia, YouTube, Reddit, LinkedIn, and review platforms.
allowed-tools:
  - Read
  - Bash
  - Write
---

# Brand Mention Scanner

Brand mentions correlate 3x more strongly with AI visibility than backlinks.

## Platform Priority

| Platform | Correlation | Check |
|----------|-------------|-------|
| Wikipedia | 0.737 (highest) | API search |
| YouTube | High | Channel presence |
| Reddit | High | Discussion presence |
| LinkedIn | Moderate | Company page |
| Review sites | Moderate | G2, Trustpilot, Capterra |

## Usage

```python
# Scan brand presence
python3 ~/.omp/agent/skills/geo/scripts/brand_scanner.py "Brand Name" domain.com

# Or use web_search for platform checks
web_search(query: "site:wikipedia.org Brand Name")
web_search(query: "site:youtube.com Brand Name")
```

## Recommendations

1. Wikipedia presence - strongest signal
2. YouTube educational content
3. Reddit authentic participation
4. LinkedIn company page + posts
5. Encourage customer reviews on G2/Trustpilot