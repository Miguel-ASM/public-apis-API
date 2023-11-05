import requests

# PUBLIC_APIS_README_URI = 'https://raw.githubusercontent.com/public-apis/public-apis/master/README.md'
# PUBLIC_APIS_README_URI = 'https://raw.githubusercontent.com/public-apis/public-apis/4ffa8107ca3041fdde19003888e4054b54011df5/README.md'

def fetchreadme(commit_sha=None):
  checkout = commit_sha or 'master'
  readme_url = f'https://raw.githubusercontent.com/public-apis/public-apis/{checkout}/README.md'
  try:
    response = requests.get(readme_url)
    return response.text
  except:
    raise Exception('Error when crawling the apis from repo readme')