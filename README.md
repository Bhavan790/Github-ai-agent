<div align="center">

# 🤖 GitHub AI Agent

### An autonomous, asynchronous AI agent that manages your GitHub profile using Gemini 3.6 Flash + FastAPI

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Gemini-3.6_Flash-8E7CC3?style=flat&logo=googlegemini&logoColor=white)](https://ai.google.dev)
[![Render](https://img.shields.io/badge/Render-Live-46E3B7?style=flat&logo=render&logoColor=white)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](LICENSE)

**Asynchronous event processing · Auto-replies to issues · Auto-labels · Automated PR code reviews · Daily README stats updater · Star thanker**

</div>

---

## ⚡ Key Features

- ⚡ **Asynchronous Background Processing**: Dispatches incoming webhooks to isolated background threads instantly (`<200ms` response time) to guarantee zero `500` delivery timeouts on GitHub.
- 💬 **Automated Issue Triage & Labeling**: Gemini reads new issue contents, generates context-aware replies, and auto-assigns tags (`bug`, `feature`, `question`).
- 🔍 **AI Pull Request Reviewer**: Evaluates code diffs in real-time, providing structured feedback and inline improvements.
- ⭐ **Stargazer Engagement**: Detects new stargazers and sends personalized thank-you notes in repository discussions.
- 📊 **Dynamic Profile README Updater**: Runs scheduled background tasks to keep GitHub profile statistics up to date.

---

## 📸 Proof of Concept & Live Demos

| Automated Issue Triage & Labeling | Real-time PR Code Review |
| :---: | :---: |
| ![Issue Proof](docs/screenshots/issue_proof.png) | ![PR Review Proof](docs/screenshots/pr_review_proof.png) |

| Live Render Deployment | Profile README Stats Update |
| :---: | :---: |
| ![Render Proof](docs/screenshots/render_proof.png) | ![README Stats Proof](docs/screenshots/readme_proof.png) |

---

## 🏗️ Architecture


GitHub Webhook Event (Issue / PR / Star)
        │
        ▼
FastAPI Webhook Server (/webhook)  ──[Returns 200 OK (<200ms)]──► GitHub
        │
        ▼ (Daemon Background Thread)
Agent Core (Routes Event)
     │               │               │
     ▼               ▼               ▼
Gemini 3.6 Flash   GitHub REST API   Scheduler
 (Reasoning)       (Executes Actions) (Background Tasks)
🛠️ Project Structure
Plaintext
github-ai-agent/
├── main.py                  # FastAPI server + Async thread webhook dispatcher
├── scheduler.py             # Daily background jobs
├── agent/
│   ├── core.py              # Event router
│   ├── claude_client.py     # Gemini 3.6 Flash client wrapper
│   └── github_client.py     # GitHub REST API interface
├── skills/
│   ├── issue_responder.py   # Auto-reply to issues
│   ├── issue_labeler.py     # Auto-label issues
│   ├── pr_reviewer.py       # Auto-review PR diffs
│   ├── readme_updater.py    # Profile README stats updater
│   └── star_thanker.py      # Stargazer engagement
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
🚀 Quick Start
1. Clone Repository
Bash
git clone [https://github.com/Bhavan790/Github-ai-agent.git](https://github.com/Bhavan790/Github-ai-agent.git)
cd Github-ai-agent/github-ai-agent
2. Configure Environment Variables
Bash
cp .env.example .env
Edit .env:

Code snippet
GITHUB_TOKEN=ghp_your_token_here
BOT_USERNAME=BhavanBot
GITHUB_WEBHOOK_SECRET=your_secret
GEMINI_API_KEY=your_gemini_api_key
3. Local Execution
Bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
🗺️ Roadmap
[x] Sub-200ms Asynchronous Threading Pipeline

[x] Issue auto-responder & labeler

[x] Automated PR code reviewer (Gemini 3.6 Flash)

[x] Daily profile README stats updater

[x] Stargazer engagement module

[x] LinkedIn automated activity summaries

[x] Multi-repository webhook dashboard

👨‍💻 Author
Bhavan Kumar RT — B.E. Electrical & Electronics Engineering, Rajalakshmi Engineering College

📄 License
MIT — see LICENSE for details.
