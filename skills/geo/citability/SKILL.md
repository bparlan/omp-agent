---
name: geo-citability
description: AI citability scoring and optimization. Analyzes web page content to determine how likely AI systems (ChatGPT, Claude, Perplexity, Gemini) are to cite or quote passages.
allowed-tools:
  - Read
  - Bash
  - Write
---

# AI Citability Scoring

## Scoring Rubric (0-100)

### Answer Block Quality (30%)
- Direct answers in 1-2 sentences
- Definition patterns ("X is...", "X refers to...")
- Answer-first structure

### Self-Containment (25%)
- Optimal word count: 134-167 words
- Low pronoun density
- Contains named entities

### Structural Readability (20%)
- Clean heading hierarchy (H1 > H2 > H3)
- Short paragraphs (2-4 sentences)
- Tables for comparisons, lists for items

### Statistical Density (15%)
- Specific percentages, dollar amounts, timeframes
- Named sources (Gartner, Harvard, etc.)
- Exact numbers over vague quantifiers

### Uniqueness Signals (10%)
- Original data ("our research found...")
- Case studies and examples
- Proprietary insights

## Usage

```python
# Run citability analysis
python3 ~/.omp/agent/skills/geo/scripts/citability_scorer.py https://example.com

# Returns JSON with per-block scores and recommendations
```

## Output

Generates `GEO-CITABILITY-SCORE.md` with:
- Overall page citability score
- Top 5 citable passages
- Bottom 5 passages needing rewrite
- Specific rewrite suggestions