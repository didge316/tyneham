# Tyneham Village — Full SEO Audit Report

**Site:** https://tynehamvillage.org  
**Audit date:** 21 May 2026  
**Pages audited:** 26 HTML files  
**Business type:** Heritage/tourism publisher — history and visitor information site  

---

## SEO Health Score: 45 / 100

| Category | Weight | Score | Weighted |
|----------|--------|-------|---------|
| Technical SEO | 22% | 55/100 | 12.1 |
| Content Quality | 23% | 40/100 | 9.2 |
| On-Page SEO | 20% | 55/100 | 11.0 |
| Schema / Structured Data | 10% | 10/100 | 1.0 |
| Performance (CWV) | 10% | 50/100 | 5.0 |
| AI Search Readiness | 10% | 45/100 | 4.5 |
| Images | 5% | 35/100 | 1.75 |
| **Total** | 100% | | **45 / 100** |

The biggest drag on score: Schema (25 of 26 pages have zero structured data) and Content/E-E-A-T (no named author anywhere on the site).

---

## Executive Summary

### Top 5 Critical Issues

1. **No schema on 25 of 26 pages** — only the homepage has any JSON-LD, and it's incomplete. Google cannot generate rich results for a single attraction, landmark, or article on this site.
2. **No named author / About page** — every page credits "Tyneham Admin". This is the single biggest E-E-A-T gap and directly limits AI citation eligibility.
3. **No llms.txt** — no machine-readable manifest for AI crawlers. The site has strong citability potential (verbatim historical quotes, specific dates, named sources) but no AI discovery file.
4. **`smuggling.html` missing from sitemap.xml** — a fully developed, indexable content page is invisible to search engines via sitemap.
5. **No security headers** — `_headers` file only sets Content-Type for sitemap.xml. No X-Content-Type-Options, X-Frame-Options, Referrer-Policy, or CSP sitewide.

### Top 5 Quick Wins

1. Add `smuggling.html` to sitemap.xml (5 minutes)
2. Fix `kimmeridge-bay.html` title tag ("Kimmeridge Bay" at 14 chars → full descriptive title)
3. Fix typo "Particualar" in `the_bond_family.html` meta description
4. Add H2s to `history_of_tyneham.html` and `the_bond_family.html` (both currently skip H1→H3)
5. Fix `alt="Advertisement"` on DVD sidebar image (appears sitewide across all pages)

---

## Technical SEO

### Redirects
- **GOOD:** www → non-www: `https://www.tynehamvillage.org/* → https://tynehamvillage.org/:splat 301` ✓
- **GOOD:** Sitemap redirects: `/sitemap` and `/sitemap/` → `/sitemap.xml 301` ✓
- **GOOD:** 19 old WordPress URL redirects in place ✓
- **GOOD:** No redirect chains detected ✓

### Canonical Tags
- All 26 pages have canonical tags pointing to the correct self-referencing URLs.
- No canonical conflicts detected.

### URL Structure — Inconsistency Issue (MEDIUM)
Six pages use underscore filenames (SEO-suboptimal — Google treats underscores as word-joiners, not separators):
- `history_of_tyneham.html`
- `map_of_tyneham.html`
- `opening_times.html`
- `the_post_office.html`
- `the_bond_family.html`
- `tyneham_village_location.html`

The `_redirects` file does **not** redirect these to hyphenated equivalents. The remaining 20 pages use hyphens correctly. This is a long-term migration risk — not urgent while canonicals are correct.

### Homepage Link Convention (MEDIUM)
All nav bars link to the homepage using relative `href="index.html"`. Cloudflare Pages serves `/index.html` and `/` as the same file, but there is no 301 from `/index.html → /`. A user or crawler following a nav link will request `/index.html`, not `/`. Adding a redirect (`/index.html → / 301`) to `_redirects` would clean this up.

### Security Headers (HIGH)
The `_headers` file contains only:
```
/sitemap.xml
  Content-Type: application/xml; charset=utf-8
```
No security headers are set sitewide. Missing:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy`

Cloudflare Pages provides HTTPS automatically. HSTS is not required in `_headers` if Always Use HTTPS is enabled in the Cloudflare dashboard.

### Robots.txt
```
User-agent: *
Allow: /
Sitemap: https://tynehamvillage.org/sitemap.xml
```
No AI crawlers blocked. All bots (GPTBot, ClaudeBot, Google-Extended, Amazonbot, CCBot, Bytespider, PerplexityBot) have full access. This is the correct configuration. ✓

### Sitemap
- 24 URLs in sitemap — correct coverage **except** `smuggling.html` is missing
- All URLs use correct canonical domain `https://tynehamvillage.org/`
- Lastmod dates are consistent and realistic (May 2026)
- Priority values are appropriately tiered (homepage 1.0, core content 0.8–0.9, nearby attractions 0.6)
- `_headers` file sets correct `Content-Type: application/xml` ✓

---

## Content Quality & E-E-A-T

### Author / Expert Attribution — CRITICAL
- Every page: `<meta name="author" content="Tyneham Admin">` — anonymous, carries zero E-E-A-T weight
- No About page anywhere on the site
- No named editor, historian, or writer credited on any content page
- The donate modal reveals PayPal email `mattg4@gmail.com` and text "This website is run by volunteers" — the only human signal, buried in a modal, not visible in content
- **The site's actual content quality is high** — it is the lack of attribution that is the problem

### Thin Content
Pages confirmed under minimum word threshold:

| Page | Estimated Words | Status |
|------|----------------|--------|
| `map_of_tyneham.html` | ~180 | CRITICAL FAIL |
| `camp-at-tyneham.html` | ~380 | CRITICAL FAIL |
| `tyneham-school.html` | ~520 | FAIL |
| `the-church-door-note.html` | ~680 | FAIL |
| `tyneham-church.html` | ~650 | FAIL |
| `the_post_office.html` | ~620 | FAIL |

The map page is essentially an image with 3 paragraphs. The camping page is 2 paragraphs + a 5-item campsite list with no practical details.

### Content Quality — Strengths
- `after-the-evacuation.html` — excellent: named families, specific dates, first-hand sources
- `the-campaign-to-return.html` — excellent: specific dates, named campaign groups, balanced perspective
- `the-church-door-note.html` — very good: verbatim quote in blockquote, provenance details
- `history_of_tyneham.html` — good: Norman Conquest to 1943, specific names and dates
- IWM and Lilian Bond's *Tyneham: A Lost Heritage* (1956) cited — positive E-E-A-T signals
- Comments sections contain genuine first-hand testimonies from descendant families (Buckler, Warr, Cooper, Taylor) — extraordinary primary source material

### Duplicate Content (MEDIUM)
- The full church door note text is quoted identically on both `the-church-door-note.html` and `tyneham-church.html`
- The core evacuation narrative ("225 residents, 28 days notice, never returned") is near-identical across `index.html`, `history_of_tyneham.html`, `after-the-evacuation.html`, and `the-campaign-to-return.html`

### Population Figure Inconsistency (MEDIUM)
- `index.html`: "225 residents"
- `after-the-evacuation.html`: "252 men, women and children"
Both appear across multiple pages. Pick 252 (more precise) and make it consistent sitewide.

### Meta Descriptions — 17 of 24 Need Rewriting

**Poor quality / WordPress-era teaser style (need complete rewrite):**
- `tyneham-church.html`: "A visit to Tyneham is Not Complete Without Going Inside St Marys Church..." (Title Case, vague)
- `tyneham-school.html`: "Tyneham School is One of The Main Attractions... Click Here to Learn More" (Title Case, "Click Here")
- `the_bond_family.html`: "...in Particualar Tyneham Village..." (typo + Title Case)
- `opening_times.html`: "Are You Visiting Tyneham Village? Check Out The Latest..." (Title Case, no info)
- `map_of_tyneham.html`: Title Case, circular ("shows the layout... don't miss the buildings")
- `tyneham_village_location.html`: "Click Here" — hides actual location info
- `tyneham-house.html`: "Click Here to Find Out What Happened to It" — hides story
- `lulworth-cove.html`: "Right Here" — cliché filler
- `durdle-door.html`: Title Case, vague
- `flowers-barrow.html`: "Click Here to Find Out More"
- `kimmeridge-bay.html`: "Click Here"

**Too long — will be SERP-truncated (trim to 155 chars):**
- `history_of_tyneham.html`: 260 chars
- `after-the-evacuation.html`: 182 chars
- `the-campaign-to-return.html`: 200 chars
- `the-church-door-note.html`: 191 chars
- `tyneham-remembered.html`: 228 chars
- `corfe-castle.html`: 188 chars
- `smuggling.html`: 193 chars
- `the-rectory.html`: ~200 chars

**Good quality, no changes needed:**
`index.html`, `contact.html`, `privacy.html`, `the_post_office.html`, `worbarrow-bay.html`

---

## On-Page SEO

### Title Tags

| Issue | Pages Affected | Severity |
|-------|---------------|---------|
| Title only 14 chars ("Kimmeridge Bay") | `kimmeridge-bay.html` | CRITICAL |
| Title only 23 chars ("The Rectory of Tyneham") | `the-rectory.html` | HIGH |
| Title only 27 chars ("Tyneham Opening Times 2026") | `opening_times.html` | HIGH |
| Title 68 chars — SERP truncation | `the-campaign-to-return.html` | HIGH |
| "Visitors Information" — vague, no keywords | `tyneham-school.html` | HIGH |
| "The Post Office - Tyneham Village" — generic | `the_post_office.html` | HIGH |

### H1 Tags
All 26 pages have exactly one H1. No missing or duplicate H1s. ✓

### Heading Hierarchy
- `history_of_tyneham.html`: H1 → H3 (skips H2 entirely throughout) — **HIGH**
- `the_bond_family.html`: H1 → H3 (skips H2 entirely throughout) — **HIGH**
- `index.html`: H3 sections appear before the second H2 — MEDIUM

### Internal Linking
- Navigation sidebar present on every page with ~15 links to core pages ✓
- Strong contextual internal linking on `history_of_tyneham.html` (9 contextual links) ✓
- **`smuggling.html` has NO nav entry or sidebar entry** — orphaned for user discovery
- Thin contextual linking on `tyneham-school.html` (only 2 links — missing bond family, church, history)
- Thin contextual linking on `kimmeridge-bay.html` (only 2 links — missing worbarrow-bay, flowers-barrow)

### Image Alt Text
- **118 images across all pages are missing alt attributes** — sitewide issue
- `alt="Advertisement"` on DVD cover sidebar image — appears on **every page** (sitewide template error)
- `tyneham-church.html`: Church door note image has `alt="Interior of St Mary's Church today"` — factually wrong
- Typo: `alt="Drawing of the post office at Tynehham village"` (double 'h') on `index.html`
- **Well-described:** Content images on corfe-castle.html, the_bond_family.html, and history_of_tyneham.html have good descriptive alt text

---

## Schema / Structured Data

### Current Status — CRITICAL

| Pages with schema | 1 of 26 |
|---|---|
| Schema type | FAQPage only (index.html) |
| BreadcrumbList | 0 of 26 |
| TouristAttraction | 0 |
| Article | 0 |
| LandmarksOrHistoricalBuildings | 0 |
| WebSite | 0 |
| OpeningHoursSpecification | 0 |

The FAQPage on `index.html` is structurally valid. However the site is essentially invisible to Google's rich result engine for attractions, landmarks, articles, and opening hours.

### Priority Schema Additions

**CRITICAL:**
1. `index.html` — Add `WebSite` schema (sitelinks searchbox eligibility) + `TouristAttraction`/`LandmarksOrHistoricalBuildings` with coordinates, address, and opening hours
2. `opening_times.html` — Add `TouristAttraction` with `OpeningHoursSpecification` — the highest-intent page on the site has zero schema

**HIGH:**
3. BreadcrumbList on all 24 inner pages (pattern: Home → [Section] → [Page])
4. `tyneham-church.html`, `tyneham-school.html` — `LandmarksOrHistoricalBuildings` + `Museum`
5. `worbarrow-bay.html`, `durdle-door.html`, `lulworth-cove.html`, `corfe-castle.html` — `TouristAttraction`

**MEDIUM:**
6. `history_of_tyneham.html`, `after-the-evacuation.html`, `the-campaign-to-return.html`, `the-church-door-note.html`, `the_bond_family.html`, `smuggling.html` — `Article` schema with `author`, `publisher`, `datePublished`
7. `tyneham-remembered.html` — `Product` schema for DVD/download offers
8. `kimmeridge-bay.html`, `flowers-barrow.html`, `tyneham-house.html`, `the-rectory.html`, `the_post_office.html` — appropriate `TouristAttraction` or `LandmarksOrHistoricalBuildings`

**Additional fixes on existing schema:**
- `index.html` FAQPage: answers in schema don't exactly match visible accordion text — Google may flag content mismatch
- `og:image` uses relative paths on all pages — must be absolute URLs for social sharing

---

## Performance (Core Web Vitals)

### LCP — Good partial signals
- Hero image on `index.html` has `fetchpriority="high"` ✓
- No preloader/spinner (unlike the Thailand site) ✓
- No `<link rel="preload">` for hero image — would improve LCP

### Render-Blocking Resources
- Bootstrap JS loaded at end of body — non-render-blocking ✓
- CSS (`styles.css`) is **233KB unminified** — includes Bootstrap + custom CSS bundled together
- No `preconnect` hints for external CDN resources

### Image Format
- **97 JPG files, 6 WebP files, 3 PNG files** in `/assets/`
- Only 6% of images are in modern format — significant opportunity
- Converting JPGs to WebP typically saves 25–35% file size

### CLS Signals
- Sidebar has CSS `min-height: 620px` for ad reservation — creates 620px blank space when ads don't load
- Mobile sidebar ad placeholder is 300px min-height (80% of a 375px phone viewport)
- Google Maps iframe on `index.html` has `width="900"` HTML attribute inside a ratio container — redundant

---

## AI Search Readiness (GEO)

### Overall AI Readiness: 6.2 / 10

### llms.txt — Missing (HIGH)
No `/llms.txt` exists. Recommended content: site description, key page index with URLs, key factual claims about Tyneham (evacuation date, population, MoD ownership, coordinates).

### AI Crawler Access
All AI bots have full access. ✓

### Citability Scores by Page
| Page | Score | Notes |
|------|-------|-------|
| `the-church-door-note.html` | 9/10 | Verbatim quote in blockquote, specific dates, provenance |
| `after-the-evacuation.html` | 8/10 | Named families, specific dates, primary source cited |
| `index.html` | 7/10 | FAQ schema, visitor facts, good density |
| `history_of_tyneham.html` | 7/10 | Strong facts, too short for topic depth |
| `tyneham-school.html` | 6/10 | Good facts, weak meta |
| `opening_times.html` | 5/10 | Dates present but JS-only "open today" widget invisible to crawlers |

### Key AI Overview Eligibility
High eligibility: "tyneham church door note", "tyneham evacuation 1943", "is tyneham national trust"  
At risk: "tyneham opening times 2026" — no FAQ schema, JS widget invisible to AI

### Entity Establishment — Incomplete (HIGH)
No `TouristAttraction` or `Place` JSON-LD to tell Google what Tyneham is as an entity. Without this, Tyneham Village is not established as a named entity in Google's Knowledge Graph from this site's signals alone.

---

## Search Experience Optimization (SXO)

### Intent Matching — Issues Found

**CRITICAL: `tyneham_village_location.html` — intent mismatch + postcode contradiction**
- Page targets "how to get to Tyneham" but opens with 5 paragraphs of scenic geography waffle
- Directions and postcode are buried 3+ scrolls down past an ad
- This page says Tyneham "doesn't have a postcode" — while `opening_times.html` gives BH20 5JH

**CRITICAL: No walking routes page**
"Tyneham walk" / "Tyneham to Worbarrow Bay walk" is likely a top-3 visitor intent. No dedicated page exists.

**HIGH: AdSense density issues**
- `index.html`: First ad appears after ONE paragraph — disrupts the primary emotional hook
- `history_of_tyneham.html`: 5 AdSense units in a medium-length article (one ad per ~200 words)
- These patterns risk Google's ad-heavy content policy signals

**HIGH: Missing high-intent pages**
- No "Tyneham parking" page (or even a section) — current FAQ answer has no useful details
- No "Tyneham dog friendly" page — mentioned in FAQ but no standalone content

**MEDIUM: Navigation gaps**
- `smuggling.html` has no nav entry — invisible to users who don't know it exists
- No search function or "Plan Your Visit" hub
- Sidebar hardcodes "Lulworth Cove" as active (highlighted) on every page regardless of current page

**MEDIUM: Mobile experience**
- Hero images on inner pages use `loading="lazy"` — may cause visible layout shift on first load (LCP concern)
- Float-right images may cause text-wrapping issues on narrow viewports (320–375px)

---

## Images

- **118 img tags across all pages missing alt attributes** (HIGH)
- 97 of ~106 image files are JPG — conversion to WebP would save significant bandwidth
- Content images that do have alt text are generally well-described (corfe-castle, bond_family, history pages excellent)
- Sitewide `alt="Advertisement"` on DVD cover sidebar — affects all pages via shared template
- One factually incorrect alt text on church page (`alt="Interior of St Mary's Church today"` on a photo of the church door note)

---

## Files Examined
- `/home/matt/claude/websites/tyneham/website/index.html`
- `/home/matt/claude/websites/tyneham/website/sitemap.xml`
- `/home/matt/claude/websites/tyneham/website/robots.txt`
- `/home/matt/claude/websites/tyneham/website/_redirects`
- `/home/matt/claude/websites/tyneham/website/_headers`
- `/home/matt/claude/websites/tyneham/website/ads.txt`
- `/home/matt/claude/websites/tyneham/website/css/styles.css` (233KB)
- Plus 20 additional HTML pages audited individually
