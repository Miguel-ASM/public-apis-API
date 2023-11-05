# In the db, there is a table for keeping a record of the latest commit hash in the public apis repo.
# Every day I will run a job that checks if the last commit in the db is different from the current commit in the repo.
# If they hashes are equal then the job has finished.
# If they don't match then I will fetch and parse the contents of the readmes of my the last commit and the repos current commit.
# If they are equal, I just keep the record of the last commit and finish the job.

import requests
import os
import json
from services.extract_apis_data_from_readme import parsereadmetext
from services.crawl_public_apis_data import fetchreadme

GITHUB_API_TOKEN = os.getenv('GITHUB_API_TOKEN')


repo = 'public-apis'
github_user = 'public-apis'

url = f"https://api.github.com/repos/{github_user}/{repo}/commits"
 
headers = {
  "Authorization": GITHUB_API_TOKEN,
  "Accept": "application/vnd.github+json",
  "X-GitHub-Api-Version": "2022-11-28"
}

query_params = {
  'per_page': 1,
  'path': 'README.md'
}

response = requests.get(url, headers=headers,params=query_params)
data = response.json()

repo_current_commit = data[0] if len(data)>0 else None

repo_current_commit_sha = repo_current_commit['sha']
repo_current_commit_date = repo_current_commit['commit']['author']['date']

print(json.dumps(repo_current_commit,indent=4))
print(repo_current_commit_sha,repo_current_commit_date)

