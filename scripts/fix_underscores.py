#!/home/matt/claude/.venv/bin/python3
"""
Rename 6 underscore-filename pages to hyphen equivalents.
Updates all internal href references, canonicals, OG URLs, schema URLs,
sitemap.xml, llms.txt, and _redirects across the whole site.
"""
import os
import re

SITE = "/home/matt/claude/websites/tyneham/website"

RENAMES = {
    "history_of_tyneham": "history-of-tyneham",
    "map_of_tyneham": "map-of-tyneham",
    "opening_times": "opening-times",
    "the_bond_family": "the-bond-family",
    "the_post_office": "the-post-office",
    "tyneham_village_location": "tyneham-village-location",
}


def update_file(path, replacements):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Updated: {os.path.basename(path)}")
    return content != original


# Build replacement pairs for HTML files
html_replacements = []
for old, new in RENAMES.items():
    html_replacements.append((f"{old}.html", f"{new}.html"))
    # Also update canonical/og:url absolute URLs
    html_replacements.append(
        (f"tynehamvillage.org/{old}", f"tynehamvillage.org/{new}")
    )

print("Updating HTML files...")
html_files = [f for f in os.listdir(SITE) if f.endswith(".html")]
changed = 0
for fname in sorted(html_files):
    if update_file(os.path.join(SITE, fname), html_replacements):
        changed += 1
print(f"  {changed} of {len(html_files)} HTML files updated\n")

# Sitemap
print("Updating sitemap.xml...")
sitemap_replacements = [
    (f"tynehamvillage.org/{old}", f"tynehamvillage.org/{new}")
    for old, new in RENAMES.items()
]
update_file(os.path.join(SITE, "sitemap.xml"), sitemap_replacements)

# llms.txt
print("Updating llms.txt...")
update_file(os.path.join(SITE, "llms.txt"), sitemap_replacements)

# _redirects
print("Updating _redirects...")
redirects_path = os.path.join(SITE, "_redirects")
with open(redirects_path, "r", encoding="utf-8") as f:
    redirects = f.read()

# Update targets that pointed to underscore .html files
for old, new in RENAMES.items():
    redirects = redirects.replace(f"/{old}.html", f"/{new}.html")
    redirects = redirects.replace(f"/{old} ", f"/{new} ")  # extensionless targets

# The /the-bond-family and /the-post-office slugs already exist as redirect
# sources pointing to the old underscore files. Now the files ARE named with
# hyphens, so Cloudflare will serve them natively — remove those now-redundant
# redirect lines to avoid a redirect loop.
lines = redirects.splitlines(keepends=True)
lines_out = []
for line in lines:
    # Remove redirect entries whose source == the new native path (would loop)
    skip = False
    for old, new in RENAMES.items():
        native_slug = f"/{new}"
        if line.strip().startswith(native_slug + " ") or line.strip().startswith(native_slug + "\t"):
            skip = True
            break
    if not skip:
        lines_out.append(line)
redirects = "".join(lines_out)

# Add new underscore-slug → hyphen-slug redirects (preserve Google index equity)
new_block = "\n# Underscore → hyphen URL redirects (SEO cleanup 2026-05)\n"
for old, new in RENAMES.items():
    new_block += f"/{old}    /{new}    301\n"
    new_block += f"/{old}/   /{new}    301\n"
    new_block += f"/{old}.html   /{new}    301\n"

redirects = redirects.rstrip() + "\n" + new_block

with open(redirects_path, "w", encoding="utf-8") as f:
    f.write(redirects)
print("  _redirects updated\n")

# Rename the actual files
print("Renaming files...")
for old, new in RENAMES.items():
    src = os.path.join(SITE, f"{old}.html")
    dst = os.path.join(SITE, f"{new}.html")
    if os.path.exists(src):
        os.rename(src, dst)
        print(f"  {old}.html → {new}.html")
    else:
        print(f"  SKIP (not found): {old}.html")

print("\nDone.")
