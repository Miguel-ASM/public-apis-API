import requests

PUBLIC_APIS_README_URI = 'https://raw.githubusercontent.com/public-apis/public-apis/master/README.md'

def fetchreadme(url=PUBLIC_APIS_README_URI):
  try:
    response = requests.get(PUBLIC_APIS_README_URI)
    return response.text
  except:
    raise Exception('Error when crawling the apis from repo readme')