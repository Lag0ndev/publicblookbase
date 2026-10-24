#!/usr/bin/env python3
from pathlib import Path
p = Path('index.html')
t = p.read_text(encoding='utf-8')
t = t.replace('src="bb-ui-fixes.js"', 'src="bb-ui-safe.js"')
t = t.replace("src='bb-ui-fixes.js'", "src='bb-ui-safe.js'")
t = t.replace('src="bb-ui-fixes.js" defer', 'src="bb-ui-safe.js" defer')
# ensure defer on helper scripts so they never block
for s in ['bb-ui-safe.js', 'bb-nav-fix.js', 'bb-leaks-tracker.js', 'bb-weekly-shop.js', 'bb-settings-enhance.js', 'bb-blooks.js']:
    t = t.replace(f'src="{s}"</script>', f'src="{s}" defer></script>')
    t = t.replace(f'src="{s}" defer></script>', f'src="{s}" defer></script>')
p.write_text(t, encoding='utf-8')
print('refs updated', 'bb-ui-safe.js' in t)
