#!/usr/bin/env python3
import base64, zlib
from pathlib import Path
B = Path("scripts/blooks_z.txt").read_text().strip()
Path("data").mkdir(exist_ok=True)
Path("data/blooks.json").write_bytes(zlib.decompress(base64.b64decode(B)))
print("ok blooks", Path("data/blooks.json").stat().st_size)
