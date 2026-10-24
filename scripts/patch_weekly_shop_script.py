#!/usr/bin/env python3
from pathlib import Path
p = Path("index.html")
t = p.read_text(encoding="utf-8")
if "bb-weekly-shop.js" in t:
    print("already present")
else:
    needle = '<script src="bb-leaks-tracker.js" defer></script>'
    inject = needle + '\n<script src="bb-weekly-shop.js" defer></script>'
    if needle in t:
        t = t.replace(needle, inject, 1)
        print("injected after leaks-tracker")
    elif "</body>" in t:
        t = t.replace("</body>", '<script src="bb-weekly-shop.js" defer></script>\n</body>', 1)
        print("injected before body")
    else:
        raise SystemExit("no injection point")
    p.write_text(t, encoding="utf-8")
    print("WROTE", len(t))
