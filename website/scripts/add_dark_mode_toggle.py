#!/home/matt/claude/.venv/bin/python3
"""
add_dark_mode_toggle.py — Add dark mode toggle button to every page navbar.

Inserts a moon/sun toggle button as the last item in the navbar's nav list,
immediately before the closing </ul> of the navbar (before </div></div></nav>).
Skips files that already have darkModeToggle.
"""

from pathlib import Path

ROOT = Path('/home/matt/claude/websites/tyneham/website')

TOGGLE_BUTTON = "          <li class=\"nav-item ms-lg-1\">\n            <button id=\"darkModeToggle\" class=\"btn btn-sm btn-outline-light px-2\" type=\"button\" aria-label=\"Toggle dark mode\">🌙</button>\n          </li>\n"

# The Donate button is the last item; we insert the toggle right after it.
ANCHOR = "          <li class='nav-item ms-lg-2'>\n            <a class='nav-link btn btn-warning btn-sm px-3 text-dark fw-semibold' href='#' data-bs-toggle='modal' data-bs-target='#donateModal'>&#9829; Donate</a>\n          </li>\n        </ul>"

REPLACEMENT = "          <li class='nav-item ms-lg-2'>\n            <a class='nav-link btn btn-warning btn-sm px-3 text-dark fw-semibold' href='#' data-bs-toggle='modal' data-bs-target='#donateModal'>&#9829; Donate</a>\n          </li>\n" + TOGGLE_BUTTON + "        </ul>"

changed = 0
skipped = 0
not_found = 0

for html_file in sorted(ROOT.glob('*.html')):
    text = html_file.read_text(encoding='utf-8')

    if 'darkModeToggle' in text:
        skipped += 1
        print(f"  · {html_file.name} (already has toggle)")
        continue

    if ANCHOR not in text:
        not_found += 1
        print(f"  ? {html_file.name} (anchor not found — skipping)")
        continue

    new_text = text.replace(ANCHOR, REPLACEMENT, 1)
    html_file.write_text(new_text, encoding='utf-8')
    changed += 1
    print(f"  ✓ {html_file.name}")

print()
print(f"Changed: {changed}  Skipped: {skipped}  Anchor-not-found: {not_found}")
