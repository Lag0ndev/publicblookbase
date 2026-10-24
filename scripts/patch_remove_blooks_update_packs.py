#!/usr/bin/env python3
"""Remove Blooks page from index.html; ensure Spooky Pack rates are official."""
from pathlib import Path
import re

p = Path('index.html')
t = p.read_text(encoding='utf-8')
orig_len = len(t)

# 1) Remove Blooks sidebar button (li with data-view="blooks")
t2, n = re.subn(
    r'\s*<li>\s*<button class="sidebar-link" data-view="blooks"[\s\S]*?</button>\s*</li>',
    '',
    t,
    count=1,
)
print('sidebar blooks removed', n)
t = t2

# 2) Remove view-blooks main-content div
t2, n = re.subn(
    r'\s*<div class="main-content" id="view-blooks"[\s\S]*?</div>(?=\s*(?:<div class="main-content"|<script|<!--))',
    '',
    t,
    count=1,
)
if n == 0:
    # simpler: from id=view-blooks until next main-content or script
    t2, n = re.subn(
        r'<div class="main-content" id="view-blooks"[^>]*>[\s\S]*?</div>\s*',
        '',
        t,
        count=1,
    )
print('view-blooks removed', n)
t = t2

# 3) Remove blooks from allowed views array
t = t.replace(", 'blooks', '404'", ", '404'")
t = t.replace(", 'blooks']", "]")
t = t.replace("'blooks', ", "")

# 4) Remove blooks from path map
t = t.replace(", blooks: 'blooks' ", " ")
t = t.replace(", blooks: 'blooks'", "")
t = t.replace("blooks: 'blooks', ", "")

# 5) Remove switchView special-case for view-blooks
t2, n = re.subn(
    r"\s*\(function\(\)\{\s*var el = document\.getElementById\('view-blooks'\);[\s\S]*?\}\)\(\);",
    '',
    t,
    count=1,
)
print('switchView view-blooks block', n)
t = t2

# Remove lines that set view-blooks display
t = re.sub(r"[^\n]*getElementById\('view-blooks'\)[^\n]*\n", '', t)

# 6) Remove bb-blooks.js script tags
t2, n = re.subn(r'\s*<script[^>]*bb-blooks\.js[^>]*>\s*</script>', '', t)
print('bb-blooks script tags', n)
t = t2

# 7) Ensure Spooky pack has official 14 blooks (idempotent)
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
t2, n = re.subn(
    r'(\{\s*\n"name": "Spooky",\s*\n"price": 25,\s*\n"blooks": )\[.*?\]',
    r'\1' + NEW_BLOOKS,
    t,
    count=1,
    flags=re.S,
)
print('spooky rates', n)
t = t2

# 8) Add Goo Monster + Spooky Moth to blookImageMap if missing
if '"Goo Monster"' not in t or 'goomonster.svg' not in t:
    t = t.replace(
        '"Pumpkin": "https://ac.blooket.com/marketassets/blooks/pumpkin.svg"',
        '"Pumpkin": "https://ac.blooket.com/marketassets/blooks/pumpkin.svg", "Goo Monster": "https://ac.blooket.com/marketassets/blooks/goomonster.svg", "Spooky Moth": "https://ac.blooket.com/marketassets/blooks/spookymoth.svg"',
        1,
    )
    print('image map patched')
elif '"Goo Monster"' not in t:
    # insert before closing of blookImageMap
    t = t.replace(
        '"Astronaut of the Day Placeholder": "https://ac.blooket.com/marketassets/blooks/placeholder.svg"}',
        '"Astronaut of the Day Placeholder": "https://ac.blooket.com/marketassets/blooks/placeholder.svg", "Goo Monster": "https://ac.blooket.com/marketassets/blooks/goomonster.svg", "Spooky Moth": "https://ac.blooket.com/marketassets/blooks/spookymoth.svg"}',
        1,
    )
    print('image map append')

# 9) Mark Spooky as seasonal/live in pack about if present
t = t.replace(
    '"name": "Spooky",\n"price": 25,',
    '"name": "Spooky",\n"price": 25,\n"status": "live",\n"type": "seasonal",',
    1,
)

p.write_text(t, encoding='utf-8')
print('index size', orig_len, '->', len(t))

# Verify
assert 'data-view="blooks"' not in t, 'blooks sidebar still present'
assert 'id="view-blooks"' not in t, 'view-blooks still present'
assert 'Goo Monster' in t and 'Spooky Moth' in t
print('OK')
