import os
import subprocess
import time
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter

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

def parse_package_json(filepath):
    deps = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            deps.extend(list(data.get('dependencies', {}).keys()))
            deps.extend(list(data.get('devDependencies', {}).keys()))
    except:
        pass
    return deps

def parse_requirements_txt(filepath):
    deps = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # e.g. requests==2.25.1 -> requests
                    pkg = re.split(r'[=<>~!]', line)[0].strip()
                    if pkg:
                        deps.append(pkg)
    except:
        pass
    return deps

def get_project_stats(dir_path, is_git):
    loc_by_lang = defaultdict(int)
    latest_mtime = 0
    largest_file = {"path": "", "loc": 0}
    tech_debt = 0
    dependencies = []
    
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        
        for f in files:
            full_path = os.path.join(root, f)
            
            # Extract dependencies
            if f == 'package.json':
                dependencies.extend(parse_package_json(full_path))
            elif f == 'requirements.txt':
                dependencies.extend(parse_requirements_txt(full_path))
                
            ext = os.path.splitext(f)[1].lower()
            if ext in CODE_EXTENSIONS:
                try:
                    mtime = os.path.getmtime(full_path)
                    if mtime > latest_mtime:
                        latest_mtime = mtime
                    
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as file:
                        lines = 0
                        for line in file:
                            line_str = line.strip()
                            if line_str:
                                lines += 1
                                # Tech Debt counter
                                if "TODO:" in line_str or "FIXME:" in line_str or "HACK:" in line_str:
                                    tech_debt += 1
                                    
                        loc_by_lang[CODE_EXTENSIONS[ext]] += lines
                        
                        if lines > largest_file["loc"]:
                            largest_file = {"path": full_path, "loc": lines}
                except:
                    pass
                    
    total_loc = sum(loc_by_lang.values())
    return loc_by_lang, total_loc, latest_mtime, largest_file, tech_debt, dependencies

def get_git_analytics(dir_path):
    analytics = {
        'recent_commits': 0,
        'commit_hours': [],
        'orphan_branches': []
    }
    try:
        # Get 7-day commits
        out = subprocess.check_output(
            ['git', 'log', '--since="7 days ago"', '--oneline'], 
            cwd=dir_path, stderr=subprocess.DEVNULL
        ).decode('utf-8')
        analytics['recent_commits'] = len([line for line in out.split('\n') if line.strip()])
        
        # Get commit hours for time-of-day tracking (last 100 commits to be fast)
        hours_out = subprocess.check_output(
            ['git', 'log', '-n', '100', '--format=%aI'], 
            cwd=dir_path, stderr=subprocess.DEVNULL
        ).decode('utf-8')
        
        for iso_date in hours_out.split('\n'):
            if iso_date.strip():
                # e.g. 2026-04-28T23:56:57+05:30
                try:
                    hour = int(iso_date[11:13])
                    analytics['commit_hours'].append(hour)
                except:
                    pass
                    
        # Check for old/orphan local branches (> 6 months old)
        six_months_ago = int((datetime.now() - timedelta(days=180)).timestamp())
        branches_out = subprocess.check_output(
            ['git', 'for-each-ref', '--format=%(refname:short)|%(committerdate:unix)', 'refs/heads/'], 
            cwd=dir_path, stderr=subprocess.DEVNULL
        ).decode('utf-8')
        
        for line in branches_out.split('\n'):
            if '|' in line:
                b_name, ts = line.split('|')
                if ts.strip().isdigit() and int(ts) < six_months_ago:
                    analytics['orphan_branches'].append(b_name.strip())
                    
    except:
        pass
        
    return analytics

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
        loc_by_lang, total_loc, last_mtime, largest_file, tech_debt, dependencies = get_project_stats(current_dir, is_git)
        
        status_info = {
            'path': current_dir,
            'is_git': is_git,
            'total_loc': total_loc,
            'loc_breakdown': dict(loc_by_lang),
            'last_modified': last_mtime,
            'largest_file': largest_file,
            'tech_debt': tech_debt,
            'dependencies': dependencies
        }
        
        if is_git:
            branch = ''
            uncommitted = 0
            remote_url = ''
            unpushed = 0
            git_analytics = get_git_analytics(current_dir)
            
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
                'recent_commits': git_analytics['recent_commits'],
                'commit_hours': git_analytics['commit_hours'],
                'orphan_branches': git_analytics['orphan_branches']
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
    top = sorted_langs[:2] # Reduced to 2 to save table space
    return "<br>".join([f"**{lang}**: {lines:,}" for lang, lines in top])

def generate_ascii_bar(value, total, width=20):
    if total == 0:
        return ""
    filled = int((value / total) * width)
    return "█" * filled + "░" * (width - filled)

def get_risk_score(s):
    if s.get('uncommitted', 0) > 20:
        return "🔴 High (Backup ASAP)"
    elif s.get('uncommitted', 0) > 5 or s.get('unpushed', 0) > 0:
        return "🟡 Mod (Needs Push)"
    elif s['is_git'] and not s.get('remote_url'):
        return "🟠 Warn (No Remote)"
    elif not s['is_git']:
        return "⚪ Unversioned"
    else:
        return "🟢 Safe"

def resolve_time_of_day(hours):
    if not hours:
        return "Unknown"
    most_common_hour = Counter(hours).most_common(1)[0][0]
    if 5 <= most_common_hour < 12:
        return "Morning Bird 🌅"
    elif 12 <= most_common_hour < 18:
        return "Afternoon Hustler ☀️"
    elif 18 <= most_common_hour < 23:
        return "Evening Coder 🌆"
    else:
        return "Night Owl 🦉"

def main():
    print(f"🔍 Scanning {ROOT_DIR} for projects (Max depth {MAX_DEPTH})...")
    projects = scan_for_projects(ROOT_DIR, 0)
    print(f"Found {len(projects)} projects. Processing analytics...")

    active_projects = []
    inactive_projects = []
    
    total_loc = 0
    total_uncommitted = 0
    total_7d_commits = 0
    total_tech_debt = 0
    global_loc_by_lang = defaultdict(int)
    global_dependencies = Counter()
    global_commit_hours = []
    total_orphan_branches = 0
    
    mac_largest_file = {"path": "", "loc": 0}
    
    for p in projects:
        total_loc += p['total_loc']
        total_tech_debt += p.get('tech_debt', 0)
        
        for lang, lines in p['loc_breakdown'].items():
            global_loc_by_lang[lang] += lines
            
        for dep in p.get('dependencies', []):
            global_dependencies[dep] += 1
            
        if p.get('commit_hours'):
            global_commit_hours.extend(p['commit_hours'])
            
        total_orphan_branches += len(p.get('orphan_branches', []))
            
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

    # Format global languages
    sorted_global_langs = sorted(global_loc_by_lang.items(), key=lambda x: -x[1])[:10]
    lang_chart_lines = []
    for lang, lines in sorted_global_langs:
        pct = (lines / total_loc) * 100 if total_loc > 0 else 0
        bar = generate_ascii_bar(lines, total_loc, width=25)
        lang_chart_lines.append(f"`{lang.ljust(12)} {bar} {pct:4.1f}% ({lines:,} LOC)`")
    lang_chart_str = "  \n".join(lang_chart_lines)
    
    # Format top dependencies
    top_deps = global_dependencies.most_common(5)
    deps_str = ", ".join([f"`{pkg}` ({count})" for pkg, count in top_deps]) if top_deps else "None detected"
    
    # Vibe Coding metrics
    time_of_day_vibe = resolve_time_of_day(global_commit_hours)

    # Save to JSON for future web UI consumption
    with open('PORTFOLIO_DATA.json', 'w') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "stats": {
                "projects_count": len(projects),
                "total_loc": total_loc,
                "uncommitted_files": total_uncommitted,
                "commits_7d": total_7d_commits,
                "tech_debt_items": total_tech_debt,
                "orphan_branches": total_orphan_branches,
                "coding_vibe": time_of_day_vibe
            },
            "top_dependencies": [{"name": k, "count": v} for k, v in top_deps],
            "language_distribution": [{"language": k, "loc": v} for k, v in sorted_global_langs],
            "projects": projects
        }, f, indent=2)

    # Generate Markdown
    readme_lines = [
        "Hi, I'm Paranjay 👋",
        "===================",
        "",
        "📍 Developer | 🤖 AI Enthusiast | 🚀 Tinkerer",
        "",
        "Currently experimenting, vibe-coding, and orchestrating ideas across multiple domains.",
        "",
        "### 📊 Global Mac Intelligence & Vibe Analysis",
        f"- **Total Projects Discovered**: {len(projects)}",
        f"- **Total Lines of Code**: {total_loc:,}",
        f"- **Unsaved Changes**: {total_uncommitted} files waiting to be committed",
        f"- **7-Day Local Commit Pulse**: 🔥 {total_7d_commits} commits",
        f"- **Tech Debt Score**: 🐛 {total_tech_debt:,} `TODO/FIXME`s across your mac",
        f"- **Dead/Orphan Branches**: 🍂 {total_orphan_branches} branches haven't been touched in >6 months",
        f"- **Top Dependencies Used**: {deps_str}",
        f"- **Primary Coding Rhythm**: {time_of_day_vibe}",
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
        "| Project | Data Risk | Tech Debt | Top Languages | Last Modified |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]

    def render_project_row(s):
        risk = get_risk_score(s)
        breakdown = format_lang_breakdown(s['loc_breakdown']) or "0"
        debt = f"🔨 {s.get('tech_debt', 0)}" if s.get('tech_debt', 0) > 0 else "✨ Clean"
        
        name = f"**{s['rel_path']}**"
        if s.get('recent_commits', 0) > 0:
            name += f" 🔥"
            
        mod = s['mod_str']
        
        return f"| {name} | {risk} | {debt} | {breakdown} | {mod} |"

    for p in active_projects:
        readme_lines.append(render_project_row(p))
        
    readme_lines.extend([
        "",
        "### 💤 Inactive Projects Archive",
        "*(No modifications in >30 days. Consider archiving or syncing.)*",
        "",
        "| Project | Data Risk | Tech Debt | Top Languages | Last Modified |",
        "| :--- | :--- | :--- | :--- | :--- |"
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

    print("✅ Wrote PORTFOLIO_DASHBOARD.md and PORTFOLIO_DATA.json!")

if __name__ == '__main__':
    main()
