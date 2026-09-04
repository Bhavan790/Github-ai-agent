"""
Skill: Star Thanker
When someone stars your repo, creates a personalized thank-you discussion.
Tracks who was already thanked to avoid duplicates.
"""

import json
import os
from agent.claude_client import ClaudeClient
from agent.github_client import GitHubClient


THANKED_FILE = "thanked_stargazers.json"


class StarThanker:
    def __init__(self):
        self.claude = ClaudeClient()
        self.github = GitHubClient()
        self.thanked = self._load_thanked()

    def _load_thanked(self) -> dict:
        if os.path.exists(THANKED_FILE):
            with open(THANKED_FILE) as f:
                return json.load(f)
        return {}

    def _save_thanked(self):
        with open(THANKED_FILE, "w") as f:
            json.dump(self.thanked, f, indent=2)

    def handle(self, repo_name: str):
        print(f"⭐ Star Thanker triggered for {repo_name}")

        stargazers = self.github.get_stargazers(repo_name)
        repo_key = f"{repo_name}"
        if repo_key not in self.thanked:
            self.thanked[repo_key] = []

        new_count = 0
        for user in stargazers:
            if user.login not in self.thanked[repo_key]:
                # Generate thank-you message
                msg = self.claude.write_star_thank_you(
                    stargazer_name=user.login,
                    repo_name=repo_name,
                )
                # Open a thank-you issue (visible, friendly)
                repo = self.github.get_repo(repo_name)
                repo.create_issue(
                    title=f"⭐ Thank you @{user.login}!",
                    body=msg + f"\n\n— Bhavan Kumar RT ([GitHub](https://github.com/Bhavan790))",
                    labels=[]
                )
                self.thanked[repo_key].append(user.login)
                new_count += 1
                print(f"   ✅ Thanked @{user.login}")

        self._save_thanked()
        print(f"⭐ Star Thanker done — {new_count} new thank-yous sent")
        return new_count
