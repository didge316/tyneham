#!/home/matt/claude/.venv/bin/python3
"""Add Wildlife at Tyneham to the Village dropdown navbar on all site pages."""
import os, glob

WEBSITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WILDLIFE_ITEM = '            <li><a class="dropdown-item" href="wildlife-at-tyneham.html">Wildlife at Tyneham</a></li>\n'

# Insert after Tyneham Village Photos (last item in The Village dropdown)
ANCHOR = '            <li><a class="dropdown-item" href="tyneham-photos.html">Tyneham Village Photos</a></li>\n'

changed = []
skipped = []

for path in sorted(glob.glob(os.path.join(WEBSITE, '*.html'))):
    fname = os.path.basename(path)
    if fname in {'404.html', 'privacy.html', 'thank-you.html'}:
        continue

    with open(path) as f:
        html = f.read()

    if 'wildlife-at-tyneham.html">Wildlife at Tyneham' in html:
        skipped.append(fname + ' (already has link)')
        continue

    orig = html
    html = html.replace(ANCHOR, ANCHOR + WILDLIFE_ITEM)

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
