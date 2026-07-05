---
name: brave-search
tools: web_search
---

# Brave Search

Search web via Brave Search API. Primary web search tool for Oh My Pi.

## Auth

Read API key from:

1. `$BRAVE_SEARCH_API_KEY`
2. `~/.config/pi/brave-search-token.json` (`apiKey` or `accessToken` field)
3. legacy fallback `~/.config/pi/brave-search-token` (raw key)

Never print API key. Do not include it in final answers, code snippets, logs, or client bundles.

## Usage

```bash
cd ~/.omp/agent/skills/brave-search/
./scripts/brave-search.py "query" --count 5
```

The script queries Brave Search API and saves results to `/tmp/brave-search.json` and `/tmp/brave-search-summary.json`.

Options:
```bash
./scripts/brave-search.py "query" --count 10 --freshness pw
./scripts/brave-search.py "query" --json
```

## Workflow

1. Use precise query terms.
2. Run helper.
3. Read `/tmp/brave-search-summary.json` first. Avoid dumping raw JSON into chat.
4. If results weak, refine query once or twice.
5. When answering from web, cite result URLs.

## Notes

- Brave Search API returns snippets, titles, URLs, metadata.
- `count` max depends on API plan; keep 5-10 unless user needs more.
- Use `web_search` tool for direct integration; script for advanced options.