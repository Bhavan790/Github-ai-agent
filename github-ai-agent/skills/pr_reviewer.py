"""
Skill: PR Reviewer
Automatically reviews Pull Requests using Claude.
"""

from agent.claude_client import ClaudeClient
from agent.github_client import GitHubClient


class PRReviewer:
    def __init__(self):
        self.claude = ClaudeClient()
        self.github = GitHubClient()

    def handle(self, repo_name: str, pr_number: int, pr_title: str, pr_body: str):
        print(f"🔍 PR Reviewer triggered — PR #{pr_number}: {pr_title}")

        # Get the code diff
        diff = self.github.get_pr_diff(repo_name, pr_number)

        if not diff:
            diff = "(no code changes detected)"

        # Ask Claude to review
        review = self.claude.review_pr(
            pr_title=pr_title,
            pr_body=pr_body or "(no description)",
            diff=diff,
            repo_name=repo_name,
        )

        # Post the review comment
        self.github.comment_on_pr(repo_name, pr_number, review)
        print(f"✅ PR #{pr_number} reviewed successfully")
        return review
