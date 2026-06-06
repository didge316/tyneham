#!/home/matt/claude/.venv/bin/python3
"""Single source of truth for the tynehamvillage.org site menu.

Every navbar dropdown and sidebar card is generated from these lists by
render_menus.py. To add, remove, or reorder a menu item, edit the list here and
re-run render_menus.py — never hand-edit the navbar/sidebar in the HTML pages.

Each entry is (slug, label):
  - slug  = the page filename without ".html" (also the clean URL; navbar/sidebar
            links are extensionless, e.g. href="gad-cliff")
  - label = the menu text shown to visitors

Sidebar mapping:
  "In Tyneham Village" card (id="sidebar-menu")      = VILLAGE + HISTORY
  "Near Tyneham"        card (id="sidebar-menu-near") = NEAR
"""

# "The Village" navbar dropdown
VILLAGE = [
    ("opening-times", "Opening Times 2026"),
    ("visiting-tyneham", "Visiting Tyneham"),
    ("tyneham-village-location", "Where is Tyneham?"),
    ("tyneham-remembered", "The Tyneham Remembered Documentary"),
    ("map-of-tyneham", "Tyneham Village Map"),
    ("the-post-office", "The Post Office"),
    ("the-rectory", "The Rectory"),
    ("tyneham-school", "Tyneham School"),
    ("tyneham-church", "Tyneham Church"),
    ("tyneham-house", "Tyneham House"),
    ("camp-at-tyneham", "Camping at Tyneham"),
    ("tyneham-photos", "Tyneham Village Photos"),
    ("wildlife-at-tyneham", "Wildlife at Tyneham"),
]

# "History" navbar dropdown
HISTORY = [
    ("history-of-tyneham", "Tyneham History"),
    ("the-bond-family", "The Bond Family"),
    ("the-church-door-note", "The Church Door Note"),
    ("after-the-evacuation", "After the Evacuation"),
    ("the-campaign-to-return", "The Campaign to Return"),
    ("ghost-village", "Dorset's Ghost Village"),
]

# "Near Tyneham" navbar dropdown
NEAR = [
    ("corfe-castle", "Corfe Castle"),
    ("durdle-door", "Durdle Door"),
    ("lulworth-cove", "Lulworth Cove"),
    ("worbarrow-bay", "Worbarrow Bay"),
    ("flowers-barrow", "Flower's Barrow"),
    ("kimmeridge-bay", "Kimmeridge Bay"),
    ("lulworth-range-walks", "Lulworth Range Walks"),
    ("gad-cliff", "Gad Cliff"),
]

# Deliberately NOT in any menu yet (served but unlisted drafts):
#   corfe-castle-walk, kimmeridge-tyneham-walk, tyneham-in-wartime
# Add them to the appropriate list above (via publish_page.py) when ready.

# Maps the category key used by new_page.py / publish_page.py to its list name.
CATEGORY_TO_LIST = {
    "village": "VILLAGE",
    "history": "HISTORY",
    "near": "NEAR",
}


def all_menu_slugs():
    """Every slug currently linked in the navbar/sidebar."""
    return {slug for slug, _ in VILLAGE + HISTORY + NEAR}
