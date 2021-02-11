import requests
from requests.auth import HTTPBasicAuth

url = "<URL>"

myData = {'somekey': 'somevalue'}
#myFiles = {'file': open('<FILEPATH>', 'rb')}
#myCookies = {'somekey': 'somevalue'}
#myHeaders = {'somekey': 'somevalue'}
#myProxies = {'http': 'somevalue', 'https': 'someothervalue'}
#myBasicAuth = HTTPBasicAuth('username', 'password')

# x = requests.post(url, data=myData, files=myFiles, cookies=myCookies, headers=myHeaders, proxies=myProxies, auth=myBasicAuth)
x = requests.post(url, data=myData)

print(x.text)
