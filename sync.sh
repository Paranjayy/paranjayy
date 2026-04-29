#!/bin/bash
# Ideaverse Orchestration Sync
echo "🚀 Starting Ideaverse Sync..."
cd "$(dirname "$0")"

# Run Intelligence Engine
python3 scripts/repo-dashboard.py

# Move Data to Web App
mkdir -p web/public/previews
cp PORTFOLIO_DATA.json web/src/data/portfolio.json

# Copy Preview Images
python3 -c "import json, shutil, os; data=json.load(open('PORTFOLIO_DATA.json')); [shutil.copy(p['full_preview_path'], 'web/public/previews/' + p['preview_image']) for p in data['projects'] if p.get('full_preview_path') and os.path.exists(p['full_preview_path'])]"

# Git Sync
echo "📡 Pushing to the Cloud..."
git add PORTFOLIO_DASHBOARD.md PORTFOLIO_DATA.json web/src/data/portfolio.json web/public/previews/
git commit -m "chore: automated ideaverse pulse sync [$(date +'%Y-%m-%d %H:%M')]"
git push origin feature/portfolio-dashboard

echo "✨ Sync Complete. Web Hub will redeploy shortly."
