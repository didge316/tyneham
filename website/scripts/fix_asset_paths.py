#!/usr/bin/env python3
"""
fix_asset_paths.py — Fix relative asset paths across all HTML files.

Changes applied to all *.html files (recursively):
  - href="css/styles.min.css?v=..." -> href="/css/styles.min.css?v=..."
  - href="assets/favicon.png" -> href="/assets/favicon.png"
  - src="assets/tyneham-dvd-cover.webp" -> src="/assets/tyneham-dvd-cover.webp"
  - 404.html: navbar dropdown hrefs missing leading/trailing slashes
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # website/

counters = {
    'css_path': 0,
    'favicon_path': 0,
    'dvd_cover_src': 0,
    '404_nav_hrefs': 0,
    'files_changed': 0,
}


def fix_file(path):
    text = path.read_text(encoding='utf-8')
    original = text
    local = {k: 0 for k in counters}

    # 1. CSS path: href="css/styles.min.css?v=..." -> /css/...
    new, n = re.subn(
        r'href="css/styles\.min\.css\?v=\d+"',
        lambda m: m.group(0).replace('href="c', 'href="/c'),
        text
    )
    local['css_path'] += n
    text = new

    # 2. Favicon path: href="assets/favicon.png" -> /assets/...
    new = text.replace('href="assets/favicon.png"', 'href="/assets/favicon.png"')
    local['favicon_path'] += text.count('href="assets/favicon.png"')
    text = new

    # 3. All src="assets/... -> /assets/... (images in page content and sidebar)
    new, n = re.subn(r'src="assets/', 'src="/assets/', text)
    local['dvd_cover_src'] += n
    text = new

    # 4. All srcset="assets/... -> srcset="/assets/... (picture source elements)
    new, n = re.subn(r'srcset="assets/', 'srcset="/assets/', text)
    local['dvd_cover_src'] += n
    text = new

    # 5. 404.html: navbar hrefs missing leading/trailing slashes
    #    (catch bare paths like href="opening-times", not already-correct ones)
    if path.name == '404.html':
        # Fix navbar dropdown hrefs that lack leading / and trailing /
        new, n = re.subn(
            r'(href=")([a-z][a-z-]+[a-z])(")',
            lambda m: m.group(0) if m.group(2).startswith('/') else f'{m.group(1)}/{m.group(2)}/{m.group(3)}',
            text
        )
        local['404_nav_hrefs'] += n
        text = new

    if text != original:
        path.write_text(text, encoding='utf-8')
        counters['files_changed'] += 1
        for k, v in local.items():
            if k in counters:
                counters[k] += v
        return True
    return False


for html_file in sorted(ROOT.rglob('*.html')):
    # Skip the template
    if 'page_template' in html_file.name:
        continue
    changed = fix_file(html_file)
    rel = html_file.relative_to(ROOT)
    status = '✓' if changed else '·'
    print(f"  {status} {rel}")

print()
print("=== Summary ===")
for k, v in counters.items():
    if v:
        print(f"  {k}: {v}")
