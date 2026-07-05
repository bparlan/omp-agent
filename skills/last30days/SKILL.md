---
name: last30days
description: "Research recent conversation about any topic using Brave Search API."
argument-hint: 'last30days <topic>'
tools: bash, read, web_search
user-invocable: true
---

# /last30days - Recent Conversation Research

Research what people say about topics in the last 30 days. Uses Brave Search API via web_search tool.

## Auth

Requires Brave Search API key:

1. `$BRAVE_SEARCH_API_KEY`
2. `~/.config/pi/brave-search-token.json`
3. `~/.config/pi/brave-search-token`

## Usage

```bash
# From the skill directory
cd ~/.omp/agent/skills/last30days/
./scripts/last30days.sh "topic"

# Or invoke via web_search tool directly
web_search query="topic"
```

## Output

Synthesizes findings with citation URLs. Uses `--freshness pm` for past month bias.