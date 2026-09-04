"""
github-ai-agent — Main FastAPI webhook server
Receives GitHub webhook events and routes them to the agent.

Run with:  uvicorn main:app --host 0.0.0.0 --port 8000
"""

import os
import hmac
import hashlib
import threading
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Header
from agent.core import AgentCore
from scheduler import run_scheduler

load_dotenv()

app = FastAPI(
    title="GitHub AI Agent",
    description="AI agent that autonomously manages Bhavan790's GitHub profile",
    version="1.0.0",
)

agent = AgentCore()

# Start scheduler in background thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()


def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """Verify the GitHub webhook secret to ensure requests are genuine."""
    secret = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    if not secret:
        return True  # Skip verification if no secret set (dev mode)
    expected = "sha256=" + hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature or "")


@app.get("/")
def root():
    return {
        "name": "GitHub AI Agent",
        "status": "running",
        "owner": "Bhavan790",
        "skills": [
            "issue_responder",
            "issue_labeler",
            "pr_reviewer",
            "readme_updater",
            "star_thanker",
        ],
    }


@app.get("/health")
def health():
    return {"status": "ok", "agent": "BhavanBot v1.0"}


@app.post("/webhook")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(None),
    x_hub_signature_256: str = Header(None),
):
    """Main webhook endpoint — register this URL in your GitHub repo settings."""

    raw_body = await request.body()

    # Verify signature
    if not verify_webhook_signature(raw_body, x_hub_signature_256 or ""):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    payload = await request.json()

    # Ignore events from the agent itself to prevent infinite loops
    sender = payload.get("sender", {}).get("login", "")
    if sender == os.getenv("GITHUB_USERNAME", "Bhavan790"):
        return {"status": "ignored", "reason": "own event"}

    # Route to agent
    if x_github_event:
        agent.handle_event(x_github_event, payload)

    return {"status": "ok", "event": x_github_event}


@app.post("/trigger/readme")
def trigger_readme_update():
    """Manually trigger a README stats update."""
    from skills.readme_updater import ReadmeUpdater
    updater = ReadmeUpdater()
    stats = updater.handle()
    return {"status": "updated", "stats": stats}


@app.post("/trigger/stars/{repo_name}")
def trigger_star_check(repo_name: str):
    """Manually trigger star check for a specific repo."""
    from skills.star_thanker import StarThanker
    thanker = StarThanker()
    count = thanker.handle(repo_name)
    return {"status": "ok", "new_thanks_sent": count}
