Blookbase full export for publicblookbase
========================================

- src/  = full tree from Lag0ndev/blookbase
- src/index.html has been replaced with the working version from commit 3c0c289
- index.html.RESTORED_FROM_3c0c289.html = same good index (standalone copy)

Quick push to publicblookbase:
  unzip blookbase-full-export.zip
  cd src
  git init
  git add .
  git commit -m "Full restore of blookbase"
  git branch -M main
  git remote add origin https://github.com/Lag0ndev/publicblookbase.git
  git push -u origin main --force

Or upload the contents of src/ via the GitHub website.
