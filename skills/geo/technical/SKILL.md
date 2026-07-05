---
name: geo-technical
description: Technical SEO audit for GEO. Analyzes crawlability, mobile-friendliness, Core Web Vitals, security headers, and SSR status.
allowed-tools:
  - Read
  - Bash
  - Write
---

# Technical GEO Audit

## Checks

- robots.txt compliance
- Mobile responsiveness
- Core Web Vitals (can be checked via PageSpeed Insights API)
- Security headers (CSP, HSTS, X-Frame-Options)
- SSR vs client-side rendering
- Sitemap presence and validity

## Usage

```bash
# Check robots.txt
read("https://example.com/robots.txt")

# Check meta tags and headers
# Use browser tool for dynamic analysis
```