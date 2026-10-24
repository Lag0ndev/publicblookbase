#!/usr/bin/env python3
"""What's New -> Spooky LIVE; Season 8 past; add video; Contest of Candy gamemode."""
from pathlib import Path
import re

p = Path('index.html')
t = p.read_text(encoding='utf-8')

NEW_WHATSNEW = r'''<div class="main-content" id="view-whatsnew" style="display: none;">
        <h1 class="header-title">What's New</h1>
        <div class="leaks-wrap">
            <div class="leaks-section">
                <h3>&#127875; Spooky Pack is LIVE!</h3>
                <p style="font-weight:700;margin:0 0 14px;line-height:1.55;opacity:0.95;">
                    Halloween is here. <b>Spooky Pack</b> is back in the Market (25 tokens) with 14 blooks &mdash; including brand-new <b>Goo Monster</b> (Epic) and <b>Spooky Moth</b> (Chroma 0.05%). <b>Contest of Candy</b> is the seasonal gamemode for this window.
                </p>
                <div style="position:relative;width:100%;aspect-ratio:16/9;border-radius:10px;overflow:hidden;border:3px solid rgba(255,255,255,0.25);background:rgba(0,0,0,0.25);margin-bottom:4px;">
                    <iframe src="https://www.youtube.com/embed/jKJxzHmmMIM" title="Blooket's SPOOKY PACK JUST CAME OUT!" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0;"></iframe>
                </div>
                <p style="font-size:12px;font-weight:700;opacity:0.85;margin:8px 0 0;">Blooket's SPOOKY PACK JUST CAME OUT! &mdash; Lag0n</p>
            </div>

            <div class="leaks-section">
                <h3>Spooky Pack &middot; 25 tokens</h3>
                <p style="font-weight:700;margin:0 0 12px;line-height:1.55;opacity:0.95;">
                    Official drop rates from the in-game Pack modal:
                </p>
                <div class="pack-blooks-grid" style="margin-top:4px;">
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/pumpkin.svg" alt="Pumpkin" loading="lazy"><div class="bn">Pumpkin</div><div class="br rarity-Uncommon">Uncommon</div><div class="chance">15.2%</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/swampmonster.svg" alt="Swamp Monster" loading="lazy"><div class="bn">Swamp Monster</div><div class="br rarity-Uncommon">Uncommon</div><div class="chance">15.2%</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/frankenstein.svg" alt="Frankenstein" loading="lazy"><div class="bn">Frankenstein</div><div class="br rarity-Uncommon">Uncommon</div><div class="chance">15.2%</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/vampire.svg" alt="Vampire" loading="lazy"><div class="bn">Vampire</div><div class="br rarity-Uncommon">Uncommon</div><div class="chance">15.2%</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/zombie.svg" alt="Zombie" loading="lazy"><div class="bn">Zombie</div><div class="br rarity-Uncommon">Uncommon</div><div class="chance">15.2%</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/mummy.svg" alt="Mummy" loading="lazy"><div class="bn">Mummy</div><div class="br rarity-Rare">Rare</div><div class="chance">4%</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/caramelapple.svg" alt="Caramel Apple" loading="lazy"><div class="bn">Caramel Apple</div><div class="br rarity-Rare">Rare</div><div class="chance">4%</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/candycorn.svg" alt="Candy Corn" loading="lazy"><div class="bn">Candy Corn</div><div class="br rarity-Rare">Rare</div><div class="chance">4%</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/crow.svg" alt="Crow" loading="lazy"><div class="bn">Crow</div><div class="br rarity-Rare">Rare</div><div class="chance">4%</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/vampirebat.svg" alt="Vampire Bat" loading="lazy"><div class="bn">Vampire Bat</div><div class="br rarity-Rare">Rare</div><div class="chance">4%</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/werewolf.svg" alt="Werewolf" loading="lazy"><div class="bn">Werewolf</div><div class="br rarity-Epic">Epic</div><div class="chance">1.65%</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/goomonster.svg" alt="Goo Monster" loading="lazy"><div class="bn">Goo Monster</div><div class="br rarity-Epic">Epic</div><div class="chance">1.65%</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/ghost.svg" alt="Ghost" loading="lazy"><div class="bn">Ghost</div><div class="br rarity-Legendary">Legendary</div><div class="chance">0.65%</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/spookymoth.svg" alt="Spooky Moth" loading="lazy"><div class="bn">Spooky Moth</div><div class="br rarity-Chroma">Chroma</div><div class="chance">0.05%</div></div>
                </div>
            </div>

            <div class="leaks-section">
                <h3>Contest of Candy</h3>
                <p style="font-weight:700;margin:0 0 12px;line-height:1.55;opacity:0.95;">
                    Seasonal Halloween host gamemode is active for the Spooky window. Collect candy, compete on the board, and pull for Spooky Pack blooks while it lasts.
                </p>
                <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
                    <img src="https://ac.blooket.com/gamemodes/logos/candy.png" alt="Contest of Candy" style="width:72px;height:72px;filter:drop-shadow(0 2px 4px rgba(0,0,0,0.25));">
                    <div style="font-weight:700;line-height:1.5;opacity:0.95;">Host mode &middot; Seasonal<br>Pairs with Spooky Pack in Market</div>
                </div>
            </div>

            <div class="leaks-section" style="opacity:0.92;">
                <h3 style="opacity:0.85;">Past &mdash; Season 8</h3>
                <p style="font-weight:700;margin:0 0 14px;line-height:1.55;opacity:0.9;">
                    Season 8 launched earlier with the Dog pack, Claw Mania, Snake Escape, Map page, Locker &amp; Achievements.
                </p>
                <div style="position:relative;width:100%;aspect-ratio:16/9;border-radius:10px;overflow:hidden;border:3px solid rgba(255,255,255,0.2);background:rgba(0,0,0,0.25);margin-bottom:4px;">
                    <iframe src="https://www.youtube.com/embed/_m9hQCrvxg0?start=9" title="Season 8 overview" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0;"></iframe>
                </div>
                <p style="font-size:12px;font-weight:700;opacity:0.8;margin:8px 0 12px;">Season 8 overview (past)</p>
                <div class="pack-blooks-grid" style="margin-top:4px;">
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/jackrussellterrier.svg" alt="Jack Russell Terrier" loading="lazy"><div class="bn">Jack Russell Terrier</div><div class="br rarity-Uncommon">Uncommon</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/marketassets/blooks/robotdog.svg" alt="Robot Dog" loading="lazy"><div class="bn">Robot Dog</div><div class="br rarity-Chroma">Chroma</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/gamemodes/logos/claw.png" alt="Claw Mania" loading="lazy"><div class="bn">Claw Mania</div><div class="br">Host</div></div>
                    <div class="pack-blook"><img src="https://ac.blooket.com/gamemodes/logos/snake.png" alt="Snake Escape" loading="lazy" onerror="this.style.display='none'"><div class="bn">Snake Escape</div><div class="br">Solo</div></div>
                </div>
            </div>
        </div>
    </div>'''

# Replace view-whatsnew block
t2, n = re.subn(
    r'<div class="main-content" id="view-whatsnew"[\s\S]*?</div>\s*(?=<div class="main-content"|<!--)',
    NEW_WHATSNEW + '\n\n    ',
    t,
    count=1,
)
if n == 0:
    t2, n = re.subn(
        r'<div class="main-content" id="view-whatsnew"[\s\S]*?</div>\s*(?=<div class="main-content")',
        NEW_WHATSNEW + '\n\n    ',
        t,
        count=1,
    )
print('whatsnew replaced', n)
t = t2
assert n == 1, 'failed to replace whatsnew'

# Add Contest of Candy to hostGamemodes if missing
if "name: 'Contest of Candy'" not in t:
    candy = (
        "{ name: 'Contest of Candy', about: 'Collect candy and compete in the Halloween contest!', "
        "difficulty: 'Normal', skills: 'Speed & Luck', time: '7 min', "
        "questions: 'Self-paced, Normal frequency', "
        "players: '1 min \u00b7 8 ideal \u00b7 60 free max \u00b7 300 Plus max', "
        "logo: 'https://ac.blooket.com/gamemodes/logos/candy.png', plus: false, seasonal: true },\n            "
    )
    t = t.replace(
        "const hostGamemodes = [\n            { name: 'Gold Quest'",
        "const hostGamemodes = [\n            " + candy + "{ name: 'Gold Quest'",
        1,
    )
    print('Contest of Candy added')
else:
    print('Contest of Candy already present')

# Prepend Spooky video to videos array
vid_entry = "{ id: 'jKJxzHmmMIM', title: \"Blooket's SPOOKY PACK JUST CAME OUT!\", channel: 'Lag0n', likes: 0, views: '\u2014', cat: 'new' },"
if "jKJxzHmmMIM" not in t:
    # Find first video entry pattern and insert before it
    t2, n = re.subn(
        r"(\[\s*\n\s*)(\{ id: '[A-Za-z0-9_-]{11}', title:)",
        r"\1" + vid_entry + "\n            \2",
        t,
        count=1,
    )
    if n:
        t = t2
        print('video prepended')
    else:
        print('WARNING: could not find videos array')
else:
    print('video already present')

p.write_text(t, encoding='utf-8')
print('size', p.stat().st_size)
assert 'jKJxzHmmMIM' in t
assert 'Spooky Pack is LIVE' in t or 'Spooky Pack is LIVE!' in t or 'SPOOKY PACK' in t
assert "name: 'Contest of Candy'" in t
print('OK')
