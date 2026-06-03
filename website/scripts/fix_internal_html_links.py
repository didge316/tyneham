#!/home/matt/claude/.venv/bin/python3
"""Strip .html extension from all internal href links across the site.

Leaves external links, anchors, and non-HTML links untouched.
"""
import re
import glob
import os

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pages that should keep .html in links (utility files, external, etc.)
SKIP_FILES = {'404.html', 'privacy.html', 'thank-you.html'}

# Pattern: href="something.html" or href="something.html#anchor"
# Must not start with http/https/mailto/# and must end with .html optionally followed by #anchor
INTERNAL_HTML_RE = re.compile(
    r'(href=")((?!https?://|mailto:|//)([^"]*?)\.html)(#[^"]*)?(")'
)

def fix_file(path):
    filename = os.path.basename(path)
    if filename in SKIP_FILES:
        return False

    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    def replace_match(m):
        prefix = m.group(1)      # href="
        full_path = m.group(2)   # path/to/page.html
        clean = m.group(3)       # path/to/page  (without .html)
        anchor = m.group(4) or ''  # #section (optional)
        suffix = m.group(5)      # "
        # Don't strip from sitemap.xml links or ads.txt etc
        if full_path.endswith('.xml') or full_path.endswith('.txt') or full_path.endswith('.csv'):
            return m.group(0)
        return f'{prefix}{clean}{anchor}{suffix}'

    updated = INTERNAL_HTML_RE.sub(replace_match, original)

    if updated != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(updated)
        count = original.count('.html"') - updated.count('.html"')
        print(f'  Fixed {count} links in {filename}')
        return True
    return False

changed = 0
for path in sorted(glob.glob(os.path.join(SITE_DIR, '*.html'))):
    if fix_file(path):
        changed += 1

print(f'\nDone — {changed} files updated.')
