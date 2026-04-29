import os
import subprocess
import time
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter

def find_all_repos():
    home = os.path.expanduser('~')
    print(f"📡 Initializing Global Search across {home}...")
    repos = []
    
    # Aggressive skip list for performance and safety
    skip_set = {
        'Library', 'Pictures', 'Music', 'Movies', 'Public', '.Trash', 
        'node_modules', '.next', '.cache', 'venv', '.venv', 'dist', 'build'
    }
    
    for root, dirs, files in os.walk(home, topdown=True):
        # Skip system junk but KEEP .git for discovery
        dirs[:] = [d for d in dirs if d not in skip_set and (not d.startswith('.') or d == '.git')]
        
        if '.git' in dirs:
            repos.append(root)
            # Prune: don't search inside found repos
            if '.git' in dirs: dirs.remove('.git')
            
    print(f"✅ Discovered {len(repos)} independent orbits.")
    return repos

SCAN_DIRS = find_all_repos()
MAX_DEPTH = 20 # Maximum Saturation Depth

SKIP_DIRS = {
    'Library', 'Applications', 'Pictures', 'Music', 'Movies', '.Trash', 
    'node_modules', '.venv', 'venv', 'env', 'site-packages', 'build', 
    'dist', '.vscode', '.next', '.cache', 'Public', 'opt', 'Pods', 'vendor',
    'target', 'out', '__pycache__', '.gradle', '.idea', '.terraform', '.git'
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

def get_narrative(proj_type, keywords, total_loc):
    main_keys = [k for k in keywords.keys() if k not in {'import', 'export', 'const', 'async', 'await'}][:3]
    vibe = "Unknown Identity"
    if not main_keys: main_keys = ["Logic", "Data", "Source"]
    
    if 'web app' in proj_type.lower():
        vibe = f"A digital interface focused on {', '.join(main_keys)}."
    elif 'extension' in proj_type.lower():
        vibe = f"A browser-level utility orchestrating {', '.join(main_keys)} workflows."
    elif 'python' in proj_type.lower() or 'script' in proj_type.lower():
        vibe = f"An automation engine built for {', '.join(main_keys)} tasks."
    else:
        vibe = f"A technical workspace centered on {', '.join(main_keys)} architecture."
    
    if total_loc > 10000:
        vibe = "High-complexity " + vibe.lower()
    return vibe

def suggest_tool(loc_breakdown, tech_debt):
    if 'Python' in loc_breakdown: return "Ruff (Fast Linting)"
    if 'TypeScript' in loc_breakdown or 'React TS' in loc_breakdown:
        if tech_debt > 10: return "Knip (Unused Code)"
        return "ESLint + Prettier"
    if 'CSS' in loc_breakdown: return "Tailwind Config Viewer"
    return "Sentry (Monitoring)"

def get_project_stats(project_path, is_git):
    loc_by_lang = defaultdict(int)
    total_loc = 0
    last_mtime = 0
    largest_file = {"path": "", "loc": 0}
    tech_debt_count = 0
    dependencies = []
    has_license = False
    env_exposed = False
    keywords = Counter()
    readme_words = 0
    naming = {'camel': 0, 'snake': 0}
    preview_image = None

    is_web = os.path.exists(os.path.join(project_path, 'package.json'))
    is_next = os.path.exists(os.path.join(project_path, 'next.config.js')) or os.path.exists(os.path.join(project_path, 'next.config.mjs'))
    is_ext = 'extension' in project_path.lower() or os.path.exists(os.path.join(project_path, 'manifest.json'))
    
    proj_type = "Script"
    if is_next: proj_type = "Web App (Next.js)"
    elif is_web: proj_type = "Web App"
    elif is_ext: proj_type = "Browser Extension"
    
    ignored_patterns = set()
    gitignore_path = os.path.join(project_path, '.gitignore')
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, 'r') as f:
                ignored_patterns = {line.strip() for line in f if line.strip() and not line.startswith('#')}
        except: pass

    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        
        for f in files:
            full_path = os.path.join(root, f)
            
            # Preview Image Detection (First suitable image)
            if not preview_image and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                if any(x in f.lower() for x in ['screenshot', 'banner', 'logo', 'preview', 'cover']):
                    preview_image = full_path

            if f.lower() in ['license', 'license.md', 'license.txt']: has_license = True
            
            if f.lower() == 'readme.md':
                try:
                    with open(full_path, 'r', errors='ignore') as rf:
                        readme_words = len(rf.read().split())
                except: pass

            if f == '.env' and is_git:
                if '.env' not in ignored_patterns: env_exposed = True

            if f == 'package.json':
                try:
                    with open(full_path, 'r') as pjf:
                        data = json.load(pjf)
                        dependencies.extend(list(data.get('dependencies', {}).keys()))
                        dependencies.extend(list(data.get('devDependencies', {}).keys()))
                except: pass
            elif f == 'requirements.txt' or f == 'pyproject.toml':
                proj_type = "Python Tool"
            elif f == 'manifest.json': proj_type = "Browser Extension"
                
            ext = os.path.splitext(f)[1].lower()
            if ext in CODE_EXTENSIONS:
                try:
                    # Skip massive files
                    if os.path.getsize(full_path) > 1024 * 1024: continue
                    
                    mtime = os.path.getmtime(full_path)
                    if mtime > last_mtime: last_mtime = mtime
                    
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                        lines = content.count('\n')
                        loc_by_lang[CODE_EXTENSIONS[ext]] += lines
                        
                        c, s = analyze_naming_vibe(content)
                        naming["camel"] += c
                        naming["snake"] += s
                        
                        words = re.findall(r'\b[a-zA-Z]{4,15}\b', content)
                        for w in words:
                            if w.lower() not in {'async', 'await', 'export', 'import', 'const', 'function', 'interface', 'class', 'return'}:
                                keywords[w.lower()] += 1

                        if any(x in content.upper() for x in ["TODO:", "FIXME:", "HACK:"]):
                            tech_debt_count += 1
                                    
                        if lines > largest_file["loc"]:
                            largest_file = {"path": full_path, "loc": lines}
                except: pass
                    
    total_loc = sum(loc_by_lang.values())
    narrative = get_narrative(proj_type, keywords, total_loc)
    suggested_tool = suggest_tool(loc_by_lang, tech_debt_count)
    
    # Internal Dependency Detection
    project_names = [os.path.basename(p) for p in SCAN_DIRS] # Simplified
    internal_deps = []
    
    # We'll populate this in a second pass in main()
    
    return {
        "loc_breakdown": dict(loc_by_lang),
        "total_loc": total_loc,
        "last_modified": last_mtime,
        "largest_file": largest_file,
        "tech_debt_count": tech_debt_count,
        "dependencies": list(set(dependencies)),
        "has_license": has_license,
        "env_exposed": env_exposed,
        "proj_type": proj_type,
        "keywords": dict(keywords.most_common(10)),
        "readme_words": readme_words,
        "naming": naming,
        "narrative": narrative,
        "suggested_tool": suggested_tool,
        "preview_image": os.path.basename(preview_image) if preview_image else None,
        "full_preview_path": preview_image,
        "internal_deps": [] # To be filled
    }

def get_git_analytics(dir_path):
    analytics = {
        'recent_commits': 0, 
        'activity_7d': [0]*7, 
        'commit_lengths': [],
        'unpushed': 0,
        'uncommitted': 0
    }
    try:
        # Activity
        for i in range(7):
            day_start = (datetime.now() - timedelta(days=i+1)).strftime("%Y-%m-%d")
            day_end = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            out = subprocess.check_output(['git', 'log', f'--after={day_start}', f'--before={day_end}', '--oneline'], cwd=dir_path, stderr=subprocess.DEVNULL).decode('utf-8')
            analytics['activity_7d'][6-i] = len([l for l in out.split('\n') if l.strip()])
        
        analytics['recent_commits'] = sum(analytics['activity_7d'])
        
        # Commit lengths
        log_out = subprocess.check_output(['git', 'log', '-n', '50', '--format=%s'], cwd=dir_path, stderr=subprocess.DEVNULL).decode('utf-8')
        for msg in log_out.split('\n'):
            if msg.strip(): analytics['commit_lengths'].append(len(msg.split()))

        # Unpushed
        try:
            unpushed_out = subprocess.check_output(['git', 'log', '@{u}..', '--oneline'], cwd=dir_path, stderr=subprocess.DEVNULL).decode('utf-8')
            analytics['unpushed'] = len([l for l in unpushed_out.split('\n') if l.strip()])
        except: pass

        # Uncommitted
        status_out = subprocess.check_output(['git', 'status', '--porcelain'], cwd=dir_path, stderr=subprocess.DEVNULL).decode('utf-8')
        analytics['uncommitted'] = len([l for l in status_out.split('\n') if l.strip()])

    except: pass
    return analytics

def calculate_health(p):
    score = 100
    if p.get('env_exposed'): score -= 40
    if not p.get('is_git'): score -= 20
    if not p.get('has_license'): score -= 10
    if p.get('unpushed', 0) > 0: score -= 15
    if p.get('uncommitted', 0) > 0: score -= 10
    if p.get('tech_debt_count', 0) > 10: score -= 10
    return max(0, score)

def scan_for_projects(current_dir, depth):
    if depth > MAX_DEPTH: return []
    projects = []
    try: entries = os.listdir(current_dir)
    except: return []
        
    is_git = '.git' in entries and os.path.isdir(os.path.join(current_dir, '.git'))
    is_non_git_project = not is_git and any(marker in entries for marker in PROJECT_MARKERS)
    
    # Don't process the scan root itself as a project if it's in SCAN_DIRS
    is_root = current_dir in SCAN_DIRS
    
    if (is_git or is_non_git_project) and not is_root:
        print(f"    - Processing: {current_dir}")
        stats = get_project_stats(current_dir, is_git)
        stats.update({'path': current_dir, 'is_git': is_git})
        
        if is_git:
            git_analytics = get_git_analytics(current_dir)
            try:
                branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=current_dir, stderr=subprocess.DEVNULL).decode('utf-8').strip()
                stats.update({'branch': branch})
            except: pass
            stats.update(git_analytics)
            
        stats['health'] = calculate_health(stats)
        if stats['total_loc'] > 0 or is_git:
            projects.append(stats)
        
        # If it's a git repo, don't look for nested projects inside it
        if is_git: return projects

    for entry in entries:
        if entry in SKIP_DIRS or entry.startswith('.'): continue
        full_path = os.path.join(current_dir, entry)
        if os.path.isdir(full_path):
            projects.extend(scan_for_projects(full_path, depth + 1))
    return projects

def main():
    all_projects = []
    print(f"🔍 Deep Scanning {len(SCAN_DIRS)} high-value orbits...")
    for target in SCAN_DIRS:
        print(f"  -> Auditing: {target}")
        all_projects.extend(scan_for_projects(target, 0))
    
    # Second Pass: Map Internal Dependencies
    proj_names = {os.path.basename(p['path']): p['path'] for p in all_projects}
    for p in all_projects:
        for name in proj_names:
            if name != os.path.basename(p['path']):
                if name.lower() in p['path'].lower() or any(name.lower() in dep.lower() for dep in p['dependencies']):
                    p['internal_deps'].append(name)
    
    # --- Markdown Generation (High Fidelity) ---
    md_content = f"# Ideaverse Dashboard ({datetime.now().strftime('%Y-%m-%d')})\n\n"
    
    # Core Language DNA
    global_loc = {}
    for p in all_projects:
        for lang, loc in p['loc_breakdown'].items():
            global_loc[lang] = global_loc.get(lang, 0) + loc
    
    total_global_loc = sum(global_loc.values())
    sorted_loc = sorted(global_loc.items(), key=lambda x: x[1], reverse=True)
    
    md_content += "### 🧬 Core Language DNA\n\n"
    md_content += "| Language | Percent | Total LOC |\n"
    md_content += "| :--- | :--- | :--- |\n"
    for lang, loc in sorted_loc[:8]:
        perc = (loc / total_global_loc) * 100
        md_content += f"| {lang} | {perc:.1f}% | {loc:,} |\n"
    md_content += "\n---\n\n"
    
    # Active Orbit Dashboard
    md_content += "### 🟢 Active Orbit Dashboard\n\n"
    md_content += "| Project | Health | Pulse (7d) | Naming | Commits | Pending | Last Modified |\n"
    md_content += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    
    for p in sorted(all_projects, key=lambda x: x['last_modified'], reverse=True):
        name = os.path.basename(p['path'])
        health_emoji = "🟢" if p['health'] > 85 else "🟡" if p['health'] > 60 else "🔴"
        
        # Simple Pulse representation
        pulse = "".join(["█" if c > 0 else "░" for c in p.get('activity_7d', [0]*7)])
        
        naming_vibe = "🐫 Camel" if p['naming']['camel'] > p['naming']['snake'] else "🐍 Snake"
        recent = p.get('recent_commits', 0)
        pending = f"🟠 {p.get('unpushed', 0)}↑ 🟡 {p.get('uncommitted', 0)}±"
        last_mod = datetime.fromtimestamp(p['last_modified']).strftime('%Y-%m-%d %H:%M')
        
        md_content += f"| **{name}**<br><small>{p['narrative']}</small> | {health_emoji} {p['health']}% | `{pulse}` | {naming_vibe} | {recent} | {pending} | {last_mod} |\n"
    
    # Global Stats
    global_langs = Counter()
    total_ecosystem_loc = 0
    
    for p in all_projects:
        total_ecosystem_loc += p['total_loc']
        for lang, loc in p['loc_breakdown'].items():
            global_langs[lang] += loc

    # Normalize Langs for Portfolio Matrix
    skills_matrix = {lang: (loc/total_ecosystem_loc)*100 for lang, loc in global_langs.items() if (loc/total_ecosystem_loc) > 0.01}
    
    # Sort Skills by proficiency
    skills_matrix = dict(sorted(skills_matrix.items(), key=lambda item: item[1], reverse=True))

    all_stats = {
        "generated_at": datetime.now().isoformat(),
        "total_projects": len(all_projects),
        "total_loc": total_ecosystem_loc,
        "skills_matrix": skills_matrix,
        "projects": all_projects
    }
    
    with open('lab/PORTFOLIO_DASHBOARD.md', 'w') as f:
        f.write(report)
        
    with open('lab/PORTFOLIO_DATA.json', 'w') as f:
        json.dump(all_stats, f, indent=2)

if __name__ == '__main__': main()
