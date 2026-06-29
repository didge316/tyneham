#!/home/matt/claude/.venv/bin/python3
"""Apply audit fixes sitewide using regex — preserves original formatting.

Changes applied:
1. Remove <meta name="keywords" ...> lines from all pages
2. Fix noindex → index,follow for 3 draft pages
3. Add <main> wrapper inside col-lg-8 content div
4. Demote comment-count H2s (e.g. "7 thoughts on...") to h3
"""

import re
from pathlib import Path

WEBSITE_DIR = Path("/home/matt/claude/websites/tyneham/website")

SKIP = {
    "404.html", "thank-you.html", "privacy.html",
    "history_of_tyneham.html", "map_of_tyneham.html",
    "the_bond_family.html", "the_post_office.html",
    "tyneham_village_location.html", "opening_times.html",
}

NOINDEX_PAGES = {
    "corfe-castle-walk.html",
    "kimmeridge-tyneham-walk.html",
    "tyneham-in-wartime.html",
}

html_files = sorted(f for f in WEBSITE_DIR.glob("*.html") if f.name not in SKIP)

for filepath in html_files:
    html = filepath.read_text(encoding="utf-8")
    original = html
    changes = []

    # ── 1. Remove <meta name="keywords" ...> (whole line) ────────────────────
    new_html = re.sub(
        r'[ \t]*<meta\s+name="keywords"[^>]*/>\n?',
        "",
        html,
        flags=re.IGNORECASE,
    )
    if new_html != html:
        changes.append("removed keywords meta")
        html = new_html

    # ── 2. Fix noindex on specific pages ─────────────────────────────────────
    if filepath.name in NOINDEX_PAGES:
        new_html = re.sub(
            r'(content=")noindex,\s*nofollow(")',
            r'\1index, follow\2',
            html,
            flags=re.IGNORECASE,
        )
        if new_html != html:
            changes.append("fixed noindex → index,follow")
            html = new_html

    # ── 3. Add <main> inside col-lg-8 (if not already present) ───────────────
    if "<main>" not in html and 'class="col-lg-8"' in html:
        # Find the opening div and insert <main> right after it
        # Strategy: find col-lg-8 div, count nested divs to find its closing tag,
        # then insert <main>...</main> around all its children.

        # Find start of col-lg-8 div content (right after the opening tag)
        m = re.search(r'(<div\s[^>]*class="col-lg-8"[^>]*>)', html)
        if m:
            insert_after = m.end()

            # Count div depth from that point to find the matching </div>
            depth = 1
            pos = insert_after
            close_pos = None
            while pos < len(html) and depth > 0:
                # Find next <div or </div
                open_m = re.search(r"<div[\s>]", html[pos:])
                close_m = re.search(r"</div>", html[pos:])
                if close_m and (not open_m or close_m.start() < open_m.start()):
                    depth -= 1
                    if depth == 0:
                        close_pos = pos + close_m.start()
                    pos += close_m.end()
                elif open_m:
                    depth += 1
                    pos += open_m.end()
                else:
                    break

            if close_pos is not None:
                # Insert </main> just before the closing </div> of col-lg-8
                # and <main> just after the opening tag
                inner_content = html[insert_after:close_pos]
                # Determine indentation of first content line
                indent_m = re.match(r"(\n[ \t]*)", inner_content)
                indent = indent_m.group(1) if indent_m else "\n      "
                main_open = f"{indent}<main>"
                main_close = f"{indent}</main>"
                new_content = main_open + inner_content + main_close
                html = html[:insert_after] + new_content + html[close_pos:]
                changes.append("added <main> wrapper")

    # ── 4. Demote comment-count H2s to h3 ────────────────────────────────────
    # Match: <h2 ...>N thought(s) on "..."</h2>  (any attributes on h2)
    def demote_comment_h2(m):
        return m.group(0).replace("<h2", "<h3", 1).replace("</h2>", "</h3>", 1)

    new_html = re.sub(
        r'<h2[^>]*>\s*\d+\s+thoughts?\s+on\s+["“].*?</h2>',
        demote_comment_h2,
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if new_html != html:
        changes.append("demoted comment-count H2 → h3")
        html = new_html

    if html != original:
        filepath.write_text(html, encoding="utf-8")
        print(f"  Updated ({', '.join(changes)}): {filepath.name}")
    else:
        print(f"  No changes: {filepath.name}")
