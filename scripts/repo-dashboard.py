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

def get_sparkline(counts):
    chars = " ▂▃▄▅▆▇█"
    if not counts: return ""
    max_count = max(counts)
    if max_count == 0: return "       "
    return "".join(chars[int(c * (len(chars)-1) / max_count)] for c in counts)

def analyze_naming_vibe(text):
    camel = len(re.findall(r'\b[a-z]+(?:[A-Z][a-z]+)+\b', text))
    snake = len(re.findall(r'\b[a-z]+(?:_[a-z]+)+\b', text))
    return camel, snake

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
    keywords = Counter()
    readme_word_count = 0
    naming_styles = {"camel": 0, "snake": 0}
    
    ignored_patterns = set()
    gitignore_path = os.path.join(dir_path, '.gitignore')
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, 'r') as f:
                ignored_patterns = {line.strip() for line in f if line.strip() and not line.startswith('#')}
        except: pass

    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        
        for f in files:
            full_path = os.path.join(root, f)
            if f.lower() in ['license', 'license.md', 'license.txt']: has_license = True
            
            if f.lower() == 'readme.md':
                try:
                    with open(full_path, 'r', errors='ignore') as rf:
                        readme_word_count = len(rf.read().split())
                except: pass

            if f == '.env' and is_git:
                if '.env' not in ignored_patterns: env_exposed = True

            if f == 'package.json':
                proj_type = "Web App"
                try:
                    with open(full_path, 'r') as pjf:
                        data = json.load(pjf)
                        dependencies.extend(list(data.get('dependencies', {}).keys()))
                        dependencies.extend(list(data.get('devDependencies', {}).keys()))
                except: pass
            elif f == 'requirements.txt' or f == 'pyproject.toml':
                proj_type = "Python Tool"
            elif f == 'manifest.json': proj_type = "Browser Extension"
            elif f == 'Dockerfile': proj_type += " (Dockerized)"
                
            ext = os.path.splitext(f)[1].lower()
            if ext in CODE_EXTENSIONS:
                try:
                    mtime = os.path.getmtime(full_path)
                    if mtime > latest_mtime: latest_mtime = mtime
                    
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                        lines = content.count('\n')
                        loc_by_lang[CODE_EXTENSIONS[ext]] += lines
                        
                        # Naming Vibe
                        c, s = analyze_naming_vibe(content)
                        naming_styles["camel"] += c
                        naming_styles["snake"] += s
                        
                        # Keywords
                        words = re.findall(r'\b[a-zA-Z]{4,15}\b', content)
                        for w in words:
                            if w.lower() in {'async', 'await', 'export', 'import', 'const', 'function', 'interface', 'class', 'return'}:
                                keywords[w.lower()] += 1

                        # Tech Debt
                        if any(x in content.upper() for x in ["TODO:", "FIXME:", "HACK:"]):
                            tech_debt_count += 1
                                    
                        if lines > largest_file["loc"]:
                            largest_file = {"path": full_path, "loc": lines}
                except: pass
                    
    total_loc = sum(loc_by_lang.values())
    return loc_by_lang, total_loc, latest_mtime, largest_file, tech_debt_count, extracted_todos, dependencies, has_license, env_exposed, proj_type, keywords, readme_word_count, naming_styles

def get_git_analytics(dir_path):
    analytics = {'recent_commits': 0, 'commit_hours': [], 'weekend_commits': 0, 'total_commits_checked': 0, 'orphan_branches': [], 'commit_words': [], 'commit_lengths': [], 'commit_emojis': [], 'age_days': 0, 'activity_7d': [0]*7}
    try:
        for i in range(7):
            day_start = (datetime.now() - timedelta(days=i+1)).strftime("%Y-%m-%d")
            day_end = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            out = subprocess.check_output(['git', 'log', f'--after={day_start}', f'--before={day_end}', '--oneline'], cwd=dir_path, stderr=subprocess.DEVNULL).decode('utf-8')
            analytics['activity_7d'][6-i] = len([l for l in out.split('\n') if l.strip()])
        
        analytics['recent_commits'] = sum(analytics['activity_7d'])
        log_out = subprocess.check_output(['git', 'log', '-n', '100', '--format=%aI|%s'], cwd=dir_path, stderr=subprocess.DEVNULL).decode('utf-8')
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
        
        for line in log_out.split('\n'):
            if '|' in line:
                analytics['total_commits_checked'] += 1
                iso_date, msg = line.split('|', 1)
                analytics['commit_lengths'].append(len(msg.split()))
                try:
                    dt = datetime.fromisoformat(iso_date)
                    analytics['commit_hours'].append(dt.hour)
                    if dt.weekday() >= 5: analytics['weekend_commits'] += 1
                except: pass
                analytics['commit_emojis'].extend(emoji_pattern.findall(msg))
                    
        branches_out = subprocess.check_output(['git', 'for-each-ref', '--format=%(refname:short)|%(committerdate:unix)', 'refs/heads/'], cwd=dir_path, stderr=subprocess.DEVNULL).decode('utf-8')
        six_months_ago = int((datetime.now() - timedelta(days=180)).timestamp())
        for line in branches_out.split('\n'):
            if '|' in line:
                b_name, ts = line.split('|')
                if ts.strip().isdigit() and int(ts) < six_months_ago: analytics['orphan_branches'].append(b_name.strip())
                    
        first_commit = subprocess.check_output(['git', 'log', '--reverse', '--format=%aI'], cwd=dir_path, stderr=subprocess.DEVNULL).decode('utf-8').split('\n')[0]
        if first_commit:
            dt = datetime.fromisoformat(first_commit)
            analytics['age_days'] = (datetime.now(dt.tzinfo) - dt).days
    except: pass
    return analytics

def calculate_health(p):
    score = 100
    if p.get('env_exposed'): score -= 40
    if not p.get('is_git'): score -= 20
    if not p.get('has_license'): score -= 10
    if p.get('unpushed', 0) > 0: score -= 10
    if p.get('tech_debt_count', 0) > 10: score -= 10
    return max(0, score)

def scan_for_projects(current_dir, depth):
    if depth > MAX_DEPTH: return []
    projects = []
    try: entries = os.listdir(current_dir)
    except PermissionError: return []
        
    is_git = '.git' in entries and os.path.isdir(os.path.join(current_dir, '.git'))
    is_non_git_project = not is_git and any(marker in entries for marker in PROJECT_MARKERS)
    
    if is_git or is_non_git_project:
        res = get_project_stats(current_dir, is_git)
        loc_by_lang, total_loc, last_mtime, largest_file, tech_debt_count, extracted_todos, dependencies, has_license, env_exposed, proj_type, keywords, readme_words, naming = res
        
        status_info = {
            'path': current_dir, 'is_git': is_git, 'total_loc': total_loc, 'loc_breakdown': dict(loc_by_lang), 'last_modified': last_mtime, 'largest_file': largest_file, 'tech_debt_count': tech_debt_count, 'dependencies': dependencies, 'has_license': has_license, 'env_exposed': env_exposed, 'proj_type': proj_type, 'keywords': dict(keywords), 'readme_words': readme_words, 'naming': naming
        }
        
        if is_git:
            git_analytics = get_git_analytics(current_dir)
            try:
                branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=current_dir, stderr=subprocess.DEVNULL).decode('utf-8').strip()
                status_out = subprocess.check_output(['git', 'status', '--porcelain'], cwd=current_dir, stderr=subprocess.DEVNULL).decode('utf-8')
                uncommitted = len([line for line in status_out.split('\n') if line.strip()])
                remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], cwd=current_dir, stderr=subprocess.DEVNULL).decode('utf-8').strip()
                unpushed = 0
                if branch and remote_url:
                    unpushed_out = subprocess.check_output(['git', 'rev-list', f'HEAD...origin/{branch}', '--count'], cwd=current_dir, stderr=subprocess.DEVNULL).decode('utf-8').strip()
                    unpushed = int(unpushed_out) if unpushed_out.isdigit() else 0
                status_info.update({'branch': branch, 'uncommitted': uncommitted, 'unpushed': unpushed, 'remote_url': remote_url})
            except: pass
            status_info.update(git_analytics)
            
        status_info['health'] = calculate_health(status_info)
        return [status_info]

    for entry in entries:
        if entry in SKIP_DIRS or entry.startswith('.'): continue
        full_path = os.path.join(current_dir, entry)
        if os.path.isdir(full_path): projects.extend(scan_for_projects(full_path, depth + 1))
    return projects

def main():
    print(f"🔍 Deep Scanning {ROOT_DIR} (Depth {MAX_DEPTH})...")
    projects = scan_for_projects(ROOT_DIR, 0)
    
    total_loc = sum(p['total_loc'] for p in projects)
    global_langs = defaultdict(int)
    global_keywords = Counter()
    global_commit_lengths = []
    global_naming = {"camel": 0, "snake": 0}
    quick_wins = []
    today = datetime.now().date()
    files_today = []

    # Local Network Detection
    project_names = {os.path.basename(p['path']) for p in projects}
    for p in projects:
        p['internal_deps'] = [d for d in p['dependencies'] if d in project_names]
        global_naming["camel"] += p['naming']["camel"]
        global_naming["snake"] += p['naming']["snake"]
        global_commit_lengths.extend(p.get('commit_lengths', []))
        global_keywords.update(p.get('keywords', {}))
        for l, count in p['loc_breakdown'].items(): global_langs[l] += count
        
        rel = os.path.relpath(p['path'], ROOT_DIR)
        if p.get('env_exposed'): quick_wins.append(f"🔒 **Security**: Secure `.env` in `{rel}`")
        if p.get('uncommitted', 0) > 15: quick_wins.append(f"📦 **Git**: Commit {p['uncommitted']} files in `{rel}`")
        if not p.get('has_license'): quick_wins.append(f"📜 **Docs**: Add LICENSE to `{rel}`")
        
        m_date = datetime.fromtimestamp(p['last_modified']).date()
        if m_date == today: files_today.append(p)

    # Coding Persona & Vibe
    naming_vibe = "Pascal/CamelCase Architect" if global_naming["camel"] > global_naming["snake"] else "Snake_Case Pragmatist"
    avg_commit_len = sum(global_commit_lengths)/len(global_commit_lengths) if global_commit_lengths else 0
    coding_persona = "Punchy Vibe-Coder" if avg_commit_len < 6 else "Deep Systems Engineer"
    
    # Export
    with open('PORTFOLIO_DATA.json', 'w') as f: json.dump({"generated_at": datetime.now().isoformat(), "projects": projects}, f, indent=2)

    # Markdown
    md = [
        "Hi, I'm Paranjay 👋",
        "===================",
        "",
        "📍 Developer | 🤖 Tinker | 🚀 Code Explorer",
        "",
        "### ⚡ The " + coding_persona + "'s Quick Wins",
        "  \n".join(quick_wins[:5]) if quick_wins else "✨ All projects are in elite shape!",
        "",
        "### 📊 Ideaverse Intelligence",
        f"- **Total Projects Discovered**: {len(projects)}",
        f"- **Naming Signature**: `{naming_vibe}`",
        f"- **Machine Weight**: {total_loc:,} LOC across {len(global_langs)} languages",
        f"- **Communication Score**: {sum(p.get('readme_words', 0) for p in projects):,} words of documentation",
        f"- **Internal Network**: {sum(len(p.get('internal_deps', [])) for p in projects)} local cross-project links detected",
        "",
        "#### 🧬 Core Language DNA",
        "\n".join([f"`{l.ljust(12)} { (count/total_loc*100):4.1f}% ({count:,} LOC)`" for l, count in sorted(global_langs.items(), key=lambda x:-x[1])[:8]]),
        "",
        "---",
        "",
        "### 🟢 Active Orbit Dashboard",
        "| Project | Health | Pulse (7d) | Internal Links | Tech Debt | Last Modified |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    for p in sorted(projects, key=lambda x: -x['last_modified'])[:15]:
        if (time.time() - p['last_modified']) > 30*24*3600: continue
        rel = os.path.relpath(p['path'], ROOT_DIR)
        spark = get_sparkline(p.get('activity_7d', [0]*7))
        h_color = "🟢" if p['health'] > 85 else "🟡" if p['health'] > 60 else "🔴"
        links = f"🔗 {len(p['internal_deps'])}" if p['internal_deps'] else "—"
        debt = f"🔨 {p['tech_debt_count']}" if p['tech_debt_count'] > 0 else "✨ Clean"
        mod = datetime.fromtimestamp(p['last_modified']).strftime('%Y-%m-%d %H:%M')
        md.append(f"| **{rel}** | {h_color} {p['health']}% | `{spark}` | {links} | {debt} | {mod} |")

    with open('PORTFOLIO_DASHBOARD.md', 'w') as f: f.write("\n".join(md))
    print("✅ 100% Saturation Reached. Dashboard updated!")

if __name__ == '__main__': main()
