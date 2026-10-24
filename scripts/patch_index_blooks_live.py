#!/usr/bin/env python3
"""Patch index.html so Blooks actually works: show view + load scripts."""
from pathlib import Path
import re

p = Path("index.html")
t = p.read_text(encoding="utf-8")
changed = False

# 1) Show/hide view-blooks in switchView
old = """            const v404 = document.getElementById('view-404');
            if (v404) v404.style.display = view === '404' ? 'flex' : 'none';
            if (view === 'blooks' && typeof window.__bbRenderBlooks === 'function') window.__bbRenderBlooks();"""

new = """            const v404 = document.getElementById('view-404');
            if (v404) v404.style.display = view === '404' ? 'flex' : 'none';
            (function(){
                var el = document.getElementById('view-blooks');
                if (el) el.style.display = view === 'blooks' ? 'flex' : 'none';
            })();
            if (view === 'blooks' && typeof window.__bbRenderBlooks === 'function') window.__bbRenderBlooks();"""

if old in t:
    t = t.replace(old, new, 1)
    print("switchView display OK")
    changed = True
elif "getElementById('view-blooks')" in t[t.find("function switchView"):t.find("function switchView")+3000]:
    print("switchView already has view-blooks display")
else:
    marker = "if (view === 'blooks' && typeof window.__bbRenderBlooks === 'function') window.__bbRenderBlooks();"
    if marker in t and "getElementById('view-blooks')" not in t[max(0,t.find(marker)-400):t.find(marker)]:
        inj = """(function(){
                var el = document.getElementById('view-blooks');
                if (el) el.style.display = view === 'blooks' ? 'flex' : 'none';
            })();
            """
        t = t.replace(marker, inj + marker, 1)
        print("switchView display injected (flex)")
        changed = True
    else:
        print("WARN: could not patch switchView display")

# 2) pageTitles
if "blooks: 'Blooks'" not in t and 'blooks: "Blooks"' not in t:
    t2, n = re.subn(
        r"(about:\s*'About',\s*)('404':\s*'Not Found')",
        r"\1blooks: 'Blooks',\n                \2",
        t,
        count=1,
    )
    if n:
        t = t2
        print("pageTitles OK")
        changed = True
    else:
        print("WARN: pageTitles")

# 3) script tags
if 'src="bb-blooks.js"' not in t:
    scripts = (
        '\n<script src="bb-blooks.js" defer></script>\n'
        '<script src="bb-settings-enhance.js" defer></script>\n'
        '<script src="bb-leaks-tracker.js" defer></script>\n'
    )
    if "</body>" in t:
        t = t.replace("</body>", scripts + "</body>", 1)
        print("scripts injected")
        changed = True
    else:
        raise SystemExit("no </body>")
else:
    print("scripts already there")

# 4) Ensure view-blooks exists
if 'id="view-blooks"' not in t:
    i = t.find('id="view-404"')
    st = t.rfind("<div", 0, i)
    shell = (
        '\n    <div class="main-content" id="view-blooks" '
        'style="display:none;flex-direction:column;align-items:center;">\n'
        '      <h1 class="header-title">Blooks</h1>\n'
        '      <div class="leaks-wrap"><p style="font-weight:800;">Loading blooks…</p></div>\n'
        '    </div>\n'
    )
    t = t[:st] + shell + t[st:]
    print("inserted view-blooks")
    changed = True

# 5) Strip secret leftovers if any
t2, n = re.subn(
    r'\s*<li>\s*<button class="sidebar-link" data-view="secret"[^>]*>[\s\S]*?</button>\s*</li>',
    '',
    t,
)
if n:
    t = t2
    print("removed secret sidebar", n)
    changed = True

if not changed:
    print("No changes needed")
else:
    p.write_text(t, encoding="utf-8")
    print("WROTE", len(t))

print("verify bb-blooks.js tag", 'src="bb-blooks.js"' in t)
print("verify suitcase", 'data-icon="suitcase"' in t)
print("verify secret sidebar", 'data-view="secret"' in t)
print("verify view-blooks", 'id="view-blooks"' in t)
