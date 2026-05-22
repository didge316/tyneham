#!/usr/bin/env python3
"""
bulk_seo_fixes.py — Apply sitewide SEO corrections to tynehamvillage.org

Changes applied to all *.html files:
  - Author: "Tyneham Admin" → "James Langton"
  - Navbar brand href: "index.html" → "/"
  - Footer home href: href="index.html" class="footer-link" → href="/"
  - alt="Advertisement" → descriptive alt text (DVD cover image)
  - og:image relative paths → absolute URLs
  - twitter:image relative paths → absolute URLs
  - Typo: "Particualar" → "Particular"
  - Add loading="lazy" to img tags missing it (skips fetchpriority and existing loading attrs)
"""

import re
from pathlib import Path

ROOT = Path('/home/matt/claude/websites/tyneham/website')

counters = {
    'author': 0,
    'navbar_href': 0,
    'footer_href': 0,
    'alt_advert': 0,
    'og_image': 0,
    'twitter_image': 0,
    'typo': 0,
    'lazy': 0,
    'files_changed': 0,
}


def add_lazy_loading(text):
    """Add loading="lazy" to <img> tags that lack a loading or fetchpriority attribute."""
    # Match self-closing and non-self-closing img tags (single-line assumption for attrs,
    # but src/alt may span to next line — handle robustly with a split approach)
    parts = re.split(r'(<img\b)', text)
    result = [parts[0]]
    i = 1
    added = 0
    while i < len(parts):
        # parts[i] is '<img'
        # parts[i+1] is everything after '<img' until the next '<img'
        tag_prefix = parts[i]
        if i + 1 < len(parts):
            rest = parts[i + 1]
        else:
            result.append(tag_prefix)
            break

        # Find the end of this img tag: first '>' that closes it
        gt_pos = rest.find('>')
        if gt_pos == -1:
            result.append(tag_prefix + rest)
            i += 2
            continue

        img_body = rest[:gt_pos + 1]
        after = rest[gt_pos + 1:]

        full_tag = tag_prefix + img_body  # e.g. <img class="..." src="..." >

        if 'loading=' not in img_body and 'fetchpriority=' not in img_body:
            # Insert loading="lazy" before the closing > or />
            if img_body.rstrip().endswith('/>'):
                new_tag = tag_prefix + img_body.rstrip()[:-2].rstrip() + ' loading="lazy" />'
            else:
                new_tag = tag_prefix + img_body.rstrip()[:-1].rstrip() + ' loading="lazy">'
            result.append(new_tag)
            added += 1
        else:
            result.append(full_tag)

        result.append(after)
        i += 2

    return ''.join(result), added


def fix_file(path):
    text = path.read_text(encoding='utf-8')
    original = text
    local = {k: 0 for k in counters}

    # 1. Author
    new = text.replace('content="Tyneham Admin"', 'content="James Langton"')
    local['author'] += text.count('content="Tyneham Admin"')
    text = new

    # 2. Navbar brand link
    new, n = re.subn(
        r'(<a class="navbar-brand" href=")index\.html(")',
        r'\1/\2',
        text
    )
    local['navbar_href'] += n
    text = new

    # 3. Footer home link (various forms seen in the codebase)
    new, n = re.subn(
        r'(<a href=")index\.html(" class="footer-link")',
        r'\1/\2',
        text
    )
    local['footer_href'] += n
    text = new

    # Also catch the reversed attribute order just in case
    new, n = re.subn(
        r'(<a class="footer-link" href=")index\.html(")',
        r'\1/\2',
        text
    )
    local['footer_href'] += n
    text = new

    # 4. alt="Advertisement"
    new = text.replace('alt="Advertisement"', 'alt="Tyneham Remembered documentary DVD cover"')
    local['alt_advert'] += text.count('alt="Advertisement"')
    text = new

    # 5. og:image relative → absolute
    new, n = re.subn(
        r'(<meta property="og:image" content=")(/assets/)',
        r'\1https://tynehamvillage.org\2',
        text
    )
    local['og_image'] += n
    text = new

    # 6. twitter:image relative → absolute
    new, n = re.subn(
        r'(<meta name="twitter:image" content=")(/assets/)',
        r'\1https://tynehamvillage.org\2',
        text
    )
    local['twitter_image'] += n
    text = new

    # 7. Typo fix
    new = text.replace('Particualar', 'Particular')
    local['typo'] += text.count('Particualar')
    text = new

    # 8. Lazy loading
    text, n = add_lazy_loading(text)
    local['lazy'] += n

    if text != original:
        path.write_text(text, encoding='utf-8')
        counters['files_changed'] += 1
        for k, v in local.items():
            if k in counters:
                counters[k] += v
        return True
    return False


for html_file in sorted(ROOT.glob('*.html')):
    changed = fix_file(html_file)
    status = '✓' if changed else '·'
    print(f"  {status} {html_file.name}")

print()
print("=== Summary ===")
for k, v in counters.items():
    if v:
        print(f"  {k}: {v}")
