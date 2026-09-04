"""
Scheduler — runs daily background tasks.
Run this alongside main.py for full automation.
"""

import schedule
import time
import threading
from skills.readme_updater import ReadmeUpdater
from skills.star_thanker import StarThanker

readme_updater = ReadmeUpdater()
star_thanker = StarThanker()

# ── Schedule daily jobs ────────────────────────────────────────
# Update README stats every day at midnight
schedule.every().day.at("00:00").do(readme_updater.handle)

# Check for new stars every 6 hours across all your main repos
def check_all_stars():
    for repo in ["ai-privacy-shield-pro", "Mes_r_ponses_Leetcode", "Python_ML"]:
        try:
            star_thanker.handle(repo)
        except Exception as e:
            print(f"⚠️  Star check failed for {repo}: {e}")

schedule.every(6).hours.do(check_all_stars)

def run_scheduler():
    print("⏰ Scheduler started")
    # Run README update immediately on startup too
    readme_updater.handle()
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()
