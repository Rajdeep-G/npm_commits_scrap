import requests
from bs4 import BeautifulSoup
from datetime import datetime


def extract_github_link(npm_package_name):    
    try:
        npm_url = f"https://www.npmjs.com/package/{npm_package_name}"
        # print(npm_url)

        response = requests.get(npm_url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        soup = BeautifulSoup(response.text, "lxml")

        # github_link_element = soup.select_one('a[href*="github.com"]')
        github_link_element=None
        github_link_element_all = [link["href"] for link in soup.select('a[href*="github.com"]')]
        for x in github_link_element_all:
            # count no of "/" in the link
            if x.count("/") ==4:
                github_link_element=x
                break
        if github_link_element:
            github_link = github_link_element
            user_name = github_link.split('/')[3]
            repo_name = github_link.split('/')[4]
            # if repo_name not in popular_npm_packages:
            with open("gh_links3.txt", "a+") as file:
                file.write(f"{npm_package_name} {user_name} {repo_name} {github_link}")
                file.write("\n")
            file.close()
        else:
            print(f"No GitHub link found for {npm_package_name}")

    except Exception as e:
        print(f"Error processing npm package '{npm_package_name}': {e}")


# print start time

with open("modified_large_repo.txt", "r") as file:
    npm_package_names = file.read().splitlines()

for x in range(0, len(npm_package_names)):
    npm_package_names[x] = npm_package_names[x].split()[0]
    npm_package_names[x] = npm_package_names[x].replace('"', '')
    npm_package_names[x] = npm_package_names[x].replace(',', '')
    # print(npm_package_names[x])




start_time = datetime.now()
for npm_package_name in npm_package_names[:5]:
    extract_github_link(npm_package_name)


print("Done")
end_time = datetime.now()

# print time taken in minutes and seconds
print(f"Time taken: {end_time - start_time}")
