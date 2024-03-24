import requests
from bs4 import BeautifulSoup
from datetime import datetime
# List of repository names
# npm_package_names = [
#   "@dotcom-reliability-kit/serialize-request",
#   "@dotcom-tool-kit/babel",
#   "@dotcom-tool-kit/backend-app",

# ]

# print start time
start_time = datetime.now()
with open("names.json", "r") as file:
    npm_package_names = file.read().splitlines()

for x in range(0, len(npm_package_names)):
    npm_package_names[x] = npm_package_names[x].split()[0]
    npm_package_names[x] = npm_package_names[x].replace('"', '')
    npm_package_names[x] = npm_package_names[x].replace(',', '')


# print(npm_package_names[100:105])
popular_npm_packages = [
    "lodash",
    "axios",
    "react",
    "next",
    "next.js",
    "express",
    "moment",
    "webpack",
    "babel",
    "jest",
    "react-router",
    "typescript"
]

with open("gh_links.txt", "w") as file:
    for npm_package_name in npm_package_names[2000:5000]:
        try:
            npm_url = f"https://www.npmjs.com/package/{npm_package_name}"
            # print(npm_url)

            response = requests.get(npm_url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            soup = BeautifulSoup(response.text, "html.parser")

            github_link_element = soup.select_one('a[href*="github.com"]')
            if github_link_element:
                github_link = github_link_element["href"]
                user_name = github_link.split('/')[3]
                repo_name = github_link.split('/')[4]
                if repo_name not in popular_npm_packages:
                    file.write(
                        f"{npm_package_name} {user_name} {repo_name} {github_link}\n")
            else:
                print(f"No GitHub link found for {npm_package_name}")

        except Exception as e:
            print(f"Error processing npm package '{npm_package_name}': {e}")

print("Done")
end_time = datetime.now()

# print time taken in minutes and seconds
print(f"Time taken: {end_time - start_time}")
