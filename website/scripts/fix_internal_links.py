#!/usr/bin/env python3
"""Fix all internal links and meta URLs: make them absolute with trailing slashes.

Before: href="about" or href="/about" or content="https://tynehamvillage.org/about"
After:  href="/about/" or content="https://tynehamvillage.org/about/"

This eliminates unnecessary 301 redirects now that pages live in
subdirectories as index.html.
"""

import re
from pathlib import Path

WEBSITE_DIR = Path('/home/matt/projects/tyneham/website')

ASSET_DIRS = {'assets', 'css', 'docs', 'js', 'scripts'}
PAGE_DIRS = sorted([
    d.name for d in WEBSITE_DIR.iterdir()
    if d.is_dir() and d.name not in ASSET_DIRS
])

DOMAIN = "https://tynehamvillage.org"


def fix_links(filepath):
    text = filepath.read_text(encoding='utf-8')
    original = text

    for slug in PAGE_DIRS:
        pat = re.escape(slug)

        # href: relative links (href="slug" → href="/slug/")
        text = re.sub(rf'href="{pat}"', rf'href="/{slug}/"', text)

        # href: absolute missing trailing slash (href="/slug" → href="/slug/")
        text = re.sub(rf'href="/{pat}"', rf'href="/{slug}/"', text)

        # meta content: full URL missing trailing slash
        text = re.sub(
            rf'content="{re.escape(DOMAIN)}/{pat}"',
            rf'content="{DOMAIN}/{slug}/"',
            text,
        )

    if text != original:
        filepath.write_text(text, encoding='utf-8')
        return True
    return False


count = 0
html_files = sorted(WEBSITE_DIR.glob('*/index.html')) + [WEBSITE_DIR / 'index.html']
for html_file in html_files:
    if fix_links(html_file):
        count += 1
        print(f"  ✓ {html_file.relative_to(WEBSITE_DIR)}")

print(f"\nDone. {count} files updated.")
