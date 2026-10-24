#!/usr/bin/env python3
import base64, pathlib
n = int(pathlib.Path("scripts/blooks_chunk_n.txt").read_text().strip())
b64 = "".join(pathlib.Path(f"scripts/blooks_chunk_{i}.b64").read_text().strip() for i in range(n))
pathlib.Path("bb-blooks.js").write_bytes(base64.b64decode(b64))
print("restored bb-blooks.js", pathlib.Path("bb-blooks.js").stat().st_size)
