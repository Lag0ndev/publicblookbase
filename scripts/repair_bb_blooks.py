#!/usr/bin/env python3
from pathlib import Path
import re
p = Path('bb-blooks.js')
t = p.read_text(encoding='utf-8')
# strip broken +\\n sequences
t = t.replace('+\\n', '+')
t = re.sub(r"\+\\n\s*", '+', t)
# Replace ensureShell body HTML with a known-good one-liner
new_shell = r'''function ensureShell(){
  var root = el('view-blooks');
  if (!root) {
    root = document.createElement('div');
    root.className = 'main-content';
    root.id = 'view-blooks';
    root.style.cssText = 'display:none;flex-direction:column;align-items:center;';
    var v404 = el('view-404');
    if (v404 && v404.parentNode) v404.parentNode.insertBefore(root, v404);
    else document.body.appendChild(root);
  }
  if (el('bb-blooks-grid')) return root;
  root.innerHTML = '<h1 class="header-title">Blooks</h1><div class="leaks-wrap" style="width:100%;max-width:1100px;"><div class="leaks-section" style="margin-bottom:14px;"><p style="font-weight:800;opacity:.9;margin:0 0 12px;">Browse Blooket pack Blooks. Filter by pack, rarity, or search.</p><div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;"><input id="bb-blooks-q" type="search" placeholder="Search blooks..." style="flex:1;min-width:160px;padding:10px 14px;border-radius:10px;border:3px solid rgba(0,0,0,.12);font-weight:700;font-size:15px;"><select id="bb-blooks-pack" style="padding:10px 12px;border-radius:10px;border:3px solid rgba(0,0,0,.12);font-weight:800;font-size:14px;"></select><select id="bb-blooks-rarity" style="padding:10px 12px;border-radius:10px;border:3px solid rgba(0,0,0,.12);font-weight:800;font-size:14px;"></select><span id="bb-blooks-count" style="font-weight:800;opacity:.85;"></span></div></div><div id="bb-blooks-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:12px;"></div></div>';
  return root;
}'''
t2, n = re.subn(r'function ensureShell\(\)\{[\s\S]*?\n\}', new_shell + '\n', t, count=1)
if n != 1:
    raise SystemExit(f'ensureShell replace failed ({n})')
p.write_text(t2)
print('fixed ensureShell', len(t2))
