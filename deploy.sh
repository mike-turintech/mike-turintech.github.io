#!/usr/bin/env bash
# One-time publish to GitHub Pages under the personal account (mbasios).
# Requires: gh logged in as mbasios  →  gh auth login   (choose the mbasios account)
set -euo pipefail
gh auth status 2>&1 | grep -q "account mbasios" || { echo "gh is not logged in as mbasios — run: gh auth login"; exit 1; }
if ! gh repo view mbasios/mbasios.github.io >/dev/null 2>&1; then
  gh repo create mbasios/mbasios.github.io --public --source=. --remote=origin --push
else
  git remote get-url origin >/dev/null 2>&1 || git remote add origin git@github.com:mbasios/mbasios.github.io.git
  git push -u origin HEAD:main
fi
# Pages serves the main branch root for <user>.github.io repos automatically.
echo "→ https://mbasios.github.io  (allow ~1–2 minutes for the first build)"
