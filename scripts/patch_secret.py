#!/usr/bin/env python3
from pathlib import Path
p = Path("index.html")
t = p.read_text(encoding="utf-8")
if 'id="view-secret"' in t and "secret: 'secret'" in t:
    print("Already patched")
    raise SystemExit(0)

old_allowed = "const allowed = ['home', 'countdown', 'whatsnew', 'videos', 'gamemodes', 'banners', 'market', 'packsim', 'updates', 'settings', 'about', '404'];"
new_allowed = "const allowed = ['home', 'countdown', 'whatsnew', 'videos', 'gamemodes', 'banners', 'market', 'packsim', 'updates', 'settings', 'about', 'secret', 'stats', 'blooks', 'bbmarket', '404'];"
assert old_allowed in t, "allowed not found"
t = t.replace(old_allowed, new_allowed, 1)

old_map = "const map = { home: 'home', countdown: 'countdown', whatsnew: 'whatsnew', leaks: 'whatsnew', videos: 'videos', gamemodes: 'gamemodes', banners: 'banners', market: 'market', packsim: 'packsim', updates: 'updates', settings: 'settings', about: 'about' };"
new_map = "const map = { home: 'home', countdown: 'countdown', whatsnew: 'whatsnew', leaks: 'whatsnew', videos: 'videos', gamemodes: 'gamemodes', banners: 'banners', market: 'market', packsim: 'packsim', updates: 'updates', settings: 'settings', about: 'about', secret: 'secret', 'secret!!!': 'secret', stats: 'stats', blooks: 'blooks', 'secret-market': 'bbmarket', smarket: 'bbmarket' };"
assert old_map in t, "map not found"
t = t.replace(old_map, new_map, 1)

marker = "if (v404) v404.style.display = view === '404' ? 'flex' : 'none';"
assert marker in t, "v404 marker not found"
secret_block = "\n            ['secret','stats','blooks','bbmarket'].forEach(function(sv){\n                var el = document.getElementById('view-' + sv);\n                if (el) el.style.display = view === sv ? 'flex' : 'none';\n            });\n            if (view === 'secret' && typeof window.__bbRenderSecret === 'function') window.__bbRenderSecret();\n"
t = t.replace(marker, marker + secret_block, 1)

secret_html = """
    <div class=\"main-content\" id=\"view-secret\" style=\"display:none;flex-direction:column;align-items:center;\">
      <h1 class=\"header-title\">Secret !!!</h1>
      <div class=\"leaks-wrap\" style=\"display:flex;flex-direction:column;align-items:center;width:100%;max-width:520px;\">
        <div style=\"background:#9a49aa;border:6px solid rgba(255,255,255,.2);border-radius:12px;padding:20px;margin-bottom:16px;box-shadow:4px 4px rgba(0,0,0,.2);color:#fff;text-align:center;width:100%;\">
          <h3 style=\"font-family:'Titan One',sans-serif;font-weight:normal;font-size:22px;margin:0 0 12px;\">Daily Tokens</h3>
          <div id=\"bb-bal\" style=\"font-size:28px;font-weight:900;margin:8px 0 4px;text-shadow:2px 2px 0 rgba(0,0,0,.2);\">0</div>
          <div style=\"font-size:13px;font-weight:800;opacity:.85;margin-bottom:12px;\">tokens</div>
          <button type=\"button\" id=\"bb-claim\" style=\"display:inline-block;background:linear-gradient(180deg,#ffd76a,#f0a020);color:#4a2a00;font-weight:900;font-size:16px;padding:12px 28px;border-radius:12px;border:4px solid rgba(255,255,255,.4);cursor:pointer;font-family:'Nunito',sans-serif;\">Claim 500 Tokens</button>
          <div id=\"bb-ts\" style=\"font-size:14px;font-weight:800;margin-top:10px;\"></div>
        </div>
        <div style=\"background:#9a49aa;border:6px solid rgba(255,255,255,.2);border-radius:12px;padding:20px;margin-bottom:16px;box-shadow:4px 4px rgba(0,0,0,.2);color:#fff;text-align:center;width:100%;\">
          <h3 style=\"font-family:'Titan One',sans-serif;font-weight:normal;font-size:22px;margin:0 0 12px;\">Secret Menu</h3>
          <p style=\"font-weight:700;opacity:.9;margin:0 0 14px;\">Only linked here — not on the main sidebar.</p>
          <div style=\"display:flex;flex-wrap:wrap;gap:12px;justify-content:center;\">
            <button type=\"button\" onclick=\"switchView('stats')\" style=\"color:#fff;font-weight:900;background:rgba(255,255,255,.18);padding:12px 20px;border-radius:12px;border:3px solid rgba(255,255,255,.35);cursor:pointer;font-family:'Nunito',sans-serif;font-size:15px;\">Stats</button>
            <button type=\"button\" onclick=\"switchView('bbmarket')\" style=\"color:#fff;font-weight:900;background:rgba(255,255,255,.18);padding:12px 20px;border-radius:12px;border:3px solid rgba(255,255,255,.35);cursor:pointer;font-family:'Nunito',sans-serif;font-size:15px;\">Market</button>
            <button type=\"button\" onclick=\"switchView('blooks')\" style=\"color:#fff;font-weight:900;background:rgba(255,255,255,.18);padding:12px 20px;border-radius:12px;border:3px solid rgba(255,255,255,.35);cursor:pointer;font-family:'Nunito',sans-serif;font-size:15px;\">Blooks</button>
          </div>
        </div>
      </div>
    </div>
    <div class=\"main-content\" id=\"view-stats\" style=\"display:none;flex-direction:column;align-items:center;\">
      <h1 class=\"header-title\">Stats</h1>
      <div class=\"leaks-wrap\"><div class=\"leaks-section\"><p style=\"font-weight:800;opacity:.9;\">Stats coming soon. Nothing here yet.</p></div></div>
    </div>
    <div class=\"main-content\" id=\"view-bbmarket\" style=\"display:none;flex-direction:column;align-items:center;\">
      <h1 class=\"header-title\">Market</h1>
      <div class=\"leaks-wrap\"><div class=\"leaks-section\"><p style=\"font-weight:800;opacity:.9;\">Secret Market coming soon. Nothing here yet.</p></div></div>
    </div>
    <div class=\"main-content\" id=\"view-blooks\" style=\"display:none;flex-direction:column;align-items:center;\">
      <h1 class=\"header-title\">Blooks</h1>
      <div class=\"leaks-wrap\"><div class=\"leaks-section\"><p style=\"font-weight:800;opacity:.9;\">Blooks inventory coming soon. Nothing here yet.</p></div></div>
    </div>
"""
idx = t.find('id="view-404"')
assert idx > 0, "view-404 not found"
start = t.rfind("<div", 0, idx)
t = t[:start] + secret_html + t[start:]

si = t.find('data-view="whatsnew"')
assert si > 0, "whatsnew not found"
li_end = t.find("</li>", si) + len("</li>")
if 'data-view="secret"' not in t[si:si+800]:
    secret_li = """
                <li>
                    <button class=\"sidebar-link\" data-view=\"secret\" onclick=\"switchView('secret')\" type=\"button\">
                        <span class=\"sidebar-listIcon\"><i class=\"fas fa-lock\"></i></span>
                        <span class=\"sidebar-text\">Secret !!!</span>
                    </button>
                </li>"""
    t = t[:li_end] + secret_li + t[li_end:]

token_js = r"""
        window.__bbRenderSecret = function() {
            function today() {
                var d = new Date();
                return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
            }
            function getTok() { try { return parseInt(localStorage.getItem('bb_tokens')||'0',10)||0; } catch(e){ return 0; } }
            function setTok(n) { try { localStorage.setItem('bb_tokens', String(n)); } catch(e){} }
            function canClaim() { try { return localStorage.getItem('bb_last_claim') !== today(); } catch(e){ return true; } }
            var bal = document.getElementById('bb-bal');
            var btn = document.getElementById('bb-claim');
            var ts = document.getElementById('bb-ts');
            if (bal) bal.textContent = String(getTok());
            if (btn && ts) {
                if (canClaim()) {
                    btn.disabled = false;
                    btn.textContent = 'Claim 500 Tokens';
                    ts.textContent = 'You can claim your daily tokens!';
                } else {
                    btn.disabled = true;
                    btn.textContent = 'Already claimed today';
                    ts.textContent = 'Come back tomorrow for another 500 tokens.';
                }
                btn.onclick = function() {
                    if (!canClaim()) return;
                    setTok(getTok() + 500);
                    try { localStorage.setItem('bb_last_claim', today()); } catch(e){}
                    if (bal) bal.textContent = String(getTok());
                    btn.disabled = true;
                    btn.textContent = 'Already claimed today';
                    ts.textContent = 'Claimed +500! Come back tomorrow.';
                };
            }
        };
"""
sv = t.find("function switchView(")
assert sv > 0, "switchView not found"
t = t[:sv] + token_js + "\n        " + t[sv:]

p.write_text(t, encoding="utf-8")
print("Patched index.html", len(t))
