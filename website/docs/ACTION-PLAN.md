# Tyneham Village — SEO Action Plan

**Source audit:** tynehamvillage.org — 06 August 2026 (78/100). Plan verified against the live code on 22 September 2026; completed items removed and the rest re-checked.

---

## CRITICAL — Fix Within 1 Week

### C1. Homepage ↔ ghost-village cannibalization (previously M5) ✅ Done 22 Sep 2026
Homepage meta/OG/Twitter refocused on visitor-guide intent (single "ghost village" mention); featured callout added linking to /ghost-village/ with descriptive anchor.

### C2. Static "Is it open today?" server-rendered line
The calendar widget answer is JS-rendered. The noscript fallback exists but is a hardcoded August 2026 date that will go stale. Consider a server-side current/next-open line (or an explicitly dated table) beside the widget so no-JS crawlers/AIs always see accurate dates.

---

## HIGH — Fix Within 2 Weeks

### H1. Map-of-tyneham expand (113 → 300–400 words)
Per-building annotations with links (church, school, post office, rectory, house), distances and walking times (car park → village → Worbarrow Bay).

### H2. Real publish dates (5 pages hardcode 2024-01-01)
after-the-evacuation, ghost-village, the-bond-family, the-campaign-to-return, the-church-door-note all set `datePublished: 2024-01-01` in Article schema. Replace with actual publication dates.

### H3. Flower's Barrow title
`Flowers Barrow: A Timeless Beacon of Dorset's History` → natural query ("Flower's Barrow | Iron Age Hillfort above Worbarrow Bay").

### H4. Homepage church-door-note text
Image-only. Add the note's text beside it (most-cited sentence in Tyneham's story — AI citability).

### H5. llms.txt
Missing `/privacy/` (only page absent). "Last Updated 2026-08-06" is stale — bump to today.

### H6. Expand the-post-office (~573 words)
Rich story (1880–1942 shopkeeper timeline, K1 kiosk, *Comrades* film) deserves ~800–900 words.

### H7. Alt text polish
- opening-times hero `alt="Worbarrow Bay"` (generic, on the highest-intent page)
- history-of-tyneham: `alt="Tyneham House"` and `alt="Tyneham today"` (label-only)
- index.html:410 `alt="...Tynehham village"` typo (missing "h")

---

## MEDIUM — Fix Within 1 Month

### M1. Reframe corfe-castle as day-trip/itinerary page
Schema is now TouristAttraction (good); frame the content as "Corfe Castle + Tyneham day trip" rather than competing for the navigational SERP.

### M2. Worbarrow-bay planner facts first
History sections still lead; put parking / 1-mile walk / range-open access / dogs / swimming rules / no facilities before the history (the differentiator).

### M3. TBT + LCP (measure after the H3-CLS work)
TBT 324–533ms (AdSense/consent JS on main thread). Ad script already loads on `window.load` (index.html:202). Trim render-blocking Bootstrap + Lora, remove 27 decorative Gravatar avatars. Re-measure with Lighthouse.

### M4. Schema polish
Standalone Organization on homepage; ContactPage on /contact; VideoObject/Movie on tyneham-remembered; per-building `geo`; WebSite SearchAction; ImageObject copyrights on /tyneham-photos; trailing slash on all schema `url` values.

---

## LOW — Backlog

### L1. GPX/KML downloads + route-trace maps on walk pages
Embedded map is currently a postcode-area satellite view, not the route.

### L2. Link building
National Trust / jurassiccoast.org / visit-dorset.com / lulworth.com / Dorset History Centre; Wikipedia citations (Worbarrow Bay, Lulworth Ranges, Flower's Barrow); reclaim swanage.co.uk / worldghosttowns.com / BBC Dorset; walking sites (iFootpath, AllTrails, Dorset Ramblers); local press.

### L3. Annual freshness (Jan 2027)
Refresh "2026" in opening-times title/meta, lulworth-range-walks H1, kimmeridge-bay charges. (Christmas text on opening-times now references Dec 2026 — not expired.)

### L4. Misc image files
`assets/TynehamHouseSouthEastView1943.jpg` is actually a PNG (565KB) despite the extension.

---

## Completed Since the 06-Aug Audit (verified 22 Sep 2026)

- [x] C1: homepage ↔ /ghost-village/ cannibalization resolved (homepage meta refocused on visitor-guide intent; featured callout added linking to the subpage)

- [x] C1: relative `js/scripts.js` path → absolute `/js/scripts.js?v=11` sitewide (no 404s)
- [x] C2: `assets/logo-publisher.png` now exists (Article rich results unblocked)
- [x] C3: attraction pages `sameAs` → their own Wikipedia/Wikidata entities (worbarrow-bay, durdle-door, lulworth-cove, kimmeridge-bay, gad-cliff); walk pages dropped `sameAs`; the three Tyneham pages (location/visiting/opening-times) correctly point to Tyneham
- [x] C4: tyneham-in-wartime gained datePublished/dateModified + publisher; ghost-village gained publisher block
- [x] C5: robots.txt AI-crawler rules clean (no managed disallow conflict, Claude-User present, no bogus `anthropic-ai`)
- [x] H1: opening-times byline consolidated to a single "Updated July 2026"; calendar footer reconciled
- [x] H2: opening-hours schema now models gate 09:00–dusk + exhibitions 10:00–16:00 with closures noted; text matches
- [x] H5: church-door-note attribution unified to "W.H. Bond, on behalf of the families of Tyneham village" (body, schema, wartime page)
- [x] H6: bylines + Person schema added to all 9 previously-missing pages
- [x] H7: durdle-door FAQPage schema added; `isAccessibleForFree` now true
- [x] H8: scrollbar-gutter CLS mitigation in CSS (re-verify revenue after)
- [x] M2: no images >1MB remain (previously 7 files up to 1.9MB)
- [x] M3: Bond tenure standardised to "nearly 260 years" (was mixing 250/260)
- [x] M4: camp-at-tyneham, corfe-castle-walk, map-of-tyneham, wildlife-at-tyneham now have 4 in-content links each (was under-linked)
- [x] M7: IndexNow key removed from robots.txt
- [x] M8: HowTo schema removed from all 3 walk pages
- [x] M9: contact page shows `admin@tynehamvillage.org`; privacy policy names operator + email
- [x] M10: /about/ Person `sameAs` removed (was pointing to the village's Wikipedia)
- [x] L3: curly-quote class corruption in history-of-tyneham fixed (4 paragraphs)