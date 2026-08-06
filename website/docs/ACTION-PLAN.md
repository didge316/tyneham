# Tyneham Village — SEO Action Plan

**Based on full audit of tynehamvillage.org — 06 August 2026**
**SEO Health Score: 78/100 → Target: 90+/100**
**Previous audit:** 19 July 2026 (82/100)
**Previous audits:** 13 July 2026 (78/100), 30 June 2026 (83/100)

See `AUDIT-2026-08-06-FULL.md` for full detail.

> Note: score dipped from 82→78 driven by newly-surfaced schema/CLS issues (missing publisher logo, wrong `sameAs`, ad-driven layout shift), not regressions. On-page and technical fundamentals are at their best yet. The `js/scripts.js` relative-path bug has been live since the JS was versioned `?v=10` — fixing it restores several visible features.

---

## CRITICAL — Fix Within 1 Week

### C1. Fix relative `js/scripts.js` path (sitewide, 36 files) ★
`<script src="js/scripts.js?v=10">` resolves to `/opening-times/js/scripts.js` on subpages → **404 on 35/36 pages**. Breaks the "Is Tyneham open today?" widget (highest-intent page), weather card, and sidebar active-page highlighting.
**Fix:** change to `<script src="/js/scripts.js?v=10">` using a `bulk_seo_fixes.py`-style script.

### C2. Missing publisher logo → zero Article rich results ★
`assets/logo-publisher.png` is referenced by `publisher.logo` on 8 Article pages but **doesn't exist** (404). Google's Article validator fails → 0/10 Article pages eligible.
**Fix:** create/upload `assets/logo-publisher.png` (600×60) or repoint each Article's `logo.url` to an existing asset.

### C3. Wrong `sameAs` on 11 attraction pages ★
worbarrow-bay, durdle-door, lulworth-cove, kimmeridge-bay, gad-cliff, corfe-castle-walk, kimmeridge-tyneham-walk, lulworth-range-walks, tyneham-village-location, visiting-tyneham, opening-times all point `sameAs` to Tyneham village's Wikipedia/Wikidata. Entity conflation misleads Google/AI.
**Fix:** point each at its own entity (Durdle Door / Corfe Castle / Lulworth Cove / Kimmeridge Bay each have Wikipedia pages) or drop the field.

### C4. Complete the two broken Articles
- `tyneham-in-wartime`: missing `datePublished`/`dateModified`, publisher has no logo
- `ghost-village`: no `publisher` block at all

### C5. robots.txt AI-crawler conflict ★
Cloudflare Managed `Disallow: /` + custom `Allow: /` for GPTBot/ClaudeBot/Google-Extended → **parser-dependent** (RFC-9309 parsers allow, Python `robotparser` blocks). Also `anthropic-ai` isn't a real Anthropic token.
**Fix:** remove the managed disallows for these agents (or disable Cloudflare's managed robots block list for them); add `Claude-User`.

---

## HIGH — Fix Within 2 Weeks

### H1. opening-times: duplicate/conflicting bylines
Two byline lines "Updated July 2026" AND "Updated January 2026" (lines 281–282) + calendar "Last updated January 2026". Conflicting freshness signals to users, crawlers and AIs.
**Fix:** keep one date; reconcile calendar footer to July.

### H2. opening-times: opening-hours schema contradicts text
Schema claims Sat/Sun 09:00–20:00 year-round; text says gate closes at dusk + closed on firing weekends.
**Fix:** model two specs — gate `09:00–dusk` and exhibitions `10:00–16:00` — and note closures.

### H3. CLS on opening-times (0.439) and home (0.16–0.27)
AdSense auto-ad insertion + status-widget growth + consent dialog. Verified: CLS ≈ 0.00 with JS off, ≈ 0.02 with ads blocked. **Do NOT add a CSP** (breaks AdSense).
**Fix:** `html { scrollbar-gutter: stable; }`, reserve final widget height (drop `py-5` bounce), constrain auto-ad slot heights; re-verify revenue after.

### H4. Update llms.txt
Missing 7 pages + homepage (26/35 listed); stale "Last Updated 2026-07-13"; URLs without trailing slash; use the `<!-- LLMS.txt Metadata -->` block.

### H5. Reconcile church-door-note attribution
"Women and Children" (body) vs "W.H. Bond, on behalf of the families" (schema) vs "The Villagers" (tyneham-in-wartime). One authoritative statement everywhere.

### H6. Add bylines + Person schema + dateModified to 9 pages
corfe-castle, corfe-castle-walk, flowers-barrow, gad-cliff, kimmeridge-tyneham-walk, map-of-tyneham, tyneham-photos, tyneham-remembered, tyneham-village-location — currently meta-author only.

### H7. durdle-door: FAQPage schema + `isAccessibleForFree`
9-question visible accordion has no FAQPage JSON-LD; schema says `isAccessibleForFree: false` while text says free entry.

### H8. Static "open today" answer on opening-times
The "is it open today?" answer is JS-rendered (invisible to no-JS crawlers/AIs). Add a server-rendered current/next-open-date line beside the widget.

---

## MEDIUM — Fix Within 1 Month

### M1. Expand map-of-tyneham (113 → 300–400 words)
Per-building annotations with links (church, school, post office, rectory, house), distances and walking times (car park → village → Worbarrow Bay).

### M2. Right-size 25 oversized images
7 files >1MB (purbeck-cliffs-aerial 1.9MB, purbeck-coast-sea-thrift 1.9MB, st-oswalds-bay 1.86MB, man-o-war-bay 1.49MB, kimmeridge-gad-cliff-view 1.48MB, lulworth-ranges-coast 1.26MB, lulworth-cove-aerial 1.17MB). Images delivered at up to 13× render size. kimmeridge-bay page weight 1.88MB → ~0.4MB after resize (≈1000px / 1600px full-width or `srcset`+`sizes`).

### M3. Bond tenure → 260 years everywhere
the-bond-family meta description + history-of-tyneham say "nearly 250 years"; bond-family body, corfe-castle, tyneham-house say 260 (correct: 1683→1943). tyneham-house says both. Standardise, including meta descriptions.

### M4. Cross-link the 4 under-linked pages
camp-at-tyneham (from kimmeridge-bay camping list + tyneham-walk + tyneham-village-location), corfe-castle-walk (from lulworth-range-walks + tyneham-walk "Going further"), map-of-tyneham, wildlife-at-tyneham.

### M5. Resolve homepage ↔ ghost-village cannibalization
Homepage ranks for "tyneham ghost village"; the 2,071-word /ghost-village/ doesn't. Make the subpage the target; strengthen the homepage's link to it.

### M6. Restructure worbarrow-bay (planner facts first)
Lead with parking / 1-mile walk / range-open access / dogs / swimming rules / no facilities, then history (the differentiator).

### M7. Remove IndexNow-key from robots.txt
Flagged as unknown directive by Lighthouse (SEO audit stuck at 92). Move to `IndexNow.txt`.

### M8. Remove deprecated HowTo schema (3 walk pages)
No rich results since Sept 2023. Keep the Article + TouristAttraction blocks.

### M9. Contact page visible email + privacy operator identity
Show `admin@tynehamvillage.org` on /contact/; name the operator + add address/identity to privacy policy.

### M10. Fix Person `sameAs` on /about/
Points to `en.wikipedia.org/wiki/Tyneham` (the village). Remove or use the author's real profile.

### M11. TBT + LCP
TBT 324–533ms (372KB AdSense/consent JS on main thread) → defer ads after `load`. LCP 2.0–2.4s → inline critical CSS / trim render-blocking Bootstrap + Lora. Remove 27 decorative Gravatar avatars.

---

## LOW — Backlog

### L1. Homepage church-door-note text
Currently image-only. Add the note's text beside it (most-cited sentence in Tyneham's story — AI citability).

### L2. Expand the-post-office (~570 words)
Rich story (1880–1942 shopkeeper timeline, K1 kiosk, *Comrades* film) deserves ~800–900 words.

### L3. Fix malformed HTML in history-of-tyneham
Curly quotes in `class="”fs-5 mb-4 pt-2”"` on 4 paragraphs (lines 343/349/353/357).

### L4. Reframe corfe-castle as day-trip/itinerary page
Can't win the navigational "corfe castle" SERP (National Trust). Switch schema to TouristAttraction; frame "Corfe Castle + Tyneham day trip".

### L5. Reframe flowers-barrow title
"A Timeless Beacon of Dorset's History" → natural query ("Flower's Barrow | Iron Age Hillfort above Worbarrow Bay").

### L6. Generic alt text polish (~12)
Opening-times hero "Worbarrow Bay", "Tyneham today", "Tyneham House", label-only cottage alts. Also fix "Tynehham" typo in tyneham-photos alt.

### L7. Schema polish
Standalone Organization on homepage; ContactPage on /contact; VideoObject/Movie on tyneham-remembered; per-building `geo`; WebSite SearchAction; ImageObject copyrights on /tyneham-photos; add trailing slash to all schema `url` values.

### L8. Real publish dates
5 pages hardcode `datePublished: 2024-01-01` (after-the-evacuation, ghost-village, the-bond-family, the-campaign-to-return, the-church-door-note).

### L9. Misc image fixes
Fix `TynehamHouseSouthEastView1943.jpg` (is actually a PNG, 565KB); real jpg fallbacks for lulworth-ranges-coast + wildflowers `<picture>` blocks; width/height on 5 ghost-village fallbacks; `decoding="async"` on 128 picture fallbacks.

### L10. GPX/KML downloads + route-trace maps on walk pages
Embedded map is currently a postcode-area satellite view, not the route.

### L11. Link building (see audit §8)
National Trust / jurassiccoast.org / visit-dorset.com / lulworth.com / Dorset History Centre; Wikipedia citations (Worbarrow Bay, Lulworth Ranges, Flower's Barrow); reclaim swanage.co.uk / worldghosttowns.com / BBC Dorset; walking sites (iFootpath, AllTrails, Dorset Ramblers); local press.

### L12. Annual freshness (Jan 2027)
Refresh "2026" in opening-times title/meta, lulworth-range-walks H1, kimmeridge-bay charges; remove the expired Dec 2025–Jan 2026 Christmas text from opening-times.

---

## Completed Items (from previous audits)

- [x] C1: Population 225→252 sitewide
- [x] C2: Parking cost £2 vs £4 resolved
- [x] C3: Underscore files deleted
- [x] H2: Opening-times noscript fallback added
- [x] H3: Sidebars made identical sitewide
- [x] H5: Location page postcode fixed (BH20 5QH)
- [x] H7: Bond tenure 400→260 on corfe-castle.html
- [x] H10: ghost-village.html Article schema author added
- [x] H11: OAI-SearchBot added to robots.txt
- [x] M2: Kimmeridge Bay postcode fixed (BH20 5PF)
- [x] M3: Lulworth Cove isAccessibleForFree fixed
- [x] M7: Author bylines added to 18/27 content pages
- [x] M9: FAQ schema vs visible text aligned
- [x] privacy page added to sitemap + JSON-LD added
- [x] Favicon added sitewide
- [x] Orphaned images cleared (271 → 0)
- [x] `<picture>` webp/jpg pairing completed (all jpgs paired)
- [x] FAQPage schema on opening-times, history-of-tyneham, church-door-note, visiting-tyneham
- [x] llms.txt factual errors fixed (residents, postcode, Tyneham Remembered)
- [x] Quotation schema added to church-door-note
