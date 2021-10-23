import requests

url = 'http://api.bilibili.cn/recommend'

data = {'tid': 23, 'order': 'new'}
rep = requests.get(url, params=data).json()
print(rep)
vlist = rep['list']
vdict = {}
for index, item in enumerate(vlist):
    v = {'aid': item['aid'], 'title': item['title']}
    vdict.update({index: v})

print(vdict.values())
