"""
Skill: Issue Labeler
Automatically labels new issues using Claude classification.
"""

from agent.claude_client import ClaudeClient
from agent.github_client import GitHubClient


class IssueLabeler:
    def __init__(self):
        self.claude = ClaudeClient()
        self.github = GitHubClient()

    def handle(self, repo_name: str, issue_number: int, issue_title: str, issue_body: str):
        print(f"🏷️  Issue Labeler triggered — #{issue_number}: {issue_title}")

        # Ask Claude to classify
        labels = self.claude.label_issue(
            issue_title=issue_title,
            issue_body=issue_body or "",
        )

        if labels:
            self.github.add_labels_to_issue(repo_name, issue_number, labels)
            print(f"✅ Labels {labels} added to issue #{issue_number}")
        return labels
