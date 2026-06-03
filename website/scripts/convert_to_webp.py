#!/home/matt/claude/.venv/bin/python3
"""Convert JPEG/PNG images that lack a WebP pair to WebP format.

Generates a .webp alongside the original and wraps any bare <img> that
references that JPEG/PNG in a <picture> tag with WebP source + original fallback.
"""
import os
import glob
import re
from PIL import Image

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(SITE_DIR, 'assets')

# Priority order — largest first
TARGETS = [
    'tyneham-evacuation-letter.jpg',
    'tyneham-village-1930s.jpg',
    'nathanial-bond-portrait.jpg',
    'arthur-grant-tyneham.jpg',
    'wafs-tyneham.jpg',
    'worbarrow-tout-aerial.jpg',
    'wafs-tyneham-2.jpg',
    'fred-knight-tyneham.jpg',
    'percy-holland-farm.jpg',
    'bf110-wwii.jpg',
    'jack-miggie-worbarrow-1930.jpg',
    'bungalow2.jpg',
    'camping_near_tyneham.png',
    'tyneham_remembered_download.png',
]

def convert(src_path, webp_path):
    img = Image.open(src_path)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGBA')
    else:
        img = img.convert('RGB')
    img.save(webp_path, 'WEBP', quality=82, method=6)
    src_kb = os.path.getsize(src_path) // 1024
    webp_kb = os.path.getsize(webp_path) // 1024
    saving = 100 - (webp_kb * 100 // src_kb)
    print(f'  {os.path.basename(src_path)}: {src_kb}KB → {webp_kb}KB ({saving}% smaller)')

def wrap_img_in_picture(html, img_filename, webp_filename):
    """Wrap bare <img src="...filename..."> in a <picture> tag if not already wrapped."""
    # Find bare <img> tags referencing this file that aren't already inside <picture>
    # We look for <img ... src="...filename..." ...> not preceded by <source
    img_re = re.compile(
        r'(?<!<picture>\s{0,200})(<img\b[^>]*\bsrc="([^"]*' + re.escape(img_filename) + r')"[^>]*>)',
        re.IGNORECASE
    )

    def wrap(m):
        img_tag = m.group(1)
        src = m.group(2)
        webp_src = src.replace(img_filename, webp_filename)
        # Check if already in a picture tag (look at surrounding context)
        return img_tag  # will be replaced by caller with picture wrap

    # Simpler approach: find <img> with this src and check if parent is <picture>
    pattern = re.compile(
        r'<img\b([^>]*\bsrc="([^"]*' + re.escape(img_filename) + r')"[^>]*)>',
        re.IGNORECASE
    )

    def replace_with_picture(m):
        attrs = m.group(1)
        src = m.group(2)
        webp_src = src.replace(img_filename, webp_filename)
        return (f'<picture>\n'
                f'  <source srcset="{webp_src}" type="image/webp">\n'
                f'  <img{attrs}>\n'
                f'</picture>')

    # Only wrap if the img isn't already inside a <picture> block
    # Simple heuristic: check if <source> appears just before this img
    result = html
    for m in reversed(list(pattern.finditer(html))):
        start = m.start()
        # Check backwards for <picture> within 200 chars
        preceding = html[max(0, start-200):start]
        if '<picture>' in preceding and '</picture>' not in preceding:
            continue  # already inside a picture tag
        replacement = replace_with_picture(m)
        result = result[:start] + replacement + result[m.end():]

    return result

# Step 1: Convert images
converted = []
for filename in TARGETS:
    src = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(src):
        print(f'  SKIP (not found): {filename}')
        continue
    webp_name = os.path.splitext(filename)[0] + '.webp'
    webp_path = os.path.join(ASSETS_DIR, webp_name)
    if os.path.exists(webp_path):
        print(f'  Already exists: {webp_name}')
        converted.append((filename, webp_name))
        continue
    try:
        convert(src, webp_path)
        converted.append((filename, webp_name))
    except Exception as e:
        print(f'  ERROR converting {filename}: {e}')

print(f'\nConverted {len(converted)} images.')

# Step 2: Update HTML files to use <picture> tags
print('\nUpdating HTML files...')
html_files = glob.glob(os.path.join(SITE_DIR, '*.html'))
html_updated = 0
for html_path in sorted(html_files):
    with open(html_path, 'r', encoding='utf-8') as f:
        original = f.read()
    updated = original
    for img_filename, webp_filename in converted:
        if img_filename in updated:
            updated = wrap_img_in_picture(updated, img_filename, webp_filename)
    if updated != original:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f'  Updated: {os.path.basename(html_path)}')
        html_updated += 1

print(f'\nDone — {html_updated} HTML files updated with <picture> tags.')
