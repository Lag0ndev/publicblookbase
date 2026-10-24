#!/usr/bin/env python3
"""Add estimated-date disclaimer to countdown page + info modal."""
from pathlib import Path
import re

p = Path("index.html")
t = p.read_text(encoding="utf-8")
changed = False

disclaimer = (
    '        <p id="countdown-disclaimer" style="max-width:520px;margin:18px auto 0;text-align:center;'
    'font-weight:800;font-size:14px;line-height:1.45;opacity:0.92;padding:10px 14px;'
    'border-radius:12px;background:rgba(0,0,0,0.18);border:2px solid rgba(255,255,255,0.2);">'
    "\u26a0\ufe0f This date is <b>not confirmed</b> by Blooket. It is only an <b>estimate</b> based on previous years\u2019 release patterns."
    "</p>\n"
)

if 'id="countdown-disclaimer"' not in t:
    insert_after = (
        'id="seconds">--</div>\n'
        '                <div class="countdown-label">Seconds</div>\n'
        '            </div>\n'
        '        </div>\n\n'
    )
    pos = t.find(insert_after)
    if pos < 0:
        raise SystemExit("countdown grid marker not found")
    end = pos + len(insert_after)
    t = t[:end] + disclaimer + t[end:]
    print("countdown disclaimer inserted")
    changed = True
else:
    print("countdown disclaimer already present")

modal_note = (
    '<p id="history-estimate-note" style="font-size:13px;font-weight:700;opacity:0.85;margin:0 0 10px;line-height:1.4;">'
    "Dates below and on the countdown are <b>not confirmed</b> \u2014 only estimates from previous release data.</p>\n                "
)

if 'id="history-estimate-note"' not in t:
    t2, n = re.subn(
        r'(id="history-title">[^<]*</p>\s*)(<ul style="list-style: none;)',
        r"\1" + modal_note + r"\2",
        t,
        count=1,
    )
    if not n:
        raise SystemExit("history modal marker not found")
    t = t2
    print("modal estimate note inserted")
    changed = True
else:
    print("modal note already present")

if changed:
    p.write_text(t, encoding="utf-8")
    print("WROTE", len(t))
else:
    print("No changes")

print("verify disclaimer", 'id="countdown-disclaimer"' in t)
print("verify not confirmed", t.count("not confirmed"))
