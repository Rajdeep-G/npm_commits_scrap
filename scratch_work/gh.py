import requests
from config import API_KEY
token=API_KEY
def get_commits(repo_owner, repo_name):
    # url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    # response = requests.get(url)
    
    # if response.status_code == 200:
    #     commits = response.json()
    #     return commits
    # else:
    #     print(f"Failed to fetch commits. Status code: {response.status_code}")
    #     return None
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

def download_webpage(url,name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # with open('webpage.html', 'wb') as file:
            with open(f'../all_commits/{name}', 'wb') as file:
                file.write(response.content)
            print(f"Webpage downloaded successfully as '{name}'")
        else:
            print(f"Failed to download webpage. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading webpage: {e}")


# Example usage
repo_owner = "npm"
repo_name = "cli"
commits = get_commits(repo_owner, repo_name)

fixed_commit_ur=f'https://github.com/{repo_owner}/{repo_name}/commit/'

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
            # download_webpage(url,filename_commit)
            
print(len(all_files))
# with open('all_files_names.txt', 'w') as file:
#     for filename in all_files:
#         file.write(f"{filename}\n")
#     print(f"All filenames written to 'all_files.txt'")