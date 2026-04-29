#!/bin/bash
# Ideaverse Orchestration Sync (Saturated Edition)
echo "🚀 Starting Omniscient Ideaverse Sync..."
cd "$(dirname "$0")/.." # Move to project root

# Run Intelligence Engine
python3 scripts/repo-dashboard.py

# Move Data to Web App
mkdir -p web/public/previews
cp lab/PORTFOLIO_DATA.json web/src/data/portfolio.json

# Copy Preview Images (Safe Copy)
python3 -c "
import json, shutil, os
try:
    data = json.load(open('lab/PORTFOLIO_DATA.json'))
    for p in data['projects']:
        if p.get('full_preview_path') and os.path.exists(p['full_preview_path']):
            src = p['full_preview_path']
            dst = 'web/public/previews/' + p['preview_image']
            if os.path.abspath(src) != os.path.abspath(dst):
                shutil.copy(src, dst)
except Exception as e:
    print(f'⚠️ Preview Sync Note: {e}')
"

# Git Sync
echo "📡 Syncing Intelligence to Cloud..."
git add lab/ web/src/data/portfolio.json web/public/previews/
git commit -m "chore: automated omniscient sync [$(date +'%Y-%m-%d %H:%M')]"
git push origin feature/portfolio-dashboard

echo "✨ Total Saturation Complete. Ideaverse Hub is live."
