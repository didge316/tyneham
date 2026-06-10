#!/home/matt/claude/.venv/bin/python3
"""Render the canonical navbar + sidebar from menu_config and inject it into every
website/*.html page.

This is the single engine that keeps the duplicated menus in sync. It is
idempotent: run it once to standardise the whole site, and re-run it after every
page add/remove. Pages with no sidebar (utility pages) keep their navbar updated
and simply skip the sidebar replacement.

Usage:
    render_menus.py            # apply to all pages
    render_menus.py --dry-run  # show what would change, write nothing
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import menu_config as mc

WEBSITE = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Builders — all menu HTML is generated here so indentation/format is uniform.
# ---------------------------------------------------------------------------

def _dropdown_items(items):
    return "\n".join(
        f'              <li><a class="dropdown-item" href="{slug}">{label}</a></li>'
        for slug, label in items
    )


def build_navbar():
    """The full <nav>...</nav> block, generated from menu_config."""
    return f"""<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <a class="navbar-brand" href="/">TynehamVillage.org</a>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ms-auto">

          <!-- The Village dropdown -->
          <li class="nav-item dropdown">
            <button class="nav-link dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
              The Village
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
{_dropdown_items(mc.VILLAGE)}
            </ul>
          </li>

          <!-- History dropdown -->
          <li class="nav-item dropdown">
            <button class="nav-link dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
              History
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
{_dropdown_items(mc.HISTORY)}
            </ul>
          </li>

          <!-- Near Tyneham dropdown -->
          <li class="nav-item dropdown">
            <button class="nav-link dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
              Near Tyneham
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
{_dropdown_items(mc.NEAR)}
            </ul>
          </li>

          <!-- Walks dropdown -->
          <li class="nav-item dropdown">
            <button class="nav-link dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
              Walks
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
{_dropdown_items(mc.WALKS)}
            </ul>
          </li>

          <li class="nav-item">
            <a class="nav-link" href="about">About</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="contact">Contact</a>
          </li>
          <li class='nav-item ms-lg-2'>
            <a class='nav-link btn btn-warning btn-sm px-3 text-dark fw-semibold' href='#' data-bs-toggle='modal' data-bs-target='#donateModal'>&#9829; Donate</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>"""


def _sidebar_items(items):
    out = []
    for slug, label in items:
        out.append(
            f'              <li class="border-bottom menu-item" data-page="{slug}.html">\n'
            f'                <a href="{slug}" class="d-block px-4 py-3 text-decoration-none text-dark hover-bg-light">{label}</a>\n'
            f'              </li>'
        )
    return "\n".join(out)


def build_sidebar(ul_id, items):
    """A sidebar <ul ...>...</ul> block. No active classes — js/scripts.js
    highlightSidebar() adds bg-light/fw-bold at runtime by matching data-page."""
    return (
        f'<ul class="list-unstyled mb-0" id="{ul_id}">\n'
        f'{_sidebar_items(items)}\n'
        f'            </ul>'
    )


# ---------------------------------------------------------------------------
# Injection
# ---------------------------------------------------------------------------

NAV_RE = re.compile(r'<nav class="navbar[^>]*>.*?</nav>', re.DOTALL)
SIDEBAR_VILLAGE_RE = re.compile(r'<ul[^>]*id="sidebar-menu">.*?</ul>', re.DOTALL)
SIDEBAR_NEAR_RE = re.compile(r'<ul[^>]*id="sidebar-menu-near">.*?</ul>', re.DOTALL)
SIDEBAR_WALKS_RE = re.compile(r'<ul[^>]*id="sidebar-menu-walks">.*?</ul>', re.DOTALL)
BODY_RE = re.compile(r'(<body[^>]*>)')


def render_page(html):
    """Return (new_html, changed_regions:list[str]) for one page's HTML."""
    changed = []

    navbar = build_navbar()
    if NAV_RE.search(html):
        new_html, n = NAV_RE.subn(lambda m: navbar, html, count=1)
        if new_html != html:
            changed.append("navbar")
        html = new_html
    elif BODY_RE.search(html):
        # No navbar present (e.g. 404) — insert one right after <body>.
        html = BODY_RE.sub(lambda m: m.group(1) + "\n\n" + navbar + "\n", html, count=1)
        changed.append("navbar(inserted)")

    village = build_sidebar("sidebar-menu", mc.VILLAGE + mc.HISTORY)
    if SIDEBAR_VILLAGE_RE.search(html):
        new_html = SIDEBAR_VILLAGE_RE.sub(lambda m: village, html, count=1)
        if new_html != html:
            changed.append("sidebar-village")
        html = new_html

    near = build_sidebar("sidebar-menu-near", mc.NEAR)
    if SIDEBAR_NEAR_RE.search(html):
        new_html = SIDEBAR_NEAR_RE.sub(lambda m: near, html, count=1)
        if new_html != html:
            changed.append("sidebar-near")
        html = new_html

    walks = build_sidebar("sidebar-menu-walks", mc.WALKS)
    if SIDEBAR_WALKS_RE.search(html):
        new_html = SIDEBAR_WALKS_RE.sub(lambda m: walks, html, count=1)
        if new_html != html:
            changed.append("sidebar-walks")
        html = new_html

    return html, changed


def iter_site_pages():
    return sorted(WEBSITE.glob("*.html"))


def main():
    ap = argparse.ArgumentParser(description="Inject canonical menus into all site pages.")
    ap.add_argument("--dry-run", action="store_true", help="show changes without writing")
    args = ap.parse_args()

    changed_files = 0
    for path in iter_site_pages():
        original = path.read_text(encoding="utf-8")
        new_html, regions = render_page(original)
        if new_html != original:
            changed_files += 1
            mark = "DRY" if args.dry_run else "✓"
            print(f"  {mark} {path.name}: {', '.join(regions)}")
            if not args.dry_run:
                path.write_text(new_html, encoding="utf-8")
        else:
            print(f"  · {path.name}")

    verb = "would change" if args.dry_run else "changed"
    print(f"\n{changed_files} file(s) {verb}.")


if __name__ == "__main__":
    main()
