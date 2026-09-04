"""
Gemini API wrapper (replaces Anthropic Claude).
All AI thinking happens here.
"""

import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


class ClaudeClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in environment variables")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.8-flash"
        self.agent_name = os.getenv("AGENT_NAME", "BhavanBot")

        # System prompt — defines the agent's personality
        self.system_prompt = f"""You are {self.agent_name}, an AI assistant managing the GitHub profile 
of Bhavan Kumar RT — a B.E. Electrical Engineering student from Rajalakshmi Engineering College, India.

Bhavan's skills: Python, Java, FastAPI, Docker, Machine Learning, LeetCode (450+ problems), 
Embedded Systems, Cybersecurity basics, NVIDIA Llama API.

His repos:
- ai-privacy-shield-pro: PII scrubber using FastAPI + NVIDIA Llama-3.1-405B + Docker
- Mes_r_ponses_Leetcode: 450+ LeetCode solutions in Java with time/space complexity
- linkedin_auto_poster: Python automation for LinkedIn posts
- Python_ML: ML algorithms with NumPy, Pandas, Scikit-learn
- Aiml-Lab: AI/ML lab experiments

Your tone: Friendly, professional, helpful, concise. You represent Bhavan authentically.
Always be genuine — never generic or spammy.
Keep responses under 300 words unless reviewing code.
Use markdown formatting for GitHub comments."""

    def think(self, prompt: str, max_tokens: int = 500) -> str:
        """General purpose Gemini call."""
        config = types.GenerateContentConfig(
            system_instruction=self.system_prompt,
            max_output_tokens=max_tokens,
        )
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config,
        )
        return response.text

    def respond_to_issue(self, issue_title: str, issue_body: str, repo_name: str) -> str:
        prompt = f"""Someone opened a GitHub issue on Bhavan's repo "{repo_name}".

Issue title: {issue_title}
Issue body: {issue_body}

Write a helpful, friendly reply as BhavanBot. 
- Acknowledge the issue
- If it's a bug: ask for reproduction steps if missing, or confirm you'll look into it
- If it's a feature request: thank them and say whether it fits the project vision
- If it's a question: answer it if you can
- End with a friendly note

Do not be generic. Be specific to what they wrote."""
        return self.think(prompt)

    def label_issue(self, issue_title: str, issue_body: str) -> list[str]:
        prompt = f"""Classify this GitHub issue and return ONLY a JSON list of labels.

Issue title: {issue_title}
Issue body: {issue_body}

Choose from: ["bug", "feature", "documentation", "question", "enhancement", "help wanted"]
Return ONLY the JSON list, nothing else. Example: ["bug", "help wanted"]"""
        result = self.think(prompt, max_tokens=50)
        try:
            # Strip potential markdown formatting block ```json ... ```
            cleaned_result = (
                result.strip()
                .replace("```json", "")
                .replace("```", "")
                .replace("'", '"')
                .strip()
            )
            labels = json.loads(cleaned_result)
            valid_labels = ["bug", "feature", "documentation", "question", "enhancement", "help wanted"]
            return [l for l in labels if l in valid_labels]
        except Exception:
            return ["question"]

    def review_pr(self, pr_title: str, pr_body: str, diff: str, repo_name: str) -> str:
        prompt = f"""Review this Pull Request on Bhavan's repo "{repo_name}".

PR title: {pr_title}
PR description: {pr_body}

Code changes (diff):
{diff[:3000]}

Write a code review comment as BhavanBot:
- Thank the contributor
- Comment on what looks good
- Point out any issues or improvements (be specific, reference line numbers if possible)
- Suggest next steps
- Be encouraging but honest"""
        return self.think(prompt, max_tokens=800)

    def generate_readme_stats_section(self, stats: dict) -> str:
        prompt = f"""Generate a short, engaging "GitHub Stats" section for Bhavan's profile README.

Current stats:
- Public repos: {stats['public_repos']}
- Followers: {stats['followers']}  
- Total stars: {stats['total_stars']}
- Total forks: {stats['total_forks']}
- Top language: {stats['top_language']}

Write it in markdown, keep it under 5 lines, make it motivating.
Include the stats naturally in prose or a small table."""
        return self.think(prompt, max_tokens=200)

    def write_star_thank_you(self, stargazer_name: str, repo_name: str) -> str:
        prompt = f"""Someone named "{stargazer_name}" just starred Bhavan's "{repo_name}" repo.

Write a warm, genuine, SHORT thank-you message (2-3 sentences max).
Mention the repo specifically. Don't be cringe or over-the-top.
This will be posted as a GitHub Discussion comment."""
        return self.think(prompt, max_tokens=150)
