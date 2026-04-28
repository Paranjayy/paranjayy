import os
import subprocess
import time
from datetime import datetime

ROOT_DIR = '/Users/paranjay'
MAX_DEPTH = 5

SKIP_DIRS = {
    'Library', 'Applications', 'Pictures', 'Music', 'Movies', '.Trash', 
    'node_modules', '.venv', 'venv', 'env', 'site-packages', 'build', 
    'dist', '.vscode', '.next', '.cache', 'Public', 'opt', 'Downloads'
}

# Only check inside /Users/paranjay/Downloads/2work or similar if we want to, 
# but let's allow Downloads for now but skip the root Downloads files unless it's a project folder?
# Actually, the user's dev folder is in Downloads/2work/dev. We must NOT skip Downloads!
# So I will REMOVE 'Downloads' from SKIP_DIRS.

SKIP_DIRS.discard('Downloads')

CODE_EXTENSIONS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.html', '.css', '.scss', 
    '.rs', '.go', '.c', '.cpp', '.h', '.java', '.sh', '.mjs', '.md', 
    '.json', '.yml', '.yaml', '.toml', '.swift'
}

PROJECT_MARKERS = {
    'package.json', 'requirements.txt', 'Cargo.toml', 'Makefile', 
    'pom.xml', 'build.gradle', 'go.mod', 'docker-compose.yml', 'CMakeLists.txt',
    'setup.py', 'gemfile', 'pyproject.toml'
}

def is_code_file(filename):
    return any(filename.endswith(ext) for ext in CODE_EXTENSIONS)

def get_project_stats(dir_path, is_git):
    loc = 0
    latest_mtime = 0
    
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        
        for f in files:
            if is_code_file(f):
                full_path = os.path.join(root, f)
                try:
                    mtime = os.path.getmtime(full_path)
                    if mtime > latest_mtime:
                        latest_mtime = mtime
                    
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as file:
                        loc += sum(1 for line in file if line.strip())
                except:
                    pass
                    
    return loc, latest_mtime

def scan_for_projects(current_dir, depth):
    if depth > MAX_DEPTH:
        return []
        
    projects = []
    
    try:
        entries = os.listdir(current_dir)
    except PermissionError:
        return []
        
    is_git = '.git' in entries and os.path.isdir(os.path.join(current_dir, '.git'))
    
    # Check for project markers to identify a non-git project
    is_non_git_project = not is_git and any(marker in entries for marker in PROJECT_MARKERS)
    
    if is_git or is_non_git_project:
        loc, last_mtime = get_project_stats(current_dir, is_git)
        
        status_info = {
            'path': current_dir,
            'is_git': is_git,
            'loc': loc,
            'last_modified': last_mtime,
        }
        
        if is_git:
            branch = ''
            uncommitted = 0
            remote_url = ''
            unpushed = 0
            try:
                branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=current_dir, stderr=subprocess.DEVNULL).decode('utf-8').strip()
                status_out = subprocess.check_output(['git', 'status', '--porcelain'], cwd=current_dir, stderr=subprocess.DEVNULL).decode('utf-8')
                uncommitted = len([line for line in status_out.split('\n') if line.strip()])
                remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], cwd=current_dir, stderr=subprocess.DEVNULL).decode('utf-8').strip()
                if branch and remote_url:
                    unpushed_out = subprocess.check_output(['git', 'rev-list', f'HEAD...origin/{branch}', '--count'], cwd=current_dir, stderr=subprocess.DEVNULL).decode('utf-8').strip()
                    unpushed = int(unpushed_out) if unpushed_out.isdigit() else 0
            except:
                pass
                
            status_info.update({
                'branch': branch,
                'uncommitted': uncommitted,
                'unpushed': unpushed,
                'remote_url': remote_url
            })
            
        return [status_info]

    # Recurse
    for entry in entries:
        if entry in SKIP_DIRS or entry.startswith('.'):
            continue
        full_path = os.path.join(current_dir, entry)
        if os.path.isdir(full_path):
            projects.extend(scan_for_projects(full_path, depth + 1))
            
    return projects

def format_time_diff(mtime):
    if not mtime:
        return "Unknown", False
    diff = time.time() - mtime
    days = diff / (3600 * 24)
    active = days < 30
    if days < 1:
        return "Today", active
    elif days < 2:
        return "Yesterday", active
    else:
        return f"{int(days)}d ago", active

def main():
    print(f"🔍 Scanning {ROOT_DIR} for projects (Max depth {MAX_DEPTH})...")
    projects = scan_for_projects(ROOT_DIR, 0)
    print(f"Found {len(projects)} projects. Generating dashboard...")

    active_projects = []
    inactive_projects = []
    
    total_loc = 0
    total_uncommitted = 0
    
    for p in projects:
        total_loc += p['loc']
        p['rel_path'] = os.path.relpath(p['path'], ROOT_DIR)
        mod_str, is_active = format_time_diff(p['last_modified'])
        p['mod_str'] = mod_str
        
        if p.get('uncommitted', 0) > 0:
            total_uncommitted += p['uncommitted']
            
        if is_active:
            active_projects.append(p)
        else:
            inactive_projects.append(p)
            
    active_projects.sort(key=lambda x: -x['loc'])
    inactive_projects.sort(key=lambda x: -x['loc'])

    readme_lines = [
        "Hi, I'm Paranjay 👋",
        "===================",
        "",
        "📍 Developer | 🤖 AI Enthusiast | 🚀 Tinkerer",
        "",
        "Currently experimenting, vibe-coding, and orchestrating ideas across multiple domains.",
        "",
        "### 📊 Global Stats",
        f"- **Total Projects Tracked**: {len(projects)}",
        f"- **Total Lines of Code Tracked**: {total_loc:,}",
        f"- **Unsaved Changes Across Mac**: {total_uncommitted} files",
        f"- **Active Projects (30 days)**: {len(active_projects)}",
        "",
        "---",
        "",
        "### 🟢 Active Projects & Orchestration Dashboard",
        "*(Modified within the last 30 days)*",
        "",
        "| Project | Type | Branch | Status | LOC | Last Modified |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    def render_project_row(s):
        if s['is_git']:
            status_str = "✅ Synced"
            if s['uncommitted'] > 0 and s['unpushed'] > 0:
                status_str = f"⚠️ {s['uncommitted']} uncommitted, {s['unpushed']} unpushed"
            elif s['uncommitted'] > 0:
                status_str = f"📝 {s['uncommitted']} uncommitted"
            elif s['unpushed'] > 0:
                status_str = f"⬆️ {s['unpushed']} ahead"
            elif not s['remote_url']:
                status_str = "🌐 Local Only"
            
            p_type = "Git 🐙"
            branch = s['branch'] or 'None'
        else:
            status_str = "📁 Unversioned"
            p_type = "Folder 📁"
            branch = "-"
            
        name = f"**{s['rel_path']}**"
        loc = f"{s['loc']:,}"
        mod = s['mod_str']
        
        return f"| {name} | {p_type} | `{branch}` | {status_str} | {loc} | {mod} |"

    for p in active_projects:
        readme_lines.append(render_project_row(p))
        
    readme_lines.extend([
        "",
        "### 💤 Inactive Projects Archive",
        "*(No modifications in >30 days. Consider archiving or syncing.)*",
        "",
        "| Project | Type | Branch | Status | LOC | Last Modified |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ])
    
    for p in inactive_projects:
        readme_lines.append(render_project_row(p))

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
