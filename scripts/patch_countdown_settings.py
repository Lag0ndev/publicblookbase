#!/usr/bin/env python3
"""Fix countdown LIVE glitch; remove Site Theme / BG size / fonts from Settings."""
from pathlib import Path
import re

p = Path('index.html')
t = p.read_text(encoding='utf-8')

# --- 1) Countdown view: show LIVE state by default (Spooky is out) ---
OLD_CD = re.search(
    r'(<div class="main-content" id="view-countdown"[^>]*>)([\s\S]*?)(</div>\s*(?=<div class="main-content"))',
    t,
)
if OLD_CD:
    NEW_CD_INNER = '''
        <h1 class="header-title countdown-title-btn" id="page-title" onclick="openInfoModal()" title="Switch countdown / info" role="button" tabindex="0">Blooket Spooktober Countdown</h1>

        <div class="countdown-grid" id="countdown">
            <div class="countdown-done" id="countdown-done-msg">&#127875; SPOOKY PACK IS LIVE! &#128123;</div>
        </div>
        <p class="calc-sub" id="countdown-sub" style="margin-top:16px;font-weight:800;opacity:0.9;text-align:center;">Spooky Pack is in the Market right now. Tap the title or ! for other countdowns.</p>
    '''
    t = t[:OLD_CD.start()] + OLD_CD.group(1) + NEW_CD_INNER + OLD_CD.group(3) + t[OLD_CD.end():]
    print('countdown view replaced')
else:
    print('WARNING: countdown view not found')

# --- 2) Harden updateCountdown ---
NEW_UC = r'''function updateCountdown() {
            const page = pages[currentPage];
            if (!page) return;
            const now = new Date();
            const diff = page.target - now;
            const container = document.getElementById('countdown');
            if (!container) return;

            if (diff <= 0) {
                container.innerHTML = '<div class="countdown-done">' + (page.doneText || 'Event is live!') + '</div>';
                const sub = document.getElementById('countdown-sub');
                if (sub) {
                    if (page.key === 'spooktober') sub.textContent = 'Spooky Pack is in the Market right now. Tap the title or ! for other countdowns.';
                    else sub.textContent = '';
                }
                return;
            }

            if (!document.getElementById('days')) {
                container.innerHTML = `
                    <div class="countdown-box">
                        <div class="countdown-number" id="days">--</div>
                        <div class="countdown-label">Days</div>
                    </div>
                    <div class="countdown-box">
                        <div class="countdown-number" id="hours">--</div>
                        <div class="countdown-label">Hours</div>
                    </div>
                    <div class="countdown-box">
                        <div class="countdown-number" id="minutes">--</div>
                        <div class="countdown-label">Minutes</div>
                    </div>
                    <div class="countdown-box">
                        <div class="countdown-number" id="seconds">--</div>
                        <div class="countdown-label">Seconds</div>
                    </div>`;
                const sub = document.getElementById('countdown-sub');
                if (sub) sub.textContent = '';
            }

            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((diff % (1000 * 60)) / 1000);
            const d = document.getElementById('days');
            const h = document.getElementById('hours');
            const m = document.getElementById('minutes');
            const s = document.getElementById('seconds');
            if (d) d.textContent = String(days);
            if (h) h.textContent = String(hours).padStart(2, '0');
            if (m) m.textContent = String(minutes).padStart(2, '0');
            if (s) s.textContent = String(seconds).padStart(2, '0');
        }'''

# Replace whole updateCountdown function - match until next function or comment
m = re.search(r'function updateCountdown\(\) \{[\s\S]*?\n        \}\n\n        /\* ----------', t)
if m:
    # keep the comment start
    t = t[:m.start()] + NEW_UC + '\n\n        /* ----------' + t[m.end():]
    print('updateCountdown replaced')
else:
    m = re.search(r'function updateCountdown\(\) \{[\s\S]*?\n        \}', t)
    if m:
        t = t[:m.start()] + NEW_UC + t[m.end():]
        print('updateCountdown replaced (alt)')
    else:
        print('WARNING: updateCountdown not found')

# Ensure countdown-done is visible / centered
if '.countdown-done' in t and 'text-align: center' not in re.search(r'\.countdown-done \{[^}]+\}', t).group(0):
    t = t.replace(
        '''.countdown-done {
            font-family: 'Titan One', sans-serif;
            font-size: 40px;
            color: white;
            text-shadow: 3px 3px 0 rgba(0,0,0,0.2);
        }''',
        '''.countdown-done {
            font-family: 'Titan One', sans-serif;
            font-size: 40px;
            color: white;
            text-align: center;
            width: 100%;
            padding: 24px 12px;
            text-shadow: 3px 3px 0 rgba(0,0,0,0.2);
        }''',
    )
    print('countdown-done CSS improved')

# --- 3) Remove Site Theme + Blook Checkers Size from Settings ---
# Remove Site Theme section (from h3 Site Theme through end of that settings-section)
t2, n = re.subn(
    r'\s*<div class="settings-section">\s*<h3>Site Theme</h3>[\s\S]*?</div>\s*(?=<div class="settings-section">)',
    '\n\n            ',
    t,
    count=1,
)
print('Site Theme section removed', n)
t = t2

t2, n = re.subn(
    r'\s*<div class="settings-section">\s*<h3>Blook Checkers Size</h3>[\s\S]*?</div>\s*(?=<div class="settings-section">)',
    '\n\n            ',
    t,
    count=1,
)
print('BG size section removed', n)
t = t2

# Remove any leftover custom-theme-panel / theme-grid if orphaned
t = re.sub(r'\s*<div class="theme-grid" id="theme-grid"></div>', '', t)
t = re.sub(r'\s*<div id="custom-theme-panel"[\s\S]*?</div>\s*(?=\s*<div class="settings-section">)', '\n', t, count=1)

p.write_text(t, encoding='utf-8')
print('index size', p.stat().st_size)

# --- 4) No-op bb-settings-enhance.js (no font/theme/BG injection) ---
se = Path('bb-settings-enhance.js')
if se.exists():
    se.write_text(
        "/* bb-settings-enhance disabled — themes/fonts/BG controls removed from Settings */\n"
        "(function(){ window.__bbSE = 1; })();\n",
        encoding='utf-8',
    )
    print('bb-settings-enhance no-op')
else:
    print('bb-settings-enhance missing')

assert 'Site Theme' not in t
assert 'Blook Checkers Size' not in t
assert 'countdown-done' in t
print('OK')
