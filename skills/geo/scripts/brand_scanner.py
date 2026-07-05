#!/usr/bin/env python3
"""
Brand Mention Scanner — Checks brand presence across AI-cited platforms.

Brand mentions correlate 3x more strongly with AI visibility than backlinks.
(Ahrefs December 2025 study of 75,000 brands)
"""

import sys
import json
import re
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Required packages not installed. Run: pip install requests beautifulsoup4 lxml")
    sys.exit(1)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def check_wikipedia_presence(brand_name: str) -> dict:
    result = {
        "platform": "Wikipedia",
        "weight": "20%",
        "has_wikipedia_page": False,
        "has_wikidata_entry": False,
        "search_url": f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(brand_name)}&format=json",
    }

    try:
        api_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(brand_name)}&format=json"
        response = requests.get(api_url, headers=DEFAULT_HEADERS, timeout=15)
        if response.status_code == 200:
            data = response.json()
            search_results = data.get("query", {}).get("search", [])
            if search_results:
                top_title = search_results[0].get("title", "").lower()
                if brand_name.lower() in top_title:
                    result["has_wikipedia_page"] = True
                result["search_results_count"] = len(search_results)
    except Exception:
        pass
    return result

def generate_brand_report(brand_name: str, domain: str = None) -> dict:
    report = {
        "brand_name": brand_name,
        "domain": domain,
        "platforms": {
            "wikipedia": check_wikipedia_presence(brand_name),
            "youtube": {"search_url": f"https://www.youtube.com/results?search_query={quote_plus(brand_name)}"},
            "reddit": {"search_url": f"https://www.reddit.com/search/?q={quote_plus(brand_name)}"},
            "linkedin": {"search_url": f"https://www.linkedin.com/search/results/companies/?keywords={quote_plus(brand_name)}"},
        }
    }
    return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python brand_scanner.py <brand_name> [domain]")
        sys.exit(1)
    brand = sys.argv[1]
    domain = sys.argv[2] if len(sys.argv) > 2 else None
    result = generate_brand_report(brand, domain)
    print(json.dumps(result, indent=2, default=str))