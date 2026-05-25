#!/home/matt/claude/.venv/bin/python3
"""Add 5 new pages to the navbar on all existing site pages."""
import os, glob, re

WEBSITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pages that already have the updated navbar (skip them)
ALREADY_UPDATED = {
    'ghost-village.html', 'visiting-tyneham.html', 'tyneham-photos.html',
    'lulworth-range-walks.html', 'gad-cliff.html',
}

# What to insert after the Opening Times line (Village dropdown)
VISITING_ITEM   = '            <li><a class="dropdown-item" href="visiting-tyneham.html">Visiting Tyneham</a></li>\n'
PHOTOS_ITEM     = '            <li><a class="dropdown-item" href="tyneham-photos.html">Tyneham Village Photos</a></li>\n'

# What to append before History dropdown closing tag
GHOST_ITEM      = '            <li><a class="dropdown-item" href="ghost-village.html">Dorset\'s Ghost Village</a></li>\n'

# What to append before Near Tyneham dropdown closing tag
WALKS_ITEM      = '            <li><a class="dropdown-item" href="lulworth-range-walks.html">Lulworth Range Walks</a></li>\n'
GAD_ITEM        = '            <li><a class="dropdown-item" href="gad-cliff.html">Gad Cliff</a></li>\n'

changed = []
skipped = []

for path in sorted(glob.glob(os.path.join(WEBSITE, '*.html'))):
    fname = os.path.basename(path)
    if fname in ALREADY_UPDATED:
        skipped.append(fname)
        continue
    if fname in {'404.html', 'privacy.html', 'thank-you.html'}:
        continue

    with open(path) as f:
        html = f.read()

    # Skip if already patched
    if 'visiting-tyneham.html">Visiting Tyneham' in html:
        skipped.append(fname)
        continue

    orig = html

    # 1. Add Visiting Tyneham after Opening Times line (old-style comments nav)
    html = html.replace(
        '<li><a class="dropdown-item" href="opening_times.html">Opening Times 2026</a></li>\n',
        '<li><a class="dropdown-item" href="opening_times.html">Opening Times 2026</a></li>\n' + VISITING_ITEM,
    )

    # 2. Add Photos before the Village dropdown closing tag — find it by the camp-at-tyneham anchor
    html = html.replace(
        '<li><a class="dropdown-item" href="camp-at-tyneham.html">Camping at Tyneham</a></li>\n',
        '<li><a class="dropdown-item" href="camp-at-tyneham.html">Camping at Tyneham</a></li>\n' + PHOTOS_ITEM,
    )

    # 3. Add Ghost Village after The Campaign to Return (last History item)
    html = html.replace(
        '<li><a class="dropdown-item" href="the-campaign-to-return.html">The Campaign to Return</a></li>\n',
        '<li><a class="dropdown-item" href="the-campaign-to-return.html">The Campaign to Return</a></li>\n' + GHOST_ITEM,
    )

    # 4. Add Walks + Gad Cliff after Kimmeridge Bay (last Near Tyneham item)
    html = html.replace(
        '<li><a class="dropdown-item" href="kimmeridge-bay.html">Kimmeridge Bay</a></li>\n',
        '<li><a class="dropdown-item" href="kimmeridge-bay.html">Kimmeridge Bay</a></li>\n' + WALKS_ITEM + GAD_ITEM,
    )

    if html != orig:
        with open(path, 'w') as f:
            f.write(html)
        changed.append(fname)
    else:
        skipped.append(fname + ' (no match)')

print(f"Updated {len(changed)} pages:")
for f in changed:
    print(f"  {f}")
print(f"\nSkipped {len(skipped)}:")
for f in skipped:
    print(f"  {f}")
