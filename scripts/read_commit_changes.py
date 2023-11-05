# In the db, there is a table for keeping a record of the latest commit hash in the public apis repo.
# Every day I will run a job that checks if the last commit in the db is different from the current commit in the repo.
# If they hashes are equal then the job has finished.
# If they don't match then I will fetch and parse the contents of the readmes of my the last commit and the repos current commit.
# If they are equal, I just keep the record of the last commit and finish the job.

import requests
import os
import re
import json
from services.extract_apis_data_from_readme import parsereadmetext
from services.crawl_public_apis_data import fetchreadme
from utils.iter import find

GITHUB_API_TOKEN = os.getenv('GITHUB_API_TOKEN')


repo = 'public-apis'
github_user = 'public-apis'

url = f"https://api.github.com/repos/{github_user}/{repo}/compare/aac6b00424df8fa35b9fce3a4c319e71a6062887...master"
 

headers = {
  "Authorization": GITHUB_API_TOKEN,
  "Accept": "application/vnd.github+json",
  "X-GitHub-Api-Version": "2022-11-28"
}


response = requests.get(url, headers=headers)
data = response.json()

readme_file_changes = find(
  lambda x: x['filename']=='README.md',
  data['files']
)

readme_file_diff = readme_file_changes.get('patch',None)


api_diff_line_regex = r'(?P<diff_type>[\+\-])\| \[(?P<name>.*?)\]\((?P<url>.*?)\) \| (?P<description>.*?) \| (?P<authentication>.*?) \| (?P<https>.*?) \| (?P<cors>.*?) \|'

matches = re.finditer(api_diff_line_regex,readme_file_diff,re.MULTILINE)


with open('diff.json','w') as file:
  json.dump([m.groupdict() for m in matches],file,indent=2)

