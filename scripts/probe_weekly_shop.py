#!/usr/bin/env python3
"""Probe Blooket CDN + weekly/limited assets; update data/weekly-shop.json + updates.json on change."""
import json, hashlib, urllib.request, ssl
from datetime import datetime, timezone, timedelta
from pathlib import Path

NOW = datetime.now(timezone.utc)
NOW_S = NOW.strftime("%Y-%m-%dT%H:%M:%SZ")
ctx = ssl.create_default_context()

URLS = [
  "https://ac.blooket.com/marketassets/blooks/purpleastronaut.svg",
  "https://ac.blooket.com/marketassets/blooks/blueastronaut.svg",
  "https://ac.blooket.com/marketassets/blooks/cyanastronaut.svg",
  "https://ac.blooket.com/marketassets/blooks/limeastronaut.svg",
  "https://ac.blooket.com/marketassets/blooks/lemoncrab.svg",
  "https://ac.blooket.com/marketassets/blooks/poisondartfrog.svg",
  "https://ac.blooket.com/marketassets/blooks/rainbownarwhal.svg",
  "https://ac.blooket.com/marketassets/blooks/rainbowjellyfish.svg",
  "https://ac.blooket.com/marketassets/blooks/blizzardclownfish.svg",
  "https://ac.blooket.com/marketassets/blooks/donutblobfish.svg",
  "https://ac.blooket.com/marketassets/blooks/crimsonoctopus.svg",
  "https://ac.blooket.com/marketassets/blooks/underconstruction.svg",
  "https://ac.blooket.com/marketassets/blooks/placeholder.svg",
  "https://ac.blooket.com/marketassets/blooks/fuego.svg",
  "https://ac.blooket.com/marketassets/blooks/dog.svg",
  "https://ac.blooket.com/marketassets/blooks/robotdog.svg",
  "https://ac.blooket.com/marketassets/blooks/clawmania.svg",
  "https://ac.blooket.com/marketassets/blooks/fishtank.svg",
  "https://ac.blooket.com/dashclassic/assets/Lunch_Pack-DWYwdJdz.png",
  "https://ac.blooket.com/dashclassic/assets/SpookyPackBottom-Bb7nZ1oD.png",
  "https://ac.blooket.com/gamemodes/logos/snake.png",
]

SHOP_URLS = [
  "https://ac.blooket.com/marketassets/blooks/fuego.svg",
  "https://ac.blooket.com/marketassets/blooks/lovelyfrog.svg",
  "https://ac.blooket.com/marketassets/blooks/luckyfrog.svg",
  "https://ac.blooket.com/marketassets/blooks/springfrog.svg",
  "https://ac.blooket.com/marketassets/blooks/vampirefrog.svg",
  "https://ac.blooket.com/marketassets/blooks/pumpkin.svg",
  "https://ac.blooket.com/marketassets/blooks/spookypumpkin.svg",
  "https://ac.blooket.com/marketassets/blooks/hamstaclaus.svg",
  "https://ac.blooket.com/marketassets/blooks/timthealien.svg",
  "https://ac.blooket.com/marketassets/blooks/rainbowastronaut.svg",
  "https://ac.blooket.com/marketassets/blooks/agentowl.svg",
  "https://ac.blooket.com/marketassets/blooks/masterelf.svg",
  "https://ac.blooket.com/marketassets/blooks/partypig.svg",
  "https://ac.blooket.com/marketassets/blooks/wiseowl.svg",
  "https://ac.blooket.com/marketassets/blooks/phantomking.svg",
  "https://ac.blooket.com/marketassets/blooks/leprechaun.svg",
  "https://ac.blooket.com/marketassets/blooks/anacondawizard.svg",
  "https://ac.blooket.com/marketassets/blooks/spookymummy.svg",
  "https://ac.blooket.com/marketassets/blooks/astronaut.svg",
  "https://ac.blooket.com/marketassets/blooks/gummybear.svg",
]

def head(url, timeout=6):
  try:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "BlookbaseTracker/1.0"})
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
      return {
        "url": url, "code": r.status, "ok": 200 <= r.status < 400,
        "contentLength": r.headers.get("Content-Length") or "",
        "etag": r.headers.get("ETag") or "",
        "name": url.rsplit("/", 1)[-1],
      }
  except Exception as e:
    return {
      "url": url, "code": 0, "ok": False, "contentLength": "", "etag": "",
      "name": url.rsplit("/", 1)[-1], "error": str(e)[:80],
    }

assets = [head(u) for u in URLS]
shop_assets = [head(u) for u in SHOP_URLS]
sig_parts = [f"{a['name']}:{a['code']}:{a['contentLength']}:{a['etag']}" for a in sorted(shop_assets, key=lambda x: x["name"])]
shop_sig = hashlib.sha256("|".join(sig_parts).encode()).hexdigest()[:16]

Path("data").mkdir(exist_ok=True)

last_check = {
  "checkedAt": NOW_S,
  "status": "ok",
  "interval": "every 5 minutes (GitHub Actions minimum)",
  "found": sum(1 for a in assets if a["ok"]),
  "missing": sum(1 for a in assets if not a["ok"]),
  "weeklyShopSignature": shop_sig,
  "assets": [{"code": str(a["code"]), "name": a["name"], "url": a["url"], "ok": a["ok"]} for a in assets],
}
Path("data/last-check.json").write_text(json.dumps(last_check, indent=2) + "\n")

ws_path = Path("data/weekly-shop.json")
try:
  ws = json.loads(ws_path.read_text()) if ws_path.exists() else {}
except Exception:
  ws = {}

prev_sig = ws.get("signature")
changed = prev_sig is not None and prev_sig != shop_sig
available = [a for a in shop_assets if a["ok"]]
monday = (NOW - timedelta(days=NOW.weekday())).strftime("%Y-%m-%d")
items = [{"name": a["name"].replace(".svg", "").replace(".png", ""), "type": "asset", "url": a["url"], "ok": True} for a in available]

ws.setdefault("history", [])
ws["lastChecked"] = NOW_S
ws["signature"] = shop_sig
ws["resetHint"] = "Mon/Tue ~6:00 PM Central (CST/CDT)"
ws["note"] = (
  "Tracks public Blooket market assets tied to limited / weekly-style rotations. "
  "Full live banner/title list needs a logged-in session; when the asset signature changes, "
  "we log a Weekly Shop rotation event on the Tracker."
)
ws["current"] = {
  "weekOf": monday,
  "signature": shop_sig,
  "availableCount": len(available),
  "missingCount": len(shop_assets) - len(available),
  "items": items[:40],
  "source": "cdn-probe",
}

if changed:
  ws["lastChanged"] = NOW_S
  ws["history"] = ([{
    "at": NOW_S, "weekOf": monday, "signature": shop_sig,
    "availableCount": len(available),
    "note": "Weekly/limited market assets signature changed",
  }] + ws["history"])[:30]

  up_path = Path("data/updates.json")
  try:
    updates = json.loads(up_path.read_text())
  except Exception:
    updates = {"entries": []}
  updates.setdefault("entries", [])
  new_entry = {
    "date": NOW.strftime("%Y-%m-%d"),
    "time": NOW.strftime("%H:%M:%SZ"),
    "type": "weekly-shop",
    "title": "Weekly Shop assets changed",
    "body": (
      f"Detected a change in limited/weekly market assets (signature {shop_sig}). "
      f"{len(available)} related assets reachable. "
      "Shop usually rotates Mon/Tue ~6PM Central — check Market → Weekly Shop in Blooket for banners, titles, and parts."
    ),
    "images": [{"label": it["name"], "src": it["url"]} for it in items[:6]],
  }
  if not updates["entries"] or updates["entries"][0].get("title") != new_entry["title"] or updates["entries"][0].get("date") != new_entry["date"]:
    updates["entries"].insert(0, new_entry)
    updates["lastUpdated"] = NOW.strftime("%Y-%m-%d")
    up_path.write_text(json.dumps(updates, indent=2) + "\n")
    print("updates.json prepended")
  print("WEEKLY SHOP CHANGE", shop_sig)
else:
  print("weekly shop stable", shop_sig)

ws_path.write_text(json.dumps(ws, indent=2) + "\n")
print("done", NOW_S)
