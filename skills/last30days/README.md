# last30days - Oh My Pi integrated version

Research what people actually say about any topic in the last 30 days using Brave Search API.

## Setup

Requires Brave Search API key. Set one of:
- `BRAVE_SEARCH_API_KEY` environment variable
- `~/.config/pi/brave-search-token.json` with `apiKey` field

## Usage

```bash
# From skill directory
cd ~/.omp/agent/skills/last30days/
./scripts/last30days.sh "topic"

# Or use web_search tool directly
web_search query="topic"
```

## Options

- `--days N` - Days to search (default: 30, options: 7, 30, 90)
- `--json` - Raw JSON output

## Integration

Uses `~/.omp/agent/skills/brave-search/scripts/brave-search.py` for web search via Brave Search API.