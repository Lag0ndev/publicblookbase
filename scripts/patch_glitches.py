#!/usr/bin/env python3
"""Small glitch fixes in index.html"""
from pathlib import Path
import re
p = Path('index.html')
t = p.read_text(encoding='utf-8')
changed = False

# Show info-btn on countdown only
old = """            const infoBtn = document.getElementById('info-btn');
            if (infoBtn) infoBtn.style.display = 'none';"""
new = """            const infoBtn = document.getElementById('info-btn');
            if (infoBtn) infoBtn.style.display = (view === 'countdown') ? 'flex' : 'none';"""
if old in t:
    t = t.replace(old, new, 1)
    print('info-btn countdown fix')
    changed = True
else:
    print('info-btn already patched or missing')

# Ensure pageTitles has blooks (idempotent)
if "blooks: 'Blooks'" not in t:
    t2, n = re.subn(
        r"(about:\s*'About',\s*)('404':\s*'Not Found')",
        r"\1blooks: 'Blooks',\n                \2",
        t, count=1)
    if n:
        t = t2
        print('pageTitles blooks')
        changed = True

if changed:
    p.write_text(t, encoding='utf-8')
    print('WROTE', len(t))
else:
    print('No index changes')
