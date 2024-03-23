import requests

def get_commits(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    response = requests.get(url)
    
    if response.status_code == 200:
        commits = response.json()
        return commits
    else:
        print(f"Failed to fetch commits. Status code: {response.status_code}")
        return None

# Example usage
repo_owner = "npm"
repo_name = "cli"
commits = get_commits(repo_owner, repo_name)

all_fix=[]
c=0
if commits:
    print(f"Commits count: {len(commits)}")
    for commit in commits:
        # print(commit)
        # print(f"Commit SHA: {commit['sha']} - Message: {commit['commit']['message']}")
        if 'fix' in commit['commit']['message'].lower():
            all_fix.append(commit['commit']['message'])
            c+=1

print(f"Total number of commits with 'fix' in the message: {c}")