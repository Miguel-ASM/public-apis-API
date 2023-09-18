import requests


PUBLIC_APIS_README_URI = 'https://raw.githubusercontent.com/public-apis/public-apis/master/README.md'

response = requests.get(PUBLIC_APIS_README_URI)

print( response.text )