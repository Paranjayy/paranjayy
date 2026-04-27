import os
import subprocess

ROOT_DIR = '/Users/paranjay/Downloads/2work/dev'

def get_repos(dir_path, depth=0, max_depth=3):
    if depth > max_depth:
        return []
    repos = []
    try:
        entries = os.listdir(dir_path)
    except PermissionError:
        return []

    if '.git' in entries and os.path.isdir(os.path.join(dir_path, '.git')):
        return [dir_path]

    for entry in entries:
        if entry == 'node_modules' or entry.startswith('.'):
            continue
        full_path = os.path.join(dir_path, entry)
        if os.path.isdir(full_path):
            repos.extend(get_repos(full_path, depth + 1, max_depth))
    return repos

def get_repo_status(repo_path):
    rel_path = os.path.relpath(repo_path, ROOT_DIR)
    if rel_path == '.':
        rel_path = 'dev'
        
    branch = ''
    try:
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=repo_path, stderr=subprocess.DEVNULL).decode('utf-8').strip()
    except:
        pass
        
    uncommitted = 0
    try:
        status_out = subprocess.check_output(['git', 'status', '--porcelain'], cwd=repo_path, stderr=subprocess.DEVNULL).decode('utf-8')
        uncommitted = len([line for line in status_out.split('\n') if line.strip()])
    except:
        pass

    remote_url = ''
    try:
        remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], cwd=repo_path, stderr=subprocess.DEVNULL).decode('utf-8').strip()
    except:
        pass

    unpushed = 0
    if branch and remote_url:
        try:
            unpushed_out = subprocess.check_output(['git', 'rev-list', f'HEAD...origin/{branch}', '--count'], cwd=repo_path, stderr=subprocess.DEVNULL).decode('utf-8').strip()
            unpushed = int(unpushed_out) if unpushed_out.isdigit() else 0
        except:
            pass

    return {
        'path': rel_path,
        'branch': branch,
        'uncommitted': uncommitted,
        'unpushed': unpushed,
        'remote_url': remote_url
    }

def main():
    print("🔍 Scanning for git repositories...")
    repos = get_repos(ROOT_DIR)
    print(f"Found {len(repos)} repositories. Checking status...")

    stats = []
    for repo in repos:
        stats.append(get_repo_status(repo))

    stats.sort(key=lambda x: (-x['uncommitted'], -x['unpushed'], x['path']))

    readme_lines = [
        "Hi, I'm Paranjay 👋",
        "===================",
        "",
        "📍 Developer | 🤖 AI Enthusiast | 🚀 Tinkerer",
        "",
        "Currently experimenting, vibe-coding, and orchestrating ideas across multiple domains.",
        "",
        "### 🛠️ Current Status & Active Orchestration",
        "*A unified dashboard to monitor project sync states, preventing data loss and keeping ideas consolidated.*",
        "",
        "| Repository | Branch | Remote | Status |",
        "| :--- | :--- | :--- | :--- |"
    ]

    for s in stats:
        status_str = "✅ Clean & Synced"
        if s['uncommitted'] > 0 and s['unpushed'] > 0:
            status_str = f"⚠️ {s['uncommitted']} uncommitted, {s['unpushed']} unpushed"
        elif s['uncommitted'] > 0:
            status_str = f"📝 {s['uncommitted']} uncommitted changes"
        elif s['unpushed'] > 0:
            status_str = f"⬆️ {s['unpushed']} commits ahead of remote"
        elif not s['remote_url']:
            status_str = "🌐 No remote set (Local only)"

        remote_link = 'None'
        if s['remote_url']:
            url = s['remote_url'].replace('.git', '') if s['remote_url'].startswith('http') else s['remote_url']
            remote_link = f"[origin]({url})"
            
        branch_disp = s['branch'] if s['branch'] else 'None'
        
        readme_lines.append(f"| **{s['path']}** | `{branch_disp}` | {remote_link} | {status_str} |")

    readme_lines.extend([
        "",
        "---",
        "",
        "### 🎨 The Aesthetic / Portfolio Idea",
        "*(Draft based on modern profiles - inspired by steipete)*",
        "",
        "**Tech Stack**: `TypeScript` `React` `Node.js` `Python` `AI Agents`",
        "",
        "**Recent Highlights**:",
        "- 🌌 **The Ideaverse Portfolio**: Modernizing scholarly portfolios with high-end aesthetic.",
        "- 🎮 **Gravity Hub**: IFTTT Gaming integrations for Windows to Mac telemetry.",
        "- ⚡ **Webdev Toolbox**: Powerful developer extensions built for God mode.",
        "- 🏰 **Gemini Design Palace**: Unslopified, premium reactive UI systems.",
        "",
        "> *“Ship beats perfect. But if it doesn’t look like Stripe Press, is it even worth shipping?”*"
    ])

    with open('PORTFOLIO_DASHBOARD.md', 'w') as f:
        f.write('\n'.join(readme_lines))

    print("✅ Wrote PORTFOLIO_DASHBOARD.md!")

if __name__ == '__main__':
    main()
