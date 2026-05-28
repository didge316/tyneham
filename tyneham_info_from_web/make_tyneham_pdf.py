#!/usr/bin/env python3
"""Compile Tyneham website text files into a structured PDF."""

import os
import re
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT

SRC = Path("/home/matt/Documents/tyhenam website/tyneham_info_from_web")
OUT = SRC / "tyneham.pdf"

# ── Section groupings (filename stem → section) ─────────────────────────────
SECTIONS = {
    "Introduction": [
        "tynehamopc.org.uk_about",
        "tynehamopc.org.uk_early-history",
        "tynehamopc.org.uk_as-time-passed-by-this-is-tynehams-story",
        "tynehamopc.org.uk_timeline",
        "tynehamopc.org.uk_local-landmarks",
        "tynehamopc.org.uk_sea-smuggling",
        "tynehamopc.org.uk_raf-brandy-bay",
        "tynehamopc.org.uk_balsons-gap-and-malhalas-fortune-by-roy-martin",
    ],
    "The 1943 Evacuation": [
        "tynehamopc.org.uk_evacuation-notice",
        "tynehamopc.org.uk_parishioners-in-1943",
        "tynehamopc.org.uk_the-1943-committee",
        "tynehamopc.org.uk_letter-to-the-wiltshire-times",
        "tynehamopc.org.uk_news-1939",
        "tynehamopc.org.uk_news-1968",
        "tynehamopc.org.uk_news-1969",
        "tynehamopc.org.uk_news-2006",
        "tynehamopc.org.uk_news",
    ],
    "The Fight to Return": [
        "tynehamopc.org.uk_fight-for-tyneham",
        "tynehamopc.org.uk_tyneham-action-group",
        "tynehamopc.org.uk_tyneham-action-group-2",
        "tynehamopc.org.uk_something-is-very-wrong",
        "tynehamopc.org.uk_hollow-ditch-and-a-hollow-promise",
        "tynehamopc.org.uk_2021-pathway-blocked-by-razor-wire",
    ],
    "War Memorial": [
        "tynehamopc.org.uk_war-dead",
        "tynehamopc.org.uk_we-will-remember-them",
    ],
    "Places – Tyneham Village": [
        "tynehamopc.org.uk_places",
        "tynehamopc.org.uk_places_tyneham",
        "tynehamopc.org.uk_places_tyneham_tyneham-house",
        "tynehamopc.org.uk_places_tyneham_tyneham-church",
        "tynehamopc.org.uk_places_tyneham_tyneham-church_rectors",
        "tynehamopc.org.uk_places_tyneham_tyneham-farm",
        "tynehamopc.org.uk_places_tyneham_tyneham-farm_scrappy-wall",
        "tynehamopc.org.uk_places_tyneham_tyneham-farm_tyneham-farm-project",
        "tynehamopc.org.uk_places_tyneham_tyneham-school",
        "tynehamopc.org.uk_places_tyneham_tyneham-rectory",
        "tynehamopc.org.uk_places_tyneham_village-fountain",
        "tynehamopc.org.uk_places_tyneham_the-row",
        "tynehamopc.org.uk_places_tyneham_the-row_post-office",
        "tynehamopc.org.uk_places_tyneham_the-row_school-house",
        "tynehamopc.org.uk_places_tyneham_the-row_labourers-cottage",
        "tynehamopc.org.uk_places_tyneham_the-row_shepherds-cottage",
        "tynehamopc.org.uk_places_tyneham_tyneham-cottages",
        "tynehamopc.org.uk_places_tyneham_tyneham-cottages_double-cottages",
        "tynehamopc.org.uk_places_tyneham_tyneham-cottages_gardeners-cottage",
        "tynehamopc.org.uk_places_tyneham_tyneham-cottages_gwyle-cottages",
        "tynehamopc.org.uk_places_tyneham_tyneham-cottages_laundry-cottages",
        "tynehamopc.org.uk_places_tyneham_tyneham-cottages_museum-cottage",
        "tynehamopc.org.uk_places_tyneham_tyneham-cottages_rectory-cottages",
        "tynehamopc.org.uk_telephone-kiosk",
    ],
    "Places – Worbarrow & Surrounds": [
        "tynehamopc.org.uk_places_worbarrow",
        "tynehamopc.org.uk_places_worbarrow_coastguard-station",
        "tynehamopc.org.uk_places_worbarrow_fern-hollow",
        "tynehamopc.org.uk_places_worbarrow_gate-cottages",
        "tynehamopc.org.uk_places_worbarrow_hill-cottage",
        "tynehamopc.org.uk_places_worbarrow_minterns-cottage",
        "tynehamopc.org.uk_places_worbarrow_rose-cottage",
        "tynehamopc.org.uk_places_worbarrow_sea-cottage",
        "tynehamopc.org.uk_places_worbarrow_sheepleaze",
        "tynehamopc.org.uk_places_worbarrow_the-bungalow",
        "tynehamopc.org.uk_places_baltington",
    ],
    "Off-Limits Areas": [
        "tynehamopc.org.uk_off-limits",
        "tynehamopc.org.uk_off-limits_tyneham-house",
        "tynehamopc.org.uk_off-limits_charnel",
        "tynehamopc.org.uk_off-limits_north-egliston",
        "tynehamopc.org.uk_off-limits_north-egliston_north-egliston-farm",
        "tynehamopc.org.uk_off-limits_south-egliston",
        "tynehamopc.org.uk_off-limits_south-egliston_black-cottage",
        "tynehamopc.org.uk_off-limits_south-egliston_south-egliston-cottage",
        "tynehamopc.org.uk_off-limits_south-egliston_south-egliston-house",
        "tynehamopc.org.uk_off-limits_south-egliston_sticklands-cottage",
        "tynehamopc.org.uk_off-limits_povington",
        "tynehamopc.org.uk_off-limits_povington_black-cottage",
        "tynehamopc.org.uk_off-limits_povington_pine-tree-cottage",
        "tynehamopc.org.uk_off-limits_povington_povington-farm",
        "tynehamopc.org.uk_off-limits_povington_primrose-cottage",
        "tynehamopc.org.uk_off-limits_povington_searleys-farm",
        "tynehamopc.org.uk_off-limits_povington_victoria-cottage",
        "tynehamopc.org.uk_off-limits_up-under-barrow",
        "tynehamopc.org.uk_off-limits_whiteway",
        "tynehamopc.org.uk_off-limits_whiteway_whiteway-farm",
    ],
    "Family Histories": [
        "tynehamopc.org.uk_family",
        "tynehamopc.org.uk_family_a-e",
        "tynehamopc.org.uk_family_a-e_balson",
        "tynehamopc.org.uk_family_a-e_barnes",
        "tynehamopc.org.uk_family_a-e_biles",
        "tynehamopc.org.uk_family_a-e_bond",
        "tynehamopc.org.uk_family_a-e_brachi",
        "tynehamopc.org.uk_family_a-e_chilcott",
        "tynehamopc.org.uk_family_a-e_churchill",
        "tynehamopc.org.uk_family_a-e_cleall",
        "tynehamopc.org.uk_family_a-e_dando",
        "tynehamopc.org.uk_family_a-e_draper",
        "tynehamopc.org.uk_family_a-e_driscoll",
        "tynehamopc.org.uk_family_a-e_elmes",
        "tynehamopc.org.uk_family_a-e_everett",
        "tynehamopc.org.uk_family_coastguard-families",
        "tynehamopc.org.uk_family_f-j",
        "tynehamopc.org.uk_family_f-j_godden",
        "tynehamopc.org.uk_family_f-j_gould",
        "tynehamopc.org.uk_family_f-j_grant",
        "tynehamopc.org.uk_family_f-j_hart-family",
        "tynehamopc.org.uk_family_f-j_hawkes",
        "tynehamopc.org.uk_family_f-j_hole",
        "tynehamopc.org.uk_family_f-j_holland",
        "tynehamopc.org.uk_family_f-j_homan",
        "tynehamopc.org.uk_family_f-j_house",
        "tynehamopc.org.uk_family_f-j_howard",
        "tynehamopc.org.uk_family_f-j_hull",
        "tynehamopc.org.uk_family_k-o",
        "tynehamopc.org.uk_family_k-o_kerley",
        "tynehamopc.org.uk_family_k-o_knight",
        "tynehamopc.org.uk_family_k-o_longman",
        "tynehamopc.org.uk_family_k-o_lucas",
        "tynehamopc.org.uk_family_k-o_meech",
        "tynehamopc.org.uk_family_k-o_miller",
        "tynehamopc.org.uk_family_k-o_miller_henry-miller-c1680-1747",
        "tynehamopc.org.uk_family_k-o_miller_john-miller-1713-1780",
        "tynehamopc.org.uk_family_k-o_miller_john-miller-1743-1808",
        "tynehamopc.org.uk_family_k-o_miller_thomas-henry-miller-1835-1926",
        "tynehamopc.org.uk_family_k-o_miller_charles_miller_1851_1943",
        "tynehamopc.org.uk_family_k-o_miller_john-alfred-miller-1866-1947",
        "tynehamopc.org.uk_family_k-o_miller_walter-ernest-miller-1889-1969",
        "tynehamopc.org.uk_family_k-o_minterne",
        "tynehamopc.org.uk_family_k-o_mintern-family",
        "tynehamopc.org.uk_family_k-o_mores",
        "tynehamopc.org.uk_family_p-t",
        "tynehamopc.org.uk_family_p-t_pritchard",
        "tynehamopc.org.uk_family_p-t_sauer-family",
        "tynehamopc.org.uk_family_p-t_smith",
        "tynehamopc.org.uk_family_p-t_stickland",
        "tynehamopc.org.uk_family_p-t_stickland_william-stickland-1780-1851",
        "tynehamopc.org.uk_family_p-t_stickland_william-lush-stickland-1814-1881",
        "tynehamopc.org.uk_family_p-t_stickland_louis-william-stickland-1841-1915",
        "tynehamopc.org.uk_family_p-t_stickland_william-louis-stickland-1872-1947",
        "tynehamopc.org.uk_family_p-t_stickland_frederick-louis-stickland-1917-2007",
        "tynehamopc.org.uk_family_p-t_taylor",
        "tynehamopc.org.uk_family_p-t_tizzard",
        "tynehamopc.org.uk_family_u-z",
        "tynehamopc.org.uk_family_u-z_upshall",
        "tynehamopc.org.uk_family_u-z_ware",
        "tynehamopc.org.uk_family_u-z_warr",
        "tynehamopc.org.uk_family_u-z_way",
        "tynehamopc.org.uk_family_u-z_wellman",
        "tynehamopc.org.uk_family_u-z_wheeler",
        "tynehamopc.org.uk_family_u-z_whitelock",
        "tynehamopc.org.uk_family_u-z_woadden",
        "tynehamopc.org.uk_family_u-z_woodman",
        "tynehamopc.org.uk_family_u-z_wrixon",
        "tynehamopc.org.uk_singleton-family",
        "tynehamopc.org.uk_tripcony",
        "tynehamopc.org.uk_nancy-openshaw-banister",
    ],
    "Parish Records & Censuses": [
        "tynehamopc.org.uk_parish-registers",
        "tynehamopc.org.uk_parish-registers_baptisms-1694-1812",
        "tynehamopc.org.uk_parish-registers_baptisms-1813-1903",
        "tynehamopc.org.uk_parish-registers_baptisms-1842-1864",
        "tynehamopc.org.uk_parish-registers_burials-1734-1812",
        "tynehamopc.org.uk_parish-registers_burials-1813-1942",
        "tynehamopc.org.uk_parish-registers_marriages-1694-1839",
        "tynehamopc.org.uk_parish-registers_marriages-1840-1921",
        "tynehamopc.org.uk_censuses",
        "tynehamopc.org.uk_censuses_1841-census",
        "tynehamopc.org.uk_censuses_1851-census",
        "tynehamopc.org.uk_censuses_1861-census",
        "tynehamopc.org.uk_censuses_1871-census",
        "tynehamopc.org.uk_censuses_1881-census",
        "tynehamopc.org.uk_censuses_1891-census",
        "tynehamopc.org.uk_censuses_1901-census",
        "tynehamopc.org.uk_censuses_1911-census",
        "tynehamopc.org.uk_censuses_1921-census",
        "tynehamopc.org.uk_censuses_1939-register",
        "tynehamopc.org.uk_electors",
        "tynehamopc.org.uk_juror-lists",
        "tynehamopc.org.uk_gaol-registers",
        "tynehamopc.org.uk_removal-orders",
        "tynehamopc.org.uk_tyneham-directories-index",
    ],
    "Gravestones": [
        "tynehamopc.org.uk_gravestones-a",
        "tynehamopc.org.uk_gravestone-images-inscriptions-c",
        "tynehamopc.org.uk_gravestones-b",
        "tynehamopc.org.uk_gravestones-d",
        "tynehamopc.org.uk_gravestones-e",
        "tynehamopc.org.uk_gravestones-f",
        "tynehamopc.org.uk_gravestones-g",
        "tynehamopc.org.uk_gravestones-h",
        "tynehamopc.org.uk_gravestones-k",
        "tynehamopc.org.uk_gravestones-l",
        "tynehamopc.org.uk_gravestones-m",
        "tynehamopc.org.uk_gravestones-n",
        "tynehamopc.org.uk_gravestones-p",
        "tynehamopc.org.uk_gravestones-r",
        "tynehamopc.org.uk_gravestones-s",
        "tynehamopc.org.uk_gravestones-t",
        "tynehamopc.org.uk_gravestones-w",
    ],
    "Wills & Probate": [
        "tynehamopc.org.uk_wills",
        "tynehamopc.org.uk_probate",
        "tynehamopc.org.uk_probate-1911",
        "tynehamopc.org.uk_probate-1945",
        "tynehamopc.org.uk_1911-probate-records",
        "tynehamopc.org.uk_1962-probate-records",
    ],
    "Obituaries & Deaths": [
        "tynehamopc.org.uk_obituaries",
        "tynehamopc.org.uk_2015-obituaries",
        "tynehamopc.org.uk_nellie-may-godden-death",
        "tynehamopc.org.uk_death-of-sheila-joy-wrixon",
        "tynehamopc.org.uk_the-late-mrs-mary-wheeler",
        "tynehamopc.org.uk_1881-death-of-william-stickland",
        "tynehamopc.org.uk_1884-worbarrow-death-of-mr-j-miller",
        "tynehamopc.org.uk_1885-tyneham-death-of-the-rev-w-truell",
        "tynehamopc.org.uk_1925-farm-labourers-fatal-accident-near-coombe-keynes",
        "tynehamopc.org.uk_1931-death-of-mrs-james-lucas",
        "tynehamopc.org.uk_1935-death-of-john-ephraim-moore",
        "tynehamopc.org.uk_1937-killed-while-riding",
        "tynehamopc.org.uk_1947-aged-evacuee-from-training-area-mrs-c-miller-dies-at-stoborough",
        "tynehamopc.org.uk_1947-death-of-claude-samuel-homan",
        "tynehamopc.org.uk_1945-dorsets-new-sheriff",
        "tynehamopc.org.uk_1980-death-of-lilian-margaret-garneys-bond-nee-bond",
        "tynehamopc.org.uk_2003-death-of-john-durant-lewis",
        "tynehamopc.org.uk_2006-death-of-poppy-ingram",
        "tynehamopc.org.uk_2010-death-of-arthur-grant",
        "tynehamopc.org.uk_2010-tributes-paid-to-legendary-purbeck-photographer-arthur-grant",
        "tynehamopc.org.uk_2015-death-of-eileen-may-eastment-nee-whitelock",
        "tynehamopc.org.uk_2019-death-of-ronald-george-whitelock",
    ],
    "Historical Newspaper Articles": [
        "tynehamopc.org.uk_1844-miraculous-escape",
        "tynehamopc.org.uk_1844-miraculous-escape-3",
        "tynehamopc.org.uk_1865-distressing-accident-in-weymouth-bay",
        "tynehamopc.org.uk_1865-loss-of-5-coastguard-men",
        "tynehamopc.org.uk_1865-west-lulworth-the-melancholy-casualty-at-sea",
        "tynehamopc.org.uk_1866-tyneham-the-gale",
        "tynehamopc.org.uk_1873-fatal-boat-accident",
        "tynehamopc.org.uk_1886-the-coastguard-accident-at-warbarrow",
        "tynehamopc.org.uk_1893-the-royal-wedding",
        "tynehamopc.org.uk_1898-local-football-news",
        "tynehamopc.org.uk_1906-tyneham-school",
        "tynehamopc.org.uk_1910-forthcoming-marriages",
        "tynehamopc.org.uk_1910-parish-meeting",
        "tynehamopc.org.uk_1914-air-rifle-shooting",
        "tynehamopc.org.uk_1920-tyneham-war-memorial",
        "tynehamopc.org.uk_1935-tyneham-house-let",
        "tynehamopc.org.uk_1935-unspoilt-worbarrow-bay",
        "tynehamopc.org.uk_1936-tyneham-rectory-roof-garden-fete",
        "tynehamopc.org.uk_1939-mr-and-mrs-charles-william-miller",
        "tynehamopc.org.uk_1968-dorset-manor-house-being-given-away",
        "tynehamopc.org.uk_1968-the-army-reclaims-a-beautiful-spot-for-shelling",
        "tynehamopc.org.uk_1969-army-opens-gunnery-beaches-to-public",
        "tynehamopc.org.uk_1975-tynehams-ration-of-nostalgia",
        "tynehamopc.org.uk_2008-history-wakes-up",
        "tynehamopc.org.uk_2010-lingering-ghosts-of-a-long-dead-england",
        "tynehamopc.org.uk_tall-story-brilliant-sketches-by-an-englishman-which-were-found-in-a-dusty-folder-show-how-the-eiffel-",
        "tynehamopc.org.uk_dorset-life-articles",
    ],
    "Emigrants": [
        "tynehamopc.org.uk_emigrants",
    ],
    "Poetry": [
        "tynehamopc.org.uk_poetry-corner",
        "tynehamopc.org.uk_poem-tyneham",
        "tynehamopc.org.uk_poem-the-tale-of-tyneham-by-angela-wybrow",
        "tynehamopc.org.uk_poem-tyneham-by-fiona-fulton",
    ],
    "Visiting Tyneham": [
        "tynehamopc.org.uk_visiting-tyneham",
        "tynehamopc.org.uk_visiting-tyneham_opening-times",
        "tynehamopc.org.uk_visiting-tyneham_directions",
        "tynehamopc.org.uk_visiting-tyneham_parking",
        "tynehamopc.org.uk_visiting-tyneham_frequently-asked-questions",
        "tynehamopc.org.uk_books-about-tyneham",
    ],
}

# Lines that are clearly navigation / UI fragments to discard
NAV_PATTERNS = [
    re.compile(r'^\s*Home\s*$', re.I),
    re.compile(r'^\s*Main menu\s*$', re.I),
    re.compile(r'^\s*Home\s*\|', re.I),
    re.compile(r'^\s*\|?\s*(Home|About|News|Places|Family|Census|Visiting|Contact)\s*\|', re.I),
    re.compile(r'^\s*By\s*$'),
    re.compile(r'^\s*Continue reading\s*$', re.I),
    re.compile(r'^\s*Tagged\s*$', re.I),
    re.compile(r'^\s*Please note pages with photos are highlighted in\s*$', re.I),
    re.compile(r'^\s*blue\s*$'),
    re.compile(r'^\s*(A|B|C|D|E|F|G|H|I\s+J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)\s*$'),
    re.compile(r'^\s*\|?\s*Tyneham Buildings:\s*\|', re.I),
    re.compile(r'^\s*Primary Resources\s*$', re.I),
    re.compile(r'^\s*\|\s*$'),
    re.compile(r'^\s*\d{4}\s*\|\s*\d{4}\s*\|'),  # year nav like 1841 | 1851 |
    re.compile(r'^\s*(School Visits|For Visitors \.\.\.|For Visitors|Opening Dates|Facilities|FAQs|How to get there|School visits)\s*$', re.I),
    re.compile(r'^\s*Opening Dates\s*&amp;\s*Times\s*$', re.I),
    re.compile(r'^\s*Opening Dates\s*&\s*Times\s*$', re.I),
]

SEPARATOR_RE = re.compile(r'^={10,}')


def is_nav(line):
    for pat in NAV_PATTERNS:
        if pat.match(line):
            return True
    return False


def parse_file(path):
    """Return (title, url, body_paragraphs) from a scraped text file."""
    with open(path, encoding='utf-8', errors='replace') as f:
        raw = f.read()

    lines = raw.splitlines()

    title = ''
    url = ''
    body_start = 0

    for i, line in enumerate(lines):
        if line.startswith('URL:'):
            url = line[4:].strip()
        elif line.startswith('TITLE:'):
            title = line[6:].strip()
            # Strip site suffix
            title = re.sub(r'\s*[-–|]\s*Tyneham.*$', '', title).strip()
            title = re.sub(r'\s*:\s*Where time stopped.*$', '', title).strip()
        elif SEPARATOR_RE.match(line):
            body_start = i + 1
            break

    body_lines = lines[body_start:]

    # Drop the first line if it's a repeat of the title
    if body_lines and body_lines[0].strip() == title:
        body_lines = body_lines[1:]

    # Remove nav, clean up
    cleaned = []
    for line in body_lines:
        if is_nav(line):
            continue
        # Collapse multiple spaces but preserve some whitespace structure
        line = re.sub(r'  +', ' ', line)
        cleaned.append(line)

    # Remove duplicate blocks (some pages repeat their content)
    text = '\n'.join(cleaned)
    half = len(text) // 2
    if half > 200 and text[:half].strip() == text[half:].strip():
        cleaned = cleaned[:len(cleaned) // 2]

    # Build paragraphs: split on blank lines, join wrapped lines
    paragraphs = []
    current = []
    for line in cleaned:
        if line.strip():
            current.append(line.strip())
        else:
            if current:
                paragraphs.append(' '.join(current))
                current = []
    if current:
        paragraphs.append(' '.join(current))

    return title, url, paragraphs


def escape_xml(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    # Strip chars that break ReportLab's XML parser
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    return text


def make_p(text, style):
    safe = escape_xml(text)
    try:
        from reportlab.platypus import Paragraph
        return Paragraph(safe, style)
    except Exception:
        plain = re.sub(r'<[^>]+>', '', safe)
        try:
            return Paragraph(plain, style)
        except Exception:
            return Paragraph('', style)


def build_styles():
    from reportlab.platypus import Paragraph
    base = getSampleStyleSheet()
    slate = colors.HexColor('#2C4A6E')   # slate blue for Dorset/heritage feel
    rust = colors.HexColor('#8B3A2A')    # muted red-brown

    return {
        'cover_title': ParagraphStyle('cover_title', parent=base['Title'],
                                      fontSize=32, textColor=slate,
                                      spaceAfter=10, alignment=TA_CENTER),
        'cover_sub': ParagraphStyle('cover_sub', parent=base['Normal'],
                                    fontSize=14, textColor=colors.HexColor('#555'),
                                    spaceAfter=8, alignment=TA_CENTER),
        'cover_body': ParagraphStyle('cover_body', parent=base['Normal'],
                                     fontSize=10, textColor=colors.HexColor('#333'),
                                     spaceAfter=6, alignment=TA_CENTER),
        'toc_section': ParagraphStyle('toc_section', parent=base['Normal'],
                                      fontSize=11, textColor=slate,
                                      spaceBefore=4, spaceAfter=1, leftIndent=0),
        'section_head': ParagraphStyle('section_head', parent=base['Heading1'],
                                       fontSize=20, textColor=slate,
                                       spaceBefore=4, spaceAfter=8),
        'article_title': ParagraphStyle('article_title', parent=base['Heading2'],
                                        fontSize=14, textColor=rust,
                                        spaceBefore=10, spaceAfter=4),
        'url': ParagraphStyle('url', parent=base['Normal'],
                              fontSize=7, textColor=colors.HexColor('#999'),
                              spaceAfter=4),
        'body': ParagraphStyle('body', parent=base['Normal'],
                               fontSize=9, leading=14, spaceAfter=5,
                               alignment=TA_JUSTIFY),
        'record': ParagraphStyle('record', parent=base['Normal'],
                                 fontSize=8, leading=12, spaceAfter=3,
                                 fontName='Courier'),
    }


def is_record_line(text):
    """Heuristic: census/register/gravestone tabular lines."""
    return bool(re.match(r'.{3,}\s{2,}.{2,}', text) and len(text) < 120 and
                not re.search(r'[.!?]\s', text))


def build_pdf(sections_data, styles):
    from reportlab.platypus import Paragraph

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=2.2*cm, rightMargin=2.2*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
        title="Tyneham – Village History Archive",
        author="tynehamopc.org.uk",
    )

    story = []
    slate = colors.HexColor('#2C4A6E')

    # ── Cover ─────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 4*cm))
    story.append(make_p("Tyneham", styles['cover_title']))
    story.append(make_p("Village History Archive", styles['cover_sub']))
    story.append(HRFlowable(width="70%", thickness=2, color=slate, spaceAfter=16))
    story.append(make_p(
        "A complete archive of the village of Tyneham, Dorset — "
        "evacuated in 1943 and never returned to its inhabitants.",
        styles['cover_body']))
    story.append(make_p(
        "Compiled from tynehamopc.org.uk",
        styles['cover_body']))
    story.append(PageBreak())

    # ── Table of Contents ─────────────────────────────────────────────────────
    story.append(make_p("Contents", styles['section_head']))
    story.append(HRFlowable(width="100%", thickness=1,
                            color=colors.HexColor('#AAA'), spaceAfter=10))
    for section_name, files_data in sections_data.items():
        n = sum(1 for f in files_data if f)
        if n == 0:
            continue
        story.append(make_p(
            f"<b>{escape_xml(section_name)}</b> ({n} entries)",
            styles['toc_section']))
    story.append(PageBreak())

    # ── Sections ─────────────────────────────────────────────────────────────
    for section_name, files_data in sections_data.items():
        non_empty = [f for f in files_data if f]
        if not non_empty:
            continue

        story.append(make_p(escape_xml(section_name), styles['section_head']))
        story.append(HRFlowable(width="100%", thickness=2, color=slate, spaceAfter=10))

        for entry in non_empty:
            title, url, paragraphs = entry
            if not paragraphs:
                continue

            entry_story = []
            if title:
                entry_story.append(make_p(escape_xml(title), styles['article_title']))

            for para in paragraphs:
                if not para.strip():
                    continue
                # Use monospace/smaller style for tabular record data
                if is_record_line(para):
                    entry_story.append(make_p(escape_xml(para), styles['record']))
                else:
                    entry_story.append(make_p(escape_xml(para), styles['body']))

            story.extend(entry_story)
            story.append(Spacer(1, 0.3*cm))
            story.append(HRFlowable(width="40%", thickness=0.5,
                                    color=colors.HexColor('#CCC'), spaceAfter=6))

        story.append(PageBreak())

    doc.build(story)
    print(f"Written: {OUT}")


def main():
    # Load all files referenced in SECTIONS
    all_stems = set()
    for stems in SECTIONS.values():
        all_stems.update(stems)

    # Check which ones actually exist
    available = {p.stem for p in SRC.glob("*.txt")}
    missing = all_stems - available
    if missing:
        print(f"Note: {len(missing)} files listed but not found:")
        for m in sorted(missing)[:10]:
            print(f"  {m}")

    # Parse each file
    cache = {}
    for stem in sorted(all_stems):
        path = SRC / f"{stem}.txt"
        if path.exists():
            try:
                cache[stem] = parse_file(path)
                print(f"  OK: {stem[:60]}")
            except Exception as e:
                print(f"  ERR: {stem}: {e}")
        else:
            cache[stem] = None

    # Build section data preserving order
    sections_data = {}
    for section_name, stems in SECTIONS.items():
        entries = []
        for stem in stems:
            entries.append(cache.get(stem))
        sections_data[section_name] = [e for e in entries if e is not None]

    print(f"\nBuilding PDF...")
    styles = build_styles()
    build_pdf(sections_data, styles)


if __name__ == '__main__':
    main()
