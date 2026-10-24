#!/usr/bin/env python3
"""Remove CSS/boot that forced #view-home visible on every page."""
from pathlib import Path
import re

p = Path('index.html')
t = p.read_text(encoding='utf-8')

# 1) Replace critical CSS — no !important on #view-home
NEW_CRIT = '''<style id="bb-critical">
      html, body { min-height: 100%; margin: 0; }
      body { color: #1a1a1a; }
      .main-content { position: relative; z-index: 1; }
    </style>'''

t2, n = re.subn(
    r'<style id="bb-critical">[\s\S]*?</style>',
    NEW_CRIT,
    t,
    count=1,
)
print('critical css replaced', n)
t = t2

# 2) Replace boot failsafe — only rescue once if NOTHING is visible; never re-force home after nav
NEW_BOOT = '''<script id="bb-boot">
(function () {
  var done = false;
  function rescue() {
    if (done) return;
    try {
      document.body && document.body.classList.remove('ps-opening', 'no-scroll', 'bb-page-editing');
      var ov = document.getElementById('sidebar-overlay');
      if (ov && !ov.classList.contains('open')) {
        ov.style.display = 'none';
      }
      var pw = document.getElementById('pack-wrapper');
      if (pw) pw.style.display = 'none';
      var any = false;
      document.querySelectorAll('.main-content').forEach(function (el) {
        var d = (el.style && el.style.display) || window.getComputedStyle(el).display;
        if (d === 'flex' || d === 'block') any = true;
      });
      if (!any) {
        var home = document.getElementById('view-home');
        if (home) home.style.display = 'flex';
      }
      done = true;
    } catch (e) {}
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', rescue);
  else rescue();
  setTimeout(rescue, 50);
})();
</script>'''

t2, n = re.subn(
    r'<script id="bb-boot">[\s\S]*?</script>',
    NEW_BOOT,
    t,
    count=1,
)
print('boot replaced', n)
t = t2

# 3) Ensure switchView explicitly hides ALL main-content then shows target
# Find and patch if needed — make display assignment solid
old_pat = re.search(
    r"document\.getElementById\('view-home'\)\.style\.display = view === 'home' \? 'flex' : 'none';",
    t,
)
if old_pat:
    # leave individual assignments but ensure they work without !important
    print('switchView home display line present')
else:
    print('WARNING: switchView home line not found in expected form')

# 4) Harden switchView: prepend a clear-all at start of view switching if not present
if "querySelectorAll('.main-content')" not in t[t.find('function switchView'):t.find('function switchView')+800]:
    t = t.replace(
        "currentView = view;",
        "currentView = view;\n            document.querySelectorAll('.main-content').forEach(function(el){ el.style.display = 'none'; });",
        1,
    )
    print('added clear-all main-content in switchView')
else:
    print('switchView already clears or different structure')

# After clear-all, individual set display flex — if we added clear-all, the subsequent lines set the right one

p.write_text(t, encoding='utf-8')
print('size', p.stat().st_size)
assert '#view-home { display: flex !important; }' not in t
assert 'id="bb-critical"' in t
print('OK')
