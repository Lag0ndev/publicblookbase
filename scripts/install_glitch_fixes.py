#!/usr/bin/env python3
import base64, pathlib, sys, subprocess
root = pathlib.Path('.')
pay = root / 'scripts' / 'payloads'
for name in ['bb-blooks.js', 'bb-settings-enhance.js', 'bb-leaks-tracker.js']:
    n = int((pay / f'{name}.n').read_text().strip())
    b64 = ''.join((pay / f'{name}.{i}.b64').read_text().strip() for i in range(n))
    (root / name).write_bytes(base64.b64decode(b64))
    print('wrote', name, (root / name).stat().st_size)
subprocess.check_call([sys.executable, 'scripts/patch_glitches.py'])
