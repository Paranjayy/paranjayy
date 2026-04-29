import fs from 'fs/promises';
import path from 'path';
import { exec } from 'child_process';
import util from 'util';

const execAsync = util.promisify(exec);

const ROOT_DIR = '/Users/paranjay/Downloads/2work/dev';

async function findGitRepos(dir, depth = 0, maxDepth = 3) {
  if (depth > maxDepth) return [];
  let repos = [];
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    
    // Check if current dir is a git repo
    if (entries.some(e => e.isDirectory() && e.name === '.git')) {
      return [dir];
    }

    for (const entry of entries) {
      if (entry.isDirectory() && entry.name !== 'node_modules' && !entry.name.startsWith('.')) {
        const subRepos = await findGitRepos(path.join(dir, entry.name), depth + 1, maxDepth);
        repos = repos.concat(subRepos);
      }
    }
  } catch (err) {
    // ignore access errors
  }
  return repos;
}

async function getRepoStatus(repoPath) {
  const result = {
    path: repoPath.replace(ROOT_DIR, '').replace(/^\//, '') || 'dev',
    branch: '',
    uncommitted: 0,
    unpushed: 0,
    remoteUrl: '',
    error: null
  };

  try {
    // Get branch
    const { stdout: branchOut } = await execAsync('git rev-parse --abbrev-ref HEAD', { cwd: repoPath }).catch(() => ({ stdout: ''}));
    result.branch = branchOut.trim();

    // Get uncommitted changes
    const { stdout: statusOut } = await execAsync('git status --porcelain', { cwd: repoPath }).catch(() => ({ stdout: ''}));
    result.uncommitted = statusOut.split('\n').filter(line => line.trim().length > 0).length;

    // Get remote URL
    const { stdout: remoteOut } = await execAsync('git config --get remote.origin.url', { cwd: repoPath }).catch(() => ({ stdout: ''}));
    result.remoteUrl = remoteOut.trim();

    // Get unpushed commits
    if (result.branch && result.remoteUrl) {
      const { stdout: unpushedOut } = await execAsync(`git rev-list HEAD...origin/${result.branch} --count`, { cwd: repoPath }).catch(() => ({ stdout: '0' }));
      result.unpushed = parseInt(unpushedOut.trim(), 10) || 0;
    }
  } catch (e) {
    result.error = e.message;
  }

  return result;
}

async function main() {
  console.log('🔍 Scanning for git repositories...');
  const repos = await findGitRepos(ROOT_DIR);
  console.log(`Found ${repos.length} repositories. Checking status...`);

  const stats = [];
  for (const repo of repos) {
    stats.push(await getRepoStatus(repo));
  }

  // Sort by uncommitted changes, then unpushed, then name
  stats.sort((a, b) => {
    if (b.uncommitted !== a.uncommitted) return b.uncommitted - a.uncommitted;
    if (b.unpushed !== a.unpushed) return b.unpushed - a.unpushed;
    return a.path.localeCompare(b.path);
  });

  const readmeContent = `
Hi, I'm Paranjay 👋
===================

📍 Developer | 🤖 AI Enthusiast | 🚀 Tinkerer

Currently experimenting, vibe-coding, and orchestrating ideas across multiple domains.

### 🛠️ Current Status & Active Orchestration
*A unified dashboard to monitor project sync states, preventing data loss and keeping ideas consolidated.*

| Repository | Branch | Remote | Status |
| :--- | :--- | :--- | :--- |
${stats.map(s => {
    let statusStr = '✅ Clean & Synced';
    if (s.uncommitted > 0 && s.unpushed > 0) {
      statusStr = \`⚠️ \${s.uncommitted} uncommitted, \${s.unpushed} unpushed\`;
    } else if (s.uncommitted > 0) {
      statusStr = \`📝 \${s.uncommitted} uncommitted changes\`;
    } else if (s.unpushed > 0) {
      statusStr = \`⬆️ \${s.unpushed} commits ahead of remote\`;
    } else if (!s.remoteUrl) {
      statusStr = \`🌐 No remote set (Local only)\`;
    }

    const remoteLink = s.remoteUrl ? (s.remoteUrl.startsWith('http') ? \`[origin](\${s.remoteUrl.replace('.git', '')})\` : \`[origin](\${s.remoteUrl})\`) : 'None';
    
    return \`| **\${s.path}** | \`\${s.branch || 'None'}\` | \${remoteLink} | \${statusStr} |\`;
  }).join('\n')}

---

### 🎨 The Aesthetic / Portfolio Idea
*(Draft based on modern profiles - inspired by steipete)*

**Tech Stack**: \`TypeScript\` \`React\` \`Node.js\` \`Python\` \`AI Agents\`

**Recent Highlights**:
- 🌌 **The Ideaverse Portfolio**: Modernizing scholarly portfolios with high-end aesthetic.
- 🎮 **Gravity Hub**: IFTTT Gaming integrations for Windows to Mac telemetry.
- ⚡ **Webdev Toolbox**: Powerful developer extensions built for God mode.
- 🏰 **Gemini Design Palace**: Unslopified, premium reactive UI systems.

> *“Ship beats perfect. But if it doesn’t look like Stripe Press, is it even worth shipping?”*
`;

  await fs.writeFile(path.join(process.cwd(), 'PORTFOLIO_DASHBOARD.md'), readmeContent.trim());
  console.log('✅ Wrote PORTFOLIO_DASHBOARD.md!');
}

main().catch(console.error);
