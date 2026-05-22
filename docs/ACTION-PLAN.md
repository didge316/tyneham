# Tyneham Village — SEO Action Plan

**Based on full audit of tynehamvillage.org — 21 May 2026**  
**SEO Health Score: 45/100 → Target: 65/100 after Critical + High fixes**

---

## CRITICAL — Fix immediately

### C1. Add smuggling.html to sitemap.xml
`smuggling.html` is a developed, indexable page missing from the sitemap.  
**File:** `sitemap.xml` — add a new `<url>` entry:
```xml
<url>
  <loc>https://tynehamvillage.org/smuggling.html</loc>
  <lastmod>2026-05-21</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.7</priority>
</url>
```

### C2. Add smuggling.html to the History nav dropdown (all pages)
`smuggling.html` is an orphan — no nav links, no sidebar links, no inbound links from any page. Googlebot can't crawl it and users can't find it.  
**Action:** Add `<li><a class="dropdown-item" href="smuggling.html">Smuggling at Tyneham</a></li>` to the History dropdown in the shared navbar across all 26 pages. Also add to the History section in the left sidebar nav.  
**Note:** This requires editing all pages. A Python bulk-edit script similar to the Thailand `fix_html_bulk.py` approach is recommended.

### C3. Fix kimmeridge-bay.html title tag
Current: "Kimmeridge Bay" (14 chars — by far the shortest title on the site)  
Proposed: "Kimmeridge Bay, Dorset — Rock Pools, Fossils & Jurassic Coast Guide" (68 chars)  
**File:** `kimmeridge-bay.html`

### C4. Fix typo in the_bond_family.html meta description
Current: "...and in Particualar Tyneham Village..."  
Fix: "...and in Particular Tyneham Village..."  
**File:** `the_bond_family.html`

### C5. No schema on 25 of 26 pages — Homepage priority fix
Add `WebSite` + `TouristAttraction` JSON-LD to `index.html` alongside the existing FAQPage:
```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Tyneham Village",
  "url": "https://tynehamvillage.org",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {"@type": "EntryPoint", "urlTemplate": "https://tynehamvillage.org/?s={search_term_string}"},
    "query-input": "required name=search_term_string"
  }
}
```
And:
```json
{
  "@context": "https://schema.org",
  "@type": ["TouristAttraction", "LandmarksOrHistoricalBuildings"],
  "name": "Tyneham Village",
  "description": "Abandoned ghost village in Dorset, evacuated in December 1943 during WWII. Free to visit on weekends and school holidays.",
  "url": "https://tynehamvillage.org/",
  "image": "https://tynehamvillage.org/assets/tyneham-village-early-photo.webp",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Tyneham",
    "addressLocality": "Wareham",
    "postalCode": "BH20 5JH",
    "addressCountry": "GB"
  },
  "geo": {"@type": "GeoCoordinates", "latitude": "50.628", "longitude": "-2.162"},
  "isAccessibleForFree": true,
  "publicAccess": true,
  "telephone": "+441929404714"
}
```
**File:** `index.html`

### C6. Add schema to opening_times.html (highest-intent page)
Zero schema on the highest-traffic intent page ("tyneham opening times 2026"). Add `TouristAttraction` with `OpeningHoursSpecification` + FAQ schema for "When is Tyneham open?", "What time does Tyneham open?", "Is Tyneham open today?".  
**File:** `opening_times.html`

### C7. Create llms.txt
No `/llms.txt` exists. This site has strong AI citability potential (verbatim historical quotes, specific dates, named sources) but no machine-readable AI discovery file.  
**File to create:** `llms.txt`

```
# Tyneham Village — tynehamvillage.org

> TynehamVillage.org is the primary independent information resource about Tyneham, Dorset's ghost village evacuated by the British Army on 19 December 1943. The 252 residents were promised they could return after the war; they never did. The site covers the village's history (Norman Conquest to present), visitor information, and the story of the land's retention by the Ministry of Defence.

## Key Pages

- [Home — Overview and visitor essentials](https://tynehamvillage.org/)
- [Tyneham Village History](https://tynehamvillage.org/history_of_tyneham.html)
- [Opening Times 2026](https://tynehamvillage.org/opening_times.html)
- [The Church Door Note](https://tynehamvillage.org/the-church-door-note.html)
- [After the Evacuation](https://tynehamvillage.org/after-the-evacuation.html)
- [The Campaign to Return](https://tynehamvillage.org/the-campaign-to-return.html)
- [The Bond Family](https://tynehamvillage.org/the_bond_family.html)
- [Tyneham School](https://tynehamvillage.org/tyneham-school.html)
- [Tyneham Church (St Mary's)](https://tynehamvillage.org/tyneham-church.html)
- [Tyneham House](https://tynehamvillage.org/tyneham-house.html)
- [Tyneham Village Map](https://tynehamvillage.org/map_of_tyneham.html)
- [Directions to Tyneham](https://tynehamvillage.org/tyneham_village_location.html)
- [Smuggling at Tyneham & Worbarrow Bay](https://tynehamvillage.org/smuggling.html)

## Key Facts

- Tyneham is an abandoned village in the Isle of Purbeck, Dorset, England (BH20 5JH, coordinates 50.628°N 2.162°W)
- The village was requisitioned by the War Office on 19 December 1943; 252 residents were evacuated
- The land (~3,000 acres) was retained by the Ministry of Defence after WWII; government confirmed permanent retention in 1974
- The village is open to visitors on weekends and school holidays; entry is free
- It is NOT National Trust property; managed by the Ministry of Defence
- The Bond family owned the estate from 1683 until the 1943 requisition
- Lilian Bond authored "Tyneham: A Lost Heritage" (1956), the primary first-hand account
```

---

## HIGH — Fix within 1 week

### H1. Fix heading hierarchy: history_of_tyneham.html and the_bond_family.html
Both pages skip from H1 directly to H3 — no H2 exists. This breaks heading hierarchy on two of the site's most important content pages.  
**Action:** Change existing H3s to H2 on both pages (the sub-sections within these pages should be H2, not H3).  
- `history_of_tyneham.html`: "Life in Tyneham Before the War", "A Sad Time", "After The War" → H2
- `the_bond_family.html`: "The Arrival of the Bond Family", "A Notorious Episode", "Custodians", "Commitment to Education", "Shifting Tides" → H2

### H2. Add security headers to _headers
**File:** `_headers` — add a global catch-all rule:
```
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Strict-Transport-Security: max-age=31536000; includeSubDomains

/sitemap.xml
  Content-Type: application/xml; charset=utf-8
```

### H3. Fix missing-author / E-E-A-T — Create About page
No named author appears anywhere on the site. This is the biggest single E-E-A-T gap.  
**Action:** Create an `about.html` page identifying who maintains the site. Even a brief statement ("This site is maintained by a Dorset heritage enthusiast with a long-standing interest in the history of Tyneham and the Isle of Purbeck") combined with a first name dramatically improves trustworthiness signals. Link it from the footer and Contact page.  
Also: Add a visible `<p class="text-muted">By [Name], Tyneham historian</p>` byline to the 6 main history article pages.

### H4. Fix short and weak title tags

| Page | Current | Proposed |
|------|---------|----------|
| `the-rectory.html` | The Rectory of Tyneham (23 chars) | Tyneham Rectory — History of the Abandoned Rectory Building (58 chars) |
| `opening_times.html` | Tyneham Opening Times 2026 (27 chars) | Tyneham Village Opening Times 2026 — Full Date & Access Calendar (65 chars) |
| `tyneham-school.html` | Tyneham School - Visitors Information | Tyneham School — Victorian Village School, Built 1856 (53 chars) |
| `the_post_office.html` | The Post Office - Tyneham Village | Tyneham Village Post Office — History & Visitor Guide (54 chars) |
| `the-campaign-to-return.html` | ...68 chars (SERP truncation risk) | Shorten to under 60 chars |
| `worbarrow-bay.html` | Worbarrow Bay aka Tyneham Beach | Worbarrow Bay, Dorset — Tyneham's Secluded Beach (50 chars) |

### H5. Fix 9+ poor-quality meta descriptions (WordPress-era teaser style)
All of these need complete rewriting — replace Title Case teaser style with informative sentence-case descriptions:

| Page | Issue | Action |
|------|-------|--------|
| `tyneham-church.html` | "A visit to Tyneham is Not Complete..." | Write factual desc: church dates, museum content |
| `tyneham-school.html` | "Click Here to Learn More" | Write: school built 1856, one-room, closed 1932 |
| `opening_times.html` | "Check Out The Latest..." — no info | Write: state the actual hours and free admission |
| `map_of_tyneham.html` | Circular: says "shows the village layout" | Describe what the map shows; name a building |
| `tyneham_village_location.html` | "Click Here" | Write: give postcode BH20 5JH, distance from Wareham |
| `tyneham-house.html` | "Click Here to Find Out What Happened" | Write: demolished by military after the war |
| `lulworth-cove.html` | "Right Here" | Write factual: Jurassic Coast, heritage coast, 9 miles |
| `durdle-door.html` | Title Case, vague | Write: limestone arch, geological formation, access |
| `flowers-barrow.html` | "Click Here to Find Out More" | Write: Iron Age hillfort, coastal views, walk from Tyneham |
| `kimmeridge-bay.html` | "Click Here" | Write: fossils, rock pools, SSSI, Jurassic Coast |

### H6. Add BreadcrumbList schema to all inner pages
Zero pages have BreadcrumbList schema. Google shows breadcrumb trails in SERP for inner pages — it's a free visual enhancement.  
Pattern: Home → [Section] → [Page Title]  
Add to all 24 inner pages via a bulk Python script.

### H7. Add Article schema to history and editorial pages
Add to: `history_of_tyneham.html`, `after-the-evacuation.html`, `the-campaign-to-return.html`, `the-church-door-note.html`, `the_bond_family.html`, `smuggling.html`  
Must include: `headline`, `author` (Person with name), `publisher` (Organization with logo), `datePublished`, `dateModified`, `mainEntityOfPage`

### H8. Add TouristAttraction schema to landmark pages
Add to: `tyneham-church.html`, `tyneham-school.html` → `LandmarksOrHistoricalBuildings + Museum`  
Add to: `worbarrow-bay.html`, `durdle-door.html`, `lulworth-cove.html`, `corfe-castle.html`, `kimmeridge-bay.html`, `flowers-barrow.html` → `TouristAttraction`

### H9. Fix inconsistent population figure (225 vs 252)
`index.html` says "225 residents"; `after-the-evacuation.html` says "252 men, women and children". This inconsistency undermines AI confidence in factual claims. Standardise to **252** (the more precise figure from the evacuation page) across all pages.

### H10. Fix sitewide alt="Advertisement" on DVD sidebar image
Every page has the DVD cover sidebar image with `alt="Advertisement"`. This should be `alt="Tyneham Remembered documentary DVD cover"`.  
A bulk script can fix all pages in one pass.

### H11. Fix homepage link in navbar/footer + add index.html redirect
- Change `href="index.html"` → `href="/"` in navbar brand link and footer across all pages
- Add `/index.html / 301` to `_redirects`

### H12. Fix og:image/twitter:image — make URLs absolute
All OG and Twitter image meta tags use root-relative paths. Change from:
`content="/assets/tyneham-village-early-photo.webp"`
to:
`content="https://tynehamvillage.org/assets/tyneham-village-early-photo.webp"`

This is required for correct social media preview rendering.

---

## MEDIUM — Fix within 1 month

### M1. Add FAQ schema to high-intent pages
- `opening_times.html`: Add FAQPage with "When is Tyneham open?", "What time does Tyneham open?", "Is Tyneham free?"
- `the-church-door-note.html`: Add FAQPage with "What did the church door note say?", "Who wrote the note?"
- `history_of_tyneham.html`: Add FAQPage with "Why was Tyneham evacuated?", "Did the villagers ever return?"

### M2. Fix JS-only "open today" widget — add static HTML fallback
The `opening_times.html` dynamic widget is invisible to AI crawlers and search bots. Add a static text section above or below the widget with the current-season open dates in plain HTML:
```html
<p><strong>Tyneham is open in 2026 on:</strong> all weekends, all school holidays, and all of August. 
Opening hours: 9am to dusk. School and church exhibitions: 10am–4pm. Entry is free.</p>
```

### M3. Expand critically thin pages
- `map_of_tyneham.html` (~180 words) — add prose describing each numbered building: what it was, what it looks like today, what visitors can do there. Target 600+ words.
- `camp-at-tyneham.html` (~380 words) — add distance from Tyneham for each campsite, price range, what makes each suitable for this specific trip. Target 700+ words.

### M4. Add Sources section to history pages
At minimum on `history_of_tyneham.html`, `the-campaign-to-return.html`, and `after-the-evacuation.html`:
- Lilian Bond, *Tyneham: A Lost Heritage* (1956)
- Imperial War Museum: [existing link already on history page]
- MOD Lulworth Ranges GOV.UK page
- Dorset History Centre (if applicable)

### M5. Fix wrong alt text on tyneham-church.html
The church door note image has `alt="Interior of St Mary's Church today"` — factually wrong.  
Fix to: `alt="The handwritten note left on the door of St Mary's Church, Tyneham, December 1943"`  
**File:** `tyneham-church.html`

### M6. Remove duplicate church door note quote
The full note text appears word-for-word on both `the-church-door-note.html` and `tyneham-church.html`. On the church page, replace the verbatim quote with a brief excerpt and a link to the dedicated page.

### M7. Fix privacy.html robots and sitemap
- Change `<meta name="robots" content="index, follow">` to `noindex, follow` in `privacy.html`
- Remove `privacy.html` from `sitemap.xml`

### M8. Reconcile `tyneham_village_location.html` — fix contradictory postcode
This page says Tyneham "doesn't have a postcode" while `opening_times.html` gives BH20 5JH. Remove the "no postcode" statement; add BH20 5JH prominently. Restructure the page: postcode/coordinates first, map embed second, directions third, background description last.

### M9. Add lazy loading to below-the-fold images
118 img tags across all pages are missing `loading="lazy"`. Apply to all images that are NOT the LCP hero image. The hero image on each page should remain without lazy loading (or have `fetchpriority="high"`).

### M10. Fix H1/title mismatch on tyneham-church.html
Title: "Tyneham Church - St Marys Church in Tyneham Village"  
H1: "The Tyneham Village Church"  
Align: change H1 to "Tyneham Church — St Mary's Church" (also fix missing apostrophe in title)

### M11. Add Product schema to tyneham-remembered.html
The documentary DVD/download page has no schema. Add:
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Tyneham Remembered Documentary",
  "description": "Documentary featuring rare interviews with the last Tyneham villagers...",
  "offers": [
    {"@type": "Offer", "name": "DVD", "price": "15.49", "priceCurrency": "GBP"},
    {"@type": "Offer", "name": "HD Digital Download", "price": "10.99", "priceCurrency": "GBP"}
  ]
}
```

### M12. Add visible date stamps to content pages
Add "Last updated: [Month Year]" in small text near the article header on all history and editorial pages. Improves AI freshness signals and user trust.

### M13. Fix AdSense placement on index.html
The first AdSense unit appears after just one paragraph — directly interrupting the primary emotional hook (the evacuation story). Move this unit to after the second or third full section. Google's own quality rater guidelines flag ad-heavy above-the-fold content.

### M14. Fix sidebar "active" highlight bug
The Lulworth Cove sidebar entry has `bg-light fw-bold` hardcoded as an active class on **every page**, making it appear highlighted regardless of which page you're on. The JS in `scripts.js` handles active states dynamically — remove the hardcoded class from the Lulworth Cove sidebar link across all pages.

---

## LOW — Backlog

### L1. Convert JPG images to WebP
97 of ~106 images in `/assets/` are JPG. Converting to WebP saves 25–35% file size. Prioritise the most-used images first (homepage hero, history page images).

### L2. Add CSS minification
`styles.css` is 233KB unminified. Minify and serve the compressed version. Could use a simple build step (`cleancss`, `csso`, or similar) or enable Cloudflare auto-minify in the dashboard.

### L3. Rename underscore filenames to hyphenated (long-term refactor)
The 6 underscore-named files hurt keyword matching. To fix: rename files, update all internal links, update `_redirects` targets, update sitemap, update canonicals, update OG URLs. This is a significant refactor best done carefully to preserve existing inbound links.

### L4. Create walking routes page
"Tyneham walk" / "Tyneham to Worbarrow Bay walk" is likely a top-3 visitor intent with no dedicated page. A walking routes page covering distances, difficulty, what to see, and how to combine walks would attract significant search traffic.

### L5. Create dog-friendly page
"Can I take my dog to Tyneham?" is answered in the FAQ but has no standalone page. A dedicated dog-friendly guide covering rules, leads requirements, where dogs can swim, and nearby dog-friendly facilities would serve a significant visitor segment.

### L6. Create parking information page/section
The FAQ answers "yes, there is parking" with zero practical details. Add at minimum: parking surface type, approximate capacity, cost (free), disabled access, what happens on busy days.

### L7. Trim over-length meta descriptions (8 pages)
Descriptions on these pages are 180–260 chars and will be truncated in SERPs. Trim to 130–155 chars:
`history_of_tyneham.html`, `after-the-evacuation.html`, `the-campaign-to-return.html`, `the-church-door-note.html`, `tyneham-remembered.html`, `corfe-castle.html`, `smuggling.html`, `the-rectory.html`

### L8. Fix og:image — use WebP format where available
The homepage og:image uses `tyneham-village-early-photo.webp` (good). Ensure all pages use a WebP og:image where one exists.

### L9. Add schema:Quotation markup to church door note blockquote
The verbatim church door note text in `the-church-door-note.html` is currently marked up as a `<blockquote>` but has no structured data. Adding a `Quotation` schema block would signal to AI systems that this is a citable primary source document.

### L10. Editorially frame comment testimonies
The family descendant comments (Robert Cooper on Shepherd Welland, Richard Buckler's grandmother, etc.) are extraordinary primary source material. Add a brief editorial note above the comments: "Comments from descendants of Tyneham families" — improves E-E-A-T framing without modifying the comments themselves.

---

## Appendix: Pages with No Schema (Priority Order)

| Priority | Page | Recommended Schema |
|----------|------|-------------------|
| CRITICAL | `opening_times.html` | TouristAttraction + OpeningHoursSpecification + FAQPage |
| CRITICAL | `index.html` (supplement existing) | WebSite + TouristAttraction |
| HIGH | `tyneham-church.html` | LandmarksOrHistoricalBuildings + Museum |
| HIGH | `tyneham-school.html` | LandmarksOrHistoricalBuildings + Museum |
| HIGH | `worbarrow-bay.html` | TouristAttraction + Beach |
| HIGH | `durdle-door.html` | TouristAttraction + LandmarksOrHistoricalBuildings |
| HIGH | `lulworth-cove.html` | TouristAttraction |
| HIGH | `corfe-castle.html` | LandmarksOrHistoricalBuildings + TouristAttraction |
| HIGH | `history_of_tyneham.html` | Article + BreadcrumbList |
| HIGH | `after-the-evacuation.html` | Article + BreadcrumbList |
| HIGH | `the-campaign-to-return.html` | Article + BreadcrumbList |
| HIGH | `the-church-door-note.html` | Article + FAQPage + BreadcrumbList |
| HIGH | `the_bond_family.html` | Article + BreadcrumbList |
| HIGH | `smuggling.html` | Article + BreadcrumbList |
| MEDIUM | `kimmeridge-bay.html` | TouristAttraction + BreadcrumbList |
| MEDIUM | `flowers-barrow.html` | LandmarksOrHistoricalBuildings + BreadcrumbList |
| MEDIUM | `tyneham-house.html` | LandmarksOrHistoricalBuildings + BreadcrumbList |
| MEDIUM | `the-rectory.html` | LandmarksOrHistoricalBuildings + BreadcrumbList |
| MEDIUM | `the_post_office.html` | LandmarksOrHistoricalBuildings + BreadcrumbList |
| MEDIUM | `tyneham-remembered.html` | Product + BreadcrumbList |
| MEDIUM | `tyneham_village_location.html` | TouristAttraction + BreadcrumbList |
| MEDIUM | `map_of_tyneham.html` | Map + BreadcrumbList |
| LOW | `camp-at-tyneham.html` | Article + BreadcrumbList |
| LOW | `contact.html` | ContactPage |
