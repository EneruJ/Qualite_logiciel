import os
import openai
from git import Repo

# Configuration de l'API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Fonction pour récupérer les diffs des commits
def get_commit_diffs(repo_path):
    repo = Repo(repo_path)
    diffs = []
    for diff in repo.head.commit.diff(None):
        diffs.append(diff.diff.decode('utf-8'))
    return diffs

# Fonction pour analyser les diffs avec GPT
def analyze_diffs(diffs):
    for diff in diffs:
        prompt = (
            f"Analyze the following diff and provide a detailed code review:\n{diff}\n\n"
            "Identify potential bugs, syntax errors, and violations of naming conventions. "
            "Also, suggest improvements for code quality and readability."
        )
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=300
        )
        print(response.choices[0].text)

if __name__ == "__main__":
    repo_path = '.'
    diffs = get_commit_diffs(repo_path)
    analyze_diffs(diffs)
