#!/usr/bin/env python3
"""
fix_script_path.py — Convert relative js/scripts.js references to absolute /js/scripts.js

The site uses <script src="js/scripts.js?v=10"> which resolves to
/opening-times/js/scripts.js on subpages (404). Must be /js/scripts.js.
"""
from pathlib import Path

ROOT = Path('/home/matt/projects/tyneham/website')

count = 0
files_changed = 0
for html_file in sorted(ROOT.rglob('index.html')):
    text = html_file.read_text(encoding='utf-8')
    new = text.replace('src="js/scripts.js', 'src="/js/scripts.js')
    if new != text:
        html_file.write_text(new, encoding='utf-8')
        files_changed += 1
        count += text.count('src="js/scripts.js')
        print(f"  ✓ {html_file.relative_to(ROOT)}")

print(f"\nChanged {files_changed} files, {count} references")
