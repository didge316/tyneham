# Tyneham Village — SEO Fix Checklist

Generated from AUDIT-2026-06-03.md · Score: 74/100 → target 86/100  
Updated with 8-agent audit findings (2026-06-03)

---

## CRITICAL

- [x] **C1** Fix population figure 225 → 252 on all pages (index.html ×3, history-of-tyneham.html, after-the-evacuation.html, ghost-village.html ×3) and llms.txt — *done 2026-06-03*
- [ ] **C2** Verify and fix parking cost contradiction: visiting-tyneham.html says £2, opening-times.html FAQ schema says £4 — *schema fixed to £2; verify actual MOD figure is £2*
- [x] **C3** Fix 6 underscore legacy pages: canonical href and og:url now point to hyphen URLs — *done 2026-06-03*
- [ ] **C4** Delete the 6 underscore .html files from the repo — `history_of_tyneham.html`, `map_of_tyneham.html`, `opening_times.html`, `the_bond_family.html`, `the_post_office.html`, `tyneham_village_location.html`. Cloudflare serves physical files before `_redirects`, so they are currently live and self-canonical to the wrong URL.
- [ ] **C5** Remove Cloudflare Bulk Redirects (dashboard task) — the 13 entries in `website/cloudflare-bulk-redirects.csv` point old WordPress slugs to underscore URLs, creating two-hop chains (WP slug → underscore → hyphen). Delete all 13 from Cloudflare Dashboard → Bulk Redirects.

---

## HIGH

- [x] **H1** Fix llms.txt: "252 residents", postcode BH20 5QH, added tyneham-remembered entry — *done 2026-06-03*
- [x] **H2** Add noscript fallback to opening-times "open today" widget — *done 2026-06-03*
- [x] **H3** Synchronise index.html sidebar — added visiting-tyneham, tyneham-photos, ghost-village, lulworth-range-walks, gad-cliff — *done 2026-06-03*
- [x] **H4** Fix tyneham-village-location.html: body now says "Use postcode BH20 5QH for sat-nav", schema updated — *done 2026-06-03*
- [x] **H5** Fix worbarrow-bay.html: station closed 1911, demolished 1912 — both occurrences consistent — *done 2026-06-03*
- [x] **H6** Fix corfe-castle.html: Bond family "nearly 260 years" — *done 2026-06-03*
- [x] **H7** Fix the-church-door-note.html body text: "signed by W.H. Bond, on behalf of the families" — *done 2026-06-03*
- [x] **H8** Add OAI-SearchBot to robots.txt — *done 2026-06-03*
- [x] **H9** Add author property to ghost-village.html Article schema — *done 2026-06-03*
- [ ] **H10** Expand about.html author bio (currently ~220 words, needs 500+, needs author photo)
- [ ] **H11** Sitewide internal link cleanup — all 42 pages use `href="page.html"` internally but canonical URLs are clean (no .html). Run a bulk script to strip `.html` from all internal hrefs. Canonicals and Googlebot both prefer the clean URL; the mismatch splits PageRank.
- [ ] **H12** Fix WordPress legacy redirects in `_redirects` — 17 rules point to `.html` targets (e.g. `/a-brief-history-of-tyneham → /history-of-tyneham.html`). Change all to clean URLs (e.g. `→ /history-of-tyneham`).
- [ ] **H13** Add `sameAs` to TouristAttraction schema on index.html (and opening-times.html, visiting-tyneham.html) pointing to `https://en.wikipedia.org/wiki/Tyneham` and Wikidata entity. No sameAs exists anywhere on the site — this is the single highest-impact schema improvement for AI citation and Bing.
- [ ] **H14** Add FAQPage schema to `history-of-tyneham.html` and `after-the-evacuation.html` — both pages have H2 question headings with answers already written. Wrap in FAQPage JSON-LD. Directly improves Google AI Overviews coverage for research queries.
- [ ] **H15** Add Content-Security-Policy header to `_headers`. Site loads AdSense, Bootstrap JS CDN, Gravatar, Google Maps iframe, and PayPal — no CSP is in place. Start with: `default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://pagead2.googlesyndication.com; frame-src https://www.google.com; img-src 'self' https: data:;`

---

## MEDIUM

- [x] **M1** Fix Kimmeridge Bay postcode: both references now BH20 5PF — *done 2026-06-03*
- [x] **M2** Fix lulworth-cove.html: isAccessibleForFree: true — *done 2026-06-03*
- [x] **M3** Fix tyneham-church.html title: "St Mary's Church" with apostrophe in title, og:title, twitter:title — *done 2026-06-03*
- [x] **M4** Add forward links in history-of-tyneham.html → after-the-evacuation + the-campaign-to-return — *done 2026-06-03*
- [x] **M5** Add in-article links to the-church-door-note.html (→ tyneham-church, → the-bond-family, → history-of-tyneham) — *done 2026-06-03*
- [x] **M6** Add author bylines to 5 nearby-attraction pages (lulworth-cove, durdle-door, kimmeridge-bay, worbarrow-bay, lulworth-range-walks) — *done 2026-06-03*
- [x] **M7** Fix FAQ schema vs visible accordion on index.html — accordion answer now includes GOV.UK reference and 01929 404714 — *done 2026-06-03*
- [x] **M8** Fix duplicate sentence in lulworth-range-walks.html Flower's Barrow section — *done 2026-06-03*
- [ ] **M9** Fix schema typo on `opening-times.html` TouristAttraction description: "an abandoned village in Dorset in Dorset" → "an abandoned village in Dorset". May appear verbatim in AI-generated answers.
- [ ] **M10** Convert 16 JPEGs to WebP — missing WebP pairs in descending size priority: `tyneham-evacuation-letter.jpg` (1.9MB), `tyneham-village-1930s.jpg` (1.2MB), `nathanial-bond-portrait.jpg` (1.1MB), `arthur-grant-tyneham.jpg` (920KB), `wafs-tyneham.jpg` (567KB), `worbarrow-tout-aerial.jpg` (564KB), `wafs-tyneham-2.jpg` (496KB), `fred-knight-tyneham.jpg` (488KB), `percy-holland-farm.jpg` (460KB), `bf110-wwii.jpg` (262KB), `jack-miggie-worbarrow-1930.jpg` (193KB), `bungalow2.jpg` (175KB). Also convert `camping_near_tyneham.png` (227KB) and `tyneham_remembered_download.png` (551KB). Update HTML to use `<picture>` tag with WebP source.
- [ ] **M11** Add LCP image preload to 5 high-traffic pages missing it — `opening-times.html`, `history-of-tyneham.html`, `ghost-village.html`, `visiting-tyneham.html`, `worbarrow-bay.html`. Homepage already does this correctly. Add `<link rel="preload" as="image" href="...">` in `<head>` for each page's first above-fold image.
- [ ] **M12** Fix `ghost-village.html` meta description: 162 chars (limit 160). Trim 2 chars.
- [ ] **M13** Fix `tyneham-church.html` meta description: 169 chars (limit 160). Trim 9 chars.
- [ ] **M14** Add visible author byline to `index.html` and `opening-times.html` — both pages have `meta name="author"` in schema only. The history, visiting, and ghost-village pages already show "By James Langton — Updated May 2026" in the page body. Apply the same pattern here.
- [ ] **M15** Implement IndexNow — generate key at indexnow.org, place `.txt` file in website root, submit URLs on content updates. Useful for time-sensitive content like opening-times changes.

---

## LOW

- [x] **L1** Fix generic anchor "click on this link" → "open Tyneham in Google Maps" on tyneham-village-location.html — *done 2026-06-03*
- [x] **L2** Add Quotation schema to church door note blockquote — *done 2026-06-03*
- [ ] **L3** Add sameAs to about.html Person schema — *needs external URL for James Langton*
- [ ] **L8** Fix alt text typo on `opening-times.html` — `alt="Worbarrow BAy"` → `alt="Worbarrow Bay"`
- [ ] **L9** Add RSL 1.0 license declaration and `dateUpdated` field to `llms.txt` — two-line addition signals AI-ecosystem awareness
- [ ] **L10** Fix coordinate inconsistency on `index.html` — body text says "50.628°N / 2.162°W" but all schema blocks say "50.6239°N / 2.1601°W". Update prose to match schema values.
- [ ] **L11** Add brief sources note to `ghost-village.html` (and ideally `after-the-evacuation.html`) — history page already has a formal sources section; other editorial pages making specific factual claims should follow the same pattern
- [ ] **L12** Expand `history-of-tyneham.html` by ~400 words covering the 1948 retention decision and 1952 compulsory purchase — currently deferred entirely to after-the-evacuation.html; readers landing on the history page should not need two more clicks for the full story
- [ ] **L4** Enable Cloudflare Auto Minify for CSS (Dashboard → Speed → Optimization) — *dashboard only*
- [x] **L5** Expand lulworth-cove.html — added ~450 words: cove formation, three rock bands, Lulworth Crumple, Fossil Forest — *done 2026-06-03*
- [x] **L6** Expand tyneham-church.html — added architecture section: Norman origins, alterations timeline, bells to Steeple, Bible inscription, churchyard still in use — *done 2026-06-03*
- [x] **L7** Renamed worrbarrow-bay-today assets to worbarrow-bay-today, updated all HTML references — *done 2026-06-03*

---

## Draft pages — do before publishing

- [ ] wildlife-at-tyneham.html: add Article schema, add author byline, change robots to index/follow, add to navbar/sidebar
- [ ] tyneham-in-wartime.html: add to History nav dropdown + sidebar, add contextual links from ghost-village + history pages, add to sitemap.xml
- [ ] corfe-castle-walk.html: add to walks section, link from corfe-castle.html, add to sitemap.xml
- [ ] kimmeridge-tyneham-walk.html: add to walks section, link from kimmeridge-bay.html, add to sitemap.xml

---

_Full audit detail: website/docs/AUDIT-2026-06-03.md_
