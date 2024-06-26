import os
import logging
import openai
import requests
import subprocess

# Configuration de l'API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fonction pour exécuter une commande shell
def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command {command}: {e}")
        return ""

# Fonction pour récupérer les diffs des commits
def get_commit_diffs():
    run_command(['git', 'fetch', 'origin', 'main'])
    diffs = run_command(['git', 'diff', 'origin/main'])
    return diffs.split('\n')

# Fonction pour analyser les diffs avec GPT
def analyze_diffs(diffs):
    comments = []
    for diff in diffs:
        if not diff.strip():
            continue
        prompt = (
            f"Analyze the following diff and provide a detailed code review:\n{diff}\n\n"
            "Identify potential bugs, syntax errors, and violations of naming conventions. "
            "Also, suggest improvements for code quality and readability."
        )
        logging.info(f"Prompt sent to OpenAI: {prompt}")
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
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments'
    for comment in comments:
        data = {'body': comment}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            logging.info(f"Successfully posted comment to PR #{pr_number}")
        else:
            logging.error(f"Failed to post comment to PR #{pr_number}: {response.content}")

if __name__ == "__main__":
    pr_number = os.getenv("PR_NUMBER")
    repo_owner = os.getenv("GITHUB_REPOSITORY_OWNER")
    repo_name = os.getenv("GITHUB_REPOSITORY_NAME")
    github_token = os.getenv("TOKEN_GITHUB")

    logging.info(f"PR_NUMBER: {pr_number}")
    logging.info(f"GITHUB_REPOSITORY_OWNER: {repo_owner}")
    logging.info(f"GITHUB_REPOSITORY_NAME: {repo_name}")

    if not pr_number or not repo_owner or not repo_name or not github_token:
        logging.error("Missing environment variables")
        exit(1)

    diffs = get_commit_diffs()
    if not diffs:
        logging.info("No diffs found")
        default_comment = "No code changes detected. Please ensure that your changes are committed properly."
        post_comments_to_pr([default_comment], pr_number, repo_owner, repo_name, github_token)
        exit(0)

    comments = analyze_diffs(diffs)
    if comments:
        post_comments_to_pr(comments, pr_number, repo_owner, repo_name, github_token)
    else:
        logging.info("No comments to post")
