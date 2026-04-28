import os
import subprocess
import time
import json
import re
import math
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
    """Generates a 7-day sparkline."""
    chars = " ▂▃▄▅▆▇█"
    if not counts: return ""
    max_count = max(counts)
    if max_count == 0: return "       "
    return "".join(chars[int(c * (len(chars)-1) / max_count)] for c in counts)

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
    keywords = Counter()
    readme_word_count = 0
    
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
            
            if f.lower() == 'readme.md':
                try:
                    with open(full_path, 'r', errors='ignore') as rf:
                        readme_word_count = len(rf.read().split())
                except: pass

            if f == '.env' and is_git:
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
                                # Keywords (inspired by WordCounter)
                                words = re.findall(r'\b[a-zA-Z]{4,15}\b', line_str)
                                for w in words:
                                    if w.lower() in {'async', 'await', 'export', 'import', 'const', 'function', 'interface', 'class', 'return'}:
                                        keywords[w.lower()] += 1

                                # Tech Debt
                                upper_line = line_str.upper()
                                if "TODO:" in upper_line or "FIXME:" in upper_line or "HACK:" in upper_line:
                                    tech_debt_count += 1
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
    return loc_by_lang, total_loc, latest_mtime, largest_file, tech_debt_count, extracted_todos, dependencies, has_license, env_exposed, proj_type, keywords, readme_word_count

def get_git_analytics(dir_path):
    analytics = {
        'recent_commits': 0,
        'commit_hours': [],
        'weekend_commits': 0,
        'total_commits_checked': 0,
        'orphan_branches': [],
        'commit_words': [],
        'commit_lengths': [],
        'commit_emojis': [],
        'age_days': 0,
        'activity_7d': [0]*7
    }
    try:
        # 7-day activity sparkline data
        for i in range(7):
            day_start = (datetime.now() - timedelta(days=i+1)).strftime("%Y-%m-%d")
            day_end = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            out = subprocess.check_output(
                ['git', 'log', f'--after={day_start}', f'--before={day_end}', '--oneline'], 
                cwd=dir_path, stderr=subprocess.DEVNULL
            ).decode('utf-8')
            analytics['activity_7d'][6-i] = len([l for l in out.split('\n') if l.strip()])
        
        analytics['recent_commits'] = sum(analytics['activity_7d'])
        
        # Habits & Emojis
        log_out = subprocess.check_output(
            ['git', 'log', '-n', '100', '--format=%aI|%s'], 
            cwd=dir_path, stderr=subprocess.DEVNULL
        ).decode('utf-8')
        
        stopwords = {'merge', 'branch', 'into', 'and', 'the', 'to', 'for', 'a', 'in', 'of', 'fix', 'update', 'add', 'added'}
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
        
        for line in log_out.split('\n'):
            if '|' in line:
                analytics['total_commits_checked'] += 1
                iso_date, msg = line.split('|', 1)
                
                # Length Analysis (Sentence Length Vibe)
                words = msg.split()
                analytics['commit_lengths'].append(len(words))
                
                try:
                    dt = datetime.fromisoformat(iso_date)
                    analytics['commit_hours'].append(dt.hour)
                    if dt.weekday() >= 5:
                        analytics['weekend_commits'] += 1
                except: pass
                    
                msg_words = re.findall(r'\b[a-zA-Z]{3,}\b', msg.lower())
                analytics['commit_words'].extend([w for w in msg_words if w not in stopwords])
                
                emojis_found = emoji_pattern.findall(msg)
                if emojis_found:
                    analytics['commit_emojis'].extend(emojis_found)
                    
        # Branches & Age
        branches_out = subprocess.check_output(
            ['git', 'for-each-ref', '--format=%(refname:short)|%(committerdate:unix)', 'refs/heads/'], 
            cwd=dir_path, stderr=subprocess.DEVNULL
        ).decode('utf-8')
        six_months_ago = int((datetime.now() - timedelta(days=180)).timestamp())
        for line in branches_out.split('\n'):
            if '|' in line:
                b_name, ts = line.split('|')
                if ts.strip().isdigit() and int(ts) < six_months_ago:
                    analytics['orphan_branches'].append(b_name.strip())
                    
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
    try:
        entries = os.listdir(current_dir)
    except PermissionError: return []
        
    is_git = '.git' in entries and os.path.isdir(os.path.join(current_dir, '.git'))
    is_non_git_project = not is_git and any(marker in entries for marker in PROJECT_MARKERS)
    
    if is_git or is_non_git_project:
        res = get_project_stats(current_dir, is_git)
        loc_by_lang, total_loc, last_mtime, largest_file, tech_debt_count, extracted_todos, dependencies, has_license, env_exposed, proj_type, keywords, readme_words = res
        
        status_info = {
            'path': current_dir, 'is_git': is_git, 'total_loc': total_loc,
            'loc_breakdown': dict(loc_by_lang), 'last_modified': last_mtime,
            'largest_file': largest_file, 'tech_debt_count': tech_debt_count,
            'todos_sample': extracted_todos, 'dependencies': dependencies,
            'has_license': has_license, 'env_exposed': env_exposed,
            'proj_type': proj_type, 'keywords': dict(keywords), 'readme_words': readme_words
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
        if os.path.isdir(full_path):
            projects.extend(scan_for_projects(full_path, depth + 1))
    return projects

def main():
    print(f"🔍 Scanning {ROOT_DIR} (Depth {MAX_DEPTH})...")
    projects = scan_for_projects(ROOT_DIR, 0)
    
    total_loc = sum(p['total_loc'] for p in projects)
    total_uncommitted = sum(p.get('uncommitted', 0) for p in projects)
    total_7d_commits = sum(p.get('recent_commits', 0) for p in projects)
    total_tech_debt = sum(p.get('tech_debt_count', 0) for p in projects)
    
    global_langs = defaultdict(int)
    global_keywords = Counter()
    global_commit_lengths = []
    global_emojis = Counter()
    quick_wins = []

    for p in projects:
        for l, count in p['loc_breakdown'].items(): global_langs[l] += count
        global_keywords.update(p.get('keywords', {}))
        global_commit_lengths.extend(p.get('commit_lengths', []))
        global_emojis.update(p.get('commit_emojis', []))
        
        # Identify Quick Wins
        rel = os.path.relpath(p['path'], ROOT_DIR)
        if p.get('env_exposed'): quick_wins.append(f"🔒 **Security**: Add `.env` to `.gitignore` in `{rel}`")
        if p.get('uncommitted', 0) > 10: quick_wins.append(f"📦 **Git**: Commit {p['uncommitted']} pending files in `{rel}`")
        if not p.get('has_license'): quick_wins.append(f"📜 **Docs**: Add a LICENSE file to `{rel}`")

    # Metrics
    avg_commit_len = sum(global_commit_lengths)/len(global_commit_lengths) if global_commit_lengths else 0
    coding_vibe = "Detailed Engineer" if avg_commit_len > 6 else "Punchy Vibe-Coder"

    # Export JSON
    with open('PORTFOLIO_DATA.json', 'w') as f:
        json.dump({"generated_at": datetime.now().isoformat(), "projects": projects}, f, indent=2)

    # Generate Markdown
    md = [
        "Hi, I'm Paranjay 👋",
        "===================",
        "",
        "📍 Developer | 🤖 Tinker | 🚀 Code Explorer",
        "",
        "### ⚡ Quick Wins (Actionable Insights)",
        "  \n".join(quick_wins[:5]) if quick_wins else "✨ All projects are in great shape!",
        "",
        "### 📊 Machine Intelligence",
        f"- **Total Projects**: {len(projects)} | **Total LOC**: {total_loc:,}",
        f"- **Unsaved Changes**: {total_uncommitted} files | **7-Day Pulse**: {total_7d_commits} commits",
        f"- **Coding Persona**: `{coding_vibe}` (Avg Commit: {avg_commit_len:.1f} words)",
        f"- **Top Keywords**: " + ", ".join([f"`{k}`" for k, _ in global_keywords.most_common(5)]),
        f"- **Favorite Emojis**: " + " ".join([k for k, _ in global_emojis.most_common(5)]),
        "",
        "#### 🧬 Language DNA Breakdown",
        "\n".join([f"`{l.ljust(12)} { (count/total_loc*100):4.1f}% ({count:,} LOC)`" for l, count in sorted(global_langs.items(), key=lambda x:-x[1])[:8]]),
        "",
        "---",
        "",
        "### 🟢 Active Orbit Dashboard",
        "| Project | Health | Pulse (7d) | Risk | Tech Debt | Top Languages |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    for p in sorted(projects, key=lambda x: -x['last_modified'])[:15]:
        if (time.time() - p['last_modified']) > 30*24*3600: continue
        rel = os.path.relpath(p['path'], ROOT_DIR)
        spark = get_sparkline(p.get('activity_7d', [0]*7))
        h_color = "🟢" if p['health'] > 80 else "🟡" if p['health'] > 50 else "🔴"
        risk = "🔥 CRITICAL" if p.get('env_exposed') else "🔴 High" if p.get('uncommitted', 0) > 20 else "🟢 Safe"
        debt = f"🔨 {p['tech_debt_count']}" if p['tech_debt_count'] > 0 else "✨ Clean"
        langs = "<br>".join([f"**{l}**: {c:,}" for l, c in sorted(p['loc_breakdown'].items(), key=lambda x:-x[1])[:2]])
        md.append(f"| **{rel}** | {h_color} {p['health']}% | `{spark}` | {risk} | {debt} | {langs} |")

    with open('PORTFOLIO_DASHBOARD.md', 'w') as f:
        f.write("\n".join(md))
    print("✅ Dashboard updated!")

if __name__ == '__main__':
    main()
