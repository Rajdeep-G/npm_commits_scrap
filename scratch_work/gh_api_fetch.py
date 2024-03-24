import requests
from config import API_KEY
import os
token=API_KEY
def get_all_commits(repo_owner, repo_name):
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    params = {'per_page': 100}  # Request up to 100 commits per page
    headers = {'Authorization': f'token {token}'}
    commits = []

    while url:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            # commits += response.json()
            commits.extend(response.json())
            # Check if there are more pages to fetch
            url = response.links.get('next', {}).get('url')
        else:
            print(f"Failed to fetch commits. Status code: {response.status_code}")
            return None

    return commits

def get_30_commits(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    response = requests.get(url)
    
    if response.status_code == 200:
        commits = response.json()
        return commits
    else:
        print(f"Failed to fetch commits. Status code: {response.status_code}")
        return None

def download_webpage(url,name,org_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # with open('webpage.html', 'wb') as file:
            # create a folder named all_commits in the current directory
            os.makedirs(f'../{org_name}', exist_ok=True)
            with open(f'../{org_name}/{name}', 'wb') as file:
                file.write(response.content)
            print(f"Webpage downloaded successfully as '{name}'")
        else:
            print(f"Failed to download webpage. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading webpage: {e}")

def flow(repo_owner, repo_name,org_name):
    
    commits = get_all_commits(repo_owner, repo_name)

    fixed_commit_ur=f'https://github.com/{repo_owner}/{repo_name}/commit/'
    print(fixed_commit_ur)
    all_files=[]
    c=0
    if commits:
        print(f"Commits count: {len(commits)}")
        for commit in commits:
            # print(commit['sha'], commit['commit']['message'])
            if 'fix' in commit['commit']['message'].lower():
                url=fixed_commit_ur+commit['sha']
                filename_commit=commit['sha']+'.html'
                all_files.append(filename_commit)
                download_webpage(url,filename_commit,org_name)
                
    print(len(all_files))
    with open(f'{org_name}_file_names.txt', 'w') as file:
        for filename in all_files:
            file.write(f"{filename}\n")
        # print(f"All filenames written to 'all_files.txt'")


gh_links = []
with open("../gh_links.txt", "r") as file:
    all_files = file.read().splitlines()
    for line in all_files:
        temp=[]
        temp.append(line.split()[0])
        temp.append(line.split()[1])
        temp.append(line.split()[2])
        gh_links.append(temp)

for link in gh_links:
    repo_owner=link[1]
    repo_name=link[2]
    org_name=link[0]
    print(repo_owner,repo_name,org_name)
    flow(repo_owner, repo_name,org_name)
    


# repo_owner = "npm"
# repo_name = "cli"