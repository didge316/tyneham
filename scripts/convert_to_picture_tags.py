#!/home/matt/claude/.venv/bin/python3
"""
Convert <img src="*.jpg"> to <picture> tags with webp source + jpg fallback.
Only wraps images where a corresponding .webp file exists in assets/.
Skips img tags already inside <picture> tags.
"""

import re
from pathlib import Path

WEBSITE_DIR = Path('/home/matt/claude/websites/tyneham/website')


def process_file(html_path):
    path = Path(html_path)
    content = path.read_text(encoding='utf-8')
    original = content

    # Step 1: stash existing <picture> blocks so we don't double-wrap
    placeholders = {}
    counter = [0]

    def stash_picture(m):
        key = f'__PICTURE_{counter[0]}__'
        placeholders[key] = m.group(0)
        counter[0] += 1
        return key

    content = re.sub(
        r'<picture\b[^>]*>.*?</picture>',
        stash_picture,
        content,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Step 2: wrap jpg/jpeg img tags where a .webp sibling exists
    src_re = re.compile(r'''\bsrc=['"]([^'"]+\.(?:jpg|jpeg))['"]''', re.IGNORECASE)
    img_re = re.compile(r'<img\b[^>]*>', re.IGNORECASE)

    def replace_img(m):
        tag = m.group(0)
        src_match = src_re.search(tag)
        if not src_match:
            return tag
        src = src_match.group(1)
        if '://' in src:
            return tag
        webp_src = re.sub(r'\.(jpg|jpeg)$', '.webp', src, flags=re.IGNORECASE)
        # Handle both "assets/..." and "/assets/..." paths
        check_src = webp_src.lstrip('/')
        if not (WEBSITE_DIR / check_src).exists():
            return tag
        return (
            f'<picture>'
            f'<source srcset="{webp_src}" type="image/webp">'
            f'{tag}'
            f'</picture>'
        )

    content = img_re.sub(replace_img, content)

    # Step 3: restore stashed picture blocks
    for key, value in placeholders.items():
        content = content.replace(key, value)

    if content != original:
        path.write_text(content, encoding='utf-8')
        return True
    return False


html_files = sorted(WEBSITE_DIR.glob('*.html'))
changed = 0
for html_file in html_files:
    if process_file(html_file):
        print(f'  Updated: {html_file.name}')
        changed += 1

print(f'\nDone. Updated {changed} of {len(html_files)} files.')
