#!/usr/bin/env python3
from pathlib import Path
import re

p = Path('index.html')
t = p.read_text(encoding='utf-8')

# Remove bb-blooks script tags
t2, n = re.subn(r'\s*<script[^>]*bb-blooks\.js[^>]*>\s*</script>', '', t)
print('bb-blooks script removed', n)
t = t2

# Remove any leftover sidebar blooks button
t2, n = re.subn(
    r'\s*<li>\s*<button class="sidebar-link" data-view="blooks"[\s\S]*?</button>\s*</li>',
    '',
    t,
)
print('sidebar blooks', n)
t = t2

# Remove view-blooks section if present
t2, n = re.subn(
    r'\s*<div class="main-content" id="view-blooks"[\s\S]*?</div>\s*(?=<div class="main-content"|<script|<!--)',
    '\n',
    t,
    count=1,
)
print('view-blooks', n)
t = t2

# Strip blooks from allowed / path maps if present
t = t.replace(", 'blooks'", '')
t = t.replace("'blooks', ", '')
t = t.replace(", blooks: 'blooks'", '')
t = t.replace("blooks: 'blooks', ", '')

# Glitch: ensure no home !important force
t = t.replace('#view-home { display: flex !important; }', '/* view-home not forced */')
t = t.replace('body.ps-opening .main-content { display: flex !important; }', '/* pack opening does not force all views */')

p.write_text(t, encoding='utf-8')
print('index', p.stat().st_size)

# vercel.json without /blooks
v = Path('vercel.json')
if v.exists():
    text = v.read_text(encoding='utf-8')
    text2 = re.sub(r'\s*\{ "source": "/blooks", "destination": "/index.html" \},?\n', '\n', text)
    v.write_text(text2, encoding='utf-8')
    print('vercel blooks route stripped', text != text2)

assert 'bb-blooks.js' not in t
print('OK')
