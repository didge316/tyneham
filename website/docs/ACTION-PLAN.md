# Tyneham Village — SEO Action Plan

**Based on full audit of tynehamvillage.org — 30 June 2026**
**SEO Health Score: 83/100 → Target: 90+/100**
**Previous audit:** 3 June 2026 (70/100)
**Previous baseline:** 21 May 2026 (45/100)

See `AUDIT-2026-06-30.md` for full detail.

---

## HIGH — Fix Within 1 Week

### H1. Fix privacy.html barkingdolphin.com reference (NEW)
`privacy.html` line 153: "Where necessary, barkingdolphin.com uses cookies..." — template leftover. Change to tynehamvillage.org.

### H2. Fix church door note attribution conflict
FAQ answer 2 still says "on behalf of the women and children" while Quotation schema and FAQ answer 1 say "W.H. Bond on behalf of the families". Body blockquote footer says "The Women and Children of Tyneham". Pick one consistent attribution and apply everywhere.

### H3. Fix llms.txt Bond family tenure
Line 25: "The squires of Tyneham for **over 400 years**" → "nearly 260 years". Current text causes AI to contradict the bond-family page.

### H4. Expand about.html to 500+ words
Currently ~400 words of author bio. Add author photo, credentials, external validation. Target: 500+ words.

### H5. Add sameAs to Person schema on about.html
Critical for AI entity trust. Add LinkedIn, Wikipedia, or Wikidata link.

---

## MEDIUM — Fix Within 1 Month

### M1. Add Content-Security-Policy to _headers
Permissive CSP covering Bootstrap CDN and Google AdSense.

### M2. Enable Cloudflare Auto Minify for CSS
240KB → ~180KB. Dashboard → Speed → Optimization. Zero effort.

### M3. Add ContactPoint schema to contact.html
Currently only has BreadcrumbList. Add ContactPoint or Organization schema.

### M4. Fix tyneham-church.html title separator
"Tyneham Church - St Mary's..." → "Tyneham Church | St Mary's..." (pipe for consistency)

### M5. Re-compress oversized images
38 files >500KB. Convert wildflowers.png (3.4MB) to WebP. Re-compress 18 oversized WebPs.

### M6. Move Google Fonts from @import to <link>
Add `preconnect` for fonts.googleapis.com + `font-display: swap`.

### M7. Wrap direct .webp src in <picture> elements
~20 images use `<img src="image.webp">` without WebP fallback for older browsers.

### M8. Fix contact.html meta description
Currently: "Get in touch with James Langton for questions about..." — could be stronger with action prompt.

---

## LOW — Backlog

### L1. Publish draft pages
- tyneham-in-wartime.html (ready, needs nav links from ghost-village + history)
- corfe-castle-walk.html (ready)
- kimmeridge-tyneham-walk.html (ready)

### L2. Add srcset for responsive images
Especially the 3072px images on gallery pages.

### L3. Fix worbarrow-bay-today.webp filename typo
Double 'r' in filename.

### L4. Expand thin pages
- lulworth-cove.html (~750 words)
- tyneham-church.html (~700 words)

### L5. Harmonise Bond tenure: 250 vs 260 years
bond-family page: "nearly 250 years", corfe-castle: "nearly 260 years".

---

## Completed Items (from June 2026 audit)

- [x] C1: Population 225→252 sitewide
- [x] C2: Parking cost £2 vs £4 resolved
- [x] C3: Underscore files deleted
- [x] H1: llms.txt factual errors fixed (residents, postcode, Tyneham Remembered)
- [x] H2: Opening-times noscript fallback added
- [x] H3: Sidebars made identical sitewide
- [x] H5: Location page postcode fixed (BH20 5QH)
- [x] H6: Worbarrow 1911/1912 dates harmonised
- [x] H7: Bond tenure 400→260 on corfe-castle.html
- [x] H10: ghost-village.html Article schema author added
- [x] H11: OAI-SearchBot added to robots.txt
- [x] M2: Kimmeridge Bay postcode fixed (BH20 5PF)
- [x] M3: Lulworth Cove isAccessibleForFree fixed
- [x] M4: tyneham-church.html apostrophe fixed
- [x] M5: history forward links added
- [x] M6: church-door-note in-article links added
- [x] M7: Author bylines added to all pages
- [x] M8: Duplicate sentence removed
- [x] M9: FAQ schema vs visible text aligned
- [x] L2: Generic anchor text fixed
- [x] L3: Quotation schema added
- [x] L4: worrbarrow typo cleaned
