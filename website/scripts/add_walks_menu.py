#!/home/matt/claude/.venv/bin/python3
"""
add_walks_menu.py — Add Walks dropdown to nav + sidebar; move Lulworth Range Walks into it.

Changes applied to all *.html files:
  Navbar:
    - Remove Lulworth Range Walks from Near Tyneham dropdown
    - Add new Walks dropdown (before About) containing Lulworth Range Walks
  Sidebar:
    - Remove Lulworth Range Walks <li> from sidebar-menu-near
    - Add new Walks sidebar card (after Near Tyneham card) containing Lulworth Range Walks
"""

import re
from pathlib import Path

ROOT = Path('/home/matt/claude/websites/tyneham/website')

# Navbar: exact string to remove from Near Tyneham dropdown
NAV_LULWORTH_REMOVE = (
    '              <li><a class="dropdown-item" href="lulworth-range-walks">'
    'Lulworth Range Walks</a></li>\n'
)

# Navbar: Walks dropdown to insert before About
WALKS_NAV_DROPDOWN = (
    '          <!-- Walks dropdown -->\n'
    '          <li class="nav-item dropdown">\n'
    '            <button class="nav-link dropdown-toggle" type="button"'
    ' data-bs-toggle="dropdown" aria-expanded="false">\n'
    '              Walks\n'
    '            </button>\n'
    '            <ul class="dropdown-menu dropdown-menu-end">\n'
    '              <li><a class="dropdown-item" href="lulworth-range-walks">'
    'Lulworth Range Walks</a></li>\n'
    '            </ul>\n'
    '          </li>\n'
    '\n'
    '          '
)

# About nav anchor — insert Walks dropdown immediately before this
ABOUT_NAV_ANCHOR = '<li class="nav-item">\n            <a class="nav-link" href="about">About</a>'

# Sidebar: exact <li> block to remove from sidebar-menu-near
SIDEBAR_LULWORTH_REMOVE = (
    '              <li class="border-bottom menu-item" data-page="lulworth-range-walks.html">\n'
    '                <a href="lulworth-range-walks" class="d-block px-4 py-3'
    ' text-decoration-none text-dark hover-bg-light">Lulworth Range Walks</a>\n'
    '              </li>\n'
)


def make_walks_sidebar_card(indent):
    """Return the Walks sidebar card HTML with matching outer indentation."""
    return (
        f'\n\n{indent}<!-- Sidebar: Walks -->\n'
        f'{indent}<div class="card my-5 shadow-sm">\n'
        f'{indent}    <div class="card-header bg-primary text-white">\n'
        f'{indent}        <strong>Walks</strong>\n'
        f'{indent}    </div>\n'
        f'{indent}    <div class="card-body p-0">\n'
        f'{indent}        <ul class="list-unstyled mb-0" id="sidebar-menu-walks">\n'
        f'              <li class="border-bottom menu-item" data-page="lulworth-range-walks.html">\n'
        f'                <a href="lulworth-range-walks" class="d-block px-4 py-3'
        f' text-decoration-none text-dark hover-bg-light">Lulworth Range Walks</a>\n'
        f'              </li>\n'
        f'{indent}        </ul>\n'
        f'{indent}    </div>\n'
        f'{indent}</div>'
    )


def get_near_tyneham_indent(text):
    """Capture the leading whitespace of the Near Tyneham sidebar comment."""
    m = re.search(r'^([ \t]*)<!-- Sidebar: Near Tyneham -->', text, re.MULTILINE)
    return m.group(1) if m else '    '


def insert_walks_sidebar(text):
    """Insert the Walks sidebar card after the Near Tyneham card."""
    indent = get_near_tyneham_indent(text)

    # Find sidebar-menu-near
    near_pos = text.find('id="sidebar-menu-near"')
    if near_pos == -1:
        return text

    # Find gad-cliff (last item in Near Tyneham after lulworth removal)
    gad_pos = text.find('data-page="gad-cliff.html"', near_pos)
    if gad_pos == -1:
        return text

    # Step through: close the gad-cliff </li>, </ul>, card-body </div>, card </div>
    pos = text.find('</li>', gad_pos) + 5     # after gad-cliff </li>
    pos = text.find('</ul>', pos) + 5         # after </ul> (closes sidebar-menu-near)
    pos = text.find('</div>', pos) + 6        # after </div> (closes card-body)
    pos = text.find('</div>', pos) + 6        # after </div> (closes card)

    walks_card = make_walks_sidebar_card(indent)
    return text[:pos] + walks_card + text[pos:]


def fix_file(path):
    text = path.read_text(encoding='utf-8')
    original = text
    changed_nav = changed_sidebar = False

    # --- Navbar ---
    if NAV_LULWORTH_REMOVE in text:
        text = text.replace(NAV_LULWORTH_REMOVE, '')
        changed_nav = True

    if ABOUT_NAV_ANCHOR in text and '<!-- Walks dropdown -->' not in text:
        text = text.replace(ABOUT_NAV_ANCHOR, WALKS_NAV_DROPDOWN + ABOUT_NAV_ANCHOR)
        changed_nav = True

    # --- Sidebar ---
    if SIDEBAR_LULWORTH_REMOVE in text:
        text = text.replace(SIDEBAR_LULWORTH_REMOVE, '')
        text = insert_walks_sidebar(text)
        changed_sidebar = True

    if text != original:
        path.write_text(text, encoding='utf-8')

    return changed_nav, changed_sidebar


nav_count = sidebar_count = files_changed = 0

for html_file in sorted(ROOT.glob('*.html')):
    n, s = fix_file(html_file)
    if n or s:
        files_changed += 1
        nav_count += n
        sidebar_count += s
        print(f'  ✓ {html_file.name}  nav={n} sidebar={s}')
    else:
        print(f'  · {html_file.name}')

print()
print('=== Summary ===')
print(f'  files changed : {files_changed}')
print(f'  nav updated   : {nav_count}')
print(f'  sidebar added : {sidebar_count}')
