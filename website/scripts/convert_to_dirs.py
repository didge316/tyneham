#!/usr/bin/env python3
"""Convert flat .html files to directory-based index.html files.

For each .html file in website/ (except index.html and 404.html):
  1. Create a directory named after the file (without .html)
  2. Move the file into that directory as index.html
  3. Update the canonical tag to include trailing slash
"""

import os
import re

WEBSITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORE_FILES = {"index.html", "404.html"}
DOMAIN = "https://tynehamvillage.org"


def main():
    html_files = [f for f in os.listdir(WEBSITE_DIR)
                  if f.endswith(".html") and f not in IGNORE_FILES]

    for filename in sorted(html_files):
        dirname = filename[:-5]  # strip .html
        src = os.path.join(WEBSITE_DIR, filename)
        dst_dir = os.path.join(WEBSITE_DIR, dirname)
        dst = os.path.join(dst_dir, "index.html")

        print(f"  {filename} → {dirname}/index.html")

        os.makedirs(dst_dir, exist_ok=True)

        with open(src, "r", encoding="utf-8") as f:
            content = f.read()

        # Add trailing slash to canonical URLs that don't already have one
        content = re.sub(
            rf'(<link rel="canonical" href="{re.escape(DOMAIN)}/[^"]*[^/])(")',
            r'\1/\2',
            content,
        )

        with open(dst, "w", encoding="utf-8") as f:
            f.write(content)

        os.remove(src)

    print(f"\nDone. {len(html_files)} files converted.")


if __name__ == "__main__":
    main()
