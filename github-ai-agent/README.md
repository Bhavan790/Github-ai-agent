
# Test commit for PR review

<div align="center">

# 🤖 GitHub AI Agent

### An autonomous AI agent that manages your GitHub profile using Claude + FastAPI

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Claude](https://img.shields.io/badge/Claude-Sonnet-orange?style=flat)](https://anthropic.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](LICENSE)

**Auto-replies to issues · Labels PRs · Reviews code · Updates README stats daily · Thanks new stargazers**

</div>

---

## 🧠 What It Does

| Skill | Trigger | Action |
|---|---|---|
| 💬 **Issue Responder** | New issue opened | Claude reads it → posts an intelligent reply |
| 🏷️ **Issue Labeler** | New issue opened | Claude classifies → adds bug/feature/docs labels |
| 🔍 **PR Reviewer** | New PR opened | Claude reads the diff → posts code review |
| 📊 **README Updater** | Daily at midnight | Fetches GitHub stats → updates profile README |
| ⭐ **Star Thanker** | Every 6 hours | Checks new stargazers → posts thank-you message |

---

## 🏗️ Architecture

```
GitHub Event (issue/PR/star)
        │
        ▼
FastAPI Webhook Server  (/webhook)
        │
        ▼
Agent Core  (routes event to right skill)
     │          │          │
     ▼          ▼          ▼
Claude API   GitHub API  Scheduler
(thinks)     (acts)      (daily jobs)
```

---

## 🚀 Quick Start

### 1. Clone
```bash
git clone https://github.com/Bhavan790/github-ai-agent.git
cd github-ai-agent
```

### 2. Set up credentials
```bash
cp .env.example .env
```

Edit `.env`:
```env
GITHUB_TOKEN=ghp_your_token_here        # needs: repo, issues, pull_requests scopes
GITHUB_USERNAME=Bhavan790
GITHUB_WEBHOOK_SECRET=your_secret
ANTHROPIC_API_KEY=sk-ant-your_key_here
```

**Get your tokens:**
- GitHub token → github.com/settings/tokens → New classic token
- Anthropic key → console.anthropic.com

### 3. Run with Docker
```bash
docker-compose up --build
```

Or locally:
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 4. Register webhook on GitHub
1. Go to any repo → **Settings → Webhooks → Add webhook**
2. Payload URL: `https://your-domain.com/webhook`
3. Content type: `application/json`
4. Secret: same as `GITHUB_WEBHOOK_SECRET` in `.env`
5. Events: Issues, Pull requests, Stars ✅

### 5. Expose locally for testing
```bash
# Install ngrok
ngrok http 8000
# Copy the https URL → paste in GitHub webhook settings
```

---

## 📁 Project Structure

```
github-ai-agent/
├── main.py                  # FastAPI server + webhook endpoint
├── scheduler.py             # Daily background jobs
├── agent/
│   ├── core.py              # Event router
│   ├── claude_client.py     # All Claude AI calls
│   └── github_client.py     # All GitHub API calls
├── skills/
│   ├── issue_responder.py   # Auto-reply to issues
│   ├── issue_labeler.py     # Auto-label issues
│   ├── pr_reviewer.py       # Auto-review PRs
│   ├── readme_updater.py    # Daily README stats
│   └── star_thanker.py      # Thank new stargazers
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 🛠️ Add Stats Auto-Update to Your Profile README

Add these markers anywhere in your profile README (`Bhavan790/Bhavan790`):

```markdown
<!-- STATS:START -->
<!-- STATS:END -->
```

The agent will replace the content between them every day automatically.

---

## 🗺️ Roadmap

- [x] Issue auto-responder
- [x] Issue auto-labeler
- [x] PR auto-reviewer
- [x] Daily README stats updater
- [x] Star thanker
- [ ] Weekly activity summary posted to LinkedIn
- [ ] Slack/Telegram notifications for repo events
- [ ] Auto-close stale issues after 30 days
- [ ] Multi-repo support dashboard

---

## 👨‍💻 Author

**Bhavan Kumar RT** — B.E. Electrical & Electronics, Rajalakshmi Engineering College

[![GitHub](https://img.shields.io/badge/GitHub-Bhavan790-181717?style=flat&logo=github)](https://github.com/Bhavan790)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Bhavan%20Kumar%20RT-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/bhavan-kumar-rt)

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">
  <sub>Built with 🤖 Claude + ⚡ FastAPI + 🐍 Python · Star ⭐ if this inspired you!</sub>
</div>
