import requests
from requests.auth import HTTPBasicAuth

url = "<URL>"

#myCookies = {'somekey': 'somevalue'}
#myHeaders = {'somekey': 'somevalue'}
#myProxies = {'http': 'somevalue', 'https': 'someothervalue'}
#myBasicAuth = HTTPBasicAuth('username', 'password')

# x = requests.post(url, cookies=myCookies, headers=myHeaders, proxies=myProxies, auth=myBasicAuth)
x = requests.get(url, data=myData)

print(x.text)
