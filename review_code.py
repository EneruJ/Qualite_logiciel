import os
import logging
import requests
import subprocess
from openai import OpenAI

# Configuration de l'API OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MAX_DIFF_LENGTH = 3000  # Limite de longueur du diff envoyé à l'API
MAX_REQUESTS = 5  # Nombre maximum de requêtes à l'API par exécution

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
    return diffs

# Fonction pour regrouper les diffs par fichiers
def group_diffs_by_files(diffs):
    file_diffs = {}
    current_file = None
    for line in diffs.split('\n'):
        if line.startswith('diff --git'):
            current_file = line.split(' ')[2][2:]  # obtenir le nom du fichier
            file_diffs[current_file] = []
        if current_file:
            file_diffs[current_file].append(line)
    return file_diffs

# Fonction pour analyser les diffs avec GPT
def analyze_diffs(file_diffs):
    comments = []
    request_count = 0
    for file, diff_lines in file_diffs.items():
        if request_count >= MAX_REQUESTS:
            break
        diff_content = '\n'.join(diff_lines)
        if len(diff_content) > MAX_DIFF_LENGTH:
            diff_content = diff_content[:MAX_DIFF_LENGTH] + '\n... [diff truncated] ...'
        prompt = (
            f"Analyze the following diff from file {file} and provide a detailed code review:\n{diff_content}\n\n"
            "Identify potential bugs, syntax errors, and violations of naming conventions. "
            "Also, suggest improvements for code quality and readability."
        )
        logging.info(f"Prompt sent to OpenAI: {prompt}")
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a code review assistant."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            max_tokens=300  # Limite du nombre de tokens dans la réponse
        )
        review_comment = response.choices[0].message.content.strip()
        comments.append(f"### Review for {file}\n{review_comment}")
        logging.info(f"Review for file {file}:\n{review_comment}")
        request_count += 1
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

    if not pr_number or not repo_owner or not repo_name or not github_token or not api_key:
        logging.error("Missing environment variables")
        exit(1)

    diffs = get_commit_diffs()
    if not diffs:
        logging.info("No diffs found")
        default_comment = "No code changes detected. Please ensure that your changes are committed properly."
        post_comments_to_pr([default_comment], pr_number, repo_owner, repo_name, github_token)
        exit(0)

    file_diffs = group_diffs_by_files(diffs)
    comments = analyze_diffs(file_diffs)
    if comments:
        post_comments_to_pr(comments, pr_number, repo_owner, repo_name, github_token)
    else:
        logging.info("No comments to post")
