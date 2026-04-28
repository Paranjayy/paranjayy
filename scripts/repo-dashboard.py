import os
import subprocess
import time
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter

ROOT_DIR = '/Users/paranjay'
MAX_DEPTH = 12

SKIP_DIRS = {
    'Library', 'Applications', 'Pictures', 'Music', 'Movies', '.Trash', 
    'node_modules', '.venv', 'venv', 'env', 'site-packages', 'build', 
    'dist', '.vscode', '.next', '.cache', 'Public', 'opt', 'Pods', 'vendor'
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
    tech_debt_count = 0
    extracted_todos = []
    dependencies = []
    has_license = False
    env_exposed = False
    proj_type = "Project"
    
    # Check for gitignore content if it exists
    ignored_patterns = set()
    gitignore_path = os.path.join(dir_path, '.gitignore')
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, 'r') as f:
                ignored_patterns = {line.strip() for line in f if line.strip() and not line.startswith('#')}
        except:
            pass

    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        
        for f in files:
            full_path = os.path.join(root, f)
            
            if f.lower() in ['license', 'license.md', 'license.txt']:
                has_license = True
            
            # Check for exposed .env files
            if f == '.env' and is_git:
                # If .env is present, check if it's in gitignore
                if '.env' not in ignored_patterns:
                    env_exposed = True

            if f == 'package.json':
                dependencies.extend(parse_package_json(full_path))
                proj_type = "Web App"
            elif f == 'requirements.txt' or f == 'pyproject.toml':
                dependencies.extend(parse_requirements_txt(full_path))
                proj_type = "Python Tool"
            elif f == 'manifest.json' and 'Extension' not in proj_type:
                proj_type = "Browser Extension"
            elif f == 'Dockerfile':
                proj_type += " (Dockerized)"
                
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
                                # Search for actionable tech debt
                                upper_line = line_str.upper()
                                if "TODO:" in upper_line or "FIXME:" in upper_line or "HACK:" in upper_line:
                                    tech_debt_count += 1
                                    # Store a few sample TODOs for the JSON payload
                                    if len(extracted_todos) < 5:
                                        clean_todo = line_str.replace('//', '').replace('/*', '').replace('#', '').strip()
                                        if clean_todo:
                                            extracted_todos.append(clean_todo)
                                    
                        loc_by_lang[CODE_EXTENSIONS[ext]] += lines
                        
                        if lines > largest_file["loc"]:
                            largest_file = {"path": full_path, "loc": lines}
                except:
                    pass
                    
    total_loc = sum(loc_by_lang.values())
    return loc_by_lang, total_loc, latest_mtime, largest_file, tech_debt_count, extracted_todos, dependencies, has_license, env_exposed, proj_type

def get_git_analytics(dir_path):
    analytics = {
        'recent_commits': 0,
        'commit_hours': [],
        'weekend_commits': 0,
        'total_commits_checked': 0,
        'orphan_branches': [],
        'commit_words': [],
        'age_days': 0
    }
    try:
        # Get 7-day commits count
        out = subprocess.check_output(
            ['git', 'log', '--since="7 days ago"', '--oneline'], 
            cwd=dir_path, stderr=subprocess.DEVNULL
        ).decode('utf-8')
        analytics['recent_commits'] = len([line for line in out.split('\n') if line.strip()])
        
        # Analyze last 100 commits for habits (time, weekend, words, emojis)
        log_out = subprocess.check_output(
            ['git', 'log', '-n', '100', '--format=%aI|%s'], 
            cwd=dir_path, stderr=subprocess.DEVNULL
        ).decode('utf-8')
        
        stopwords = {'merge', 'branch', 'into', 'and', 'the', 'to', 'for', 'a', 'in', 'of', 'fix', 'update', 'add', 'added'}
        
        # Simple regex to catch common emojis
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
        
        for line in log_out.split('\n'):
            if '|' in line:
                analytics['total_commits_checked'] += 1
                iso_date, msg = line.split('|', 1)
                
                # Analyze time and day
                try:
                    dt = datetime.fromisoformat(iso_date)
                    analytics['commit_hours'].append(dt.hour)
                    if dt.weekday() >= 5: # Saturday=5, Sunday=6
                        analytics['weekend_commits'] += 1
                except:
                    pass
                    
                # Analyze words (ignore common boring words)
                words = re.findall(r'\b[a-zA-Z]{3,}\b', msg.lower())
                analytics['commit_words'].extend([w for w in words if w not in stopwords])
                
                # Analyze emojis
                emojis_found = emoji_pattern.findall(msg)
                if emojis_found:
                    if 'commit_emojis' not in analytics:
                        analytics['commit_emojis'] = []
                    analytics['commit_emojis'].extend(emojis_found)
                    
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
                    
        # Get project age (first commit date)
        first_commit = subprocess.check_output(
            ['git', 'log', '--reverse', '--format=%aI'], 
            cwd=dir_path, stderr=subprocess.DEVNULL
        ).decode('utf-8').split('\n')[0]
        if first_commit:
            dt = datetime.fromisoformat(first_commit)
            analytics['age_days'] = (datetime.now(dt.tzinfo) - dt).days

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
        loc_by_lang, total_loc, last_mtime, largest_file, tech_debt_count, extracted_todos, dependencies, has_license, env_exposed, proj_type = get_project_stats(current_dir, is_git)
        
        status_info = {
            'path': current_dir,
            'is_git': is_git,
            'total_loc': total_loc,
            'loc_breakdown': dict(loc_by_lang),
            'last_modified': last_mtime,
            'largest_file': largest_file,
            'tech_debt_count': tech_debt_count,
            'todos_sample': extracted_todos,
            'dependencies': dependencies,
            'has_license': has_license,
            'env_exposed': env_exposed,
            'proj_type': proj_type
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
                'weekend_commits': git_analytics['weekend_commits'],
                'total_commits_checked': git_analytics['total_commits_checked'],
                'orphan_branches': git_analytics['orphan_branches'],
                'commit_words': git_analytics['commit_words'],
                'age_days': git_analytics['age_days']
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
    top = sorted_langs[:2] 
    return "<br>".join([f"**{lang}**: {lines:,}" for lang, lines in top])

def generate_ascii_bar(value, total, width=20):
    if total == 0:
        return ""
    filled = int((value / total) * width)
    return "█" * filled + "░" * (width - filled)

def get_risk_score(s):
    if s.get('env_exposed', False):
        return "🔥 CRITICAL (.env Exposed)"
    elif s.get('uncommitted', 0) > 20:
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
        return "Morning (5AM - 12PM)"
    elif 12 <= most_common_hour < 18:
        return "Afternoon (12PM - 6PM)"
    elif 18 <= most_common_hour < 23:
        return "Evening (6PM - 11PM)"
    else:
        return "Night Owl (11PM - 5AM)"

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
    global_commit_words = Counter()
    global_commit_emojis = Counter()
    total_orphan_branches = 0
    total_weekend_commits = 0
    total_commits_checked = 0
    
    mac_largest_file = {"path": "", "loc": 0}
    
    for p in projects:
        total_loc += p['total_loc']
        total_tech_debt += p.get('tech_debt_count', 0)
        
        for lang, lines in p['loc_breakdown'].items():
            global_loc_by_lang[lang] += lines
            
        for dep in p.get('dependencies', []):
            global_dependencies[dep] += 1
            
        if p.get('commit_hours'):
            global_commit_hours.extend(p['commit_hours'])
            
        if p.get('commit_words'):
            for w in p['commit_words']:
                global_commit_words[w] += 1
                
        if p.get('commit_emojis'):
            for e in p['commit_emojis']:
                global_commit_emojis[e] += 1
                
        total_weekend_commits += p.get('weekend_commits', 0)
        total_commits_checked += p.get('total_commits_checked', 0)
            
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
    
    # Format commit words
    top_words = global_commit_words.most_common(5)
    words_str = ", ".join([f"`{word}` ({count})" for word, count in top_words]) if top_words else "Not enough history"

    # Format commit emojis
    top_emojis = global_commit_emojis.most_common(5)
    emojis_str = " ".join([f"{emoji}" for emoji, count in top_emojis]) if top_emojis else "No emojis used"

    weekend_pct = (total_weekend_commits / total_commits_checked * 100) if total_commits_checked > 0 else 0
    time_of_day_vibe = resolve_time_of_day(global_commit_hours)

    # Save to JSON for web consumption
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
                "primary_coding_time": time_of_day_vibe,
                "weekend_commit_pct": round(weekend_pct, 1)
            },
            "top_commit_words": [{"word": k, "count": v} for k, v in top_words],
            "top_commit_emojis": [{"emoji": k, "count": v} for k, v in top_emojis],
            "top_dependencies": [{"name": k, "count": v} for k, v in top_deps],
            "language_distribution": [{"language": k, "loc": v} for k, v in sorted_global_langs],
            "projects": projects
        }, f, indent=2)

    # Generate Markdown
    readme_lines = [
        "Hi, I'm Paranjay 👋",
        "===================",
        "",
        "📍 Developer | 🤖 Tinker | 🚀 Code Explorer",
        "",
        "A space to track projects, capture ideas, and monitor repository health across my local machine.",
        "",
        "### 📊 Dashboard Metrics",
        f"- **Projects Discovered**: {len(projects)}",
        f"- **Total Lines of Code**: {total_loc:,}",
        f"- **Unsaved Changes**: {total_uncommitted} files waiting to be committed",
        f"- **7-Day Commit Pulse**: 🔥 {total_7d_commits} commits",
        f"- **Tech Debt Markers**: 🐛 {total_tech_debt:,} (`TODO`, `FIXME`, or `HACK` tags found in code files)",
        f"- **Forgotten Branches**: 🍂 {total_orphan_branches} local branches untouched in >6 months",
        f"- **Top Dependencies**: {deps_str}",
        f"- **Most Used Commit Words**: {words_str}",
        f"- **Favorite Commit Emojis**: {emojis_str}",
        f"- **Coding Hours**: Mostly {time_of_day_vibe} ({weekend_pct:.1f}% on weekends)",
        f"- **Largest Monolith File**: `{os.path.basename(mac_largest_file['path'])}` ({mac_largest_file['loc']:,} LOC)",
        "",
        "#### 🧬 Language Breakdown",
        lang_chart_str,
        "",
        "---",
        "",
        "### 🟢 Active Projects Dashboard",
        "*(Modified within the last 30 days)*",
        "",
        "| Project | Type | Data Risk | Tech Debt | Top Languages | Last Modified |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    def render_project_row(s):
        risk = get_risk_score(s)
        breakdown = format_lang_breakdown(s['loc_breakdown']) or "0"
        debt = f"🔨 {s.get('tech_debt_count', 0)}" if s.get('tech_debt_count', 0) > 0 else "✨ Clean"
        
        name = f"**{s['rel_path']}**"
        
        # Add license badge if present
        if s.get('has_license'):
            name += " 📜"
            
        # Format age if available
        age = s.get('age_days', 0)
        age_str = f" ({age}d old)" if age > 0 else ""
        
        if s.get('recent_commits', 0) > 0:
            name += f" 🔥"
            
        name += age_str
        mod = s['mod_str']
        p_type = s.get('proj_type', 'Project')
        
        return f"| {name} | {p_type} | {risk} | {debt} | {breakdown} | {mod} |"

    for p in active_projects:
        readme_lines.append(render_project_row(p))
        
    readme_lines.extend([
        "",
        "### 💤 Inactive Projects Archive",
        "*(No modifications in >30 days.)*",
        "",
        "| Project | Type | Data Risk | Tech Debt | Top Languages | Last Modified |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ])
    
    for p in inactive_projects:
        readme_lines.append(render_project_row(p))

    readme_lines.extend([
        "",
        "---",
        "",
        "### 🎨 About this Repository",
        "*(Draft based on modern profiles)*",
        "",
        "**Tech Stack**: `TypeScript` `React` `Node.js` `Python`",
        "",
        "**Recent Highlights**:",
        "- 🌌 **The Ideaverse Portfolio**: Modernizing scholarly portfolios.",
        "- 🎮 **Gravity Hub**: IFTTT Gaming integrations for Windows to Mac telemetry.",
        "- ⚡ **Webdev Toolbox**: Powerful developer extensions.",
        "- 🏰 **Gemini Design Palace**: Unslopified, premium reactive UI systems.",
        "",
        "> *“Ship beats perfect.”*"
    ])

    with open('PORTFOLIO_DASHBOARD.md', 'w') as f:
        f.write('\n'.join(readme_lines))

    print("✅ Wrote PORTFOLIO_DASHBOARD.md and PORTFOLIO_DATA.json!")

if __name__ == '__main__':
    main()
