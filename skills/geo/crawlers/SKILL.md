---
name: geo-crawlers
description: AI crawler access analysis. Checks robots.txt for AI crawler directives (GPTBot, ClaudeBot, PerplexityBot, etc.).
allowed-tools:
  - Read
  - Bash
  - Write
---

# AI Crawler Analysis

## Crawlers to Check

| Crawler | Service |
|---------|---------|
| GPTBot | OpenAI / ChatGPT |
| OAI-SearchBot | OpenAI search |
| ClaudeBot | Anthropic / Claude |
| PerplexityBot | Perplexity AI |
| Google-Extended | Google Gemini |
| Bytespider | ByteDance / TikTok |
| Applebot-Extended | Apple Intelligence |

## Crawler Access Score

- Start at 100
- Deduct 15 for each critical crawler blocked (GPTBot, ClaudeBot, PerplexityBot)
- Deduct 5 for secondary crawlers
- Floor at 0

## Usage

```python
# Check robots.txt manually or via read tool
read("https://example.com/robots.txt")

# Or use browser tool for dynamic sites
browser(url: "https://example.com/robots.txt")
```

## Recommendations

- Always allow: GPTBot, ClaudeBot, PerplexityBot
- Add sitemap reference to robots.txt
- Consider Content-Signal directive (see https://contentsignals.org/)