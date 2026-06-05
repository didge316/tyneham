# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**tynehamvillage.org** — a static HTML website about Tyneham, Dorset's WWII ghost village. Hosted on Cloudflare Pages. No build step, no framework, no CMS. The live site files are in the `website/` subdirectory.

## Running Locally

```bash
python3 -m http.server 8766 --directory website
# Then open http://localhost:8766
```

## Repository Layout

```
website/          # Live site — deploy this directory to Cloudflare Pages
  assets/         # All images (jpg + webp pairs for every image)
  css/            # Custom styles (Bootstrap loaded from CDN)
  js/scripts.js   # Sidebar active-page highlighting + opening times calculator
  docs/           # SEO audit reports and action plan (not served)
  scripts/        # Utility scripts (bulk_seo_fixes.py)
  _headers        # Cloudflare Pages: security headers + cache rules
  _redirects      # Cloudflare Pages: www→non-www, WordPress slug redirects
  robots.txt      # Allows AI crawlers (GPTBot, ClaudeBot, etc.), blocks CCBot/Bytespider
  llms.txt        # AI discovery file
  sitemap.xml     # Must be kept in sync when pages are added/removed
content/          # Content research and drafts (not served)
outreach/         # Link-building outreach notes (not served)
tyneham_info_from_web/  # Scraped source material for content research
```

## Page Structure

Every HTML page follows the same structure:
- Bootstrap 5 (CDN) + custom CSS
- Shared navbar with dropdown menus (History, Nearby Attractions)
- Left sidebar with `data-page` attributes — `js/scripts.js` highlights the current page
- Main content column
- Footer

When adding a new page, copy an existing page and update: `<title>`, all meta tags (description, OG, Twitter, canonical), the sidebar `data-page` highlight target, and add the page to `sitemap.xml`.

## Bulk Edits

`website/scripts/bulk_seo_fixes.py` is the pattern for sitewide HTML edits. When a change must be applied across all 26+ pages (e.g. adding a nav link, fixing a typo), write a script in this style rather than editing files one by one.

```bash
python3 website/scripts/bulk_seo_fixes.py
```

## Cloudflare Deployment

Deploys automatically on push to the connected Git branch. The `website/` directory is the publish directory. No build command.

- `_headers` controls cache (assets/css/js are immutable, 1-year TTL)
- `_redirects` handles the www redirect and all old WordPress URLs

## ⚠️ NEVER ADD A Content-Security-Policy HEADER

**DO NOT add a `Content-Security-Policy` header to `_headers` under any circumstances.**

AdSense Auto Ads is critical revenue for this site. A CSP `connect-src` restriction blocks the dynamic Google subdomains AdSense needs to fetch ad creatives. Google's ad stack uses too many unpredictable subdomains to whitelist reliably — every attempt has broken AdSense (this has happened twice: commits c65e261 and 86ed74f). The site already has strong security via HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy. A CSP is not worth the trade-off.

## Contact Form

`contact.html` posts to Web3Forms (`https://api.web3forms.com/submit`). The access key is embedded in the form. On success, redirects to `thank-you.html` (noindex). Spam protection via a hidden `botcheck` honeypot field.

## SEO Notes

- `docs/ACTION-PLAN.md` — prioritised SEO action list from the May 2026 audit
- `docs/AUDIT-2026-05-21.md` — full audit detail
- Images: every image should have a `.webp` version alongside the original; use `<picture>` with webp source + jpg fallback
- Schema: most pages still lack JSON-LD (see action plan — homepage and opening_times.html are the priority)
- The `opening_times.html` page is the highest-intent page on the site

## Content To-Do

See `website/TODO.md` for planned new pages (walking routes, wildlife, Gad Cliff, visiting guide, Corfe Castle) and additions to existing pages (red telephone box, Jurassic Coast UNESCO context).
