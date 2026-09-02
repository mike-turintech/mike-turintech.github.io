#!/usr/bin/env bash
# One-time publish to GitHub Pages under the personal account (mbasios).
# Requires: gh logged in as mbasios  →  gh auth login   (choose the mbasios account)
set -euo pipefail
gh auth status 2>&1 | grep -q "account mike-turintech" || { echo "gh is not logged in as mbasios — run: gh auth login"; exit 1; }
if ! gh repo view mike-turintech/mike-turintech.github.io >/dev/null 2>&1; then
  gh repo create mike-turintech/mike-turintech.github.io --public --source=. --remote=origin --push
else
  git remote get-url origin >/dev/null 2>&1 || git remote add origin git@github.com:mike-turintech/mike-turintech.github.io.git
  git push -u origin HEAD:master
fi
# Pages serves the main branch root for <user>.github.io repos automatically.
echo "→ https://mike-turintech.github.io  (allow ~1–2 minutes for the first build)"
