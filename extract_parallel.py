import concurrent.futures
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import time


def process_npm_package(npm_package_name):
    try:
        # npm_url = f"https://www.npmjs.com/package/{npm_package_name}"
        npm_url = f"https://www.npmjs.com/package/@adobe/firefly-apis"
        response = requests.get(npm_url)
        response.raise_for_status()
        # soup = BeautifulSoup(response.text, "html.parser")
        soup = BeautifulSoup(response.text, "lxml")
        
        # github_link_element = soup.select_one('a[href*="github.com"]')
        github_link_element_all = [link["href"] for link in soup.select('a[href*="github.com"]')]
        for x in github_link_element_all:
            # count no of "/" in the link
            if x.count("/") ==4:
                github_link_element=x
                break
        # print(github_link_element)
        if github_link_element:
            github_link = github_link_element
            user_name = github_link.split('/')[3]
            repo_name = github_link.split('/')[4]
            file_lock = threading.Lock()
            if repo_name not in popular_npm_packages:
                with file_lock:
                    with open("gh_link_test.txt", "a") as file:
                        file.write(
                            f"{npm_package_name} {user_name} {repo_name} {github_link}\n")
        else:
            print(f"No GitHub link found for {npm_package_name}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error connecting to the server: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    except Exception as e:
        print(
            f"Unexpected error processing npm package '{npm_package_name}': {e}")


start_time = datetime.now()
# Define the list of popular npm packages
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

with open("names.json", "r") as file:
    npm_package_names = file.read().splitlines()


npm_package_names= npm_package_names[:100]
# npm_package_names = npm_package_names[10000:100000]

for x in range(0, len(npm_package_names)):
    npm_package_names[x] = npm_package_names[x].split()[0]
    npm_package_names[x] = npm_package_names[x].replace('"', '')
    npm_package_names[x] = npm_package_names[x].replace(',', '')

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     # executor.map(process_npm_package, npm_package_names)
#     for i, npm_package_name in enumerate(npm_package_names, start=1):
#         executor.submit(process_npm_package, npm_package_name)
#         if i % 100 == 0:
#             time.sleep(1)
process_npm_package("test")

print("Done")
end_time = datetime.now()
print(f"Time taken: {end_time - start_time}")
