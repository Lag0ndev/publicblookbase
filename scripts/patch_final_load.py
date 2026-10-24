#!/usr/bin/env python3
"""Make index.html load even if CDNs/scripts fail. Keep UI the same."""
from pathlib import Path
import re

p = Path('index.html')
t = p.read_text(encoding='utf-8')
orig = len(t)

# --- 1) MQTT: never block HTML parsing ---
t = t.replace(
    '<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>',
    '<script src="https://unpkg.com/mqtt/dist/mqtt.min.js" defer async></script>',
)
t = re.sub(
    r'<script src="https://unpkg.com/mqtt/dist/mqtt\.min\.js"[^>]*></script>',
    '<script src="https://unpkg.com/mqtt/dist/mqtt.min.js" defer async></script>',
    t,
    count=1,
)

# Guard mqtt.connect
if "typeof mqtt === 'undefined'" not in t:
    t = t.replace(
        'client = mqtt.connect(url, {',
        "if (typeof mqtt === 'undefined' || !mqtt || !mqtt.connect) { try { renderCount(); } catch (e) {} return; }\n                    client = mqtt.connect(url, {",
        1,
    )

# --- 2) Home visible without JS ---
t = t.replace(
    '<div class="main-content" id="view-home">',
    '<div class="main-content" id="view-home" style="display:flex;">',
    1,
)
# ensure other main views start hidden if missing style
for vid in ['countdown','whatsnew','videos','gamemodes','banners','market','packsim','updates','settings','about','404','blooks']:
    t = re.sub(
        rf'(<div class="main-content" id="view-{vid}")(?![^>]*style=)',
        rf'\1 style="display:none;"',
        t,
        count=1,
    )

# --- 3) Critical CSS: always-visible text/background ---
crit = '''
    <style id="bb-critical">
      html, body { min-height: 100%; margin: 0; }
      body { color: #1a1a1a; background: #2a9fe8; }
      .main-content { position: relative; z-index: 1; }
      #view-home { display: flex !important; }
      .header-title, .home-banner h2, .home-banner p, .sidebar-text { color: #fff !important; }
      body.ps-opening .main-content { display: flex !important; }
    </style>
'''
if 'id="bb-critical"' not in t:
    t = t.replace('</head>', crit + '</head>', 1)

# --- 4) Boot failsafe right after <body> ---
failsafe = '''
<script id="bb-boot">
(function () {
  function rescue() {
    try {
      document.body && document.body.classList.remove('ps-opening', 'no-scroll', 'bb-page-editing');
      var ov = document.getElementById('sidebar-overlay');
      if (ov) { ov.classList.remove('open'); ov.style.display = 'none'; }
      var pw = document.getElementById('pack-wrapper');
      if (pw) pw.style.display = 'none';
      var home = document.getElementById('view-home');
      if (!home) return;
      var visible = false;
      document.querySelectorAll('.main-content').forEach(function (el) {
        var d = (el.style && el.style.display) || '';
        if (d === 'flex' || d === 'block') visible = true;
      });
      if (!visible) {
        document.querySelectorAll('.main-content').forEach(function (el) { el.style.display = 'none'; });
        home.style.display = 'flex';
      }
    } catch (e) {}
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', rescue);
  else rescue();
  setTimeout(rescue, 0);
  setTimeout(rescue, 300);
  setTimeout(rescue, 1000);
  setTimeout(rescue, 3000);
})();
</script>
'''
if 'id="bb-boot"' not in t:
    t = t.replace('<body>', '<body>\n' + failsafe, 1)

# --- 5) Unknown routes -> home (not hard 404 blank feel) ---
t = t.replace(
    "} else {\n                switchView('404', true);\n            }",
    "} else {\n                switchView('home', true);\n            }",
    1,
)

# --- 6) Theme sanitizer so bad localStorage can't blank the UI ---
san = '''
<script id="bb-theme-safe">
(function () {
  try {
    var k = localStorage.getItem('blookbase_theme');
    if (k && k.length > 40) localStorage.removeItem('blookbase_theme');
  } catch (e) {}
  try {
    var c = localStorage.getItem('blookbase_custom_theme');
    if (c) {
      var o = JSON.parse(c);
      if (!o || typeof o !== 'object') localStorage.removeItem('blookbase_custom_theme');
    }
  } catch (e) {
    try { localStorage.removeItem('blookbase_custom_theme'); } catch (e2) {}
  }
})();
</script>
'''
if 'id="bb-theme-safe"' not in t:
    t = t.replace('<body>', '<body>\n' + san, 1)

# --- 7) Noscript fallback ---
if '<noscript>' not in t:
    t = t.replace(
        '<body>',
        '<body>\n<noscript style="display:block;padding:24px;font-family:sans-serif;background:#fff;color:#000;"><h1>Blookbase</h1><p>Enable JavaScript to use the full site. Static content requires JS for navigation.</p></noscript>',
        1,
    )

p.write_text(t, encoding='utf-8')
print('index', orig, '->', len(t))

# Safe vercel.json: only rewrite extensionless paths; never touch .js/.css/.png
Path('vercel.json').write_text('''{
  "cleanUrls": false,
  "trailingSlash": false,
  "rewrites": [
    { "source": "/", "destination": "/index.html" },
    { "source": "/countdown", "destination": "/index.html" },
    { "source": "/whatsnew", "destination": "/index.html" },
    { "source": "/leaks", "destination": "/index.html" },
    { "source": "/videos", "destination": "/index.html" },
    { "source": "/gamemodes", "destination": "/index.html" },
    { "source": "/banners", "destination": "/index.html" },
    { "source": "/packs", "destination": "/index.html" },
    { "source": "/market", "destination": "/index.html" },
    { "source": "/calculator", "destination": "/index.html" },
    { "source": "/packsim", "destination": "/index.html" },
    { "source": "/about", "destination": "/index.html" },
    { "source": "/blooks", "destination": "/index.html" },
    { "source": "/updates", "destination": "/index.html" },
    { "source": "/settings", "destination": "/index.html" }
  ],
  "headers": [
    {
      "source": "/index.html",
      "headers": [
        { "key": "Cache-Control", "value": "no-cache, no-store, must-revalidate" },
        { "key": "X-Blookbase-Deploy", "value": "2026-10-02-final-load" }
      ]
    },
    {
      "source": "/",
      "headers": [
        { "key": "Cache-Control", "value": "no-cache, no-store, must-revalidate" },
        { "key": "X-Blookbase-Deploy", "value": "2026-10-02-final-load" }
      ]
    }
  ]
}
''', encoding='utf-8')
print('vercel.json ok')
assert 'bb-boot' in t or 'bb-critical' in t
print('OK')
