#!/usr/bin/env python3
import base64, pathlib
a=pathlib.Path("scripts/bb_blooks_a.b64").read_text().strip()
b=pathlib.Path("scripts/bb_blooks_b.b64").read_text().strip()
pathlib.Path("bb-blooks.js").write_bytes(base64.b64decode(a+b))
print("bb-blooks ok", len(a+b))
