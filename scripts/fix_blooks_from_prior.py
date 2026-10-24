#!/usr/bin/env python3
import urllib.request, pathlib, re

urls = [
  "https://cdn.jsdelivr.net/gh/Lag0ndev/blookbase@cf5a8076b1a52b54986db901a831ec28ca15c351/bb-blooks.js",
  "https://raw.githubusercontent.com/Lag0ndev/blookbase/cf5a8076b1a52b54986db901a831ec28ca15c351/bb-blooks.js",
]
data = None
for u in urls:
  try:
    data = urllib.request.urlopen(u, timeout=30).read().decode("utf-8")
    if "groupByPack" in data and len(data) > 5000:
      print("got", u, len(data))
      break
  except Exception as e:
    print("fail", u, e)
if not data or "groupByPack" not in data:
  raise SystemExit("could not fetch good bb-blooks.js")

def esc_repl(m):
  return (
    "function esc(s) {\n"
    "    return String(s == null ? '' : s)\n"
    "      .replace(/&/g, '\\x26amp;').replace(/</g, '\\x26lt;').replace(/>/g, '\\x26gt;')\n"
    "      .replace(/\"/g, '\\x26quot;').replace(/'/g, '\\x26#39;');\n"
    "  }"
  )
data2, n = re.subn(r"function esc\(s\) \{[\s\S]*?\n  \}", esc_repl, data, count=1)
print("esc replacements", n)
data = data2

if "bb-blooks-grid" not in data:
  needle = "if (el('bb-packs-container')) return root;"
  inj = (
    "// Upgrade old white-card grid shell if still present\n"
    "    if (el('bb-blooks-grid') && !el('bb-packs-container')) {\n"
    "      root.innerHTML = '';\n"
    "    }\n"
    "    if (el('bb-packs-container')) return root;"
  )
  if needle in data:
    data = data.replace(needle, inj, 1)
    print("shell upgrade")

if "blookImageMap" not in data:
  old = (
    "if (typeof window.openBlookDetail === 'function') {\n"
    "      window.openBlookDetail(b.name, b.rarity, null, b.pack);\n"
    "      return;\n"
    "    }"
  )
  new = (
    "if (typeof window.openBlookDetail === 'function') {\n"
    "      try {\n"
    "        if (b.img && typeof blookImageMap === 'object' && blookImageMap) blookImageMap[b.name] = b.img;\n"
    "      } catch (e) {}\n"
    "      window.openBlookDetail(b.name, b.rarity, null, b.pack);\n"
    "      return;\n"
    "    }"
  )
  if old in data:
    data = data.replace(old, new, 1)
    print("image seed")

pathlib.Path("bb-blooks.js").write_text(data, encoding="utf-8")
print("wrote", len(data))
