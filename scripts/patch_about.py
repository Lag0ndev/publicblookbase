#!/usr/bin/env python3
"""Update About page + SEO meta for Blookbase."""
from pathlib import Path
import re

p = Path("index.html")
t = p.read_text(encoding="utf-8")

# Meta description
new_meta = (
    'name="description" content="Blookbase is a free fan-made Blooket hub: season countdowns, '
    "What's New, packs & rarities, gamemodes, leaks, update tracker, and videos. "
    'Unofficial — not affiliated with Blooket."'
)
t2, n = re.subn(r'name="description" content="[^"]*"', new_meta, t, count=1)
if n != 1:
    raise SystemExit(f"meta description replace failed ({n})")
t = t2

if 'name="keywords"' not in t:
    t = t.replace(
        new_meta,
        new_meta + '\n    <meta name="keywords" content="Blookbase, Blooket, Blooket countdown, Blooket season, Blooket packs, Blooket gamemodes, Blooket leaks, Blooket tracker, Spooktober, Season 9">',
        1,
    )

if 'property="og:title"' not in t:
    og = (
        '\n    <meta property="og:title" content="Blookbase — Fan-made Blooket hub">'
        '\n    <meta property="og:description" content="Season countdowns, packs, gamemodes, leaks, update tracker, and videos for Blooket. Free fan site — not affiliated with Blooket.">'
        '\n    <meta property="og:type" content="website">'
        '\n    <meta property="og:url" content="https://blookbase.vercel.app/">'
        '\n    <meta name="twitter:card" content="summary">\n'
    )
    t = t.replace("</title>", "</title>" + og, 1)

start = t.find('id="view-about"')
if start < 0:
    raise SystemExit("view-about not found")
box = t.find("about-box", start)
if box < 0:
    raise SystemExit("about-box not found")
# close about-box, then close main-content view-about
e1 = t.find("</div>", box)
e2 = t.find("</div>", e1 + 1)
about_end = e2 + len("</div>")

new_about = """id="view-about" style="display: none;">
        <h1 class="header-title">About</h1>
        <div class="about-box">
            <p>
                <b>Blookbase</b> is a free fan-made hub for <b>Blooket</b> — the classroom game with Blooks, packs, seasons, and gamemodes.
            </p>
            <p>
                Use it to follow <b>season countdowns</b>, <b>What&apos;s New</b>, <b>packs &amp; rarities</b>, <b>gamemodes</b>, <b>leaks</b> (unreleased or rare Blooks), an <b>update tracker</b>, and <b>community videos</b> — all in one place.
            </p>
            <hr>
            <p>
                <b>What you&apos;ll find</b>
            </p>
            <p>
                <b>Countdown</b> — switch between seasonal timers (Spooktober, Season 9, holidays, and more). Use the <b>!</b> button on that page for past release dates.<br>
                <b>What&apos;s New</b> — season highlights and recent changes.<br>
                <b>Leaks</b> — fan tracking of secret / unreleased Blooks, uniques, mysticals, and gamemode status.<br>
                <b>Tracker</b> — chronological Blooket update history with images when available.<br>
                <b>Videos</b> — Blooket YouTube content.<br>
                <b>Gamemodes &amp; Packs</b> — reference for modes, pack contents, and odds.
            </p>
            <hr>
            <p>
                Made by <b><a href="https://www.youtube.com/@Lag0n4/" target="_blank" rel="noopener noreferrer">Lag0n</a></b>.
            </p>
            <p>
                <b>Not affiliated with or endorsed by Blooket.</b> All Blooket names, art, and assets belong to their owners. This is an independent fan project for informational and entertainment use.
            </p>
        </div>
    </div>"""

t = t[:start] + new_about + t[about_end:]
p.write_text(t, encoding="utf-8")
print("About + meta patched", len(t))
