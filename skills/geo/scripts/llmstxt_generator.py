#!/usr/bin/env python3
"""
llms.txt Generator — Creates and validates llms.txt files for AI crawler guidance.
"""

import sys
import json
import re
from urllib.parse import urljoin, urlparse

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

def validate_llmstxt(url: str) -> dict:
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    llms_url = f"{base_url}/llms.txt"
    llms_full_url = f"{base_url}/llms-full.txt"

    result = {
        "url": llms_url,
        "exists": False,
        "format_valid": False,
        "has_title": False,
        "has_description": False,
        "has_sections": False,
        "has_links": False,
        "section_count": 0,
        "link_count": 0,
        "issues": [],
    }

    try:
        response = requests.get(llms_url, headers=DEFAULT_HEADERS, timeout=15)
        if response.status_code == 200:
            result["exists"] = True
            content = response.text
            lines = content.strip().split("\n")

            if lines and lines[0].startswith("# "):
                result["has_title"] = True
            else:
                result["issues"].append("Missing title (should start with '# Site Name')")

            if any(l.startswith("> ") for l in lines):
                result["has_description"] = True

            sections = [l for l in lines if l.startswith("## ")]
            result["section_count"] = len(sections)
            result["has_sections"] = len(sections) > 0

            link_pattern = r"- \[.+\]\(.+\)"
            links = re.findall(link_pattern, content)
            result["link_count"] = len(links)
            result["has_links"] = len(links) > 0

            result["format_valid"] = result["has_title"] and result["has_sections"] and result["has_links"]
    except Exception as e:
        result["issues"].append(f"Error fetching: {str(e)}")

    return result

def generate_llmstxt(url: str, max_pages: int = 30) -> dict:
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    result = {"generated_llmstxt": "", "pages_analyzed": 0}

    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)
        soup = BeautifulSoup(response.text, "lxml")
    except Exception as e:
        result["error"] = f"Failed to fetch: {str(e)}"
        return result

    title = soup.find("title")
    site_name = title.get_text(strip=True).split("|")[0].split("-")[0].strip() if title else parsed.netloc
    meta_desc = soup.find("meta", attrs={"name": "description"})
    site_description = meta_desc.get("content", "") if meta_desc else f"Official website of {site_name}"

    llms_lines = [f"# {site_name}", f"> {site_description}", ""]

    seen = set()
    pages = {"Main Pages": [], "Company": [], "Support": []}

    for link in soup.find_all("a", href=True):
        href = urljoin(base_url, link["href"])
        if href in seen or len(seen) >= max_pages:
            continue
        parsed_href = urlparse(href)
        if parsed_href.netloc != parsed.netloc:
            continue
        seen.add(href)
        link_text = link.get_text(strip=True)[:50]
        pages["Main Pages"].append({"url": href, "title": link_text})

    for section, section_pages in pages.items():
        if section_pages:
            llms_lines.append(f"## {section}")
            for page in section_pages[:10]:
                llms_lines.append(f"- [{page['title']}]({page['url']})")
            llms_lines.append("")

    llms_lines.extend(["## Contact", f"- Website: {base_url}", f"- Email: contact@{parsed.netloc}", ""])

    result["generated_llmstxt"] = "\n".join(llms_lines)
    result["pages_analyzed"] = len(seen)
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python llmstxt_generator.py <url> [mode]")
        print("Modes: validate, generate")
        sys.exit(1)

    target_url = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "validate"

    if mode == "validate":
        data = validate_llmstxt(target_url)
    elif mode == "generate":
        data = generate_llmstxt(target_url)
    else:
        print(f"Unknown mode: {mode}. Use 'validate' or 'generate'.")
        sys.exit(1)

    print(json.dumps(data, indent=2, default=str))