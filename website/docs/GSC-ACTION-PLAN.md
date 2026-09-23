# Tyneham Village — GSC Content Gap & Opportunity Plan

**Data:** Google Search Console, 2026-08-01 → 2026-09-22 (2,670 query rows · 2,015 clicks · 47,874 impressions)
**Generated:** 2026-09-23
**Source export:** `gsc/gsc_export.py` → `gsc/data/2026-08.csv`, `2026-09.csv` (gitignored)

> Replaces the stale `SEOtodo.md` (June 2026 audit checklist, now superseded by this plan and `ACTION-PLAN.md`).
> This plan is **traffic-data-driven** (what Google actually shows and what we're failing to win), as opposed to the audit-driven items in `ACTION-PLAN.md`.

---

## What's Working — Protect

These queries already perform well; do not disturb them.

- `tyneham village opening times 2026` — 4,292 i @ pos 8.5, **556 clicks**. Money page (`/opening-times/`).
- `how to get to tyneham village` — pos 3.6.
- `tyneham village car park postcode` — pos 6.6.
- `tyneham photos` — pos 7.2.
- `tyneham village map` — steady clicks.
- `worbarrow bay opening times 2026` — pos 4.1.
- `tyneham village opening times 2026 tomorrow` — pos 5.8.

---

## TIER 1 — Owned Intent, Near-Zero Effort (title/meta/H1)

These are queries the site *should* own — the pages exist and cover the topic — but rank 40–55 because the title/H1/meta don't name the query.

### G1. `tyneham beach` — 379 i @ pos 54.9 (5+0 clicks)
Worbarrow Bay **is** Tyneham's beach. Page title is "Worbarrow Bay | Secluded Dorset Beach near Tyneham Village" — contains "Dorset Beach" but not the queried "Tyneham beach".
- Add "Tyneham beach" to `worbarrow-bay` `<title>`, H1, meta description (e.g. "Worbarrow Bay — the Tyneham beach, 1 mile on foot…").
- Target: pos 54 → top 5. Largest owned-intent gap.

### G2. `tyneham village postcode` / `tyneham postcode` — 398 i @ pos 40 / 29.9
Page body says "Use postcode BH20 5QH for sat-nav" but `<title>` is "Where is Tyneham? Location, Directions & Parking" — no "postcode".
- Add "postcode BH20 5QH" to `tyneham-village-location` `<title>` + meta.
- Target: top 3.

### G3. `is tyneham village open today` / `open tomorrow` / `when is tyneham open` — ~1,330 i @ pos 40–51 (49 clicks)
The day-intent phrasing is untargeted. Only the "2026" phrasing ranks (pos 8.5). Page has the live open/closed widget.
- Reframe `opening-times` `<title>`/meta to include the "open today?" intent alongside "Opening Times 2026" (e.g. "…| Is Tyneham Village Open Today?").
- Target: pos 40–51 → top 5. This cluster converts (49 clicks already at pos ~45).

### G4. `tyneham car park` / `tyneham village car park` — ~370 i @ pos 42–50 (16 clicks)
`visiting-tyneham` title has "Parking" but not "car park"; the parking section exists.
- Add "car park" phrasing to `visiting-tyneham` `<title>`/meta.
- Target: top 5.

---

## TIER 2 — Needs Content, Medium Effort

### G5. Tide times — Kimmeridge cluster 767 i @ pos 9.6, only 12 clicks
`tide times kimmeridge bay` 450 i @ 9.6 · `tide times kimmeridge` 87 i · `kimmeridge tide times` 49 i · etc. Page ranks page-1 but gets ~1.5% CTR; no tide resource on the page.
- Add a **tide times** section to `kimmeridge-bay` (link to an authoritative live tide table for Kimmeridge Bay + a quick "check tides before rock-pooling" note).
- Target: hold pos ~9 but lift CTR to ~5%+.

### G6. `worbarrow bay` head term + `worbarrow bay opening times` — 2,267 i @ pos 28 / 35.9
`worbarrow bay` 1,337 i @ pos **28** — the page under-ranks for its own name. `worbarrow bay opening times` 136 i @ 35.9. `worbarrow beach` 101 i @ 12.9.
- **Aligns with pending `ACTION-PLAN.md` M2 ("Worbarrow-bay planner facts first").** Do the M2 content rework (parking / 1-mile walk / ranges access / dogs / swimming rules / no facilities before the history) **and** tighten title/meta for the head term.
- Highest-value content task on the site.

---

## TIER 3 — Biggest Volume, Peripheral Topic

### G7. Durdle Door sub-queries — 4,797 i, only 10 clicks (0.2% CTR)
- `durdle door` 2,306 i @ 10.1 · `durdle door postcode` 616 i @ 9.2 · `opening times` 97 i · `closing time` 51 i · `beach postcode` 92 i · `car park postcode` 89 i · `facts`/`how old`/`how tall`/`entry fee`/`free to visit` ~130 i — **all 0 clicks**.
- Page ranks page-1 bottom but never wins the snippet; title "Durdle Door – Dorset's Most Famous Attraction" doesn't answer sub-intents.
- **Optional / low priority** (peripheral "Near Tyneham" page, competitive SERP dominated by the National Trust + Durdle Door Holiday Park). If pursued: put postcode BH20 5PU + opening + "free entry" in `<title>`/meta so the snippet answers the sub-queries.

---

## TIER 4 — Minor

- **G8. `tyneham ghost village`** 297 i @ pos 16 — tighten `ghost-village` title/meta ("Tyneham: Dorset's Ghost Village | Abandoned Village" is close; lift pos 16 → 5–8).
- **G9. `tyneham house`** 183 i @ pos 35.7 — tighten `tyneham-house` title/meta.
- **G10. `kimmeridge bay postcode`** 128 i @ pos 7.5, 0 clicks — put BH20 5PF in the snippet (desc already mentions it; ensure it's in the `<title>`).
- **G11. `flowers barrow`** 125 i @ 12.8 + `flower barrow` 52 i @ 6.3 — small; title already improved (H3 done).
- **G12. Misspellings** — `tingham` 136 i · `tineham` 95 i · `tynam village` 54 i · `tyford england` 33 i · `tyenham`/`tynehan` ~50 i — all pos 5–8, **0 clicks**. Add a "sometimes spelled Tyneham" note (location page) for completeness; low value.

---

## Not Worth Pursuing

- **Kiosk / phone box** — zero impressions for any `phone`/`kiosk`/`telephone`/`box` query. Build the kiosk page as an internal story/AI-discovery page, **not** for keyword traffic.
- **Walking cluster** — 317 i total (`tyneham walks` 20 i @ 58). No new walk pages justified by data.
- **Dogs** — 17 i total. Negligible.
- **History cluster** — 278 i; `corfe castle history` 103 i is peripheral. Leave.

---

## Suggested Sequence

1. **G1 + G2** (15 min) — the two biggest owned-intent gaps.
2. **G3 + G4** (15 min) — opening-times and car park intent.
3. **G6** with `ACTION-PLAN.md` **M2** (2–3 h) — worbarrow-bay rework (biggest content task).
4. **G5** (30 min) — tide-times section on kimmeridge-bay.
5. **G7** optional (30 min) — durdle-door snippet pass.
6. **G8–G12** as time allows.

**Re-measure:** re-export GSC (`gsc/gsc_export.py --current`) after 4–6 weeks; check positions for the G1–G6 target queries.