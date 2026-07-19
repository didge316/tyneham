#!/usr/bin/env python3
"""
Remaining HIGH fixes:
1. Convert orphaned <img> with .jpg src to <picture> with WebP fallback
2. Fix heading hierarchy (h3→h2) on opening-times and tyneham-school
3. Page-specific OG images for pages using the generic fallback
"""

import re
from pathlib import Path

ROOT = Path('/home/matt/projects/tyneham/website')
ASSETS = ROOT / 'assets'

# Which assets exist?
existing_webps = {p.name for p in ASSETS.glob('*.webp')}
existing_webps.update({p.name for p in ASSETS.glob('*.png')})
existing_jpgs = {p.name for p in ASSETS.glob('*.jpg')}


def jpg_to_webp(jpg_name):
    """Given 'foo.jpg', return 'foo.webp' if it exists."""
    webp = jpg_name[:-4] + '.webp'
    if webp in existing_webps:
        return webp
    return None


def convert_img_to_picture(text, img_match):
    """Wrap a single <img> tag in a <picture> element with WebP source."""
    # img_match is a re.Match object for the full <img...> tag
    img_tag = img_match.group(0)
    # Extract src attribute
    src_match = re.search(r'src="([^"]+)"', img_tag)
    if not src_match:
        return img_tag  # can't process

    src = src_match.group(1)
    # Get just the filename
    fname = src.rsplit('/', 1)[-1]
    if not fname.endswith('.jpg'):
        return img_tag

    webp_fname = jpg_to_webp(fname)
    if not webp_fname:
        return img_tag  # no WebP exists

    webp_path = '/assets/' + webp_fname

    # Preserve indentation by looking at preceding whitespace
    indent = img_match.group(1) if img_match.lastindex else ''

    # Build picture element — keep the existing img attributes but remove fetchpriority
    # (fetchpriority goes on the first source/img in picture, we keep it on img)
    picture = (
        f'{indent}<picture>'
        f'<source srcset="{webp_path}" type="image/webp">'
        f'{img_tag}'
        f'</picture>'
    )
    return picture


def fix_picture_elements(path):
    """Wrap bare <img src=*.jpg> in <picture> if WebP exists, unless already in <picture>."""
    text = path.read_text(encoding='utf-8')
    original = text
    count = 0

    # Find <img> tags that are NOT inside a <picture> block
    # Strategy: find <picture>...</picture> blocks, mark them, then process remaining imgs

    # Split on <picture> and track picture blocks
    parts = re.split(r'(<picture>.*?</picture>)', text, flags=re.DOTALL)
    result = []
    for i, part in enumerate(parts):
        if part.startswith('<picture>'):
            result.append(part)  # already in picture — skip
        else:
            # This is outside any <picture> — process <img> tags here
            def replace_img(m):
                return convert_img_to_picture(part, m)

            new_part, n = re.subn(
                r'([ \t]*)<img\b[^>]*src="[^"]*\.jpg"[^>]*>',
                convert_img_to_picture_text,
                part
            )
            result.append(new_part)
            count += 1  # count each img processed

    return ''.join(result), text != ''.join(result)


def convert_img_to_picture_text(match):
    """Helper to convert <img> to <picture> keeping indentation."""
    img_tag = match.group(0)
    src_match = re.search(r'src="([^"]*\.jpg)"', img_tag)
    if not src_match:
        return img_tag

    jpg_fname = src_match.group(1).rsplit('/', 1)[-1]
    webp_fname = jpg_to_webp(jpg_fname)
    if not webp_fname:
        return img_tag

    webp_path = '/assets/' + webp_fname
    # Strip any leading whitespace for the image tag indentation
    stripped = img_tag.lstrip()
    indent = img_tag[:len(img_tag) - len(stripped)]

    return f'{indent}<picture><source srcset="{webp_path}" type="image/webp">{stripped}</picture>'


# --- Fix 2: Heading hierarchy ---
def fix_headings(text):
    """Convert h3→h2 on pages with only 1 h2 but multiple h3s."""
    # On opening-times: h2=1, h3=5 → convert h3s to h2s for proper hierarchy
    # On tyneham-school: h2=1, h3=3
    # Strategy: if page has 1 h2 and >2 h3s, convert all h3s to h2s

    h2_count = len(re.findall(r'<h2\b', text))
    h3_count = len(re.findall(r'<h3\b', text))

    if h2_count <= 1 and h3_count >= 2:
        text = text.replace('<h3 class="fw-bold mt-4">', '<h2 class="fw-bold mt-5">')
        text = text.replace('</h3>', '</h2>')
        return text, True

    return text, False


# --- Fix 3: Page-specific OG images ---
# Pages and their best hero image
PAGE_OG_IMAGES = {
    'index.html': '/assets/tyneham-village-early-photo.webp',
    'opening-times': '/assets/worbarrow-bay-today.webp',
    'visiting-tyneham': '/assets/tyneham-village.webp',
    'history-of-tyneham': '/assets/tyneham-village-early-photo.webp',
    'tyneham-church': '/assets/tyneham-church.webp',
    'tyneham-house': '/assets/tyneham-house.webp',
    'tyneham-school': '/assets/school.webp',
    'the-post-office': '/assets/The-Post-Office.webp',
    'the-rectory': '/assets/tyneham-rectory.webp',
    'the-bond-family': '/assets/john-bond.webp',
    'the-church-door-note': '/assets/note-left-on-church-door.webp',
    'after-the-evacuation': '/assets/tyneham-village-c1930.webp',
    'the-campaign-to-return': '/assets/tyneham-village-early-photo.webp',
    'ghost-village': '/assets/tyneham-village.webp',
    'map-of-tyneham': '/assets/tyneham-village-map.webp',
    'tyneham-village-location': '/assets/tyneham-location.webp',
    'tyneham-in-wartime': '/assets/wafs-tyneham-2.webp',
    'tyneham-photos': '/assets/tyneham-collage.webp',
    'tyneham-remembered': '/assets/tyneham-dvd-cover.webp',
    'camp-at-tyneham': '/assets/camping_near_tyneham.webp',
    'worbarrow-bay': '/assets/worbarrow-bay.webp',
    'flowers-barrow': '/assets/flowers-barrow.webp',
    'kimmeridge-bay': '/assets/kimmeridge_bay.webp',
    'gad-cliff': '/assets/kimmeridge-gad-cliff-view.webp',
    'lulworth-cove': '/assets/lulworth-cove.webp',
    'durdle-door': '/assets/durdle-door-closeup.webp',
    'corfe-castle': '/assets/corfe-castle.webp',
    'lulworth-range-walks': '/assets/lulworth-ranges-coast.webp',
    'wildlife-at-tyneham': '/assets/sika-stag-crop.webp',
    'about': '/assets/tyneham-village.webp',
    'tyneham-walk': '/assets/lulworth-ranges-coast.webp',
    'corfe-castle-walk': '/assets/corfe-castle.webp',
    'kimmeridge-tyneham-walk': '/assets/hounds-tout-worbarrow-bay.webp',
}

GENERIC_OG = '/assets/tyneham-village-early-photo.webp'
GENERIC_OG_ABS = 'https://tynehamvillage.org' + GENERIC_OG


def fix_og_image(path, image_path):
    """Replace generic OG image with page-specific one."""
    text = path.read_text(encoding='utf-8')
    original = text
    new_abs = 'https://tynehamvillage.org' + image_path

    # Replace in og:image and twitter:image
    text = text.replace(
        f'property="og:image" content="{GENERIC_OG_ABS}"',
        f'property="og:image" content="{new_abs}"',
    )
    text = text.replace(
        f'name="twitter:image" content="{GENERIC_OG_ABS}"',
        f'name="twitter:image" content="{new_abs}"',
    )
    # Also replace relative paths
    text = text.replace(
        f'property="og:image" content="{GENERIC_OG}"',
        f'property="og:image" content="{image_path}"',
    )
    text = text.replace(
        f'name="twitter:image" content="{GENERIC_OG}"',
        f'name="twitter:image" content="{image_path}"',
    )
    # Also try catching variations (other generic images)
    other_generics = [
        '/assets/tyneham-village.jpg',
        '/assets/tyneham-village.webp',
    ]
    for g in other_generics:
        g_abs = 'https://tynehamvillage.org' + g
        text = text.replace(
            f'property="og:image" content="{g_abs}"',
            f'property="og:image" content="{new_abs}"',
        )
        text = text.replace(
            f'property="og:image" content="{g}"',
            f'property="og:image" content="{image_path}"',
        )
        text = text.replace(
            f'name="twitter:image" content="{g_abs}"',
            f'name="twitter:image" content="{new_abs}"',
        )
        text = text.replace(
            f'name="twitter:image" content="{g}"',
            f'name="twitter:image" content="{image_path}"',
        )

    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


if __name__ == '__main__':
    print('=== 1. Converting <img> to <picture> with WebP ===')
    pages_with_jpg_imgs = [
        'durdle-door', 'ghost-village', 'history-of-tyneham',
        'tyneham-church', 'tyneham-house', 'tyneham-photos',
        'tyneham-school', 'tyneham-village-location',
        'worbarrow-bay',
    ]

    for folder in pages_with_jpg_imgs:
        path = ROOT / folder / 'index.html'
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        original = text
        count = 0

        # Find all <img> tags with .jpg that are NOT inside <picture>
        # Use a different approach: split into picture/non-picture segments
        segments = re.split(r'(<picture>.*?</picture>)', text, flags=re.DOTALL)
        new_segments = []
        for seg in segments:
            if seg.startswith('<picture>'):
                new_segments.append(seg)
            else:
                new_seg, n = re.subn(
                    r'(<img\b[^>]*src="[^"]*\.jpg"[^>]*>)',
                    convert_img_to_picture_text,
                    seg
                )
                new_segments.append(new_seg)
                count += (1 if n else 0)

        if count:
            path.write_text(''.join(new_segments), encoding='utf-8')
            print(f'  ✓ {folder}: {count} images wrapped')
        else:
            print(f'  · {folder}: no images to wrap')

    print()
    print('=== 2. Fixing heading hierarchy ===')
    for folder in ['opening-times', 'tyneham-school']:
        path = ROOT / folder / 'index.html'
        text = path.read_text(encoding='utf-8')
        new_text, changed = fix_headings(text)
        if changed:
            path.write_text(new_text, encoding='utf-8')
            print(f'  ✓ {folder}: h3→h2 converted')
        else:
            print(f'  · {folder}: already correct')

    print()
    print('=== 3. Page-specific OG images ===')
    fixed = 0
    for folder, img in PAGE_OG_IMAGES.items():
        if folder in ['about', 'privacy', 'contact', 'thank-you']:
            continue  # low priority pages
        path = ROOT / folder / 'index.html' if '/' not in folder else ROOT / folder
        if not path.exists():
            path = ROOT / folder / 'index.html'
        if not path.exists():
            continue
        if fix_og_image(path, img):
            print(f'  ✓ {folder}')
            fixed += 1
        else:
            print(f'  · {folder} (no change)')
    print(f'\n  {fixed} pages updated')

    print()
    print('Done.')
