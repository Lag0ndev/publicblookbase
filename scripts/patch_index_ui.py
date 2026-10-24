#!/usr/bin/env python3
"""Patch index.html: home Spooky LIVE + What's New clickable blooks + bb-ui-fixes script."""
import re
from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")
changed = False

EM = "\u2014"
MID = "\u00b7"

if 'src="https://ac.blooket.com/marketassets/blooks/pumpkin.svg" alt="Spooktober"' in html:
    html = html.replace(
        'src="https://ac.blooket.com/marketassets/blooks/pumpkin.svg" alt="Spooktober"',
        'src="https://ac.blooket.com/marketassets/blooks/spookymoth.svg" alt="Spooky Pack"',
        1,
    )
    html = html.replace(
        '<div class="home-banner-label">Spooktober</div>',
        '<div class="home-banner-label">Spooktober ' + MID + ' LIVE</div>',
        1,
    )
    html = html.replace(
        '<h2>Spooktober is coming!</h2>',
        '<h2>Spooky Pack is LIVE!</h2>',
        1,
    )
    new_p = (
        "Halloween is here "
        + EM
        + " Spooky Pack is in the Market with 14 blooks. Open Countdown for event timers and Season updates."
    )

    def repl_p(m):
        return m.group(1) + new_p + m.group(2)

    html, n = re.subn(
        r'(<div class="home-banner">[\s\S]*?<p>)The Halloween event countdown is live.{0,120}?(</p>)',
        repl_p,
        html,
        count=1,
    )
    changed = True
    print("banner patched", n)
elif "Spooky Pack is LIVE!" in html and "Spooktober is coming!" not in html:
    print("banner already LIVE")
else:
    print("WARNING: banner pattern not found")

start = html.find('id="view-whatsnew"')
end = html.find('id="view-videos"')
if start > 0 and end > start:
    section = html[start:end]
    idx = section.find("pack-blooks-grid")
    g_end = section.find('<div class="leaks-section">\n                <h3>Contest of Candy</h3>')
    if g_end < 0:
        g_end = section.rfind('<div class="leaks-section"', idx if idx > 0 else 0)
    if idx >= 0 and g_end > idx:
        grid = section[idx:g_end]
        counter = [0]

        def r2(m):
            inner = m.group(1)
            if "onclick=" in m.group(0) or "bb-click" in m.group(0):
                return m.group(0)
            name_m = re.search(r'class="bn">([^<]+)', inner)
            rar_m = re.search(r'class="br[^"]*">([^<]+)', inner)
            ch_m = re.search(r'class="chance">([^<%]+)', inner)
            if not name_m:
                return m.group(0)
            name = name_m.group(1).strip()
            rarity = rar_m.group(1).strip() if rar_m else "Uncommon"
            c = ch_m.group(1).strip() if ch_m else None
            try:
                carg = str(float(c)) if c is not None else "null"
            except Exception:
                carg = "null"
            counter[0] += 1
            return (
                '<div class="pack-blook bb-click" style="cursor:pointer" '
                + "onclick=\"openBlookDetail('"
                + name
                + "', '"
                + rarity
                + "', "
                + carg
                + ", 'Spooky Pack')\">"
                + inner
                + "</div>"
            )

        grid2 = re.sub(r'<div class="pack-blook">([\s\S]*?)</div>', r2, grid)
        if counter[0]:
            section2 = section[:idx] + grid2 + section[g_end:]
            html = html[:start] + section2 + html[end:]
            changed = True
            print("whatsnew clickable", counter[0])
        else:
            print("whatsnew already clickable or no matches")
    else:
        print("WARNING: whatsnew grid not found", idx, g_end)
else:
    print("WARNING: whatsnew section not found")

if "bb-ui-fixes.js" not in html:
    old = (
        '<script src="bb-settings-enhance.js" defer></script>\n'
        '<script src="bb-leaks-tracker.js" defer></script>\n'
        '<script src="bb-weekly-shop.js" defer></script>'
    )
    new = old + '\n<script src="bb-ui-fixes.js" defer></script>'
    if old in html:
        html = html.replace(old, new, 1)
        changed = True
        print("script tag added")
    else:
        print("WARNING: script block not found")
else:
    print("script already present")

if changed:
    path.write_text(html, encoding="utf-8")
    print("wrote index.html", len(html))
else:
    print("no changes")
