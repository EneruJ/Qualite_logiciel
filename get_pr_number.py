import os
import requests
import sys

def get_pr_number(repo_owner, repo_name, branch_name, github_token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    params = {
        'head': f'{repo_owner}:{branch_name}',
        'state': 'open'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error: Unable to fetch pull requests - {response.status_code}")
        return None
    
    prs = response.json()
    if not prs:
        print("No open pull requests found for the branch")
        return None

    return prs[0]['number']

if __name__ == "__main__":
    repo_owner = os.getenv("GITHUB_REPOSITORY_OWNER")
    repo_name = os.getenv("GITHUB_REPOSITORY_NAME")
    branch_name = os.getenv("BRANCH_NAME")
    github_token = os.getenv("TOKEN_GITHUB")

    pr_number = get_pr_number(repo_owner, repo_name, branch_name, github_token)
    if pr_number:
        print(f"::set-output name=PR_NUMBER::{pr_number}")
    else:
        sys.exit(1)
