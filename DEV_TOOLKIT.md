# 🛠️ Paranjay's Developer Toolkit

A curated collection of tools for high-performance development, orchestration, and maintaining code quality in the age of AI.

## 🚀 Recommended Tooling (Anti-Slop Edition)

Based on recent industry shifts and the "vibe-coding" workflow, these are the essential tools to prevent AI-generated code from becoming unmaintainable.

### 🧹 Code Quality & Maintenance
- **[Fallow](https://fallow.tools/)**: (Highly Recommended) A Rust-powered CLI that finds dead code, duplication, and architectural boundary violations. Perfect for cleaning up after AI adds thousands of lines you don't need.
- **[Knip](https://knip.dev/)**: Finds unused files, dependencies, and exports in TypeScript projects.
- **[jscpd](https://jscpd.org/)**: Detects copy-pasted code blocks across your repositories.
- **[ESLint](https://eslint.org/) + [Prettier](https://prettier.io/)**: The standard for keeping code style consistent and catching logical errors before they ship.

### 🧪 Observability & Stability
- **[Sentry](https://sentry.io/)**: Real-time error tracking to see exactly where your apps are failing in production.
- **[PostHog](https://posthog.com/)**: Open-source product analytics. Essential for understanding how people actually use what you build.

### 📦 Infrastructure & Workflow
- **[Docker](https://www.docker.com/)**: Containerization to ensure "it works on my machine" translates to "it works everywhere."
- **[Vite](https://vitejs.dev/)**: The fastest frontend build tool available right now.
- **[Bun](https://bun.sh/)**: A fast all-in-one JavaScript runtime, package manager, and test runner.

---

## 🤖 AI Orchestration Tools
Tools mentioned in the "Syntax" circuit for improving AI coding reliability:
- **agent-browser**: For giving AI agents the ability to navigate the web.
- **chrome-devtools-mcp**: For deep debugging and inspection by AI.
- **Storybook AI**: For visual component testing and discovery.

---

## 💎 Professional Recommendation: The "Anti-Slop" Stack

If you are building fast with AI, I strongly recommend integrating **Fallow** into your workflow. 

**Why?** 
AI loves to add code but rarely deletes it. Over time, your projects will accumulate "contextual debt"—unused exports, duplicated functions, and abandoned types. This confuses AI agents in future turns because they see outdated patterns as still being "active." 

**Action Item**: Run `npx fallow dead-code` on your larger projects (like `ipl-2026-engine`) to see how much weight you can shed.

---

> *"The best code is the code you can delete."*
