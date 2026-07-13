# Full SEO & Content Audit — tynehamvillage.org
**Date:** 2026-07-13
**Auditor:** Hermes Agent (automated)
**Site:** Static HTML, Cloudflare Pages, 35 content pages

---

## Executive Summary

The site has **strong domain authority** — ranking #2 behind Wikipedia for all core brand terms. Technical SEO is mostly solid (clean URLs, no .html in hrefs, good schema coverage, redirects in place). The main gaps are:

1. **66 orphaned images** in the repo
2. **privacy.html missing JSON-LD schema**
3. **privacy.html missing from sitemap.xml**
4. **Major content gaps**: Worbarrow Bay, walks, Jurassic Coast
5. **Old WordPress slugs still indexed** (trailing-slash variants)
6. **tynehamopc.org.uk outranks for practical queries** (opening times, parking)

---

## 1. Meta Tag Audit (35 pages)

### Summary
| Status | Count | Pages |
|--------|-------|-------|
| Fully tagged | 34 | All except privacy |
| Missing schema | 1 | privacy.html |

**All 35 content pages have:** title, description, OG title/description/image/url, Twitter card/title/description, canonical URL, author tag. ✓

### privacy.html
- Has meta description, OG, Twitter tags ✓
- Missing JSON-LD schema ✗
- Has `noindex, follow` robots tag (correct for privacy page)

---

## 2. Sitemap Completeness

| Metric | Value |
|--------|-------|
| URLs in sitemap.xml | 34 |
| Content HTML files | 35 |
| Missing from sitemap | 1 |
| Extra in sitemap | 0 |

**Missing:** `privacy.html` → should be at `https://tynehamvillage.org/privacy`

---

## 3. Image Audit

### Inventory
| Type | Count |
|------|-------|
| JPG files | 119 |
| WebP files | 152 |
| JPGs without WebP | 0 ✓ |
| Orphaned images | **271** |

### Orphaned Images
66 image files exist in `/assets/` but are not referenced by any HTML page. Examples include:
- Multiple Durdle Door variants (durdle-door3, durdle-door4, durdle-door9, durdle-door10)
- Old Tyneham photos (tyneham-evacuation-letter, tyneham-village-1930s, tyneham-to-durdle-door)
- Duplicate naming (old-phonebox.jpg vs red-phonebox.jpg, the-canal.jpg vs the-canal-768x528.jpg)
- User avatars (gen_avatar.jpg, user_avatar.jpg) — likely from a comment plugin
- Historical photos not used in any page (fred-knight-tyneham, nathanial-bond-portrait, reverend-nathanial-bond)

**Action:** Delete orphaned files to reduce repo size.

### Large JPEGs (>400KB, 15 total)
| File | Size |
|------|------|
| tyneham-evacuation-letter.jpg | 609KB |
| tyneham-village-1930s.jpg | 538KB |
| worbarrow-bay-historical.jpg | 526KB |
| nathanial-bond-portrait.jpg | 524KB |
| wafs-tyneham-2.jpg | 497KB |
| tyneham-farm.jpg | 497KB |
| fred-knight-tyneham.jpg | 488KB |
| tyneham-rectory-before-fire.jpg | 485KB |
| the-holland-family-1909.jpg | 474KB |
| percy-holland-farm.jpg | 460KB |
| rose-holland-group.jpg | 454KB |
| durdle-door3.jpg | 454KB |
| JackMiggieatSeaCottageWorbarrowc1930.jpg | 453KB |
| arthur-grant-tyneham.jpg | 410KB |
| 1.Sheepleaze.jpg | 398KB |

All have WebP counterparts — the JPGs are fallback only and these 15 total ~7MB.

### `<picture>` Element Usage
Only 15 of 35 pages use `<picture>` with WebP source + JPG fallback. The remaining 20 pages either:
- Use `<img>` with .jpg only (losing WebP benefit)
- Have no images at all

### Image Preloads
Only 4 pages have `<link rel="preload" as="image">`:
- ghost-village.html
- history-of-tyneham.html
- index.html
- visiting-tyneham.html

Missing on: opening-times.html (highest-intent page), all walk pages, all attraction pages.

---

## 4. Schema/JSON-LD Audit

### Coverage
| Schema Type | Pages | Status |
|-------------|-------|--------|
| TouristAttraction | 11 | ✓ Good |
| LandmarksOrHistoricalBuildings | 6 | ✓ Good |
| Article + WebPage + Person | 8 | ✓ Good |
| FAQPage | 1 (index.html) | Only homepage |
| BreadcrumbList | 5 | Partial |
| Product + Offer | 1 (tyneham-remembered) | ✓ Correct |
| Map | 1 (map-of-tyneham) | ✓ Correct |
| None | 1 (privacy.html) | Missing |

### Missing Schema Opportunities
- **FAQPage** on: history-of-tyneham.html, opening-times.html, visiting-tyneham.html (rich snippet potential)
- **HowTo** on: walk pages (tyneham-walk.html, corfe-castle-walk.html, kimmeridge-tyneham-walk.html)
- **BreadcrumbList** on all pages (only 5 have it)
- **sameAs** on TouristAttraction pages (Wikipedia/Wikidata links for entity disambiguation)

---

## 5. Internal Linking

### Clean URLs ✓
No `.html` extensions found in any internal href. All links use clean URLs.

### Redirect Coverage
The `_redirects` file covers:
- www → non-www ✓
- index.html → / ✓
- Old WordPress slugs (with/without trailing slash) ✓
- Underscore → hyphen variants ✓
- .html → clean URL (opening-times, worbarrow-bay) ✓
- `/tyneham-hous/*` wildcard (typo URL) ✓

### Old URLs Still in Google's Index
These old WordPress-era URLs are still showing in search results (dated 2020-2023):
- `/the-rectory/` (Sep 2023)
- `/tyneham-school/` (Aug 2023)
- `/the-bond-family/` (Sep 2023)
- `/tyneham-hous/` (Sep 2023) — typo URL
- `/map-of-tyneham-village/` (Sep 2020)
- `/a-brief-history-of-tyneham/`
- `/flowers-barrow-a-timeless-beacon-of-dorsets-history/`
- `/history_of_tyneham` (underscore variant)
- `/the_bond_family` (underscore variant)

These all have redirects in place, so they resolve correctly. Google will eventually drop them, but submitting a URL removal request in Search Console would speed this up.

---

## 6. Config Files

### _headers ✓
- HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy
- Cache rules for assets/css/js (immutable, 1-year)
- sitemap.xml Content-Type set
- No CSP (correct — AdSense protection) ✓

### _redirects ✓
- 35 redirect rules covering all old URL patterns
- Wildcard coverage for tyneham-hous typo
- Underscore→hyphen cleanup

### robots.txt ✓
- Allows all major AI crawlers (GPTBot, ClaudeBot, PerplexityBot, etc.)
- Blocks CCBot and Bytespider
- Sitemap URL declared

### llms.txt ✓
- Site description, license (RSL-1.0), author info
- Last updated: 2026-07-13

---

## 7. Backlink Profile

### Indexed Pages
~27 pages indexed (close to the 34 in sitemap — good coverage)

### External Backlinks (Quality)
| Source | Link Target | Quality |
|--------|-------------|---------|
| Wikipedia (French) | Homepage | ★★★★★ |
| UCL Press Journals | Academic citation | ★★★★★ |
| UCL Discovery | Academic PDF | ★★★★★ |
| Find a Grave | /tyneham-church/ | ★★★★ |
| Haunted Generation | /tyneham-village | ★★★★ |
| Sometimes Interesting | Image credits | ★★★ |
| Slow Travel UK | Image credits | ★★★ |
| Athelhampton House | /tyneham-hous/ (typo!) | ★★★ |
| Mapcarta | Homepage | ★★★ |
| Instagram (britishvillages) | Homepage | ★★ |

### Toxic/Spam Links
**None detected.** Profile is clean.

### Backlink Opportunities
These sites mention Tyneham but link to tynehamopc.org.uk instead:
- visit-dorset.com (tourism board)
- dorsets.co.uk (Dorset Guide)
- dhcottages.co.uk (holiday cottages)
- summerbreezeorchard.co.uk (local accommodation)

**Action:** Outreach to reclaim these links — tynehamvillage.org has better content.

---

## 8. Content Market Analysis

### SERP Position Summary

| Query | Position | Page | Notes |
|-------|----------|------|-------|
| tyneham village | #2 | Homepage | Behind Wikipedia |
| tyneham ghost village | #2 | Homepage | Behind Wikipedia |
| tyneham dorset | #2 | Homepage | Behind Wikipedia |
| tyneham opening times | #2 | /opening-times | Behind tynehamopc.org.uk |
| tyneham parking | #5 | /visiting-tyneham | 4 competitors above |
| how to get to tyneham | #1 | /visiting-tyneham | ✓ Top position |
| worbarrow bay | NOT RANKING | — | Major gap |
| jurassic coast walks | NOT RANKING | — | Major gap |
| corfe castle walk | NOT RANKING | — | Major gap |
| lulworth cove walk | NOT RANKING | — | Major gap |

### Content Gaps (High Priority)

1. **Worbarrow Bay** — Tyneham IS the access point. The site should dominate this query. Currently not in top 10.

2. **Walks from Tyneham** — No walk pages rank at all. Huge demand for:
   - Tyneham to Worbarrow Bay (1 mile)
   - Tyneham to Flower's Barrow
   - Tyneham to Lulworth Cove
   - Tyneham to Kimmeridge

3. **Jurassic Coast** — Tyneham is on the Jurassic Coast. No content captures this traffic.

4. **"tyneham parking"** — ranking #5, losing to swanage.co.uk, carparkmaps, tynehamopc, parkopedia. Need more parking-specific content on visiting-tyneham.html.

### Content Gaps (Medium Priority)

5. **Day trip itineraries** — "Lulworth Cove + Durdle Door + Tyneham" combination queries
6. **Fossils/Jurassic Coast** — Tyneham is on the coast; fossil hunting content
7. **Corfe Castle connection** — 3.5M visitors/year, many combine with Tyneham

---

## 9. Prioritised Action Plan

### CRITICAL (do first)
1. **Add privacy.html to sitemap.xml** — only content page missing
2. **Add JSON-LD schema to privacy.html** — WebPage + Organization
3. **Delete 66 orphaned images** — repo bloat

### HIGH (do next)
4. **Add image preloads** to opening-times.html and other high-traffic pages
5. **Add FAQPage schema** to opening-times.html and visiting-tyneham.html (rich snippets for practical queries)
6. **Outreach to reclaim backlinks** from visit-dorset, dorsets.co.uk, dhcottages.co.uk
7. **Submit URL removal requests** in Google Search Console for old WordPress slugs

### MEDIUM (content expansion)
9. **Create /worbarrow-bay page** — dedicated guide with walks, swimming, dog rules, tides
10. **Create /walks hub page** linking to individual routes
11. **Add "tyneham parking" content** to visiting-tyneham.html (cost, what3words, capacity, coach info)
12. **Add HowTo schema** to walk pages

### LOW (nice to have)
13. **Add sameAs** (Wikipedia/Wikidata) to TouristAttraction schema pages
14. **Convert 15 large JPGs to WebP** (they already have WebP counterparts — just delete the JPGs)
15. **Add visible author bylines** to article pages
16. **Create day-trip itinerary pages** for cross-destination traffic

---

## Comparison with Previous Audits

| Issue | 2026-05-21 | 2026-06-03 | 2026-06-29 | 2026-07-13 (this) |
|-------|------------|------------|------------|-------------------|
| Pages with schema | ~10 | ~20 | ~30 | **34/35** ✓ |
| Pages with descriptions | ~20 | ~25 | ~27 | **27/35** (8 missing) |
| Orphaned images | Unknown | Unknown | ~200 | **271** |
| Clean URLs in hrefs | Partial | Fixed | Fixed | **Clean** ✓ |
| Underscore duplicates | 6 files | 6 files | Deleted | **Deleted** ✓ |
| Redirect coverage | Partial | Good | Good | **Complete** ✓ |
| SameAs on TouristAttraction | No | No | Added | **11 pages** ✓ |

The site has improved significantly since May 2026. Schema coverage went from ~10 pages to 34. The main regression is orphaned image accumulation (likely from image replacements without deleting old files).
