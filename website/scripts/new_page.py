#!/home/matt/claude/.venv/bin/python3
"""Scaffold a new draft content page for tynehamvillage.org.

Creates website/<slug>.html from page_template.html with complete, validated
metadata (title, description, OG/Twitter, canonical, Article + BreadcrumbList
JSON-LD) and the canonical navbar/sidebar injected by render_menus. The page is
created as a DRAFT (robots: noindex, nofollow) and is NOT added to any menu — it is
served but linked from nowhere until you run publish_page.py.

Example:
    new_page.py \\
      --slug red-telephone-box \\
      --title "The Red Telephone Box" \\
      --title-suffix "Tyneham's Most Photographed Feature, Dorset" \\
      --description "The K6 red telephone box is Tyneham's most photographed feature..." \\
      --hero red-telephone-box.webp \\
      --hero-alt "The red K6 telephone box in Tyneham village" \\
      --lead "Tyneham's most photographed survivor" \\
      --keywords "tyneham telephone box, red phone box dorset"

Then fill in the TODO sections, and when ready:
    publish_page.py --slug red-telephone-box --category village --label "Red Telephone Box"
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_menus  # noqa: E402  (also resolves WEBSITE root)

WEBSITE = Path(__file__).resolve().parent.parent
TEMPLATE = Path(__file__).resolve().parent / "page_template.html"

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def build_page(args, robots="noindex, nofollow"):
    """Return the fully-rendered page HTML (tokens substituted + menus injected)."""
    today = dt.date.today().isoformat()
    keywords_meta = (
        f'  <meta name="keywords" content="{args.keywords}" />\n' if args.keywords else ""
    )
    tokens = {
        "TITLE": args.title,
        "TITLE_SUFFIX": args.title_suffix,
        "DESCRIPTION": args.description,
        "KEYWORDS_META": keywords_meta,
        "ROBOTS": robots,
        "OG_TITLE": args.og_title or args.title,
        "OG_DESCRIPTION": args.og_description or args.description,
        "SLUG": args.slug,
        "HERO_IMAGE": args.hero,
        "HERO_ALT": args.hero_alt,
        "HEADLINE": args.headline or args.title,
        "LEAD": args.lead,
        "BREADCRUMB_NAME": args.breadcrumb or args.title,
        "DATE_PUBLISHED": today,
        "DATE_MODIFIED": today,
    }
    html = TEMPLATE.read_text(encoding="utf-8")
    for key, val in tokens.items():
        html = html.replace("{{" + key + "}}", val)
    leftover = re.findall(r"\{\{[A-Z_]+\}\}", html)
    if leftover:
        sys.exit(f"ERROR: template tokens not substituted: {sorted(set(leftover))}")
    # Inject the canonical navbar + sidebars into the placeholders.
    html, _ = render_menus.render_page(html)
    return html


def validate(args):
    errors, warnings = [], []
    if not SLUG_RE.match(args.slug):
        errors.append(f"--slug '{args.slug}' must be kebab-case (lowercase, hyphens, no .html)")
    for field in ("title", "description", "hero", "hero_alt"):
        if not getattr(args, field).strip():
            errors.append(f"--{field.replace('_', '-')} is required and must be non-empty")
    if "{{" in args.hero or "." not in args.hero:
        errors.append(f"--hero '{args.hero}' should be an image filename with extension, e.g. foo.webp")
    if not (50 <= len(args.description) <= 160):
        warnings.append(f"description is {len(args.description)} chars (aim for 50-160 for SEO)")
    hero_path = WEBSITE / "assets" / args.hero
    if not hero_path.exists():
        warnings.append(f"hero image not found: assets/{args.hero} (add it before publishing)")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", required=True, help="page filename without .html (also the clean URL)")
    ap.add_argument("--title", required=True, help="<title> main text and default H1/headline")
    ap.add_argument("--title-suffix", default="Tyneham, Dorset", help="text after the | in <title>")
    ap.add_argument("--description", required=True, help="meta description (~155 chars)")
    ap.add_argument("--hero", required=True, help="hero image filename in assets/, e.g. badger.webp")
    ap.add_argument("--hero-alt", required=True, help="alt text for the hero image")
    ap.add_argument("--keywords", default="", help="optional comma-separated keywords")
    ap.add_argument("--og-title", default="", help="Open Graph/Twitter title (defaults to --title)")
    ap.add_argument("--og-description", default="", help="OG/Twitter description (defaults to --description)")
    ap.add_argument("--headline", default="", help="H1 + schema headline (defaults to --title)")
    ap.add_argument("--lead", default="", help="lead subtitle under the H1")
    ap.add_argument("--breadcrumb", default="", help="breadcrumb name (defaults to --title)")
    ap.add_argument("--category", choices=sorted(__import__("menu_config").CATEGORY_TO_LIST),
                    help="intended menu (used by publish_page.py later); recorded for guidance only")
    ap.add_argument("--dry-run", action="store_true", help="print the page instead of writing it")
    args = ap.parse_args()

    errors, warnings = validate(args)
    for w in warnings:
        print(f"  ⚠ {w}")
    if errors:
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)

    html = build_page(args)

    if args.dry_run:
        sys.stdout.write(html)
        return

    dest = WEBSITE / f"{args.slug}.html"
    if dest.exists():
        sys.exit(f"ERROR: {dest.name} already exists — refusing to overwrite.")
    dest.write_text(html, encoding="utf-8")

    cat = args.category or "<village|history|near>"
    label = args.title
    print(f"\n✓ Created draft: website/{args.slug}.html  (robots: noindex, nofollow)")
    print("\nNext steps:")
    print(f"  1. Fill in the TODO sections in website/{args.slug}.html")
    print(f"  2. Add the hero image assets/{args.hero} if it isn't there yet")
    print("  3. Preview: python3 -m http.server 8766 --directory website  →  "
          f"http://localhost:8766/{args.slug}.html")
    print("  4. When ready to go live (adds to menu, sitemap, llms; flips to index):")
    print(f"       scripts/publish_page.py --slug {args.slug} --category {cat} --label \"{label}\"")


if __name__ == "__main__":
    main()
