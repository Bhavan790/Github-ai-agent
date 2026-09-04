"""
Skill: README Updater
Runs daily — fetches latest GitHub stats and updates profile README.
Replaces content between <!-- STATS:START --> and <!-- STATS:END --> markers.
"""

import re
from datetime import datetime
from agent.claude_client import ClaudeClient
from agent.github_client import GitHubClient


class ReadmeUpdater:
    def __init__(self):
        self.claude = ClaudeClient()
        self.github = GitHubClient()
        self.profile_repo = "Bhavan790"  # your profile README repo

    def handle(self):
        print("📊 README Updater triggered")

        # Fetch real stats
        stats = self.github.get_profile_stats()
        print(f"   Stats fetched: {stats}")

        # Get current README
        try:
            readme = self.github.get_file_content(self.profile_repo, "README.md")
        except Exception as e:
            print(f"❌ Could not fetch README: {e}")
            return

        # Build the stats block
        updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        stats_block = f"""<!-- STATS:START -->
| 📦 Repos | ⭐ Stars | 👥 Followers | 🍴 Forks | 🏆 Top Language |
|---|---|---|---|---|
| {stats['public_repos']} | {stats['total_stars']} | {stats['followers']} | {stats['total_forks']} | {stats['top_language']} |

*Auto-updated by [github-ai-agent](https://github.com/Bhavan790/github-ai-agent) on {updated_at}*
<!-- STATS:END -->"""

        # Replace the block in README (between markers)
        pattern = r"<!-- STATS:START -->.*?<!-- STATS:END -->"
        if re.search(pattern, readme, re.DOTALL):
            new_readme = re.sub(pattern, stats_block, readme, flags=re.DOTALL)
        else:
            # Append if markers not found
            new_readme = readme + "\n\n" + stats_block

        if new_readme == readme:
            print("ℹ️  README unchanged — skipping commit")
            return

        # Commit the update
        self.github.update_file(
            repo_name=self.profile_repo,
            filepath="README.md",
            new_content=new_readme,
            commit_msg=f"chore: auto-update GitHub stats [{updated_at}]",
        )
        print("✅ README updated with latest stats!")
        return stats
