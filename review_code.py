import os
import logging
import openai
import requests
from git import Repo

# Configuration de l'API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fonction pour récupérer les diffs des commits
def get_commit_diffs(repo_path):
    repo = Repo(repo_path)
    diffs = []
    for diff in repo.head.commit.diff(None):
        diffs.append(diff.diff.decode('utf-8'))
    return diffs

# Fonction pour analyser les diffs avec GPT
def analyze_diffs(diffs):
    comments = []
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
        review_comment = response.choices[0].text.strip()
        comments.append(review_comment)
        logging.info(f"Review for diff: {diff}\n{review_comment}")
    return comments

# Fonction pour poster les commentaires à la pull request
def post_comments_to_pr(comments, pr_number, repo_owner, repo_name, github_token):
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    for comment in comments:
        data = {'body': comment}
        response = requests.post(
            f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments',
            headers=headers,
            json=data
        )
        if response.status_code == 201:
            logging.info(f"Successfully posted comment to PR #{pr_number}")
        else:
            logging.error(f"Failed to post comment to PR #{pr_number}: {response.content}")

if __name__ == "__main__":
    repo_path = '.'
    pr_number = os.getenv("PR_NUMBER")
    repo_owner = os.getenv("GITHUB_REPOSITORY_OWNER")
    repo_name = os.getenv("GITHUB_REPOSITORY_NAME")
    github_token = os.getenv("TOKEN_GITHUB")

    logging.info(f"PR_NUMBER: {pr_number}")
    logging.info(f"GITHUB_REPOSITORY_OWNER: {repo_owner}")
    logging.info(f"GITHUB_REPOSITORY_NAME: {repo_name}")

    diffs = get_commit_diffs(repo_path)
    comments = analyze_diffs(diffs)
    post_comments_to_pr(comments, pr_number, repo_owner, repo_name, github_token)
