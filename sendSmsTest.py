import ssl

from urllib import request, parse



host = 'https://fesms.market.alicloudapi.com'
path = '/smsmsg'
method = 'GET'
appcode = '9fc05d770b0445fe8bc096753f6bef93'
print("2018-06-13 10:45:12".replace(" ","("))
querys = 'param=2018-06-13(10:56:12|usdt|eos|100&phone=18980028490&sign=1&skin=9303'
url = host + path + '?' + querys

req = request.Request(url)
req.add_header('Authorization', 'APPCODE ' + appcode)

with request.urlopen(req) as f:
    print('Status:', f.status, f.reason)
    print(f)