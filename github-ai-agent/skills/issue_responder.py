"""
Skill: Issue Responder
Automatically replies to new GitHub issues using Claude.
"""

from agent.claude_client import ClaudeClient
from agent.github_client import GitHubClient


class IssueResponder:
    def __init__(self):
        self.claude = ClaudeClient()
        self.github = GitHubClient()

    def handle(self, repo_name: str, issue_number: int, issue_title: str, issue_body: str):
        print(f"🔍 Issue Responder triggered — #{issue_number}: {issue_title}")

        # Generate AI response
        reply = self.claude.respond_to_issue(
            issue_title=issue_title,
            issue_body=issue_body or "(no description provided)",
            repo_name=repo_name,
        )

        # Post the comment
        self.github.comment_on_issue(repo_name, issue_number, reply)
        print(f"✅ Issue #{issue_number} replied to successfully")
        return reply
