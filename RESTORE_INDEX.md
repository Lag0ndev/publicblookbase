# Restore index.html

The main index.html was accidentally emptied.

## Fastest restore (GitHub website)

1. Go to: https://github.com/Lag0ndev/blookbase/commits/main
2. Find commit **3c0c289** ("Remove Pack Sim nav links and home card completely") from Oct 3
3. Click that commit
4. Click **index.html**
5. Click the three dots (...) → **View file** or use the history to restore

Or use this direct link to the good version:
https://github.com/Lag0ndev/blookbase/blob/3c0c289a7d70b75afd60f5787b553fbbb67c92a2/index.html

Then click the raw button, copy everything, and paste it back into the current index.html.

## With git (recommended)

```bash
git fetch origin
git checkout 3c0c289a7d70b75afd60f5787b553fbbb67c92a2 -- index.html
git add index.html
git commit -m "Restore original index.html"
git push
```

The fake Account Lookup page has already been removed.
