import requests
from pprint import pprint
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"}
url = "https://baike.baidu.com/item/Python/407313"
res = requests.get(url, headers= headers)
res.encoding = 'utf8'
pprint(res.text)
