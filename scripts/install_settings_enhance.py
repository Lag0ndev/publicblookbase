#!/usr/bin/env python3
import base64, pathlib
parts=[]
i=0
while pathlib.Path(f"scripts/settings_enh_{i}.b64").exists():
    parts.append(pathlib.Path(f"scripts/settings_enh_{i}.b64").read_text().strip())
    i+=1
pathlib.Path("bb-settings-enhance.js").write_bytes(base64.b64decode("".join(parts)))
print("wrote enhance", len("".join(parts)))
