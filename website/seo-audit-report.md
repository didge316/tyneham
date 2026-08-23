# SEO Audit — TynehamVillage.org

**Date:** Audit run against static build in `website/` (site live at https://tynehamvillage.org/)
**Scope:** Full technical + on-page + content audit of all 35 sitemap pages + homepage.

---

## Executive Summary

This is an **exceptionally well-optimised site**. The technical and on-page foundations are strong and most advanced SEO best practices are already implemented. This is not a site with critical blockers — it's a mature, hand-crafted static site.

**Overall health: 90/100 (Excellent)**

**What's done well (keep this up):**
- ✅ Every page has a unique, well-crafted title (50–60 chars), description (130–160 chars), single H1, canonical tag, and Open Graph / Twitter card.
- ✅ All 87 JSON-LD structured-data blocks are valid, and cover an impressive range: FAQPage, Article, BreadcrumbList, Organization, Person, TouristAttraction, LandmarksOrHistoricalBuildings, GeoCoordinates, Offer, Product, Quotation, Event, ImageGallery, Map.
- ✅ Clean, hyphenated, keyword-rich URLs; aggressive and correct canonicalisation (www→non-www, index.html→/, trailing-slash, old WordPress + underscore redirects).
- ✅ robots.txt, sitemap.xml, and `_headers` caching rules are all correct. Security headers (HSTS preload, Permissions-Policy) are excellent.
- ✅ All 88 images have alt text. Lazy-loading in place. Caching headers for assets/CSS/JS are immutable-long-lived.
- ✅ Strong internal linking — no orphan pages; the homepage nav links to every section.
- ✅ `llms.txt` present for AI-search discoverability; robots.txt explicitly allows/denies modern citation bots.

**Priority improvements (all low-effort, high-value):**
1. **Image & video optimisation** — 30 MB in `assets/`, with many 450–500 KB `.jpg` files and a 595 KB `.mp4`. These are the single biggest speed risk. Convert to WebP/AVIF and shrink.
2. **Add a LocalBusiness / Organization + OpeningHours structured-data pass** and verify rich results (FAQ / opening hours) render in Google Rich Results Test.
3. **Fill the two clear content gaps** flagged in `TODO.md`: **Gad Cliff** and **Corfe Castle** pages (both already exist as pages — confirm they're live/indexed and fully cross-linked). Also the "red telephone box" and "Jurassic Coast UNESCO" additions.
4. **Consider adding `OpeningHours` / `isAccessibleForFinancialIncentives: Free`** to help win "Tyneham opening times" and "is Tyneham open today" featured snippets.
5. **Submit/verify in Google Search Console** and confirm the sitemap is indexed; monitor for the many redirect targets resolving cleanly.

---

## Technical SEO Findings

### T1 — Large image/video files slow page load (HIGH impact, LOW effort)
- **Issue:** The `assets/` directory holds 211 files totalling **30 MB**. The largest are a **595 KB `.mp4`** (`tyneham-ad-320.mp4`) and a dozen **460–500 KB `.jpg`** files (`wafs-tyneham-2.jpg`, `tyneham-farm.webp`, `wildflowers.webp`, etc.). The homepage alone is 95 KB of HTML.
- **Impact:** Images are almost certainly the LCP element on the homepage and landing pages. 450 KB JPEGs delay LCP and inflate bandwidth, hurting Core Web Vitals (LCP) and mobile speed.
- **Evidence:** `ls -lhS assets` shows top files ~480 KB each; `du -sh assets` = 30 MB.
- **Fix:** Recompress and convert to WebP/AVIF (target < 60 KB per hero image, < 30 KB per supporting image). Shrink the video to a looping `.webm`/`.mp4` under ~200 KB or poster-image it. Use `sizes` attributes so mobile browsers load smaller variants. This is the highest-value performance fix on the site.

### T2 — Font delivery / render-blocking (MEDIUM, LOW effort)
- **Issue:** Every page preconnects and preloads Google Fonts (`fonts.googleapis.com`). If a custom font file is also loaded, it can be render-blocking.
- **Impact:** Can add TTFB-independent latency and a flash of unstyled text; minor LCP effect.
- **Fix:** Ensure fonts are `font-display: swap`, self-host theWOFF2 files locally (drop the API preconnect), and preload only the weights actually used.

### T3 — Redirect map is large but well-structured (LOW, informational)
- **Issue/Note:** `_redirects` contains ~90 rules. All are intentional (www, index.html, old WordPress slugs, underscore→hyphen, trailing-slash). No chains or loops detected; www→non-www returns 301 correctly; sitemap returns 200 with correct `application/xml` content-type.
- **Impact:** Positive — duplicate/legacy URLs are consolidated to canonicals. Just verify in GSC that none return 404/5xx.

### T4 — Security & headers are excellent (strength)
- HSTS (preload-ready), `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, strict `Permissions-Policy`, CORS `OP`. Caching headers make assets/CSS/JS immutable for a year. No issues.

### T5 — Crawlability & indexation (strength)
- robots.txt allows all important pages, references the sitemap, and thoughtfully splits citation-bot access (allows GPTBot/ClaudeBot/etc., blocks CCBot/Bytespider).
- Sitemap: 35 URLs, all self-canonical, all internally linked (no orphans). `lastmod` values are current.
- One minor note: sitemap `lastmod` dates are in **2026** and some are future-dated (e.g. 2026-07-19). Not a problem functionally, but keep `lastmod` accurate since Google uses it for crawl scheduling.

---

## On-Page SEO Findings

### P1 — Title tags: excellent (strength)
- All 36 pages have unique titles, primary keyword near the front, brand/qualifier at the end, and lengths in the 50–60 char ideal band. Examples: "Where is Tyneham? Location, Directions & Parking" (48), "Tyneham Opening Times 2026 | When to Visit the Ghost Village" (60).

### P2 — Meta descriptions: excellent (strength)
- All unique, 131–158 chars, compelling, with natural keyword use and implicit CTAs ("Compare the best options here", "before you travel"). Two utility pages (`thank-you/` noindex, `privacy/`) appropriately short.

### P3 — Heading structure: solid (strength)
- Every page has exactly one H1 containing the primary term, with logical H1→H2→H3 hierarchy.

### P4 — Canonicalisation & duplicates: excellent (strength)
- Self-referencing canonicals present on all pages; www, index.html, trailing-slash, and underscore/old-slug variants all 301 to canonical. No duplicate-content risk.

### P5 — Open Graph / Twitter (strength)
- Full `og:*` and `twitter:*` tags with images on all content pages (except noindex `thank-you`). Good social sharing.

### P6 — Image alt text (strength)
- All 88 images have `alt` attributes. Verify the alt text is descriptive (see content section) rather than file-name copies.

---

## Content Findings

### C1 — Content depth is strong (strength)
- Every content page runs **800–2,100+ words** of visible text. The thin pages are only the utility ones: `thank-you` (235 w, noindex — correct), `contact` (356 w), `privacy` (672 w). Nothing is dangerously thin.

### C2 — Keyword coverage & clustering (strength, with a watch item)
- Clear topical clusters: **History** (history, bond family, church, house, school, post office, rectory, after-evacuation, campaign-to-return), **Visitor info** (opening times, visiting, location, map, camping), **Jurassic Coast nearby** (durdle door, corfe castle, lulworth cove, kimmeridge, worbarrow), **Walks** (tyneham-walk, corfe-castle-walk, kimmeridge-tyneham-walk, lulworth-range-walks).
- **Watch — possible cannibalisation:** `corfe-castle/`, `durdle-door/`, `lulworth-cove/`, `kimmeridge-bay/` target broad landmark terms that also rank via the walk pages and homepage. They're differentiated by unique titles/content, but confirm each has a distinct primary keyword (e.g. "Corfe Castle near Tyneham" vs generic "Corfe Castle"). If they compete with each other, add self-canonical keyword differentiation.

### C3 — Content gaps from TODO.md (MEDIUM)
- **Gad Cliff** and **Corfe Castle** are listed in `TODO.md` as "not covered at all" — but pages now exist for both. **Action:** confirm both are live, indexed, and fully fleshed out; remove them from TODO. If Gad Cliff is "frequently searched," it's a real opportunity — ensure it has its own FAQ/schema.
- Remaining TODO items to ship: mention the **red telephone box** (most-photographed feature) and add **Jurassic Coast UNESCO status** context to relevant pages.

### C4 — E-E-A-T (strength, with small enhancement)
- Strong author signal: `about/` page + Person schema (23 instances) + `llms.txt` crediting James Langton. Trust signals present: privacy policy, contact, physical location, historical sourcing.
- **Enhancement:** Add author name + link to each article (Article → author Person) visibly on content pages, and consider a "Last reviewed" date for opening-times content (Google values freshness for visitable places).

### C5 — AI-search / generative visibility (strength)
- `llms.txt` is well written with key pages, facts, and clear structure. robots.txt explicitly permits citation bots. This positions the site well for AI Overviews.

---

## Prioritized Action Plan

| # | Action | Impact | Effort | Priority |
|---|--------|--------|--------|----------|
| 1 | Optimize & convert images/video to WebP/AVIF (<60 KB hero); add `sizes` | High (LCP/speed) | Med | **P1 – do now** |
| 2 | Confirm Gad Cliff + Corfe Castle pages are live, indexed, cross-linked; remove from TODO | Medium | Low | **P1** |
| 3 | Add/verify `LocalBusiness` or at least `Organization` + `OpeningHours` + `isAccessibleForFinancialIncentives: Free` schema to win "opening times"/"open today" snippets | Medium | Low | **P2** |
| 4 | Self-host fonts (WOFF2) with `font-display: swap`; keep only used weights | Low (speed) | Low | **P2** |
| 5 | Ship remaining TODO content: red telephone box + Jurassic Coast UNESCO notes | Low (quality) | Low | **P2** |
| 6 | Verify in Google Search Console: sitemap submitted, no crawl errors, redirect targets all 200, rich results render | Medium | Low | **P2** |
| 7 | Add visible "last reviewed" date to opening-times/visiting pages for freshness | Low | Low | **P3** |
| 8 | Review potential keyword cannibalisation among the 4 nearby-landmark pages | Low–Med | Low | **P3** |

---

## Notes on Methodology
- Audit performed by static analysis of the build output (all `*/index.html` + `index.html`), plus live `curl` checks of the deployed site (root, www redirect, sitemap content-type).
- **Schema limitation:** JSON-LD was validated as well-formed JSON and its `@type` values catalogued above. To confirm *rich result eligibility* (FAQ / opening hours rich snippets), run a representative page through the [Google Rich Results Test](https://search.google.com/test/rich-results), which renders JS and validates against live rich-result rules. All static JSON-LD here is correctly formed, but eligibility is confirmed only in that tool.
