#!/usr/bin/env python3
import json
from pathlib import Path

SPOOKY_BLOOKS = [
  {"name": "Pumpkin", "rarity": "Uncommon", "chance": 15.2, "url": "https://ac.blooket.com/marketassets/blooks/pumpkin.svg", "slug": "pumpkin"},
  {"name": "Swamp Monster", "rarity": "Uncommon", "chance": 15.2, "url": "https://ac.blooket.com/marketassets/blooks/swampmonster.svg", "slug": "swampmonster"},
  {"name": "Frankenstein", "rarity": "Uncommon", "chance": 15.2, "url": "https://ac.blooket.com/marketassets/blooks/frankenstein.svg", "slug": "frankenstein"},
  {"name": "Vampire", "rarity": "Uncommon", "chance": 15.2, "url": "https://ac.blooket.com/marketassets/blooks/vampire.svg", "slug": "vampire"},
  {"name": "Zombie", "rarity": "Uncommon", "chance": 15.2, "url": "https://ac.blooket.com/marketassets/blooks/zombie.svg", "slug": "zombie"},
  {"name": "Mummy", "rarity": "Rare", "chance": 4, "url": "https://ac.blooket.com/marketassets/blooks/mummy.svg", "slug": "mummy"},
  {"name": "Caramel Apple", "rarity": "Rare", "chance": 4, "url": "https://ac.blooket.com/marketassets/blooks/caramelapple.svg", "slug": "caramelapple"},
  {"name": "Candy Corn", "rarity": "Rare", "chance": 4, "url": "https://ac.blooket.com/marketassets/blooks/candycorn.svg", "slug": "candycorn"},
  {"name": "Crow", "rarity": "Rare", "chance": 4, "url": "https://ac.blooket.com/marketassets/blooks/crow.svg", "slug": "crow"},
  {"name": "Vampire Bat", "rarity": "Rare", "chance": 4, "url": "https://ac.blooket.com/marketassets/blooks/vampirebat.svg", "slug": "vampirebat"},
  {"name": "Werewolf", "rarity": "Epic", "chance": 1.65, "url": "https://ac.blooket.com/marketassets/blooks/werewolf.svg", "slug": "werewolf"},
  {"name": "Goo Monster", "rarity": "Epic", "chance": 1.65, "url": "https://ac.blooket.com/marketassets/blooks/goomonster.svg", "slug": "goomonster"},
  {"name": "Ghost", "rarity": "Legendary", "chance": 0.65, "url": "https://ac.blooket.com/marketassets/blooks/ghost.svg", "slug": "ghost"},
  {"name": "Spooky Moth", "rarity": "Chroma", "chance": 0.05, "url": "https://ac.blooket.com/marketassets/blooks/spookymoth.svg", "slug": "spookymoth"},
]

# packs.json
packs_path = Path("data/packs.json")
data = json.loads(packs_path.read_text())
packs = data.get("packs", [])
for i, p in enumerate(packs):
  if p.get("id") == "spooky" or p.get("name") == "Spooky Pack":
    packs[i] = {
      **p,
      "id": "spooky",
      "name": "Spooky Pack",
      "cost": p.get("cost", 25),
      "type": "seasonal",
      "status": "live",
      "packBottom": p.get("packBottom") or "https://ac.blooket.com/dashclassic/assets/SpookyPackBottom-Bb7nZ1oD.png",
      "blookBackground": p.get("blookBackground") or "https://ac.blooket.com/dashclassic/assets/Highlighted_Background_Spooky-BE3Q44ax.svg",
      "blooks": [{k: v for k, v in b.items() if k != "slug"} for b in SPOOKY_BLOOKS],
      "released": "2026-09-30",
      "notes": "LIVE. Drop rates from in-game Pack modal. Goo Monster + Spooky Moth on CDN.",
    }
    break
data = {"lastUpdated": "2026-10-01", "packs": packs}
packs_path.write_text(json.dumps(data, indent=2) + "\n")
print("packs updated")

# countdown.json
countdown = {
  "lastUpdated": "2026-10-01",
  "events": [
    {
      "id": "spooky-2026",
      "name": "Spooky Pack",
      "start": "2026-09-30",
      "end": "2026-11-01",
      "status": "live",
      "notes": "LIVE NOW in Market. 14 blooks incl. Goo Monster (Epic 1.65%) and Spooky Moth (Chroma 0.05%). End date estimated from prior Halloween windows - not confirmed by Blooket."
    },
    {
      "id": "blizzard-2026",
      "name": "Blizzard Pack",
      "start": "2026-12-01",
      "end": "2027-01-05",
      "status": "upcoming",
      "notes": "Typical winter holiday window. Not confirmed - estimated on previous data."
    }
  ]
}
Path("data/countdown.json").write_text(json.dumps(countdown, indent=2) + "\n")
print("countdown updated")

# updates.json
up = json.loads(Path("data/updates.json").read_text())
entry = {
  "date": "2026-09-30",
  "time": "23:06:00Z",
  "type": "pack",
  "title": "Spooky Pack is LIVE",
  "body": "Spooky Pack is out in the Market with 14 blooks. Drop rates: Pumpkin/Swamp Monster/Frankenstein/Vampire/Zombie 15.2%, Mummy/Caramel Apple/Candy Corn/Crow/Vampire Bat 4%, Werewolf/Goo Monster 1.65%, Ghost 0.65%, Spooky Moth 0.05%.",
  "images": [
    {"label": "Goo Monster", "src": "https://ac.blooket.com/marketassets/blooks/goomonster.svg"},
    {"label": "Spooky Moth", "src": "https://ac.blooket.com/marketassets/blooks/spookymoth.svg"},
    {"label": "Caramel Apple", "src": "https://ac.blooket.com/marketassets/blooks/caramelapple.svg"},
    {"label": "Crow", "src": "https://ac.blooket.com/marketassets/blooks/crow.svg"},
    {"label": "Vampire Bat", "src": "https://ac.blooket.com/marketassets/blooks/vampirebat.svg"},
    {"label": "Ghost", "src": "https://ac.blooket.com/marketassets/blooks/ghost.svg"},
  ]
}
entries = up.get("entries") or []
if not entries or entries[0].get("title") != entry["title"]:
  entries.insert(0, entry)
up["entries"] = entries
up["lastUpdated"] = "2026-10-01"
Path("data/updates.json").write_text(json.dumps(up, indent=2) + "\n")
print("updates updated")

# blooks.json - merge Spooky Pack in-place
blooks_path = Path("data/blooks.json")
try:
  blooks = json.loads(blooks_path.read_text())
  if not isinstance(blooks, list):
    blooks = blooks.get("blooks") or []
except Exception:
  blooks = []

spooky_slugs = {b["slug"] for b in SPOOKY_BLOOKS}
spooky_names = {b["name"].lower() for b in SPOOKY_BLOOKS}
kept = []
for b in blooks:
  if b.get("pack") == "Spooky Pack":
    continue
  if b.get("slug") in spooky_slugs:
    continue
  if (b.get("name") or "").lower() in spooky_names:
    continue
  kept.append(b)

for b in SPOOKY_BLOOKS:
  kept.append({
    "name": b["name"],
    "slug": b["slug"],
    "rarity": b["rarity"],
    "pack": "Spooky Pack",
    "img": b["url"],
    "dropRate": b["chance"],
  })

blooks_path.write_text(json.dumps(kept, indent=2) + "\n")
print("blooks updated", len(kept), "spooky", sum(1 for b in kept if b.get("pack")=="Spooky Pack"))
