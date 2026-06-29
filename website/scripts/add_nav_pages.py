#!/home/matt/claude/.venv/bin/python3
"""Add tyneham-in-wartime, corfe-castle-walk, kimmeridge-tyneham-walk to nav + sidebar."""

import os
import glob

WEBSITE_DIR = os.path.join(os.path.dirname(__file__), "..")

# Exact strings to find and replace
CHANGES = [
    # 1. History nav dropdown: add tyneham-in-wartime after after-the-evacuation
    (
        '<li><a class="dropdown-item" href="after-the-evacuation">After the Evacuation</a></li>\n'
        '              <li><a class="dropdown-item" href="the-campaign-to-return">The Campaign to Return</a></li>',
        '<li><a class="dropdown-item" href="after-the-evacuation">After the Evacuation</a></li>\n'
        '              <li><a class="dropdown-item" href="tyneham-in-wartime">Tyneham in Wartime</a></li>\n'
        '              <li><a class="dropdown-item" href="the-campaign-to-return">The Campaign to Return</a></li>',
    ),
    # 2. Walks nav dropdown: add corfe-castle-walk and kimmeridge-tyneham-walk after tyneham-walk
    (
        '<li><a class="dropdown-item" href="tyneham-walk">Tyneham Circular Walk</a></li>\n'
        '            </ul>\n'
        '          </li>\n'
        '\n'
        '          <li class="nav-item ms-lg-3">',
        '<li><a class="dropdown-item" href="tyneham-walk">Tyneham Circular Walk</a></li>\n'
        '              <li><a class="dropdown-item" href="corfe-castle-walk">Corfe Castle Circular Walk</a></li>\n'
        '              <li><a class="dropdown-item" href="kimmeridge-tyneham-walk">Kimmeridge to Tyneham Walk</a></li>\n'
        '            </ul>\n'
        '          </li>\n'
        '\n'
        '          <li class="nav-item ms-lg-3">',
    ),
    # 3. Sidebar history: add tyneham-in-wartime after after-the-evacuation
    (
        '<li class="border-bottom menu-item" data-page="after-the-evacuation.html">\n'
        '                <a href="after-the-evacuation" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">After the Evacuation</a>\n'
        '              </li>\n'
        '              <li class="border-bottom menu-item" data-page="the-campaign-to-return.html">',
        '<li class="border-bottom menu-item" data-page="after-the-evacuation.html">\n'
        '                <a href="after-the-evacuation" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">After the Evacuation</a>\n'
        '              </li>\n'
        '              <li class="border-bottom menu-item" data-page="tyneham-in-wartime.html">\n'
        '                <a href="tyneham-in-wartime" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Tyneham in Wartime</a>\n'
        '              </li>\n'
        '              <li class="border-bottom menu-item" data-page="the-campaign-to-return.html">',
    ),
    # 4. Sidebar walks: add corfe-castle-walk and kimmeridge-tyneham-walk after tyneham-walk
    (
        '<li class="border-bottom menu-item" data-page="tyneham-walk.html">\n'
        '                <a href="tyneham-walk" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Tyneham Circular Walk</a>\n'
        '              </li>\n'
        '            </ul>',
        '<li class="border-bottom menu-item" data-page="tyneham-walk.html">\n'
        '                <a href="tyneham-walk" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Tyneham Circular Walk</a>\n'
        '              </li>\n'
        '              <li class="border-bottom menu-item" data-page="corfe-castle-walk.html">\n'
        '                <a href="corfe-castle-walk" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Corfe Castle Circular Walk</a>\n'
        '              </li>\n'
        '              <li class="border-bottom menu-item" data-page="kimmeridge-tyneham-walk.html">\n'
        '                <a href="kimmeridge-tyneham-walk" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Kimmeridge to Tyneham Walk</a>\n'
        '              </li>\n'
        '            </ul>',
    ),
]

html_files = sorted(glob.glob(os.path.join(WEBSITE_DIR, "*.html")))
modified = 0

for fpath in html_files:
    with open(fpath, "r", encoding="utf-8") as f:
        original = f.read()

    updated = original
    for old, new in CHANGES:
        updated = updated.replace(old, new)

    if updated != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(updated)
        fname = os.path.basename(fpath)
        # Count which changes applied
        applied = [i + 1 for i, (old, new) in enumerate(CHANGES) if old not in original or new in updated and old not in updated]
        print(f"  {fname}")
        modified += 1

print(f"\nDone — {modified} files updated.")
