# Full SEO Audit — tynehamvillage.org

**Date:** 2026-08-06
**Method:** Live crawl (35 pages) + Lighthouse 13.4.1 (3 pages × mobile/desktop) + Playwright rendering checks + specialist subagent audits (technical, content/E-E-A-T, schema, GEO, SXO, backlinks via Common Crawl, images/visual)
**Site:** Static HTML, Cloudflare Pages, 35 content pages
**Previous audits:** 2026-07-19 (82/100), 2026-07-13 (78/100), 2026-06-30 (83/100)

---

## Executive Summary

**SEO Health Score: 78/100** (slightly down from 82 in July — driven by fresh schema/CLS findings, not regressions; on-page and technical fundamentals remain excellent)

**Business type detected:** Local heritage / visitor guide (informational + transactional-local). Not a local business — no GBP; the "local" intent is visitor information (opening times, parking, directions).

**What's excellent (verified live this audit):**
- 35/35 pages: HTTP 200, self-referencing canonicals, exactly 1 H1, unique titles & meta descriptions, full OG + Twitter tags, alt text on every image
- Exemplary redirect hygiene: http→https, www→non-www, no-slash→slash all single-hop 301s
- Full security header suite (HSTS preload, XFO, XCTO, Referrer-Policy, Permissions-Policy, COOP) — no CSP (correct, preserves AdSense)
- Valid sitemap (35 URLs, synced with local site), real HTTP 404 page (not soft-404), thank-you/ correctly noindexed
- All content server-rendered — no JS/CSR indexing risk
- Clean, credible backlink profile: 15 verified referring domains incl. Wikipedia (5 language editions), UCL Press, Find a Grave, Athelhampton; zero toxic/spam signals
- High-passage-level citability (dates, numbers, named people) — best-in-class for a heritage site

**Top 5 critical issues:**
1. **`js/scripts.js` loads as a relative path → 404 on 35/36 pages.** The "Is Tyneham open today?" widget (on the site's highest-intent page), sidebar active-page highlighting, and weather card are all dead on inner pages.
2. **Publisher logo asset missing** — `assets/logo-publisher.png` referenced by 8 Article schemas but doesn't exist → **zero Article rich results** currently.
3. **Wrong `sameAs` on 11 attraction pages** — all point to Tyneham village's Wikipedia/Wikidata instead of their own entity (Durdle Door, Worbarrow Bay, etc.) → entity conflation that misleads Google/AI entity resolution.
4. **robots.txt AI-crawler conflict** — Cloudflare Managed `Disallow` + custom `Allow` for the same agents → GPTBot/ClaudeBot/Google-Extended access is **parser-dependent** (allowed by RFC-9309 parsers, blocked by Python stdlib `robotparser`).
5. **CLS failures** — opening-times 0.439, home 0.16–0.27 (AdSense-driven layout shift); TBT 324–533ms on all mobile pages (372KB AdSense/consent JS).

---

## Scoring

| Category | Weight | Score | Key deduction |
|----------|--------|-------|---------------|
| Technical SEO | 22% | 87 | robots.txt AI conflict, IndexNow-key in robots, ACAO:* |
| Content Quality | 23% | 78 | 9 pages no byline/Person schema, Bond tenure inconsistency, thin map page |
| On-Page SEO | 20% | 90 | Minor: awkward titles, thin pages |
| Schema / Structured Data | 10% | 55 | 0 Article rich results, wrong sameAs ×11, opening-hours contradiction |
| Performance (CWV) | 10% | 60 | CLS fail ×2, TBT fail ×all, LCP borderline |
| AI Search Readiness | 10% | 78 | llms.txt stale/incomplete, robots conflict |
| Images | 5% | 70 | 25 files >500KB, up to 13× over-delivery |

**Weighted total: 78/100**

---

## 1. Technical SEO

### Crawlability ✓
- 35/35 URLs 200 OK, all within 1–2 clicks of home, no orphans
- Sitemap referenced in robots.txt; valid XML, `application/xml`

### Indexability ✓
- All 35: self-referencing canonical, exactly 1 H1, `index, follow`
- `thank-you/` (noindex) correctly excluded from sitemap
- No hreflang needed (single locale)

### Security ✓
- HSTS `max-age=31536000; includeSubDomains; preload`, XFO `SAMEORIGIN`, XCTO `nosniff`, Referrer-Policy `strict-origin-when-cross-origin`, Permissions-Policy (geo/mic/camera `()`), COOP `same-origin-allow-popups`, NEL/Report-To
- HTTP/2 + HTTP/3 (`alt-svc: h3`), TLS valid, **103 Early Hints** preloads LCP hero
- Low: `Access-Control-Allow-Origin: *` returned on all responses (harmless today; scope to assets if ever serving private data)

### Redirects ✓ (all single-hop, path preserved)
- http→https 301, www→non-www 301, no-slash→slash 301 (verified live)

### 404 handling ✓
- `/does-not-exist/` → real HTTP 404 (not soft-404), useful page with nav + recovery links, `noindex, follow`

### Issues
| Sev | Issue | Recommendation |
|-----|-------|----------------|
| **High** | `<script src="js/scripts.js?v=10">` is relative → 404s on all 35 subpages (`/opening-times/js/scripts.js`). Breaks: open-today widget, weather card, sidebar highlighting. All 36 index.html use the relative path. | Bulk-change to absolute `/js/scripts.js?v=10` via `website/scripts/bulk_seo_fixes.py`-style script |
| Medium | robots.txt AI rules: Cloudflare Managed blocks + custom re-allows for GPTBot/ClaudeBot/Google-Extended → parser-dependent outcome (Protego=allow, Python `robotparser`=block). Also `anthropic-ai` is not a real Anthropic token (`ClaudeBot`/`Claude-User` are). | Remove the conflicting duplicate groups; keep one allow rule per intended agent; add `Claude-User` |
| Medium | `IndexNow-key: ...` line in robots.txt flagged as unknown directive by Lighthouse (costs the 100 on the SEO audit category) | Move key to `IndexNow.txt` file; delete the robots.txt line |
| Low | HTML served `cache-control: public, max-age=0, must-revalidate` | Optional: short HTML cache (e.g. `max-age=300`) |

---

## 2. Content Quality & E-E-A-T

**Content score: 74/100 · E-E-A-T 67/100 · AI citation readiness 80/100**

### Strengths
- Named human author (James Langton) with genuine first-person bio, funding disclosure (AdSense, no sponsored content), correction invitation
- Source transparency: names Bond's *Tyneham: A Lost Heritage* (1956), Rodney Legg's research, Dorset History Centre, National Archives, IWM oral histories, 1974 White Paper; "Sources & further reading" blocks on 3 pages
- Primary-source quotes used well (church door note verbatim; WAAF oral-history excerpt)
- Authentic descendant UGC in comments (Bucklers, Warrs, Taylors, Mills, Banister) — un-fakeable Experience signal
- Readability is good: 17–24 word sentences, jargon explained in context, clean H2/H3 hierarchy
- Duplicate-content risk low: only repeated content is the (legitimate) church-note quotation on 2 pages + site chrome

### Issues
| Sev | Issue | Evidence / Recommendation |
|-----|-------|---------------------------|
| **High** | **9 pages have no visible byline, no update date, no Person schema** (only meta author): corfe-castle, corfe-castle-walk, flowers-barrow, gad-cliff, kimmeridge-tyneham-walk, map-of-tyneham, tyneham-photos, tyneham-remembered, tyneham-village-location | Add the standard "By James Langton · Updated …" line + `dateModified` schema for consistent author attribution |
| **High** | **Opening-times page has two conflicting bylines**: "Updated July 2026" AND "Updated January 2026" (lines 281–282), plus calendar says "Last updated January 2026" | Remove the duplicate; reconcile all dates to July |
| Medium | **Bond tenure inconsistent: "nearly 250 years" vs "nearly 260 years"** (1683→1943 = 260). the-bond-family meta description + history-of-tyneham say 250; bond-family body, corfe-castle, tyneham-house say 260; tyneham-house says both on one page | Standardise on 260 everywhere including meta description |
| Medium | **Church-door-note attribution varies**: blockquote footer "The Women and Children of Tyneham" vs Quotation/FAQ schema "W.H. Bond, on behalf of the families" vs tyneham-in-wartime "The Villagers" | Pick one authoritative statement, apply across all three pages + schema |
| Medium | **map-of-tyneham is genuinely thin** (~113 content words; 424 with chrome) | Expand to ~300–400 words: per-building annotations + links, distances, walking times (car park → village → Worbarrow) |
| Medium | **Contact page is form-only** (35 words, no email/phone); operator email only inside noindexed privacy page; privacy policy is a generic template with no controller/operator name/address | Show `admin@tynehamvillage.org` on contact; name the operator + add an identity/address line to privacy |
| Medium | **Person `sameAs` on /about/ points to `en.wikipedia.org/wiki/Tyneham`** — the village, not the author | Remove or replace with real author profile |
| Low | Sources only on 3 pages, plain-text not hyperlinked; tyneham-photos alt typo "Tynehham"; a few hedged FAQ answers on homepage ("check the official website…") | Hyperlink sources; fix typo; sharpen FAQ answers |
| Low | 5 pages hardcode `datePublished: 2024-01-01` (after-the-evacuation, ghost-village, the-bond-family, the-campaign-to-return, the-church-door-note) | Set real publish dates or drop the field |

### Thin pages (content-only word counts)
| Page | Words | Verdict |
|------|-------|---------|
| map-of-tyneham | 113 | Genuinely thin — expand (see above) |
| the-post-office | 570 | Thin for a dedicated building page (rich story, deserves ~800–900) |
| tyneham-remembered | 542 | Acceptable (product/sales page) |
| about | 578 | Acceptable |
| gad-cliff, camp-at-tyneham, tyneham-school, lulworth-range-walks | 766–793 | Borderline but substantive |
| contact/thank-you/privacy | — | Functional, correct |

### Freshness
- opening-times calendar is current through Dec 2026 (Aug = open all month). ✓
- Stale: Christmas 2025/26 special-date text ("Open daily from Saturday 20 December 2025 … 4 January 2026") still on opening-times.
- Annual expiry to refresh in Jan 2027: "2026" in opening-times title/meta, lulworth-range-walks H1, kimmeridge-bay vehicle-charge references.

---

## 3. On-Page SEO

**90/100 — the strongest, cleanest dimension.**

- 35/35: unique `<title>` (mostly 45–65 chars), unique meta descriptions, 1 H1, canonical matches, full OG (5 tags) + Twitter (4 tags), `index,follow`
- All images have alt; alt quality good (~12 generic alts to improve, e.g. opening-times hero "Worbarrow Bay")
- Internal links: no orphan pages; content-cluster cross-linking strong (tyneham-walk is a model hub)
- Gaps:
  - **In-body linking:** camp-at-tyneham (1 inbound), corfe-castle-walk (1), map-of-tyneham (1), wildlife-at-tyneham (1) are under-linked. kimmeridge-bay's camping list and tyneham-walk's "Going further" never link camp-at-tyneham; tyneham-walk doesn't link corfe-castle-walk.
  - **Homepage ↔ /ghost-village/ cannibalization** for "tyneham ghost village" (homepage ranks; the 2,071-word dedicated page doesn't).
  - **/worbarrow-bay/** buries practical info (parking/access/dogs/swimming) under ~60% history — higher-volume planner intent is underserved.
  - **/corfe-castle/** can never win the navigational "corfe castle" SERP (National Trust owns it) — schema is `LandmarksOrHistoricalBuildings` not `TouristAttraction`; reframe as a Tyneham day-trip/itinerary page.
  - **flowers-barrow** title is keyword-awkward ("A Timeless Beacon of Dorset's History") vs natural query.

---

## 4. Schema / Structured Data

**55/100 — the weakest category, and the highest-leverage fix.**

### Coverage
| Type | Pages | Status |
|------|-------|--------|
| BreadcrumbList | 34 | ✓ Valid everywhere (the only universal rich-result win) |
| TouristAttraction + openingHours + geo | ~11 | ✗ sameAs wrong; hours contradicted by text |
| Article | 10 | ✗ **0 eligible** — missing publisher logo (8), missing publisher/date (2) |
| FAQPage | 6 | No Google rich result (restricted to gov/health since 2023) — keep for AI/GEO value |
| HowTo | 3 | Deprecated (retired Sept 2023) — dead weight |
| Person (about) | 1 | ✗ sameAs wrong |
| Product + Offer (tyneham-remembered) | 1 | ⚠️ Borderline (no seller/reviews) |
| Quotation (church-door-note) | 1 | ✓ |
| WebSite (home) | 1 | ⚠️ Missing SearchAction |

### Critical errors
1. **`assets/logo-publisher.png` missing (404)** — referenced by `publisher.logo` on 8 Article pages → Google's Article validator fails → **zero Article rich results**. Fix: upload a 600×60 logo (or point logo.url at an existing asset).
2. **Wrong `sameAs` ×11** — worbarrow-bay, durdle-door, lulworth-cove, kimmeridge-bay, gad-cliff, corfe-castle-walk, kimmeridge-tyneham-walk, lulworth-range-walks, tyneham-village-location, visiting-tyneham, opening-times all point `sameAs` at Tyneham village's Wikipedia/Wikidata. Each should reference its own entity (Durdle Door, Corfe Castle, Lulworth Cove, Kimmeridge Bay all have own Wikipedia pages) — or be dropped.
3. **Two incomplete Articles** — tyneham-in-wartime (no datePublished/dateModified, publisher without logo), ghost-village (no publisher at all).

### High
4. **Opening-hours contradiction** — `openingHoursSpecification` claims Sat/Sun 09:00–20:00 year-round; text says gate closes at dusk + closed on firing weekends. Model two specs (gate 9am–dusk; exhibitions 10am–4pm) and note closures.
5. **Canonical mismatch in schema** — all main-entity `url` values omit the trailing slash that canonical tags use (34 pages). Scriptable sweep.

### Medium / Low
6. Remove 3 deprecated HowTo blocks (keep the Article).
7. Add `Organization` block to homepage (name, url, logo, contactPoint); `ContactPage` on /contact/; VideoObject/Movie on /tyneham-remembered.
8. Per-building `geo` (church/school/house/post-office/rectory reuse the village centroid); ProfilePage on /about; WebSite SearchAction; ImageObject copyrights on /tyneham-photos.

---

## 5. Performance (Core Web Vitals — lab data, Lighthouse 13.4.1)

Mobile (simulated slow-4G):

| Page | Perf | LCP | TBT | CLS | FCP |
|------|------|-----|-----|-----|-----|
| / (home) | 76 | 2.33s | 533ms | **0.163 ✗** | 2.07s |
| /opening-times/ | 67 | 2.42s | 388ms | **0.439 ✗** | 1.89s |
| /history-of-tyneham/ | 90 | 2.04s | 324ms | 0.042 ✓ | 1.88s |

Accessibility 95/100 · Best-Practices 100/96/92 · SEO audit 92/100 (IndexNow-key deduction).

**Findings:**
- **CLS fails on opening-times (0.439) and home (0.163).** Isolated via A/B: CLS with JS disabled = 0.00; with ads blocked ≈ 0.02. Root cause = AdSense auto-ad insertion + the status-widget `py-5`/`min-height:120px` growth + FundingChoices consent dialog. Fix WITHOUT CSP (per repo policy): `html { scrollbar-gutter: stable; }`, reserve final widget height, constrain auto-ad slots; re-verify revenue after.
- **TBT 324–533ms (threshold 200ms)** — ~372KB of AdSense (227KB) + FundingChoices (145KB) + bootstrap (56KB) on the main thread. Defer third-party JS / lazy-load ads after `load`.
- **LCP borderline 2.0–2.4s** — render-blocking bootstrap.min.css (~1.15s) + styles.min.css (~750ms) + Google Fonts Lora (~783ms). Inline critical CSS / preload hero (already preloaded via 103 Early Hints) / font `display=swap`.
- **Page weights:** home 1,029KB/47 requests (827KB scripts), history 975KB, opening-times 559KB. 27 decorative Gravatar avatars (~50px each) add many requests — remove.

---

## 6. Images

**70/100**

- 208 files in `/assets/`: 77 jpg + 128 webp + 3 png. **100% of jpgs have a webp pair** (0 orphans on disk now). ✓
- 128 `<picture>` blocks, all with webp source + fallback. 179 bare `<img>` (126 direct webp — no jpg fallback for ~3% of browsers). All bare imgs have width/height; 166 lazy-loaded; heroes eager + `fetchpriority=high`. ✓
- **Oversized files:** 60 files >150KB; **25 >500KB (~22.5MB combined)**; total 43.2MB. Worst: purbeck-cliffs-aerial.webp (1.9MB/3838px), purbeck-coast-sea-thrift.webp (1.9MB), st-oswalds-bay.webp (1.86MB), man-o-war-bay.webp (1.49MB), kimmeridge-gad-cliff-view.webp (1.48MB), lulworth-ranges-coast.webp (1.26MB), lulworth-cove-aerial.webp (1.17MB).
- **Over-delivery up to 13×:** 3072px natives rendered in 235px columns (kimmeridge-bay 13.1×, lulworth-range-walks 10.7×, lulworth-cove/durdle-door ~8.5×). Page image weights: kimmeridge-bay 1.88MB, worbarrow-bay 1.81MB, tyneham-walk 1.41MB, ghost-village 1.27MB. Resize to display size (≈1000px / ≈1600px full-width) or add `srcset`+`sizes` — kimmeridge-bay drops to ~0.4MB.
- Defects: `TynehamHouseSouthEastView1943.jpg` is actually a PNG (565KB mislabeled); 2 `<picture>` fallbacks are also webp (lulworth-ranges-coast, wildflowers); 5 ghost-village picture fallbacks lack width/height; `decoding="async"` missing on picture fallbacks.
- Alt: 0 missing, all ≤125 chars, quality good; ~12 generic to improve (Worbarrow Bay hero, "Tyneham today", label-only cottage alts).

---

## 7. AI Search Readiness (GEO)

**78/100** (Citability 8/10 · Structural 8/10 · Multi-modal 7/10 · Authority 6.5/10 · Technical access 9/10)

### llms.txt
- Present, live 200, in sync with git. Missing 7 content pages + homepage vs sitemap (tyneham-in-wartime, corfe-castle-walk, kimmeridge-tyneham-walk, the-post-office, the-rectory, map-of-tyneham, camp-at-tyneham). **Stale "Last Updated 2026-07-13" despite newer pages absent.** URLs omit trailing slash; license/date in `##` headings rather than the spec's `<!-- LLMS.txt Metadata -->` block.

### AI crawler access (verified live)
- HTTP level: Cloudflare returns 200 to all AI UAs (robots.txt is the only enforcement). PerplexityBot/OAI-SearchBot/ChatGPT-User allowed. CCBot/Bytespider blocked (expected).
- **GPTBot / ClaudeBot / Google-Extended: ambiguous.** Cloudflare Managed `Disallow: /` + custom `Allow: /` → RFC-9309 parsers allow, Python stdlib `robotparser` blocks. Fix by removing the managed disallows for these agents.

### Citability
- Excellent: 252 residents, 19 Dec 1943, 28 days' notice, BH20 5QH, £2 parking, phone 01929 404714, named people, verbatim quotes, FAQ schema on 6 pages.
- Homepage renders the church door note as an **image only** — add the text beside it (the most-cited sentence in the story).
- "Is Tyneham open today?" is **JS-rendered** — invisible to no-JS AI crawlers. Add a static server-rendered answer.
- opening-times FAQ + duplicate byline give AIs conflicting freshness signals.

### Authority
- Named author + strong about page; but wrong Person sameAs, no external recognition found, thin external brand presence. Brand mentions (not backlinks) are the strongest AI-visibility lever — Wikipedia citations on Worbarrow Bay/Lulworth Ranges/Flower's Barrow articles are the natural next step.

---

## 8. Backlinks (Common Crawl — Tier 0, no Moz/Bing/DataForSEO)

**Backlink Health: 70/100** (capped — CC-only snapshot)

- Domain metrics: PageRank top 19.8%, harmonic centrality top 11.4% of the 120M-domain graph. Real (small) in-degree.
- **15 verified referring domains**, realistically ~20–40 total: Wikipedia ×5 language editions (nofollow), UCL Press journal (follow, academic), Athelhampton, Find a Grave, Virtual Swanage, See Around Britain, Haunted Generation, Sometimes Interesting, Slow Travel UK, 2 foreign travel blogs.
- Anchor distribution healthy: ~53% branded, 33% URL/naked, 0% exact-match keyword. Follow ratio 60% (dragged by Wikipedia).
- **No toxic/spam signals, no disavow needed.** No broken inbound links (all legacy URLs 301 correctly).
- Authority ceiling: cannot win "durdle door"/"lulworth cove" head terms (owned by National Trust/Lulworth Estate/Wikipedia/BBC — top ~0.001% of graph). **Do not chase head terms; target adjacent long-tails** and relevance-rich follow links.

### Link-building priorities
1. National Trust / jurassiccoast.org / visit-dorset.com / lulworth.com / Dorset History Centre / Tank Museum — all cover Tyneham but don't link (highest-value follow targets).
2. Wikipedia citations on Worbarrow Bay, Lulworth Ranges, Flower's Barrow, List of lost settlements.
3. Reclaim removed links: swanage.co.uk, worldghosttowns.com, BBC Dorset.
4. Walking sites (iFootpath, AllTrails, Dorset Ramblers, Walking Britain) — the 4 walk pages are link magnets.
5. Local press: dorsetecho.co.uk / bournemouthecho.co.uk (covered Tyneham repeatedly without linking).
6. Add free Moz/Bing keys for full profile + velocity tracking.

---

## 9. Visual / Rendering (Playwright)

- No horizontal overflow, no broken images on home/opening-times (desktop + mobile). Nav usable, hamburger works.
- Opening-times desktop: **status widget stuck on "Checking if Tyneham is open today…"** (JS never loads — confirmed root cause: relative script path). Duplicate byline visible.
- Homepage: AdSense `<ins>` banner (~330px) pushes H1 below fold on desktop; mobile CLS 0.27 (ad-driven); status widget works on home but buried at y≈21,400 on mobile (below the stacked sidebar).
- Console errors on all subpages: strict-MIME refusal of the 404'd `js/scripts.js`.

---

## 10. What's Already Fixed Since July 2026 Audits

- [x] privacy page in sitemap.xml (was missing) + now has JSON-LD
- [x] Favicon present on all pages (was missing on 33/35)
- [x] `<picture>` webp/jpg coverage now 100% of jpgs (was 15/35 pages)
- [x] Orphaned images cleared (was 271)
- [x] FAQPage schema added to opening-times, history-of-tyneham, church-door-note, visiting-tyneham, tyneham-walk + 4 walk pages HowTo
- [x] Author bylines added sitewide (18/27 content pages; 9 still missing — see Content)

---

## 11. Progress vs Previous Audits

| Issue | 06-30 | 07-13 | 07-19 | 08-06 (this) |
|-------|-------|-------|-------|--------------|
| Health score | 83 | 78 | 82 | **78** |
| Pages with full meta/OG/Twitter | Partial | 34 | 35 | **35** ✓ |
| Canonicals self-referencing | ✓ | ✓ | ✓ | **35** ✓ |
| `<picture>` webp coverage | — | 15 pages | 15 pages | **All jpgs paired** ✓ |
| Orphaned images | — | 271 | 271 | **0** ✓ |
| Favicon | — | — | 0 pages | **All** ✓ |
| privacy in sitemap + schema | — | Missing | Missing | **Fixed** ✓ |
| Article rich-result eligibility | — | — | — | **0/10** (missing logo) |
| sameAs correctness | — | — | — | **✗ 11 pages wrong entity** |
| CWV CLS (opening-times) | — | — | — | **0.439 ✗** |
| llms.txt completeness | — | — | — | **26/35 pages** |

---

## 12. Prioritised Action Plan (summary)

**CRITICAL (this week):**
1. Fix relative `js/scripts.js` path → absolute (bulk, all 36 files). Restores open-today widget, weather, sidebar.
2. Upload `assets/logo-publisher.png` (600×60) or repoint Article `publisher.logo` → makes 8 Article pages eligible.
3. Fix wrong `sameAs` on 11 attraction pages (own entity or drop).
4. Complete the 2 broken Articles (tyneham-in-wartime, ghost-village).
5. Resolve robots.txt AI-group conflict (remove managed disallows for GPTBot/ClaudeBot/Google-Extended; add Claude-User).

**HIGH (1 week):**
6. Fix opening-times duplicate/conflicting byline + reconcile calendar date.
7. Fix opening-hours schema contradiction (gate 9am–dusk vs exhibitions 10–4, note closures).
8. CLS fixes: `scrollbar-gutter: stable`, reserve widget height, constrain auto-ads (no CSP).
9. Update llms.txt (add 7 missing pages + homepage, fix date, metadata block).
10. Reconcile church-door-note attribution across 3 pages + schema.
11. Add bylines + Person schema + dateModified to the 9 pages missing them.
12. Add FAQPage schema to durdle-door; fix `isAccessibleForFree` to true.
13. Add static server-rendered "open today" answer to opening-times (for AI/no-JS).

**MEDIUM (1 month):**
14. Expand map-of-tyneham (113 → 300–400 words) and the-post-office.
15. Resize/right-size 25 oversized images (esp. 7 × 1MB+ webps) → kimmeridge-bay page weight 1.88MB → ~0.4MB.
16. Bond tenure → 260 everywhere; fix tyneham-house mixed references.
17. Cross-link camp-at-tyneham, corfe-castle-walk, map-of-tyneham, wildlife-at-tyneham.
18. Resolve homepage ↔ ghost-village cannibalization; restructure worbarrow-bay (planner facts first); reframe corfe-castle as day-trip page.
19. Remove IndexNow-key from robots.txt (→ SEO audit 100); remove deprecated HowTo schema.
20. Contact page visible email + privacy operator identity; fix Person sameAs on /about.
21. TBT: defer AdSense/consent JS; LCP: cut render-blocking CSS.

**LOW (backlog):**
22. Homepage church-note text beside image; fix malformed curly-quote classes in history-of-tyneham; remove 27 Gravatars; fix mislabeled PNG; alt-text polish (~12); per-building geo; WebSite SearchAction; ContactPage schema; stretch: GPX downloads on walk pages.
