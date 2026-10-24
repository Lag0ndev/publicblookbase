#!/usr/bin/env python3
import json, pathlib
rows=[]
for i in range(2):
    rows += json.loads(pathlib.Path(f"data/_blooks_part{i}.json").read_text())
out=[{"name":n,"slug":s,"rarity":r,"pack":p,"img":"https://ac.blooket.com/marketassets/blooks/"+s+".svg"} for n,s,r,p in rows]
pathlib.Path("data/blooks.json").write_text(json.dumps(out,separators=(",",":")))
print("merged", len(out))
