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

```text
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
