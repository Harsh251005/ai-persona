import os
import requests
import base64

# --- Configuration ---
USERNAME = "Harsh251005"
REPOS = ["TruthLens-AI", "Evident-AI"]
OUTPUT_DIR = "context_data"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_readme(repo):
    """Fetches and decodes the README from the GitHub API."""
    url = f"https://api.github.com/repos/{USERNAME}/{repo}/readme"
    response = requests.get(url)

    if response.status_code == 200:
        content_b64 = response.json().get('content', '')
        readme_text = base64.b64decode(content_b64).decode('utf-8')

        file_path = os.path.join(OUTPUT_DIR, f"{repo}_README.md")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(readme_text)
        print(f"  ✅ README saved: {repo}_README.md")
    else:
        print(f"  ❌ README failed for {repo}. Status: {response.status_code}")


def fetch_commits(repo):
    """Fetches the latest 30 commits and formats them for RAG context."""
    url = f"https://api.github.com/repos/{USERNAME}/{repo}/commits?per_page=30"
    response = requests.get(url)

    if response.status_code == 200:
        commits = response.json()
        file_path = os.path.join(OUTPUT_DIR, f"{repo}_Commits.txt")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"--- Commit History for {repo} ---\n\n")
            for commit in commits:
                date = commit['commit']['author']['date']
                message = commit['commit']['message'].replace('\n', ' ')
                sha = commit['sha'][:7]

                # Formatted naturally for the LLM
                file.write(f"On {date}, Harsh made commit {sha}: {message}\n")
        print(f"  ✅ Commits saved: {repo}_Commits.txt")
    else:
        print(f"  ❌ Commits failed for {repo}. Status: {response.status_code}")


# --- Execution ---
print(f"🚀 Starting context extraction for {len(REPOS)} repositories...\n")

for repository in REPOS:
    print(f"Processing repository: {repository}")
    fetch_readme(repository)
    fetch_commits(repository)
    print("-" * 40)

print("\n🎉 All context data successfully downloaded to the context_data/ folder!")