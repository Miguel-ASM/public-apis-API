import requests
import os
from utils.iter import find
import re

from services.extract_apis_data_from_readme import cleanauthstring


GITHUB_API_TOKEN = os.getenv('GITHUB_API_TOKEN')
GITHUB_API_BASE_URL = 'https://api.github.com'

ADDED_APIS_REGEX = r'(?P<diff_type>\+)\| \[(?P<name>.*?)\]\((?P<url>.*?)\) \| (?P<description>.*?) \| (?P<auth>.*?) \| (?P<https>.*?) \| (?P<cors>.*?) \|'
REMOVED_APIS_REGEX = r'(?P<diff_type>\-)\| \[(?P<name>.*?)\]\((?P<url>.*?)\) \| (?P<description>.*?) \| (?P<auth>.*?) \| (?P<https>.*?) \| (?P<cors>.*?) \|'

repo = 'public-apis'
github_user = 'public-apis'

def getdatafromgithub(path,query_params=dict()):
  url = GITHUB_API_BASE_URL + path
  headers = {
    "Authorization": GITHUB_API_TOKEN,
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
  }
  response = requests.get(
    url,
    headers=headers,
    params=query_params
  )
  return response.json()

def getlastcommitdata():
  path = f"/repos/{github_user}/{repo}/commits"
  query_params = {
    'per_page': 1,
    'path': 'README.md',
    'sort': 'updated',
    'direction': 'desc'
  }
  return getdatafromgithub(path,query_params)[0]

def comparecommits(oldest_commit,newest_commit = 'master'):
  path = f"/repos/{github_user}/{repo}/compare/{oldest_commit}...{newest_commit}"
  return getdatafromgithub(path)

def getapischangesinapisrepo(oldest_commit,newest_commit = 'master'):
  compare_commits_data = comparecommits(oldest_commit,newest_commit)
  readme_file_changes = find(
    lambda x: x['filename']=='README.md',
    compare_commits_data['files']
  )

  readme_file_diff = readme_file_changes.get('patch',None)
  added_apis = list(
    match.groupdict() | { 'auth': cleanauthstring(match.groupdict()['auth']) } 
    for match in re.finditer(ADDED_APIS_REGEX,readme_file_diff,re.MULTILINE)
  )
  removed_apis = list(
    match.groupdict() | { 'auth': cleanauthstring(match.groupdict()['auth']) } 
    for match in re.finditer(REMOVED_APIS_REGEX,readme_file_diff,re.MULTILINE)
  )
  return {
    'added': added_apis,
    'removed': removed_apis
  }
