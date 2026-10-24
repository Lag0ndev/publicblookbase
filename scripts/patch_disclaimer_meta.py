#!/usr/bin/env python3
"""Fix broken meta tags (: > top-left) and move countdown disclaimer to ! info modal."""
from pathlib import Path
import re

p = Path('index.html')
t = p.read_text(encoding='utf-8')
orig = t

# 1) Fix broken meta tags that leak ": >" into the page
# description missing closing >
t = t.replace(
    'meta name="description" content="Blookbase is a free fan-made Blooket hub: season countdowns, What\'s New, packs & rarities, gamemodes, leaks, update tracker, and videos. Unofficial \u2014 not affiliated with Blooket."\n',
    'meta name="description" content="Blookbase is a free fan-made Blooket hub: season countdowns, What\'s New, packs & rarities, gamemodes, leaks, update tracker, and videos. Unofficial \u2014 not affiliated with Blooket.">\n',
)
# keywords has >>
t = t.replace(
    'Blooket tracker, Spooktober, Season 9">>',
    'Blooket tracker, Spooktober, Season 9">',
)
# more robust regex fallbacks
if 'Season 9">>' in t:
    t = t.replace('Season 9">>', 'Season 9">')
if re.search(r'<meta name="description" content="[^"]+"\s*\n', t):
    t = re.sub(
        r'(<meta name="description" content="[^"]+")\s*\n',
        r'\1>\n',
        t,
        count=1,
    )
print('meta fixed', 'Season 9">>' not in t)

# 2) Remove countdown-page disclaimer paragraph entirely
t2, n = re.subn(
    r'\s*<p id="countdown-disclaimer"[^>]*>[\s\S]*?</p>',
    '',
    t,
    count=1,
)
print('countdown disclaimer removed', n)
t = t2

# 3) Put full disclaimer on the ! info modal (history-estimate-note)
NEW_NOTE = (
    '⚠️ This date is <b>not confirmed</b> by Blooket. '
    'It is only an <b>estimate</b> based on previous years\u2019 release patterns.'
)
if 'id="history-estimate-note"' in t:
    t2, n = re.subn(
        r'(<p id="history-estimate-note"[^>]*>)[\s\S]*?(</p>)',
        r'\1' + NEW_NOTE + r'\2',
        t,
        count=1,
    )
    print('info modal note updated', n)
    t = t2
else:
    # insert before history-list
    t = t.replace(
        '<ul style="list-style: none; padding: 0; margin: 0; font-size: 15px;" id="history-list">',
        '<p id="history-estimate-note" style="font-size:13px;font-weight:700;opacity:0.85;margin:0 0 10px;line-height:1.4;">' + NEW_NOTE + '</p>\n                <ul style="list-style: none; padding: 0; margin: 0; font-size: 15px;" id="history-list">',
        1,
    )
    print('info modal note inserted')

p.write_text(t, encoding='utf-8')
print('size', len(orig), '->', len(t))
assert 'countdown-disclaimer' not in t
assert 'Season 9">>' not in t
assert 'not confirmed' in t  # still in info modal
print('OK')
