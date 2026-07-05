#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_URL = "https://api.search.brave.com/res/v1/web/search"
RAW_OUT = Path("/tmp/brave-search.json")
SUMMARY_OUT = Path("/tmp/brave-search-summary.json")


def load_key():
    env_key = os.environ.get("BRAVE_SEARCH_API_KEY", "").strip()
    if env_key:
        return env_key, {"source": "env", "apiKey": "<redacted>"}

    json_path = Path.home() / ".config" / "pi" / "brave-search-token.json"
    raw_path = Path.home() / ".config" / "pi" / "brave-search-token"

    if json_path.exists():
        try:
            data = json.loads(json_path.read_text())
        except Exception as exc:
            raise SystemExit(f"Could not read Brave token JSON: {exc}")
        key = (data.get("apiKey") or data.get("accessToken") or "").strip()
        redacted = dict(data)
        if redacted.get("apiKey"):
            redacted["apiKey"] = "<redacted>"
        if redacted.get("accessToken"):
            redacted["accessToken"] = "<redacted>"
        redacted["source"] = str(json_path)
        return key, redacted

    if raw_path.exists():
        return raw_path.read_text().strip(), {"source": str(raw_path), "apiKey": "<redacted>"}

    return "", {"source": "missing"}


def request_json(api_key, params):
    url = API_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": api_key,
            "User-Agent": "pi-brave-search-skill/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            body = res.read()
            if res.headers.get("Content-Encoding") == "gzip":
                import gzip
                body = gzip.decompress(body)
            return json.loads(body.decode("utf-8")), res.status
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(body)
        except Exception:
            data = {"error": body}
        RAW_OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        if exc.code in (401, 403):
            raise SystemExit(
                f"Brave Search API failed: HTTP {exc.code}. "
                "Likely invalid/revoked key, plan/quota issue, or missing access. "
                f"Response saved: {RAW_OUT}"
            )
        raise SystemExit(f"Brave Search API failed: HTTP {exc.code}. Response saved: {RAW_OUT}")
    except urllib.error.URLError as exc:
        raise SystemExit(f"Brave Search request failed: {exc}")


def pick(obj, *keys):
    for key in keys:
        val = obj.get(key)
        if val not in (None, "", [], {}):
            return val
    return None


def compact_result(item, idx):
    profile = item.get("profile") or {}
    meta_url = item.get("meta_url") or {}
    out = {
        "rank": idx,
        "title": item.get("title"),
        "url": item.get("url"),
        "description": item.get("description"),
    }
    extras = {
        "source": pick(profile, "name"),
        "hostname": pick(meta_url, "hostname", "netloc"),
        "age": item.get("age"),
    }
    extras = {k: v for k, v in extras.items() if v not in (None, "", [], {})}
    if extras:
        out["meta"] = extras

    snippets = item.get("extra_snippets") or []
    if snippets:
        out["extraSnippets"] = snippets[:2]

    deep = item.get("deep_results") or {}
    buttons = deep.get("buttons") or []
    if buttons:
        out["deepLinks"] = [
            {"title": b.get("title"), "url": b.get("url")}
            for b in buttons[:5]
            if b.get("title") or b.get("url")
        ]

    return {k: v for k, v in out.items() if v not in (None, "", [], {})}


def build_summary(data, args):
    web = data.get("web") or {}
    results = web.get("results") or []
    query_info = data.get("query") or {}

    summary = {
        "query": args.query,
        "returnedResults": len(results),
        "results": [compact_result(item, i + 1 + args.offset) for i, item in enumerate(results)],
    }

    corrected = query_info.get("altered") or query_info.get("spellcheck")
    if corrected:
        summary["queryCorrection"] = corrected
    if data.get("news", {}).get("results"):
        summary["newsResults"] = [
            compact_result(item, i + 1) for i, item in enumerate(data["news"]["results"][:5])
        ]

    return summary


def main():
    parser = argparse.ArgumentParser(description="Search web with Brave Search API")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--count", type=int, default=5, help="Number of results, usually 1-20")
    parser.add_argument("--offset", type=int, default=0, help="Result offset for paging")
    parser.add_argument("--country", default="US", help="Country code, e.g. US, GB")
    parser.add_argument("--search-lang", default="en", help="Search language, e.g. en")
    parser.add_argument("--ui-lang", default="en-US", help="UI language, e.g. en-US")
    parser.add_argument("--freshness", default=None, help="pd, pw, pm, py, or date range")
    parser.add_argument(
        "--safe-search",
        default="moderate",
        choices=["off", "moderate", "strict"],
        help="Safe search level",
    )
    parser.add_argument("--json", action="store_true", help="Print compact JSON only")
    parser.add_argument("--raw", action="store_true", help="Print raw JSON instead of summary")
    args = parser.parse_args()

    if args.count < 1 or args.count > 20:
        raise SystemExit("--count must be between 1 and 20")
    if args.offset < 0:
        raise SystemExit("--offset must be >= 0")

    api_key, _token_info = load_key()
    if not api_key:
        raise SystemExit(
            "Brave Search API key missing. Set BRAVE_SEARCH_API_KEY or ~/.config/pi/brave-search-token.json"
        )

    params = {
        "q": args.query,
        "count": args.count,
        "offset": args.offset,
        "country": args.country,
        "search_lang": args.search_lang,
        "ui_lang": args.ui_lang,
        "safesearch": args.safe_search,
    }
    if args.freshness:
        params["freshness"] = args.freshness

    data, status = request_json(api_key, params)
    RAW_OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    summary = build_summary(data, args)
    SUMMARY_OUT.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")

    if args.raw:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif args.json:
        print(json.dumps(summary, ensure_ascii=False))
    else:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        print(f"\nRaw saved: {RAW_OUT}", file=sys.stderr)
        print(f"Summary saved: {SUMMARY_OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()