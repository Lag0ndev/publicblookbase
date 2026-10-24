#!/usr/bin/env python3
from pathlib import Path
import re

p = Path("index.html")
t = p.read_text(encoding="utf-8")

t, n = re.subn(
    r'\s*<li>\s*<button class="sidebar-link" data-view="secret"[^>]*>[\s\S]*?</button>\s*</li>',
    '',
    t,
    count=1,
)
print("removed secret sidebar", n)

m = re.search(r'data-view="market"[\s\S]*?</li>', t)
if not m:
    raise SystemExit("market sidebar not found")
insert = """
                <li>
                    <button class="sidebar-link" data-view="blooks" onclick="switchView('blooks')" type="button">
                        <span class="sidebar-listIcon"><i class="fas fa-paw"></i></span>
                        <span class="sidebar-text">Blooks</span>
                    </button>
                </li>"""
after = t[m.end(): m.end() + 600]
if 'sidebar-text">Blooks</span>' not in after:
    t = t[: m.end()] + insert + t[m.end() :]
    print("added blooks sidebar")
else:
    print("blooks sidebar already nearby")

old_map = "const map = { home: 'home', countdown: 'countdown', whatsnew: 'whatsnew', leaks: 'whatsnew', videos: 'videos', gamemodes: 'gamemodes', banners: 'banners', market: 'market', packsim: 'packsim', updates: 'updates', settings: 'settings', about: 'about', secret: 'secret', 'secret!!!': 'secret', stats: 'stats', blooks: 'blooks', 'secret-market': 'bbmarket', smarket: 'bbmarket' };"
new_map = "const map = { home: 'home', countdown: 'countdown', whatsnew: 'whatsnew', leaks: 'whatsnew', videos: 'videos', gamemodes: 'gamemodes', banners: 'banners', market: 'market', packsim: 'packsim', updates: 'updates', settings: 'settings', about: 'about', secret: 'secret', blooks: 'blooks' };"
if old_map in t:
    t = t.replace(old_map, new_map, 1)
    print("path map exact replace")
else:
    t2, n = re.subn(r"const map = \{ home: 'home'[^;]+;", new_map, t, count=1)
    t = t2
    print("path map regex", n)

old_a = "const allowed = ['home', 'countdown', 'whatsnew', 'videos', 'gamemodes', 'banners', 'market', 'packsim', 'updates', 'settings', 'about', 'secret', 'stats', 'blooks', 'bbmarket', '404'];"
new_a = "const allowed = ['home', 'countdown', 'whatsnew', 'videos', 'gamemodes', 'banners', 'market', 'packsim', 'updates', 'settings', 'about', 'secret', 'blooks', '404'];"
if old_a in t:
    t = t.replace(old_a, new_a, 1)
    print("allowed exact")
else:
    t2, n = re.subn(r"const allowed = \[[^\]]+\];", new_a, t, count=1)
    t = t2
    print("allowed regex", n)

marker = "if (v404) v404.style.display = view === '404' ? 'flex' : 'none';"
t = re.sub(
    r"\n\s*\['secret','stats','blooks','bbmarket'\]\.forEach\([\s\S]{0,400}?__bbRenderSecret\(\);\n?",
    "\n",
    t,
    count=1,
)
if marker in t and "['secret','blooks'].forEach" not in t:
    block = """
            ['secret','blooks'].forEach(function(sv){
                var el = document.getElementById('view-' + sv);
                if (el) el.style.display = view === sv ? 'flex' : 'none';
            });
            if (view === 'secret' && typeof window.__bbRenderSecret === 'function') window.__bbRenderSecret();
            if (view === 'blooks' && typeof window.__bbRenderBlooks === 'function') window.__bbRenderBlooks();
"""
    t = t.replace(marker, marker + block, 1)
    print("hooks added")
elif "__bbRenderBlooks" not in t and "__bbRenderSecret" in t:
    t = t.replace(
        "window.__bbRenderSecret();",
        "window.__bbRenderSecret();\n            if (view === 'blooks' && typeof window.__bbRenderBlooks === 'function') window.__bbRenderBlooks();",
        1,
    )
    print("blooks hook appended")

secret_html = '''id="view-secret" style="display:none;flex-direction:column;align-items:center;">
      <h1 class="header-title">Secret</h1>
      <div class="leaks-wrap" style="display:flex;flex-direction:column;align-items:center;width:100%;max-width:420px;">
        <div style="background:#9a49aa;border:6px solid rgba(255,255,255,.2);border-radius:12px;padding:20px;margin-bottom:16px;box-shadow:4px 4px rgba(0,0,0,.2);color:#fff;text-align:center;width:100%;">
          <h3 style="font-family:'Titan One',sans-serif;font-weight:normal;font-size:22px;margin:0 0 12px;">Daily Tokens</h3>
          <div id="bb-bal" style="font-size:28px;font-weight:900;margin:8px 0 4px;text-shadow:2px 2px 0 rgba(0,0,0,.2);">0</div>
          <div style="font-size:13px;font-weight:800;opacity:.85;margin-bottom:12px;">tokens</div>
          <button type="button" id="bb-claim" class="settings-reset-btn" style="background:#fff;color:#4a2a00;font-weight:900;border:3px solid rgba(0,0,0,.15);">Claim 500 Tokens</button>
          <div id="bb-ts" style="font-size:14px;font-weight:800;margin-top:10px;"></div>
        </div>
        <p style="font-weight:700;opacity:.75;text-align:center;">Opened from Settings. Tokens stay on this device.</p>
      </div>
    </div>'''
if 'id="view-secret"' in t:
    s = t.find('id="view-secret"')
    nxt = t.find('id="view-', s + 10)
    if nxt < 0:
        raise SystemExit("no next view after secret")
    div_next = t.rfind("<div", 0, nxt)
    t = t[:s] + secret_html + t[div_next:]
    print("secret simplified")
else:
    i = t.find('id="view-404"')
    st = t.rfind("<div", 0, i)
    t = t[:st] + '<div class="main-content" ' + secret_html + t[st:]
    print("secret inserted")

blooks_shell = '''id="view-blooks" style="display:none;flex-direction:column;align-items:center;">
      <h1 class="header-title">Blooks</h1>
      <div class="leaks-wrap"><p style="font-weight:800;">Loading blooks…</p></div>
    </div>'''
if 'id="view-blooks"' in t:
    s = t.find('id="view-blooks"')
    nxt = t.find('id="view-', s + 10)
    if nxt > 0:
        div_next = t.rfind("<div", 0, nxt)
        t = t[:s] + blooks_shell + t[div_next:]
        print("blooks refreshed")
else:
    i = t.find('id="view-404"')
    st = t.rfind("<div", 0, i)
    t = t[:st] + '<div class="main-content" ' + blooks_shell + t[st:]
    print("blooks inserted")

if "Open Secret" not in t:
    block = """
            <div class="settings-section">
                <h3>Secret</h3>
                <p class="settings-hint">Daily tokens (saved on this device only).</p>
                <button class="settings-reset-btn" type="button" onclick="switchView('secret')">Open Secret</button>
            </div>
"""
    marker_admin = '<div class="settings-section" id="admin-gate">'
    if marker_admin in t:
        t = t.replace(marker_admin, block + marker_admin, 1)
        print("settings secret before admin-gate")
    else:
        raise SystemExit("admin-gate section not found")
else:
    print("Open Secret already there")

p.write_text(t, encoding="utf-8")
print("OK size", len(t))
