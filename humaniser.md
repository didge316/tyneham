# Humaniser tracker — tynehamvillage.org

Tracking sheet for running the **humanizer** skill (`~/.claude/skills/humanizer`)
across the site's content pages.

## How to use this file

- **Protected keywords** = the exact SEO phrases, place names, and proper nouns the
  humaniser **must NOT rewrite, reword, or remove**. They are what the page ranks for.
  Preserve verbatim (including date-spans, postcodes, and documented quotes).
- **Done?** — `[ ]` not yet, `[x]` humanised and committed.
- Pages are live; humanise prose only — never touch schema JSON-LD, meta/og tags,
  alt text, or the `_redirects` / `_headers` files.
- **All pages: Sonnet** — the entire site is uniform AI-generated output with no mixed
  human authorship. No page requires Opus judgment.

Status: 10 / 27 article pages humanised.

---

## History

| Page (slug) | Protected keywords — DO NOT TOUCH | Done? | Notes |
|---|---|:---:|---|
| after-the-evacuation | 252 people, December 1943, Churchill's pledge, evacuation notice | [x] | 2026-06-20 |
| ghost-village | Dorset's ghost village, evacuated 1943, no entry charge, no gift shop | [x] | 2026-06-20 |
| history-of-tyneham | Tyneham village history, Norman Conquest 1066, Bond family, Lilian Bond, Tyneham: A Lost Heritage | [x] | 2026-06-20 |
| the-bond-family | Bond family, 1683, Lady Alice Lisle, Lilian Bond, Tyneham: A Lost Heritage | [x] | 2026-06-20 |
| the-campaign-to-return | campaign to return, Churchill's pledge, 1974 White Paper, Tyneham Action Group, Philip Draper | [x] | 2026-06-20 |
| the-church-door-note | church door note, "Please treat the church and houses with care", 19 December 1943 | [x] | 2026-06-20 — quoted note text untouched |
| tyneham-in-wartime | Tyneham in Wartime, 1943 evacuation, WAAFs, Chain Home radar, Dragon's Teeth | [x] | 2026-06-20 |

## Buildings & places

| Page (slug) | Protected keywords — DO NOT TOUCH | Done? | Notes |
|---|---|:---:|---|
| the-post-office | Post Office, village shop, telephone kiosk K1, 1929, Kimmeridge 221 | [x] | 2026-06-20 |
| the-rectory | Rectory, 1853, Reverend Nathaniel Bond, WAAFs, 1960s fire | [x] | 2026-06-20 |
| tyneham-church | St Mary's Church, Norman transitional style c.1190, Bond family chapel, church as museum | [x] | 2026-06-20 |
| tyneham-house | Tyneham House, Elizabethan manor, Bond family 260 years, WAAFs, 1973 demolition | [ ] | |
| tyneham-school | Tyneham School, 1856, Mrs Pritchard, one-room classroom, closed 1932 | [ ] | |

## Visitor information

| Page (slug) | Protected keywords — DO NOT TOUCH | Done? | Notes |
|---|---|:---:|---|
| camp-at-tyneham | camping near Tyneham, campsites near Tyneham, specific campsite names & postcodes | [ ] | Preserve all postcode/distance data exactly |
| map-of-tyneham | Tyneham village map, 10 key buildings, The Rectory, St Mary's Church, Tyneham School | [ ] | Light touch — headings + captions only |
| opening-times | Tyneham opening times 2026, weekends and school holidays, 9am to dusk | [ ] | Light touch — calendar/status text only |
| tyneham-photos | Tyneham Church, Tyneham School, Post Office, ruined cottages | [ ] | Light touch — captions + headings only |
| tyneham-remembered | Tyneham Remembered, Arthur Grant, Peter Wellman, Doug Churchill, oral history | [ ] | |
| tyneham-village-location | Tyneham village location, Isle of Purbeck, postcode BH20 5QH, Jurassic Coast | [ ] | Preserve all postcodes and road numbers exactly |
| visiting-tyneham | visiting Tyneham, free entry, opening times, what to expect, red telephone box | [ ] | |
| wildlife-at-tyneham | wildlife, Purbeck Heaths National Nature Reserve, Dartford warblers, early spider orchids, six native reptile species | [ ] | |

## Nearby attractions

| Page (slug) | Protected keywords — DO NOT TOUCH | Done? | Notes |
|---|---|:---:|---|
| corfe-castle | Corfe Castle, National Trust, ruined Norman fortress, Lady Bankes, Swanage Railway | [ ] | |
| durdle-door | Durdle Door, postcode BH20 5PU, limestone arch, Jurassic Coast, free entry | [ ] | Preserve postcode exactly |
| flowers-barrow | Flower's Barrow, Iron Age hillfort, coastal hill fort, 2,500 years ago, coastal erosion | [ ] | |
| gad-cliff | Gad Cliff, limestone headland, Brandy Bay, smuggling, coastal erosion | [ ] | |
| kimmeridge-bay | Kimmeridge Bay, Jurassic Coast, fossil hunting, ammonites, belemnites, UNESCO World Heritage | [ ] | |
| lulworth-cove | Lulworth Cove, horseshoe-shaped bay, UNESCO World Heritage, Portland limestone, Purbeck beds | [ ] | |
| worbarrow-bay | Worbarrow Bay, Jurassic Coast, dinosaur footprints, Worbarrow Tout, Purbeck Monocline | [ ] | |

## Walks

| Page (slug) | Protected keywords — DO NOT TOUCH | Done? | Notes |
|---|---|:---:|---|
| corfe-castle-walk | Corfe Castle circular walk, Purbeck ridge, 7–8 miles, Noel Hill, Ridgeway Hill | [ ] | Preserve all distances, times, and waypoint names exactly |
| kimmeridge-tyneham-walk | Kimmeridge Bay to Tyneham, 7.5 miles, South West Coast Path | [ ] | Preserve all distances, times, and waypoint names exactly |
| lulworth-range-walks | Walk 1 Tyneham to Worbarrow Bay, Walk 2 Gad Cliff Circular, Walk 3 Flower's Barrow Hillfort | [ ] | Preserve all distances, times, and waypoint names exactly |
| tyneham-walk | Tyneham circular walk, 4.3 miles, Whiteway Hill, Flower's Barrow, Worbarrow Bay | [ ] | Preserve all distances, times, and waypoint names exactly |

---

## Out of scope — do NOT humanise

| Page | Reason |
|---|---|
| `index.html` | Intentionally minimal homepage |
| `about.html` | Authentic owner voice — leave as is |
| `contact.html` | Form page |
| `thank-you.html` | Form confirmation page |
| `privacy.html` | Legal boilerplate |
| `404.html` | Error page |
| `history_of_tyneham.html`, `map_of_tyneham.html`, `opening_times.html`, `the_bond_family.html`, `the_post_office.html`, `tyneham_village_location.html` | Underscore-slug redirect targets — not canonical |
