#!/usr/bin/env python3
import urllib.request, pathlib

urls = [
  "https://cdn.jsdelivr.net/gh/Lag0ndev/blookbase@cedf964d0fbd9e4e0cdee84a22ded09b10e51f82/bb-settings-enhance.js",
  "https://raw.githubusercontent.com/Lag0ndev/blookbase/cedf964d0fbd9e4e0cdee84a22ded09b10e51f82/bb-settings-enhance.js",
]
data = None
for u in urls:
  try:
    data = urllib.request.urlopen(u, timeout=30).read().decode("utf-8")
    if "resetFontsAndGrad" in data and "bb-tp-box" in data:
      print("got", u, len(data))
      break
  except Exception as e:
    print("fail", u, e)
if not data or "resetFontsAndGrad" not in data:
  raise SystemExit("could not fetch good settings")

if "blookbase_font_header" not in data or "bb_font_h" not in data:
  data = data.replace(
    "var hFont=localStorage.getItem('bb_font_h')||'titan';",
    "var hFont=localStorage.getItem('bb_font_h')||localStorage.getItem('blookbase_font_header')||'titan';",
  )
  data = data.replace(
    "var bFont=localStorage.getItem('bb_font_b')||'nunito';",
    "var bFont=localStorage.getItem('bb_font_b')||localStorage.getItem('blookbase_font_body')||'nunito';",
  )
  print("font migrate init")

pathlib.Path("bb-settings-enhance.js").write_text(data, encoding="utf-8")
print("wrote", len(data))
