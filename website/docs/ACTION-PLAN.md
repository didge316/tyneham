# Tyneham Village — SEO Action Plan

**Based on full audit of tynehamvillage.org — 3 June 2026**  
**SEO Health Score: 70/100 → Target: 82/100 after Critical + High fixes**  
**Previous audit:** 21 May 2026 (45/100)

See `AUDIT-2026-06-03.md` for full detail.

---

## CRITICAL — Fix Immediately

### C1. Fix population figure: 225 → 252 (sitewide)
The number of evacuated residents appears as 225 on multiple pages but the correct figure is **252** (confirmed in about.html and primary sources). Fix all instances across:
- `index.html` (lines 299, 360, meta description, schema)
- `history-of-tyneham.html` (meta description, og:description, schema description, body line 266)
- `after-the-evacuation.html` (meta description, og:description, schema)
- `ghost-village.html` (og:description, twitter:description, schema, body ×3)
- `llms.txt` (line 9)

Note: "around 250 people" on `history-of-tyneham.html` line 229 refers to the **pre-war village population** — this is a separate figure and is correct. Do not change it.

### C2. Verify and fix parking cost contradiction
`visiting-tyneham.html` says **£2**. `opening-times.html` FAQ schema says **£4**. One is wrong. Google surfaces the schema figure in rich results. Verify the real figure and align both pages.

### C3. Fix underscore legacy pages: canonicals point to wrong URLs
Six underscore HTML files (`history_of_tyneham.html` etc.) have `robots: index, follow` and self-canonicalise to underscore URLs instead of the canonical hyphen URLs. Fix all six canonical href values to point to their hyphen equivalents.

---

## HIGH — Fix Within 1 Week

### H1. Fix llms.txt factual errors
- Line 9: "225 residents" → "252 residents"
- Key Facts postcode: "BH20 5QS" → "BH20 5QH"
- Add Tyneham Remembered to Key Pages list
- Full corrected version in `AUDIT-2026-06-03.md` Appendix A

### H2. Add noscript fallback to opening-times "open today" widget
Googlebot crawls before JS renders. Add above the widget:
```html
<noscript><p>Use the calendar below to check whether Tyneham is open on your planned visit date. The gate opens at 9am on non-firing days.</p></noscript>
```

### H3. Synchronise all page sidebars sitewide
The homepage sidebar has 15 links; opening-times page has 18. `visiting-tyneham.html` (highest visitor intent page) is missing from the homepage sidebar. Use `bulk_seo_fixes.py` to make all sidebars identical using the opening-times.html sidebar as template.

### H4. Fix tyneham-village-location.html postcode contradiction
Body (line 229–230) says "Tyneham does not have a postcode". Schema (line 49) says BH20 5QS. Every other page uses BH20 5QH. Replace "no postcode" statement with: "Use postcode **BH20 5QH** for sat-nav." Update schema postalCode to BH20 5QH.

### H5. Fix Worbarrow Bay coastguard station date contradiction
Line 295: "station closed in **1911**" vs line 348: "demolished in **1912**". Check primary source and standardise.

### H6. Fix Bond family tenure error on corfe-castle.html
Line 220: "roughly **four hundred years**" — incorrect. Should be "nearly 260 years" (acquired c.1683, lost 1943). History page correctly says "nearly 250 years".

### H7. Fix church door note attribution conflict
`the-church-door-note.html` FAQPage schema has two contradictory answers:
- Schema line 75: signed "W.H. BOND, on behalf of the families of Tyneham village"
- Schema line 83: signed "on behalf of the women and children of Tyneham village"
- Body text: "signed simply...by *the women and children of Tyneham*"
Establish one consistent attribution and apply it to both FAQ answers and body text.

### H8. Add OAI-SearchBot to robots.txt
OpenAI's search-mode bot is not listed. Add:
```
User-agent: OAI-SearchBot
Allow: /
```

### H9. Add author property to ghost-village.html Article schema
All other Article-type pages have the author property. `ghost-village.html` is missing it.

### H10. Expand about.html to 500+ words
Current author bio is ~220 words. No author photo. No external validation. The About page is the primary E-E-A-T trust document for the entire site.

---

## MEDIUM — Fix Within 1 Month

### M1. Fix Kimmeridge Bay postcode contradiction
Line 191: **BH20 5PE** vs line 236: **BH20 5PF** for the same car park. Verify correct postcode and remove the other.

### M2. Fix Lulworth Cove schema: isAccessibleForFree should be true
Line 52: `"isAccessibleForFree": false` — the cove itself is free to access. Change to `true`.

### M3. Fix tyneham-church.html title tag
`<title>Tyneham Church - St Marys Church in Tyneham Village</title>` — missing apostrophe in "St Mary's". Also appears in og:title and twitter:title.

### M4. Add forward links in history-of-tyneham.html
Article body does not link to `after-the-evacuation.html` or `the-campaign-to-return.html`. Add 2 contextual links in the final "Tyneham Today" section.

### M5. Add in-article links to the-church-door-note.html
Article has zero in-body outbound links. Add links to:
- `tyneham-church.html` (where the note was displayed)
- `the-bond-family.html` (W.H. Bond attribution)
- `history-of-tyneham.html` (context)

### M6. Add author bylines to nearby-attraction pages
`lulworth-cove.html`, `durdle-door.html`, `kimmeridge-bay.html`, `worbarrow-bay.html`, `lulworth-range-walks.html` have no visible "By James Langton" byline.

### M7. Fix FAQ schema vs visible text on index.html
FAQPage schema for "Are Tyneham Ranges Open Today?" gives "GOV.UK website or call 01929 404714". Visible accordion answer lacks the URL and phone number. Align them.

### M8. Fix duplicate sentence in lulworth-range-walks.html
"More than half the original earthworks have been lost to coastal erosion" appears twice in the Flower's Barrow section. Remove one.

### M9. Add Content-Security-Policy header to _headers
Currently missing from the global `/*` rule. A permissive CSP covering Bootstrap CDN and Google AdSense would improve security posture.

---

## LOW — Backlog

### L1. Fix generic anchor text on tyneham-village-location.html
"click on this link" → "open Tyneham in Google Maps"

### L2. Add Quotation schema to church door note blockquote
Mark up the verbatim note text with `@type: Quotation`. Strong AI citability signal for the site's most citable primary source.

### L3. Add sameAs to about.html Person schema
Link to any verifiable external profile (LinkedIn, Wikidata, published article) to help AI systems validate the author entity.

### L4. Minify CSS
`css/styles.css` is ~233KB. Enable Cloudflare Auto Minify (Dashboard → Speed → Optimization) — no build step needed.

### L5. Expand lulworth-cove.html (~750 words)
Competing against National Trust for "Lulworth Cove" queries. Add 400–500 words on the Lulworth Crumple geology, the cove's formation, or historical context.

### L6. Expand tyneham-church.html (~700 words)
Key landmark page. Missing: tower dimensions, bells/organ fate, WWII damage chronology.

### L7. Fix Worbarrow Bay OG image filename typo
File is correctly named `worrbarrow-bay-today.webp` (matching the URL), so it loads. But the double 'r' is a typo in the filename. Low-priority hygiene fix.

---

## When Publishing Draft Pages

The following draft pages should have these actions done before publishing:

| Page | Action before publish |
|------|-----------------------|
| wildlife-at-tyneham.html | Add Article schema, add author byline, change robots to `index, follow`, add to navbar and sidebar |
| tyneham-in-wartime.html | Add to History nav dropdown and sidebar, add contextual links from ghost-village.html and history-of-tyneham.html, add to sitemap.xml |
| corfe-castle-walk.html | Add to walks section in navbar/sidebar, link from corfe-castle.html, add to sitemap.xml |
| kimmeridge-tyneham-walk.html | Add to walks section, link from kimmeridge-bay.html, add to sitemap.xml |

---

## Completed Items (from May 2026 audit)

- [x] C3: Kimmeridge Bay title fixed
- [x] C5: Schema added to index.html (27 references)
- [x] C6: Schema added to opening-times.html (20 references)
- [x] C7: llms.txt created
- [x] H2: Security headers added to _headers
- [x] H3: About page created
- [x] H6: Heading hierarchy fixed on history and bond family pages
- [x] H9: Inconsistent alt text fixed ("Advertisement" alt removed)
- [x] H10: Sidebar active highlight bug fixed
- [x] H11: Navbar brand href="/" fixed
- [x] H12: OG/Twitter image URLs made absolute
- [x] M7: privacy.html set to noindex
- [x] New pages: ghost-village, visiting-tyneham, tyneham-photos, lulworth-range-walks, gad-cliff
