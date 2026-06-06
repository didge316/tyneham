#!/home/matt/claude/.venv/bin/python3
"""Publish a draft page: wire it into the site menus, sitemap, and llms.txt.

Run this once a draft (created by new_page.py) is written and reviewed. It:
  1. adds (slug, label) to the correct list in menu_config.py (the source of truth),
  2. flips the page's robots meta to "index, follow",
  3. re-runs render_menus.py so the new link appears in every page's navbar+sidebar,
  4. adds the page to sitemap.xml and llms.txt.
All steps are idempotent.

Example:
    publish_page.py --slug red-telephone-box --category village \\
        --label "Red Telephone Box" \\
        --llms-desc "Tyneham's most photographed feature, the K6 red phone box"
"""
import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
WEBSITE = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))
import menu_config as mc  # noqa: E402

MENU_CONFIG = SCRIPTS / "menu_config.py"
SITEMAP = WEBSITE / "sitemap.xml"
LLMS = WEBSITE / "llms.txt"


def add_to_menu_config(slug, label, category):
    list_name = mc.CATEGORY_TO_LIST[category]
    text = MENU_CONFIG.read_text(encoding="utf-8")
    if re.search(rf'\(\s*"{re.escape(slug)}"\s*,', text):
        return False  # already listed somewhere — idempotent
    if '"' in label:
        sys.exit(f'ERROR: --label may not contain a double quote: {label!r}')
    m = re.search(rf"{list_name} = \[\n(.*?)\n\]", text, re.DOTALL)
    if not m:
        sys.exit(f"ERROR: could not find list {list_name} in menu_config.py")
    new_body = m.group(1) + f'\n    ("{slug}", "{label}"),'
    MENU_CONFIG.write_text(text[: m.start(1)] + new_body + text[m.end(1):], encoding="utf-8")
    return True


def set_indexable(slug):
    page = WEBSITE / f"{slug}.html"
    if not page.exists():
        sys.exit(f"ERROR: page not found: {page.name} (create it with new_page.py first)")
    text = page.read_text(encoding="utf-8")
    new = re.sub(r'(<meta name="robots" content=")[^"]*(")',
                 r"\1index, follow\2", text, count=1)
    if new != text:
        page.write_text(new, encoding="utf-8")
        return True
    return False


def add_to_sitemap(slug, lastmod):
    text = SITEMAP.read_text(encoding="utf-8")
    if f"/{slug}</loc>" in text:
        return False
    entry = (f"  <url>\n    <loc>https://tynehamvillage.org/{slug}</loc>\n"
             f"    <lastmod>{lastmod}</lastmod>\n  </url>\n")
    SITEMAP.write_text(text.replace("</urlset>", entry + "</urlset>", 1), encoding="utf-8")
    return True


def add_to_llms(slug, label, desc):
    text = LLMS.read_text(encoding="utf-8")
    if f"/{slug})" in text:
        return False
    line = f"- [{label}](https://tynehamvillage.org/{slug}) — {desc}\n"
    anchor = "- [About James Langton]"
    if anchor in text:
        text = text.replace(anchor, line + anchor, 1)
    else:
        text = text.rstrip("\n") + "\n" + line
    LLMS.write_text(text, encoding="utf-8")
    return True


def meta_description(slug):
    text = (WEBSITE / f"{slug}.html").read_text(encoding="utf-8")
    m = re.search(r'<meta name="description" content="([^"]*)"', text)
    return m.group(1) if m else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--category", required=True, choices=sorted(mc.CATEGORY_TO_LIST))
    ap.add_argument("--label", required=True, help="menu text shown to visitors")
    ap.add_argument("--llms-desc", default="", help="short blurb for llms.txt (defaults to meta description)")
    ap.add_argument("--lastmod", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true", help="render_menus dry-run; still previews config/robots changes")
    args = ap.parse_args()

    page = WEBSITE / f"{args.slug}.html"
    if not page.exists():
        sys.exit(f"ERROR: page not found: {page.name} (create it with new_page.py first)")

    llms_desc = args.llms_desc or meta_description(args.slug)
    if not llms_desc:
        sys.exit("ERROR: no --llms-desc and page has no meta description to fall back on.")

    if args.dry_run:
        print("DRY RUN — no files written.")
        print(f"  would add to menu_config.{mc.CATEGORY_TO_LIST[args.category]}: (\"{args.slug}\", \"{args.label}\")")
        print(f"  would set {args.slug}.html robots → index, follow")
        print(f"  would add to sitemap.xml and llms.txt (\"{llms_desc}\")")
        subprocess.run([sys.executable, str(SCRIPTS / "render_menus.py"), "--dry-run"], check=True)
        return

    added = add_to_menu_config(args.slug, args.label, args.category)
    print(f"  menu_config: {'added' if added else 'already present'}")
    print(f"  robots: {'flipped to index' if set_indexable(args.slug) else 'already index'}")
    # Re-render in a fresh process so the updated menu_config is read.
    subprocess.run([sys.executable, str(SCRIPTS / "render_menus.py")], check=True)
    print(f"  sitemap.xml: {'added' if add_to_sitemap(args.slug, args.lastmod) else 'already present'}")
    print(f"  llms.txt: {'added' if add_to_llms(args.slug, args.label, llms_desc) else 'already present'}")
    print(f"\n✓ Published {args.slug} — now linked sitewide and indexable.")


if __name__ == "__main__":
    main()
