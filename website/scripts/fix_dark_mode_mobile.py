#!/home/matt/claude/.venv/bin/python3
"""
fix_dark_mode_mobile.py — Fix dark mode toggle visibility on mobile.

Two changes per page:
1. Add a mobile-only .dark-mode-btn button before the navbar-toggler (always visible).
2. Convert the existing in-nav button from id="darkModeToggle" to class="dark-mode-btn d-none d-lg-block".
"""

from pathlib import Path

ROOT = Path('/home/matt/claude/websites/tyneham/website')

# --- Change 1: insert mobile button before the navbar-toggler ---
TOGGLER_START = '      <button class="navbar-toggler"'
MOBILE_BTN = '      <button class="dark-mode-btn btn btn-sm btn-outline-light px-2 me-2 d-lg-none" type="button" aria-label="Toggle dark mode">🌙</button>\n'

# --- Change 2: update the in-nav button ---
OLD_NAV_BTN = '<button id="darkModeToggle" class="btn btn-sm btn-outline-light px-2" type="button" aria-label="Toggle dark mode">🌙</button>'
NEW_NAV_BTN = '<button class="dark-mode-btn btn btn-sm btn-outline-light px-2 d-none d-lg-block" type="button" aria-label="Toggle dark mode">🌙</button>'

changed = 0
skipped = 0

for html_file in sorted(ROOT.glob('*.html')):
    text = html_file.read_text(encoding='utf-8')

    if MOBILE_BTN.strip() in text:
        skipped += 1
        print(f'  · {html_file.name} (already patched)')
        continue

    if TOGGLER_START not in text or OLD_NAV_BTN not in text:
        print(f'  ? {html_file.name} (pattern not found — skipping)')
        continue

    # Insert mobile button before the toggler line
    text = text.replace(TOGGLER_START, MOBILE_BTN + TOGGLER_START, 1)
    # Update the in-nav button
    text = text.replace(OLD_NAV_BTN, NEW_NAV_BTN, 1)

    html_file.write_text(text, encoding='utf-8')
    changed += 1
    print(f'  ✓ {html_file.name}')

print()
print(f'Changed: {changed}  Skipped: {skipped}')
