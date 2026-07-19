#!/usr/bin/env python3
"""
Bulk fixes 2026-07-19:
1. Add HowTo schema to 3 walk pages
2. Add image preloads to 3 walk pages
3. Fix title-H1 alignment on 3 pages
"""

import re
from pathlib import Path

ROOT = Path('/home/matt/projects/tyneham/website')

# HowTo schemas for walk pages
HOWTO_SCHEMAS = {
    'tyneham-walk': {
        'walk_name': 'Tyneham Circular Walk',
        'description': 'A 4.3-mile circuit from Tyneham village through Whiteway Hill, Flower\'s Barrow Iron Age hillfort, Worbarrow Bay, and back via the valley track. Moderate grade, 337m climb, 2.5-3 hours.',
        'totalTime': 'PT2H30M',
        'steps': [
            ('Tyneham village to Whiteway Hill', 'From the car park, walk back past the church and pick up the footpath heading north, marked by two yellow posts alongside the churchyard. A gravel farm track climbs steadily up Whiteway Hill. At the top, join the prehistoric ridgeway along the crest of the Purbeck Hills.'),
            ('Along the ridge to Flower\'s Barrow', 'Turn west and follow the ridge for about a mile to Flower\'s Barrow, an Iron Age hillfort perched on the cliff edge. Double and triple ramparts guard its eastern and western approaches.'),
            ('The descent to Worbarrow Bay', 'From the hillfort, the coast path drops steeply to Worbarrow Bay. Take it slowly — the correct path into the bay is a gap in the embankment marked by two yellow posts.'),
            ('Worbarrow Bay and the Tout', 'Explore the bay: a great arc of shingle and sand backed by dramatically tilted cliffs. At the eastern end, scramble up Worbarrow Tout for panoramic views.'),
            ('The valley track back to Tyneham', 'A flat, well-graded track follows the stream inland through the valley, an easy mile back to the village, passing the ruins of Gate Cottages and WWII anti-tank defences. Turn left at Tyneham Farm for the car park.'),
        ],
    },
    'corfe-castle-walk': {
        'walk_name': 'Corfe Castle Circular Walk',
        'description': 'A 7-8 mile circular route on the Purbeck ridge taking in Noel Hill, Ridgeway Hill and East Creech, with the ruined Corfe Castle as its centrepiece. Moderate grade, 3-3.5 hours walking.',
        'totalTime': 'PT3H30M',
        'steps': [
            ('Corfe Castle village and the ruins', 'Leave the car park on foot and follow the main street up through the village toward the castle gatehouse. The National Trust charges entry to the ruins themselves, but the scale of destruction is clear even from the street. If visiting the ruins, allow at least 45 minutes.'),
            ('Noel Hill and Ridgeway Hill', 'From the castle, pick up the footpath that climbs west then south up the spine of the Purbeck ridge. The ascent is the most demanding section. From the top, the panorama includes Poole Harbour, Swanage, Church Knowle, and the distant hills above Kimmeridge.'),
            ('Descent to East Creech', 'From Ridgeway Hill, the path descends north off the ridge to the small village of East Creech. The descent is gradual. The duck pond is the landmark: fork left after it, then take the signed path east toward the Purbeck Way.'),
            ('Purbeck Way and return', 'Follow the Purbeck Way east across fields and over gentle ground, with Corfe Castle appearing ahead as you approach from the north. The final section brings you back into the village from the north, joining the main street and returning to the car park.'),
        ],
    },
    'kimmeridge-tyneham-walk': {
        'walk_name': 'Kimmeridge to Tyneham Coastal Walk',
        'description': 'A 7.5-mile one-way route on the South West Coast Path from Kimmeridge Bay to Tyneham village through the Lulworth Ranges. Strenuous grade with significant climbing, 3.5-4 hours. Only accessible on range open days.',
        'totalTime': 'PT4H',
        'steps': [
            ('Kimmeridge Bay', 'Start at the car park above Kimmeridge Bay. Explore the wave-cut rock ledges at low tide — one of the best places on the Jurassic Coast for fossils. Look for the Clavel Tower folly and the Kimmeridge oil nodding donkey pump visible from the path.'),
            ('Into the ranges', 'West of Kimmeridge, the path enters the Lulworth Ranges. The transition is marked by clear signage. Keep to the path — the clifftop offers unbroken views along the Jurassic Coast with significant undulations.'),
            ('Gad Cliff and Brandy Bay', 'The path passes above Gad Cliff, a dramatic limestone headland rising about 160 metres. Looking back east, the full sweep of the coast is visible. The path along this section can be narrow and exposed.'),
            ('Worbarrow Bay', 'Descend steeply to Worbarrow Bay, a wide shingle and sand beach backed by chalk cliffs. The dramatically tilted strata are part of the Purbeck Monocline. Dinosaur footprints have been found in the limestone at the cliff base.'),
            ('Tyneham Village', 'Follow the flat valley track inland for about 1.5 miles to reach the car park at Tyneham village. The church and school exhibitions are open 10am-4pm on range open days. Allow at least an hour to explore the village.'),
        ],
    },
}

HERO_IMAGES = {
    'tyneham-walk': '/assets/lulworth-ranges-coast.webp',
    'corfe-castle-walk': '/assets/corfe-castle.webp',
    'kimmeridge-tyneham-walk': '/assets/hounds-tout-worbarrow-bay.webp',
}


def make_howto_schema(info):
    steps_json = ',\n'.join(
        f'''      {{
        "@type": "HowToStep",
        "position": {i},
        "name": "{name}",
        "text": "{text}"
      }}'''
        for i, (name, text) in enumerate(info['steps'], 1)
    )

    slug_prefix = info['walk_name'].lower().replace(' ', '-').replace("'", '').replace(',', '')
    # steps_json has {{slug(i)}} but we need proper URL. Let's just use section anchors with step numbers
    from textwrap import dedent

    return dedent(f'''\
  <!-- HowTo Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": "{info['walk_name']}",
    "description": "{info['description']}",
    "totalTime": "{info['totalTime']}",
    "step": [
{steps_json}
    ]
  }}
  </script>''')


def build_preload_tag(hero_path):
    return f'    <link rel="preload" as="image" href="{hero_path}">'


def fix_walk_page(folder, info):
    path = ROOT / folder / 'index.html'
    text = path.read_text(encoding='utf-8')

    # Add image preload before </head>
    preload_tag = build_preload_tag(HERO_IMAGES[folder])
    if 'rel="preload" as="image"' not in text:
        text = text.replace('</head>', f'  {preload_tag}\n</head>')

    # Add HowTo schema before the closing </article> or after Article schema
    howto_schema = make_howto_schema(info)
    if 'HowTo' not in text:
        # Find the BreadcrumbList schema (present on all pages) and insert HowTo before it
        bc_pos = text.find('BreadcrumbList Schema')
        if bc_pos > 0:
            # Find <!-- BreadcrumbList Schema -->
            comment_start = text.rfind('<!--', 0, bc_pos)
            text = text[:comment_start] + howto_schema + '\n\n  ' + text[comment_start:]

    path.write_text(text, encoding='utf-8')
    return True


def fix_title_h1(page_path, new_title, new_h1):
    path = ROOT / page_path
    text = path.read_text(encoding='utf-8')

    if new_title:
        text = re.sub(
            r'<title>[^<]*</title>',
            f'<title>{new_title}</title>',
            text,
            count=1,
        )
    if new_h1:
        text = re.sub(
            r'<h1[^>]*>[^<]*</h1>',
            lambda m: m.group(0).replace(
                re.search(r'>[^<]*<', m.group(0)).group(0),
                f'>{new_h1}<',
            ),
            text,
            count=1,
        )

    path.write_text(text, encoding='utf-8')
    return True


if __name__ == '__main__':
    print('=== Adding HowTo + preloads to walk pages ===')
    for folder, info in HOWTO_SCHEMAS.items():
        try:
            fix_walk_page(folder, info)
            print(f'  ✓ {folder}')
        except Exception as e:
            print(f'  ✗ {folder}: {e}')

    print()
    print('=== Fixing title-H1 alignment ===')
    fixes = [
        # (path, new_title, new_h1)
        ('index.html', None, 'Tyneham Village &mdash; Dorset&#39;s Ghost Village'),
        ('camp-at-tyneham/index.html', None, 'Camping near Tyneham Village'),
    ]
    for p, t, h1 in fixes:
        try:
            fix_title_h1(p, t, h1)
            print(f'  ✓ {p}')
        except Exception as e:
            print(f'  ✗ {p}: {e}')

    print()
    print('Done.')
