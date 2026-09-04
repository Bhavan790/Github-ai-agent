"""
Agent Core — routes incoming GitHub webhook events to the right skill.
"""

from skills.issue_responder import IssueResponder
from skills.issue_labeler import IssueLabeler
from skills.pr_reviewer import PRReviewer
from skills.star_thanker import StarThanker


class AgentCore:
    def __init__(self):
        self.issue_responder = IssueResponder()
        self.issue_labeler = IssueLabeler()
        self.pr_reviewer = PRReviewer()
        self.star_thanker = StarThanker()

    def handle_event(self, event_type: str, payload: dict):
        """
        Routes GitHub webhook events to the right skill.
        event_type: 'issues', 'pull_request', 'watch' (stars), etc.
        """
        print(f"\n🔔 Event received: {event_type}")

        # ── New Issue Opened ──────────────────────────────────
        if event_type == "issues" and payload.get("action") == "opened":
            repo_name = payload["repository"]["name"]
            issue = payload["issue"]
            issue_number = issue["number"]
            issue_title = issue["title"]
            issue_body = issue.get("body", "")

            # Run labeler first, then responder
            self.issue_labeler.handle(repo_name, issue_number, issue_title, issue_body)
            self.issue_responder.handle(repo_name, issue_number, issue_title, issue_body)

        # ── New Pull Request Opened ───────────────────────────
        elif event_type == "pull_request" and payload.get("action") == "opened":
            repo_name = payload["repository"]["name"]
            pr = payload["pull_request"]
            pr_number = pr["number"]
            pr_title = pr["title"]
            pr_body = pr.get("body", "")

            self.pr_reviewer.handle(repo_name, pr_number, pr_title, pr_body)

        # ── New Star ──────────────────────────────────────────
        elif event_type == "watch" and payload.get("action") == "started":
            repo_name = payload["repository"]["name"]
            self.star_thanker.handle(repo_name)

        else:
            print(f"ℹ️  Event '{event_type}' with action '{payload.get('action')}' — no skill matched")
