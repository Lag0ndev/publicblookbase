#!/usr/bin/env python3
"""Patch index.html: Spooktober LIVE + official Spooky Pack drop rates."""
from pathlib import Path
import re

p = Path('index.html')
t = p.read_text(encoding='utf-8')
orig = t

# 1) Countdown target already passed -> shows doneText
t = t.replace(
    'target: new Date("2026-10-01T00:00:00"),\n                doneText: \'\U0001f383 Spooktober is here! \U0001f383\'',
    'target: new Date("2026-09-30T00:00:00"),\n                doneText: \'\U0001f383 SPOOKY PACK IS LIVE! \U0001f47b\'',
)
# fallback without emoji escape issues
if t == orig:
    t = re.sub(
        r'target: new Date\("2026-10-01T00:00:00"\),\s*doneText: \'[^\']*\'',
        'target: new Date("2026-09-30T00:00:00"),\n                doneText: \'\U0001f383 SPOOKY PACK IS LIVE! \U0001f47b\'',
        t,
        count=1,
    )

# 2) Replace Spooky pack blooks list with official 14 from Market modal
old_spooky = re.search(
    r'\{\s*\n"name": "Spooky",\s*\n"price": 25,\s*\n"blooks": \[.*?\],\s*\n"year":',
    t,
    flags=re.S,
)

NEW_BLOOKS = '''[
    { "name": "Pumpkin", "chance": 15.2, "rarity": "Uncommon" },
    { "name": "Swamp Monster", "chance": 15.2, "rarity": "Uncommon" },
    { "name": "Frankenstein", "chance": 15.2, "rarity": "Uncommon" },
    { "name": "Vampire", "chance": 15.2, "rarity": "Uncommon" },
    { "name": "Zombie", "chance": 15.2, "rarity": "Uncommon" },
    { "name": "Mummy", "chance": 4.0, "rarity": "Rare" },
    { "name": "Caramel Apple", "chance": 4.0, "rarity": "Rare" },
    { "name": "Candy Corn", "chance": 4.0, "rarity": "Rare" },
    { "name": "Crow", "chance": 4.0, "rarity": "Rare" },
    { "name": "Vampire Bat", "chance": 4.0, "rarity": "Rare" },
    { "name": "Werewolf", "chance": 1.65, "rarity": "Epic" },
    { "name": "Goo Monster", "chance": 1.65, "rarity": "Epic" },
    { "name": "Ghost", "chance": 0.65, "rarity": "Legendary" },
    { "name": "Spooky Moth", "chance": 0.05, "rarity": "Chroma" }
]'''

if old_spooky:
    # Keep year/about/icon after blooks - replace only the blooks array
    t2 = re.sub(
        r'(\{\s*\n"name": "Spooky",\s*\n"price": 25,\s*\n"blooks": )\[.*?\]',
        r'\1' + NEW_BLOOKS,
        t,
        count=1,
        flags=re.S,
    )
    t = t2
    print('spooky pack rates replaced')
else:
    print('WARNING: Spooky pack block not found')

# 3) History note
if '2026 \u2014 September 30th (Spooky Pack LIVE)' not in t and '2026 \u2014 September 30th' not in t:
    t = t.replace(
        "'2025 \u2014 October 1st'",
        "'2025 \u2014 October 1st',\n                    '2026 \u2014 September 30th (Spooky Pack LIVE)'",
    )
    t = t.replace(
        "'2025 \u2014 October 1st'",
        "'2025 \u2014 October 1st',\n                    '2026 \u2014 September 30th (Spooky Pack LIVE)'",
    )

if t == orig:
    # Try simpler target-only patch
    t = t.replace('new Date("2026-10-01T00:00:00")', 'new Date("2026-09-30T00:00:00")')
    print('applied target-only fallback' if t != orig else 'NO CHANGES')
else:
    print('patched index.html')

p.write_text(t, encoding='utf-8')
print('size', p.stat().st_size)
# verify
assert '2026-09-30T00:00:00' in t or 'Goo Monster' in t
print('ok')
