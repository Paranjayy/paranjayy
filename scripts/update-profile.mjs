import fs from 'fs/promises';
import path from 'path';

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const USERNAME = 'paranjayy';
const HEADERS = {
  Accept: 'application/vnd.github.v3+json',
  ...(GITHUB_TOKEN ? { Authorization: `token ${GITHUB_TOKEN}` } : {}),
};

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function fetchJSON(url, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const res = await fetch(url, { headers: HEADERS });
      if (res.status === 403 || res.status === 429 || res.status === 504) {
        const reset = res.headers.get('x-ratelimit-reset');
        const waitMs = reset
          ? Math.max(0, Number(reset) * 1000 - Date.now()) + 1000
          : 2000 * (i + 1);
        console.log(`Rate limited (${res.status}), waiting ${waitMs}ms...`);
        await sleep(Math.min(waitMs, 10000));
        continue;
      }
      if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
      return await res.json();
    } catch (err) {
      if (i === retries - 1) throw err;
      await sleep(1000 * (i + 1));
    }
  }
}

async function getRecentlyUpdatedRepos() {
  try {
    const data = await fetchJSON(
      `https://api.github.com/users/${USERNAME}/repos?sort=pushed&per_page=10`
    );
    return data
      .filter((r) => !r.fork && r.description)
      .slice(0, 5)
      .map((r) => ({
        name: r.name,
        url: r.html_url,
        description: r.description,
      }));
  } catch (err) {
    console.error('Failed to fetch recently updated repos:', err.message);
    return [];
  }
}

async function getLatestRepos() {
  try {
    await sleep(500); // sequential delay
    const data = await fetchJSON(
      `https://api.github.com/users/${USERNAME}/repos?sort=created&per_page=6`
    );
    return data
      .filter((r) => !r.fork)
      .slice(0, 5)
      .map((r) => ({
        name: r.name,
        url: r.html_url,
        description: r.description || 'No description',
      }));
  } catch (err) {
    console.error('Failed to fetch latest repos:', err.message);
    return [];
  }
}

async function getRecentPRs() {
  try {
    await sleep(500);
    const data = await fetchJSON(
      `https://api.github.com/search/issues?q=author:${USERNAME}+type:pr&sort=created&per_page=5`
    );
    return (data.items || []).map((pr) => ({
      title: pr.title,
      url: pr.html_url,
      repo: pr.repository_url.split('/').slice(-2).join('/'),
      state: pr.state,
    }));
  } catch (err) {
    console.error('Failed to fetch recent PRs:', err.message);
    return [];
  }
}

async function getRecentIssues() {
  try {
    await sleep(500);
    const data = await fetchJSON(
      `https://api.github.com/search/issues?q=author:${USERNAME}+type:issue&sort=created&per_page=5`
    );
    return (data.items || []).map((issue) => ({
      title: issue.title,
      url: issue.html_url,
      repo: issue.repository_url.split('/').slice(-2).join('/'),
      state: issue.state,
      comments: issue.comments,
    }));
  } catch (err) {
    console.error('Failed to fetch recent issues:', err.message);
    return [];
  }
}

async function getRecentStars() {
  try {
    await sleep(500);
    const data = await fetchJSON(
      `https://api.github.com/users/${USERNAME}/starred?sort=created&per_page=5`
    );
    return data.map((r) => ({
      name: `${r.owner.login}/${r.name}`,
      url: r.html_url,
      description: r.description || 'No description',
    }));
  } catch (err) {
    console.error('Failed to fetch recent stars:', err.message);
    return [];
  }
}

function renderCurrentlyWorking(repos) {
  if (repos.length === 0) return '- *Building something cool...*';
  return repos
    .map((r) => `- [${r.name}](${r.url}) - ${r.description}`)
    .join('\n');
}

function renderLatestProjects(repos) {
  if (repos.length === 0) return '- *Nothing yet...*';
  return repos
    .map((r) => `- [${r.name}](${r.url}) - ${r.description}`)
    .join('\n');
}

function renderRecentPRs(prs) {
  if (prs.length === 0) return '- *No recent PRs...*';
  return prs
    .map(
      (pr) =>
        `- [${pr.title}](${pr.url}) on [${pr.repo}](https://github.com/${pr.repo}) \`${pr.state}\``
    )
    .join('\n');
}

function renderRecentIssues(issues) {
  if (issues.length === 0) return '- *No recent issues...*';
  return issues
    .map(
      (issue) =>
        `- [${issue.title}](${issue.url}) on [${issue.repo}](https://github.com/${issue.repo}) \`${issue.state}\` 💬${issue.comments}`
    )
    .join('\n');
}

function renderRecentStars(stars) {
  if (stars.length === 0) return '- *No recent stars...*';
  return stars
    .map((s) => `- [${s.name}](${s.url}) - ${s.description}`)
    .join('\n');
}

async function main() {
  console.log('Fetching GitHub data...');

  // Sequential fetching to avoid rate limits
  const workingOn = await getRecentlyUpdatedRepos();
  console.log(`Found ${workingOn.length} repos in progress`);

  const latestRepos = await getLatestRepos();
  console.log(`Found ${latestRepos.length} latest repos`);

  const recentPRs = await getRecentPRs();
  console.log(`Found ${recentPRs.length} recent PRs`);

  const recentIssues = await getRecentIssues();
  console.log(`Found ${recentIssues.length} recent issues`);

  const recentStars = await getRecentStars();
  console.log(`Found ${recentStars.length} recent stars`);

  const readmePath = path.join(process.cwd(), 'README.md');
  let readme = await fs.readFile(readmePath, 'utf-8');

  // Replace dynamic sections
  const replacements = {
    '<!-- DYNAMIC: currently_working_on -->': renderCurrentlyWorking(workingOn),
    '<!-- DYNAMIC: latest_projects -->': renderLatestProjects(latestRepos),
    '<!-- DYNAMIC: recent_prs -->': renderRecentPRs(recentPRs),
    '<!-- DYNAMIC: recent_issues -->': renderRecentIssues(recentIssues),
    '<!-- DYNAMIC: recent_stars -->': renderRecentStars(recentStars),
  };

  for (const [marker, content] of Object.entries(replacements)) {
    readme = readme.replace(marker, content);
  }

  await fs.writeFile(readmePath, readme);
  console.log('README updated successfully!');
}

main().catch((err) => {
  console.error('Error:', err);
  process.exit(1);
});
