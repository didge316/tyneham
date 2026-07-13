---
name: gitignore-gotchas
description: tynehamvillage.org .gitignore rules that affect what actually deploys
metadata:
  type: project
---

In `website/`'s repo, `.gitignore` has two non-obvious rules that affect the live site:

1. `*.png` is gitignored. Existing PNGs referenced in HTML (favicon.png, logo-publisher.png, camping_near_tyneham.png, tyneham_remembered_download.png) were force-added (`git add -f`) so they ARE live. But any NEW .png will silently NOT deploy unless force-added. Check `git ls-files --error-unmatch website/assets/<file>.png` before assuming a PNG is live. (June 2026: `wildflowers.png` was referenced but never deployed — fixed by pointing the `<img>` at the existing `.webp`.)

2. The 6 underscore-named legacy HTML files (`history_of_tyneham.html`, `map_of_tyneham.html`, `opening_times.html`, `the_bond_family.html`, `the_post_office.html`, `tyneham_village_location.html`) are intentionally gitignored — they exist locally but never deploy. They are covered by underscore→hyphen 301s in `_redirects`. So they are NOT a duplicate-content problem on the live site, even though they show up locally. Don't bother "fixing" them.

Canonical internal links use extensionless clean URLs (e.g. `href="opening-times"`), never `.html`.
