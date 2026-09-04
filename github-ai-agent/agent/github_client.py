"""
GitHub API client wrapper using PyGithub.
Handles all interactions with GitHub repos, issues, PRs.
"""

import os
from github import Github, GithubException
from dotenv import load_dotenv

load_dotenv()


class GitHubClient:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN not set in .env")
        self.client = Github(token)
        self.username = os.getenv("GITHUB_USERNAME", "Bhavan790")
        self.user = self.client.get_user(self.username)

    def get_repo(self, repo_name: str):
        """Get a repo by name. e.g. 'ai-privacy-shield-pro'"""
        return self.client.get_repo(f"{self.username}/{repo_name}")

    def get_all_repos(self):
        """Get all public repos for the user."""
        return list(self.user.get_repos())

    # ── Issues ────────────────────────────────────────────────
    def get_open_issues(self, repo_name: str):
        repo = self.get_repo(repo_name)
        return list(repo.get_issues(state="open"))

    def comment_on_issue(self, repo_name: str, issue_number: int, body: str):
        repo = self.get_repo(repo_name)
        issue = repo.get_issue(issue_number)
        issue.create_comment(body)
        print(f"✅ Commented on issue #{issue_number} in {repo_name}")

    def add_labels_to_issue(self, repo_name: str, issue_number: int, labels: list[str]):
        repo = self.get_repo(repo_name)
        issue = repo.get_issue(issue_number)
        # Create labels if they don't exist
        existing = [l.name for l in repo.get_labels()]
        label_colors = {
            "bug": "d73a4a",
            "feature": "0075ca",
            "documentation": "0075ca",
            "question": "d876e3",
            "enhancement": "a2eeef",
            "help wanted": "008672",
        }
        for label in labels:
            if label not in existing:
                color = label_colors.get(label, "ededed")
                try:
                    repo.create_label(label, color)
                except GithubException:
                    pass
        issue.add_to_labels(*labels)
        print(f"✅ Added labels {labels} to issue #{issue_number}")

    def close_issue(self, repo_name: str, issue_number: int):
        repo = self.get_repo(repo_name)
        issue = repo.get_issue(issue_number)
        issue.edit(state="closed")

    # ── Pull Requests ──────────────────────────────────────────
    def get_open_prs(self, repo_name: str):
        repo = self.get_repo(repo_name)
        return list(repo.get_pulls(state="open"))

    def comment_on_pr(self, repo_name: str, pr_number: int, body: str):
        repo = self.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        pr.create_issue_comment(body)
        print(f"✅ Commented on PR #{pr_number} in {repo_name}")

    def get_pr_diff(self, repo_name: str, pr_number: int) -> str:
        """Get the file changes in a PR as a readable string."""
        repo = self.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        files = pr.get_files()
        diff_text = ""
        for f in files:
            diff_text += f"\n--- {f.filename} ---\n"
            if f.patch:
                diff_text += f.patch[:2000]  # limit size
        return diff_text

    # ── README / Files ─────────────────────────────────────────
    def get_file_content(self, repo_name: str, filepath: str) -> str:
        repo = self.get_repo(repo_name)
        content = repo.get_contents(filepath)
        return content.decoded_content.decode("utf-8")

    def update_file(self, repo_name: str, filepath: str, new_content: str, commit_msg: str):
        repo = self.get_repo(repo_name)
        contents = repo.get_contents(filepath)
        repo.update_file(
            path=filepath,
            message=commit_msg,
            content=new_content,
            sha=contents.sha,
        )
        print(f"✅ Updated {filepath} in {repo_name}")

    # ── Stars ──────────────────────────────────────────────────
    def get_stargazers(self, repo_name: str):
        repo = self.get_repo(repo_name)
        return list(repo.get_stargazers())

    # ── Stats ──────────────────────────────────────────────────
    def get_profile_stats(self) -> dict:
        """Get summary stats for your GitHub profile."""
        repos = self.get_all_repos()
        total_stars = sum(r.stargazers_count for r in repos)
        total_forks = sum(r.forks_count for r in repos)
        languages = {}
        for repo in repos:
            for lang, count in repo.get_languages().items():
                languages[lang] = languages.get(lang, 0) + count
        top_lang = max(languages, key=languages.get) if languages else "Python"
        return {
            "public_repos": self.user.public_repos,
            "followers": self.user.followers,
            "following": self.user.following,
            "total_stars": total_stars,
            "total_forks": total_forks,
            "top_language": top_lang,
        }
