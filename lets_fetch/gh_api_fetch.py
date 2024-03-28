import requests

from config import API_KEY
from datetime import datetime
import gzip
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
        if '/' in org_name:
            org_name=org_name.replace('/','_')
        if response.status_code == 200:
            # with open('webpage.html', 'wb') as file:
            # create a folder named all_commits in the current directory
            os.makedirs(f'webpages/{org_name}', exist_ok=True)
            with gzip.open(f'webpages/{org_name}/{name}.gz', 'wb') as file:
                file.write(response.content)
            print(f"Webpage downloaded successfully as '{name}'")
        else:
            print(f"Failed to download webpage. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading webpage: {e}")

def flow(repo_owner, repo_name,org_name):
    
    commits = get_all_commits(repo_owner, repo_name)
    if '/' in org_name:
        org_name=org_name.replace('/','_')
    fixed_commit_ur=f'https://github.com/{repo_owner}/{repo_name}/commit/'
    # print(fixed_commit_ur)
    all_files=[]
    commit_count=len(commits)
    commit_count_fix=0
    if commits:
        print(f"Commits count: {len(commits)}")
        for commit in commits:
            # print(commit['sha'], commit['commit']['message'])
            if 'fix' in commit['commit']['message'].lower():
                commit_count_fix+=1
                url=fixed_commit_ur+commit['sha']
                filename_commit=commit['sha']+'.html'
                all_files.append(filename_commit)
                download_webpage(url,filename_commit,org_name)
                
    # print(len(all_files))
    if len(all_files)>0:
        with open(f'filenames/{org_name}.txt', 'w') as file:
            for filename in all_files:
                file.write(f"{filename}\n")
    return commit_count, commit_count_fix
    # with open("summary.txt", "a") as file:
        # file.write(f"{repo_name} {org_name} {commit_count} {commit_count_fix}\n")


start_time_global = datetime.now()

gh_links = []
serial=1
with open(f'links/o{serial}.txt', "r") as file:
    all_files = file.read().splitlines()
    for line in all_files[:10]:
        temp=[]
        temp.append(line.split()[0])
        temp.append(line.split()[1])
        temp.append(line.split()[2])
        gh_links.append(temp)

for link in gh_links:
    start_time = datetime.now()
    repo_owner=link[1]
    repo_name=link[2]
    org_name=link[0]
    print(repo_owner,repo_name,org_name)
    # flow(repo_owner, repo_name,org_name)
    commit_count, commit_count_fix = flow(repo_owner, repo_name,org_name)
    end_time = datetime.now()
    print(f"Time taken: {end_time - start_time}")
    # print(f"Total commits with 'fix' keyword: {commit_count_fix}")
    with open("status.txt", "a") as file:
        file.write(f"{repo_name} {org_name} {end_time - start_time} {commit_count} {commit_count_fix}\n")
    print("............................................")
    

end_time_global = datetime.now()
print(f"Total time taken: {end_time_global - start_time_global}")
