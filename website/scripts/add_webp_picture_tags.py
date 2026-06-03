#!/home/matt/claude/.venv/bin/python3
"""Wrap <img> tags referencing JPEG/PNG images that have a WebP pair in <picture> tags."""
import os
import re
import glob

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(SITE_DIR, 'assets')

# Build list of (original_filename, webp_filename) pairs where both exist
pairs = []
for fname in os.listdir(ASSETS_DIR):
    if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
        webp_name = os.path.splitext(fname)[0] + '.webp'
        if os.path.exists(os.path.join(ASSETS_DIR, webp_name)):
            pairs.append((fname, webp_name))

print(f'Found {len(pairs)} image pairs with WebP versions')

IMG_PATTERN = re.compile(r'<img\b([^>]*?)>', re.IGNORECASE | re.DOTALL)

def needs_picture_wrap(html, pos):
    """Check if the img at pos is already inside a <picture> tag."""
    preceding = html[max(0, pos - 300):pos]
    # Find last <picture> and last </picture> before this position
    last_open = preceding.rfind('<picture>')
    last_close = preceding.rfind('</picture>')
    return last_open > last_close  # inside an unclosed <picture>

def get_src(attrs):
    m = re.search(r'\bsrc="([^"]+)"', attrs, re.IGNORECASE)
    return m.group(1) if m else ''

def wrap_in_picture(img_tag, src, webp_src):
    return (f'<picture>\n'
            f'          <source srcset="{webp_src}" type="image/webp">\n'
            f'          {img_tag}\n'
            f'        </picture>')

total_wrapped = 0
for html_path in sorted(glob.glob(os.path.join(SITE_DIR, '*.html'))):
    with open(html_path, 'r', encoding='utf-8') as f:
        original = f.read()

    result = original
    offset = 0
    wrapped_in_file = 0

    for m in IMG_PATTERN.finditer(original):
        attrs = m.group(1)
        src = get_src(attrs)
        if not src:
            continue

        # Check if this src references one of our target images
        matched_pair = None
        for orig_name, webp_name in pairs:
            if src.endswith('/' + orig_name) or src == orig_name:
                matched_pair = (orig_name, webp_name)
                break
        if not matched_pair:
            continue

        orig_name, webp_name = matched_pair
        webp_src = src.replace(orig_name, webp_name)

        # Adjust position for any earlier replacements
        adj_start = m.start() + offset
        adj_end = m.end() + offset

        # Check if already in a picture tag
        if needs_picture_wrap(result, adj_start):
            continue

        img_tag = m.group(0)
        replacement = wrap_in_picture(img_tag, src, webp_src)
        result = result[:adj_start] + replacement + result[adj_end:]
        offset += len(replacement) - len(img_tag)
        wrapped_in_file += 1

    if wrapped_in_file > 0:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f'  {os.path.basename(html_path)}: wrapped {wrapped_in_file} images')
        total_wrapped += wrapped_in_file

print(f'\nDone — {total_wrapped} images wrapped in <picture> tags across all pages.')
