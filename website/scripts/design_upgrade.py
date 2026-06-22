#!/home/matt/claude/.venv/bin/python3
"""
Sitewide design upgrade:
  - Add Bootstrap 5.2.3 CSS from CDN + Lora font preconnects to all pages
  - Bump styles.css to v=8 (now custom-only, no bundled Bootstrap)
  - Replace minimal footer with multi-column heritage footer
  - Add back-to-top button
"""
import os
import re
import glob

WEBSITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NEW_HEAD_BLOCK = """\
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    <!-- Custom CSS -->
    <link href="css/styles.css?v=8" rel="stylesheet" />"""

NEW_FOOTER = """\
  <footer class="site-footer py-5 bg-dark">
    <div class="container">
      <div class="row g-4 mb-2">
        <div class="col-lg-3 col-md-6">
          <h6 class="footer-heading">Tyneham Village</h6>
          <p class="footer-description">An independent guide to Dorset's ghost village, evacuated in 1943 and never returned.</p>
          <a href="#" class="btn btn-warning btn-sm px-3 fw-semibold" data-bs-toggle="modal" data-bs-target="#donateModal">&#9829; Donate</a>
        </div>
        <div class="col-lg-3 col-md-6">
          <h6 class="footer-heading">The Village</h6>
          <ul>
            <li><a href="opening-times">Opening Times 2026</a></li>
            <li><a href="visiting-tyneham">Visiting Tyneham</a></li>
            <li><a href="tyneham-village-location">Getting Here</a></li>
            <li><a href="tyneham-church">Tyneham Church</a></li>
            <li><a href="tyneham-school">Tyneham School</a></li>
            <li><a href="the-post-office">The Post Office</a></li>
          </ul>
        </div>
        <div class="col-lg-3 col-md-6">
          <h6 class="footer-heading">History</h6>
          <ul>
            <li><a href="history-of-tyneham">Tyneham History</a></li>
            <li><a href="the-bond-family">The Bond Family</a></li>
            <li><a href="the-church-door-note">The Church Door Note</a></li>
            <li><a href="after-the-evacuation">After the Evacuation</a></li>
            <li><a href="the-campaign-to-return">The Campaign to Return</a></li>
            <li><a href="tyneham-remembered">Documentary</a></li>
          </ul>
        </div>
        <div class="col-lg-3 col-md-6">
          <h6 class="footer-heading">Nearby</h6>
          <ul>
            <li><a href="worbarrow-bay">Worbarrow Bay</a></li>
            <li><a href="lulworth-cove">Lulworth Cove</a></li>
            <li><a href="corfe-castle">Corfe Castle</a></li>
            <li><a href="durdle-door">Durdle Door</a></li>
            <li><a href="kimmeridge-bay">Kimmeridge Bay</a></li>
            <li><a href="tyneham-walk">Circular Walk</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom d-flex flex-wrap align-items-center justify-content-between gap-2">
        <div>
          <a href="contact" class="footer-link me-3">Contact</a>
          <a href="privacy" class="footer-link me-3">Privacy Policy</a>
          <a href="/" class="footer-link">Home</a>
        </div>
        <span>&copy; Tyneham Village 2026</span>
      </div>
    </div>
  </footer>"""

BACK_TO_TOP = '    <button id="back-to-top" aria-label="Back to top">&#8593;</button>'


def upgrade_head(content):
    """Replace old CSS link block with Bootstrap CDN + Lora + custom CSS."""
    # Case 1: page already has Bootstrap CDN CSS separately — just update styles.css version
    if 'bootstrap@5.2.3/dist/css' in content:
        content = re.sub(
            r'<link[^>]+css/styles\.css[^>]*>',
            '<link href="css/styles.css?v=8" rel="stylesheet" />',
            content
        )
        return content

    # Case 2: page has bundled Bootstrap via styles.css — replace the whole CSS comment+link
    # Handles both "  " and "    " indentation and with/without version number
    content = re.sub(
        r'[ \t]*<!-- CSS -->\s*\n[ \t]*<link[^>]+css/styles\.css[^>]*>',
        NEW_HEAD_BLOCK,
        content
    )

    # Fallback: no <!-- CSS --> comment, just the bare link
    if 'css/styles.css' in content and 'bootstrap@5.2.3/dist/css' not in content:
        content = re.sub(
            r'[ \t]*<link[^>]+css/styles\.css[^>]*>',
            NEW_HEAD_BLOCK,
            content
        )

    return content


def upgrade_footer(content):
    """Replace the old minimal site footer with the new multi-column footer."""
    # Match the main site footer (class contains py-5 bg-dark) — not blockquote-footer
    # Match footer with any extra classes after py-5 bg-dark (e.g. mt-5)
    content = re.sub(
        r'<footer class="py-5 bg-dark[^"]*">.*?</footer>',
        NEW_FOOTER,
        content,
        flags=re.DOTALL
    )
    return content


def add_back_to_top(content):
    """Insert back-to-top button before Bootstrap JS or closing body tag."""
    if 'back-to-top' in content:
        return content
    if '<!-- Bootstrap core JS-->' in content:
        content = re.sub(
            r'([ \t]*<!-- Bootstrap core JS-->)',
            BACK_TO_TOP + '\n' + r'\1',
            content
        )
    else:
        content = re.sub(
            r'([ \t]*</body>)',
            BACK_TO_TOP + '\n' + r'\1',
            content
        )
    return content


def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original
    content = upgrade_head(content)
    content = upgrade_footer(content)
    content = add_back_to_top(content)

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    html_files = glob.glob(os.path.join(WEBSITE_DIR, '*.html'))
    changed = 0
    skipped = 0
    for path in sorted(html_files):
        fname = os.path.basename(path)
        if process_file(path):
            print(f'  updated: {fname}')
            changed += 1
        else:
            print(f'  skipped: {fname}')
            skipped += 1
    print(f'\nDone — {changed} updated, {skipped} unchanged.')


if __name__ == '__main__':
    main()
