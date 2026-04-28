import os
import subprocess
import time
from datetime import datetime, timedelta
from collections import defaultdict

ROOT_DIR = '/Users/paranjay'
MAX_DEPTH = 7

SKIP_DIRS = {
    'Library', 'Applications', 'Pictures', 'Music', 'Movies', '.Trash', 
    'node_modules', '.venv', 'venv', 'env', 'site-packages', 'build', 
    'dist', '.vscode', '.next', '.cache', 'Public', 'opt'
}

CODE_EXTENSIONS = {
    '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.tsx': 'React TS', 
    '.jsx': 'React JS', '.html': 'HTML', '.css': 'CSS', '.scss': 'SCSS', 
    '.rs': 'Rust', '.go': 'Go', '.c': 'C', '.cpp': 'C++', '.h': 'C Header', 
    '.java': 'Java', '.sh': 'Shell', '.mjs': 'Node JS', '.md': 'Markdown', 
    '.json': 'JSON', '.yml': 'YAML', '.yaml': 'YAML', '.toml': 'TOML', 
    '.swift': 'Swift', '.sql': 'SQL', '.graphql': 'GraphQL', '.vue': 'Vue'
}

PROJECT_MARKERS = {
    'package.json', 'requirements.txt', 'Cargo.toml', 'Makefile', 
    'pom.xml', 'build.gradle', 'go.mod', 'docker-compose.yml', 'CMakeLists.txt',
    'setup.py', 'gemfile', 'pyproject.toml'
}

def is_code_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in CODE_EXTENSIONS

def get_project_stats(dir_path, is_git):
    loc_by_lang = defaultdict(int)
    latest_mtime = 0
    largest_file = {"path": "", "loc": 0}
    
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in CODE_EXTENSIONS:
                full_path = os.path.join(root, f)
                try:
                    mtime = os.path.getmtime(full_path)
                    if mtime > latest_mtime:
                        latest_mtime = mtime
                    
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as file:
                        lines = sum(1 for line in file if line.strip())
                        loc_by_lang[CODE_EXTENSIONS[ext]] += lines
                        
                        if lines > largest_file["loc"]:
                            largest_file = {"path": full_path, "loc": lines}
                except:
                    pass
                    
    total_loc = sum(loc_by_lang.values())
    return loc_by_lang, total_loc, latest_mtime, largest_file

def get_recent_commits(dir_path):
    try:
        # Get commits in the last 7 days
        out = subprocess.check_output(
            ['git', 'log', '--since="7 days ago"', '--oneline'], 
            cwd=dir_path, stderr=subprocess.DEVNULL
        ).decode('utf-8')
        return len([line for line in out.split('\n') if line.strip()])
    except:
        return 0

def scan_for_projects(current_dir, depth):
    if depth > MAX_DEPTH:
        return []
        
    projects = []
    
    try:
        entries = os.listdir(current_dir)
    except PermissionError:
        return []
        
    is_git = '.git' in entries and os.path.isdir(os.path.join(current_dir, '.git'))
    is_non_git_project = not is_git and any(marker in entries for marker in PROJECT_MARKERS)
    
    if is_git or is_non_git_project:
        loc_by_lang, total_loc, last_mtime, largest_file = get_project_stats(current_dir, is_git)
        
        status_info = {
            'path': current_dir,
            'is_git': is_git,
            'total_loc': total_loc,
            'loc_breakdown': dict(loc_by_lang),
            'last_modified': last_mtime,
            'largest_file': largest_file
        }
        
        if is_git:
            branch = ''
            uncommitted = 0
            remote_url = ''
            unpushed = 0
            recent_commits = get_recent_commits(current_dir)
            
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
                'remote_url': remote_url,
                'recent_commits': recent_commits
            })
            
        return [status_info]

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

def format_lang_breakdown(loc_dict):
    if not loc_dict:
        return "None"
    sorted_langs = sorted(loc_dict.items(), key=lambda x: -x[1])
    top = sorted_langs[:3]
    return "<br>".join([f"**{lang}**: {lines:,}" for lang, lines in top])

def generate_ascii_bar(value, total, width=20):
    if total == 0:
        return ""
    filled = int((value / total) * width)
    return "█" * filled + "░" * (width - filled)

def get_risk_score(s):
    if s.get('uncommitted', 0) > 20:
        return "🔴 High (Backup ASAP!)"
    elif s.get('uncommitted', 0) > 5 or s.get('unpushed', 0) > 0:
        return "🟡 Moderate (Needs Push)"
    elif s['is_git'] and not s.get('remote_url'):
        return "🟠 Warning (No Remote)"
    elif not s['is_git']:
        return "⚪ Unversioned (Local)"
    else:
        return "🟢 Safe"

def main():
    print(f"🔍 Scanning {ROOT_DIR} for projects (Max depth {MAX_DEPTH})...")
    projects = scan_for_projects(ROOT_DIR, 0)
    print(f"Found {len(projects)} projects. Generating dashboard...")

    active_projects = []
    inactive_projects = []
    
    total_loc = 0
    total_uncommitted = 0
    total_7d_commits = 0
    global_loc_by_lang = defaultdict(int)
    
    mac_largest_file = {"path": "", "loc": 0}
    
    for p in projects:
        total_loc += p['total_loc']
        for lang, lines in p['loc_breakdown'].items():
            global_loc_by_lang[lang] += lines
            
        if p['largest_file']['loc'] > mac_largest_file['loc']:
            mac_largest_file = p['largest_file']
            
        p['rel_path'] = os.path.relpath(p['path'], ROOT_DIR)
        mod_str, is_active = format_time_diff(p['last_modified'])
        p['mod_str'] = mod_str
        
        if p.get('uncommitted', 0) > 0:
            total_uncommitted += p['uncommitted']
            
        total_7d_commits += p.get('recent_commits', 0)
            
        if is_active:
            active_projects.append(p)
        else:
            inactive_projects.append(p)
            
    active_projects.sort(key=lambda x: -x['total_loc'])
    inactive_projects.sort(key=lambda x: -x['total_loc'])

    # Build ASCII Language Chart
    sorted_global_langs = sorted(global_loc_by_lang.items(), key=lambda x: -x[1])[:10]
    lang_chart_lines = []
    for lang, lines in sorted_global_langs:
        pct = (lines / total_loc) * 100 if total_loc > 0 else 0
        bar = generate_ascii_bar(lines, total_loc, width=25)
        lang_chart_lines.append(f"`{lang.ljust(12)} {bar} {pct:4.1f}% ({lines:,} LOC)`")
        
    lang_chart_str = "  \n".join(lang_chart_lines)

    readme_lines = [
        "Hi, I'm Paranjay 👋",
        "===================",
        "",
        "📍 Developer | 🤖 AI Enthusiast | 🚀 Tinkerer",
        "",
        "Currently experimenting, vibe-coding, and orchestrating ideas across multiple domains.",
        "",
        "### 📊 Global Mac Intelligence",
        f"- **Total Projects Discovered**: {len(projects)}",
        f"- **Total Lines of Code Handled**: {total_loc:,}",
        f"- **Unsaved Changes Across Mac**: {total_uncommitted} files waiting to be committed.",
        f"- **7-Day Local Commit Pulse**: 🔥 {total_7d_commits} commits in the past week.",
        f"- **Biggest Monolith File**: `{os.path.basename(mac_largest_file['path'])}` ({mac_largest_file['loc']:,} LOC)",
        "",
        "#### 🧬 Language DNA Breakdown",
        lang_chart_str,
        "",
        "---",
        "",
        "### 🟢 Active Projects & Orchestration Dashboard",
        "*(Modified within the last 30 days)*",
        "",
        "| Project | Type | Branch | Data Risk | LOC Breakdown | Last Modified |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    def render_project_row(s):
        p_type = "Git 🐙" if s['is_git'] else "Folder 📁"
        branch = s.get('branch', '') or '-'
        risk = get_risk_score(s)
        breakdown = format_lang_breakdown(s['loc_breakdown']) or "0"
            
        name = f"**{s['rel_path']}**"
        if s.get('recent_commits', 0) > 0:
            name += f" 🔥"
            
        mod = s['mod_str']
        
        return f"| {name} | {p_type} | `{branch}` | {risk} | {breakdown} | {mod} |"

    for p in active_projects:
        readme_lines.append(render_project_row(p))
        
    readme_lines.extend([
        "",
        "### 💤 Inactive Projects Archive",
        "*(No modifications in >30 days. Consider archiving or syncing.)*",
        "",
        "| Project | Type | Branch | Data Risk | LOC Breakdown | Last Modified |",
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
