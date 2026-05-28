#!/home/matt/claude/.venv/bin/python3
"""
Comprehensive fix for the 5 new pages and all sidebars.

1. Add 5 new pages to sidebar menu on all 27 existing pages.
2. Fix 5 new pages: correct navbar + add full sidebar + fix layout.
"""

import re
from pathlib import Path

WEBSITE_DIR = Path('/home/matt/claude/websites/tyneham/website')

NEW_PAGES = [
    'ghost-village.html',
    'visiting-tyneham.html',
    'tyneham-photos.html',
    'lulworth-range-walks.html',
    'gad-cliff.html',
]

# Pages with no sidebar
SKIP_SIDEBAR = {'index.html', 'privacy.html', 'thank-you.html', '404.html'}

# -----------------------------------------------------------------------
# Extract correct navbar from after-the-evacuation.html
# -----------------------------------------------------------------------
source = (WEBSITE_DIR / 'after-the-evacuation.html').read_text()

nav_match = re.search(
    r'(<nav class="navbar navbar-expand-lg navbar-dark bg-dark">.*?</nav>)',
    source, re.DOTALL
)
if not nav_match:
    raise SystemExit('ERROR: could not extract navbar from after-the-evacuation.html')
CORRECT_NAVBAR = nav_match.group(1)

# -----------------------------------------------------------------------
# Full correct sidebar HTML
# -----------------------------------------------------------------------
SIDEBAR_HTML = """\
      <!-- Side widgets -->
      <div class="col-lg-4">

        <!-- Square Ad (Desktop only) -->
        <div class="card my-5 d-none d-lg-block">
          <div class="card-body text-center py-5">
            <a href="tyneham-remembered.html">
              <img src="assets/tyneham-dvd-cover.webp" class="img-fluid rounded" alt="Tyneham Remembered Documentary" loading="lazy" width="300" height="288">
            </a>
          </div>
        </div>

        <!-- Tyneham Open or Closed -->
        <div class="container my-5 pt-4 text-center mb-5">
          <div id="tynehamStatusSidebar" class="alert fs-3 fw-bold py-5 shadow-lg border-0 rounded-4 mb-4" role="alert"
            style="min-height: 120px;">
            <div class="spinner-border spinner-border-lg text-primary mb-3 d-none" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <div id="statusContent">
              Checking if Tyneham is open today...
            </div>
          </div>
          <div class="row justify-content-center">
            <div class="col-md-8">
              <p class="fs-5 text-muted mb-4">
                <strong>Tyneham Village opening times powered by official MOD 2026 schedule</strong><br>
                Hours: Typically 9am to dusk (exhibitions 10am-4pm). <a
                  href="https://www.gov.uk/government/publications/lulworth-access-times" target="_blank"
                  rel="noopener">Always confirm via GOV.UK</a> or call <a href="tel:+441929404714">01929 404714</a>.
              </p>
              <div class="text-center">
                <a href="opening_times.html" class="btn btn-warning btn-lg">View Full 2026 Calendar</a>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar: In Tyneham Village -->
        <div class="card my-5 shadow-sm">
          <div class="card-header bg-primary text-white">
            <strong>In Tyneham Village</strong>
          </div>
          <div class="card-body p-0">
            <ul class="list-unstyled mb-0" id="sidebar-menu">
              <li class="border-bottom menu-item" data-page="opening_times.html">
                <a href="opening_times.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Opening Times 2026</a>
              </li>
              <li class="border-bottom menu-item" data-page="visiting-tyneham.html">
                <a href="visiting-tyneham.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Visiting Tyneham</a>
              </li>
              <li class="border-bottom menu-item" data-page="tyneham_village_location.html">
                <a href="tyneham_village_location.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Where is Tyneham?</a>
              </li>
              <li class="border-bottom menu-item" data-page="tyneham-remembered.html">
                <a href="tyneham-remembered.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">The Tyneham Remembered Documentary</a>
              </li>
              <li class="border-bottom menu-item" data-page="map_of_tyneham.html">
                <a href="map_of_tyneham.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Tyneham Village Map</a>
              </li>
              <li class="border-bottom menu-item" data-page="history_of_tyneham.html">
                <a href="history_of_tyneham.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Tyneham History</a>
              </li>
              <li class="border-bottom menu-item" data-page="the_post_office.html">
                <a href="the_post_office.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">The Post Office</a>
              </li>
              <li class="border-bottom menu-item" data-page="the_bond_family.html">
                <a href="the_bond_family.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">The Bond Family of Tyneham</a>
              </li>
              <li class="border-bottom menu-item" data-page="the-rectory.html">
                <a href="the-rectory.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">The Rectory</a>
              </li>
              <li class="border-bottom menu-item" data-page="tyneham-school.html">
                <a href="tyneham-school.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Tyneham School</a>
              </li>
              <li class="border-bottom menu-item" data-page="tyneham-church.html">
                <a href="tyneham-church.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Tyneham Church</a>
              </li>
              <li class="border-bottom menu-item" data-page="camp-at-tyneham.html">
                <a href="camp-at-tyneham.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Camping at Tyneham</a>
              </li>
              <li class="border-bottom menu-item" data-page="tyneham-house.html">
                <a href="tyneham-house.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Tyneham House</a>
              </li>
              <li class="border-bottom menu-item" data-page="tyneham-photos.html">
                <a href="tyneham-photos.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Tyneham Village Photos</a>
              </li>
              <li class="border-bottom menu-item" data-page="the-church-door-note.html">
                <a href="the-church-door-note.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">The Church Door Note</a>
              </li>
              <li class="border-bottom menu-item" data-page="after-the-evacuation.html">
                <a href="after-the-evacuation.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">After the Evacuation</a>
              </li>
              <li class="border-bottom menu-item" data-page="the-campaign-to-return.html">
                <a href="the-campaign-to-return.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">The Campaign to Return</a>
              </li>
              <li class="border-bottom menu-item" data-page="ghost-village.html">
                <a href="ghost-village.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Dorset's Ghost Village</a>
              </li>
            </ul>
          </div>
        </div>

        <!-- Sidebar: Near Tyneham -->
        <div class="card my-5 shadow-sm">
          <div class="card-header bg-primary text-white">
            <strong>Near Tyneham</strong>
          </div>
          <div class="card-body p-0">
            <ul class="list-unstyled mb-0" id="sidebar-menu-near">
              <li class="border-bottom menu-item" data-page="corfe-castle.html">
                <a href="corfe-castle.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Corfe Castle</a>
              </li>
              <li class="border-bottom menu-item" data-page="durdle-door.html">
                <a href="durdle-door.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Durdle Door</a>
              </li>
              <li class="border-bottom menu-item" data-page="lulworth-cove.html">
                <a href="lulworth-cove.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Lulworth Cove</a>
              </li>
              <li class="border-bottom menu-item" data-page="worbarrow-bay.html">
                <a href="worbarrow-bay.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Worbarrow Bay</a>
              </li>
              <li class="border-bottom menu-item" data-page="flowers-barrow.html">
                <a href="flowers-barrow.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Flower's Barrow</a>
              </li>
              <li class="border-bottom menu-item" data-page="kimmeridge-bay.html">
                <a href="kimmeridge-bay.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Kimmeridge Bay</a>
              </li>
              <li class="border-bottom menu-item" data-page="lulworth-range-walks.html">
                <a href="lulworth-range-walks.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Lulworth Range Walks</a>
              </li>
              <li class="border-bottom menu-item" data-page="gad-cliff.html">
                <a href="gad-cliff.html" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">Gad Cliff</a>
              </li>
            </ul>
          </div>
        </div>

      </div>"""

# -----------------------------------------------------------------------
# PART 1: Update sidebar on all existing pages
# -----------------------------------------------------------------------


def insert_after_page(content, target_page, new_item_page, new_item_label):
    """Insert a sidebar <li> item after the item for target_page, if not already present."""
    if f'data-page="{new_item_page}"' in content:
        return content  # already in sidebar
    # Match the <li>...</li> block for target_page regardless of indentation
    pattern = re.compile(
        r'([ \t]*<li\b[^>]*data-page="' + re.escape(target_page) + r'"[^>]*>.*?</li>)',
        re.DOTALL
    )
    m = pattern.search(content)
    if not m:
        return content
    # Detect indentation from the matched li
    indent = re.match(r'([ \t]*)', m.group(1)).group(1)
    inner = indent + '  '
    new_li = (
        f'\n{indent}<li class="border-bottom menu-item" data-page="{new_item_page}">\n'
        f'{inner}<a href="{new_item_page}" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">'
        f'{new_item_label}</a>\n'
        f'{indent}</li>'
    )
    return content[:m.end()] + new_li + content[m.end():]


existing_updated = 0
for page in sorted(WEBSITE_DIR.glob('*.html')):
    if page.name in SKIP_SIDEBAR or page.name in NEW_PAGES:
        continue
    content = page.read_text()
    original = content

    if 'sidebar-menu' in content:
        content = insert_after_page(content, 'opening_times.html', 'visiting-tyneham.html', 'Visiting Tyneham')
        content = insert_after_page(content, 'tyneham-house.html', 'tyneham-photos.html', 'Tyneham Village Photos')
        content = insert_after_page(content, 'the-campaign-to-return.html', 'ghost-village.html', "Dorset's Ghost Village")
        content = insert_after_page(content, 'kimmeridge-bay.html', 'lulworth-range-walks.html', 'Lulworth Range Walks')
        content = insert_after_page(content, 'lulworth-range-walks.html', 'gad-cliff.html', 'Gad Cliff')

    if content != original:
        page.write_text(content)
        print(f'  Sidebar updated: {page.name}')
        existing_updated += 1

print(f'\nPart 1 done: {existing_updated} existing pages updated.')

# -----------------------------------------------------------------------
# PART 2: Fix the 5 new pages (navbar + sidebar + layout)
# -----------------------------------------------------------------------
new_fixed = 0
for page_name in NEW_PAGES:
    page = WEBSITE_DIR / page_name
    content = page.read_text()
    original = content

    # 2a. Replace navbar
    content = re.sub(
        r'<!-- Responsive navbar -->\s*\n\s*<nav\b.*?</nav>|<nav class="navbar navbar-expand-lg navbar-dark bg-dark">.*?</nav>',
        CORRECT_NAVBAR,
        content, flags=re.DOTALL
    )

    # 2b. Fix row class
    content = content.replace(
        '<div class="row justify-content-center">',
        '<div class="row">'
    )

    # 2c. Insert sidebar: replace everything between </article> and <footer
    content = re.sub(
        r'</article>.*?(<footer)',
        '      </article>\n      </div>\n\n' + SIDEBAR_HTML + '\n\n    </div>\n  </div>\n\n  \\1',
        content, flags=re.DOTALL
    )

    if content != original:
        page.write_text(content)
        print(f'  New page fixed: {page_name}')
        new_fixed += 1
    else:
        print(f'  WARNING: no changes made to {page_name}')

print(f'\nPart 2 done: {new_fixed} new pages fixed.')
print(f'\nTotal: {existing_updated + new_fixed} files updated.')
