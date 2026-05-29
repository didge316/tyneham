#!/home/matt/claude/.venv/bin/python3
"""Remove all dark mode toggle buttons from every HTML page."""

import re
from pathlib import Path

ROOT = Path('/home/matt/claude/websites/tyneham/website')

# Mobile button (outside collapse, before navbar-toggler)
MOBILE_BTN = '      <button class="dark-mode-btn btn btn-sm btn-outline-light px-2 me-2 d-lg-none" type="button" aria-label="Toggle dark mode">🌙</button>\n'

# Desktop button (inside nav list)
DESKTOP_LI = '          <li class="nav-item ms-lg-1">\n            <button class="dark-mode-btn btn btn-sm btn-outline-light px-2 d-none d-lg-block" type="button" aria-label="Toggle dark mode">🌙</button>\n          </li>\n'

changed = 0
for html_file in sorted(ROOT.glob('*.html')):
    text = html_file.read_text(encoding='utf-8')
    new = text.replace(MOBILE_BTN, '').replace(DESKTOP_LI, '')
    if new != text:
        html_file.write_text(new, encoding='utf-8')
        changed += 1
        print(f'  ✓ {html_file.name}')

print(f'\nChanged: {changed}')
