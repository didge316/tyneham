---
name: project-audit-june2026
description: Results and key findings from the June 2026 full SEO audit of tynehamvillage.org
metadata:
  type: project
---

Full SEO and content audit completed 2026-06-03. Score improved from 45/100 (May 2026) to 70/100.

**Why:** Significant content and schema work done since May audit. New pages added, schema added across all pages, about.html created, security headers added.

**Top unresolved issues (as of 2026-06-03):**

1. Population figure "225" is wrong on index.html, history-of-tyneham.html, after-the-evacuation.html, ghost-village.html, and llms.txt — correct figure is **252**
2. Parking cost contradiction: visiting-tyneham.html says £2, opening-times.html schema says £4 — must verify actual figure
3. Six underscore legacy pages (history_of_tyneham.html etc.) are indexable with self-canonicals pointing to underscore URLs — need bulk canonical fix
4. llms.txt errors: "225" and wrong postcode "BH20 5QS" (should be BH20 5QH) — corrected version in AUDIT-2026-06-03.md Appendix A
5. tyneham-village-location.html says "Tyneham has no postcode" — contradicts BH20 5QH used everywhere else
6. Worbarrow Bay: coastguard station demolition date is both 1911 and 1912 on same page
7. Bond family tenure "roughly 400 years" on corfe-castle.html — should be ~260 years (acquired 1683, lost 1943)
8. Church door note attribution conflict in FAQPage schema (W.H. BOND vs women and children)

**Draft pages (noindex, not to be published yet):** corfe-castle-walk.html, kimmeridge-tyneham-walk.html, tyneham-in-wartime.html, wildlife-at-tyneham.html

**Full audit report:** website/docs/AUDIT-2026-06-03.md
**Action plan:** website/docs/ACTION-PLAN.md

**How to apply:** When working on any page, check these issues first. The bulk fixes (population figure, sidebar sync, canonical fix) are highest ROI and should be done with bulk_seo_fixes.py.
