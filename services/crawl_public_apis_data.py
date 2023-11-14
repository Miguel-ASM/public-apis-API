import requests

def fetchreadme(commit_sha=None):
  checkout = commit_sha or 'master'
  readme_url = f'https://raw.githubusercontent.com/public-apis/public-apis/{checkout}/README.md'
  try:
    response = requests.get(readme_url)
    return response.text
  except:
    raise Exception('Error when crawling the apis from repo readme')