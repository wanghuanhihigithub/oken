# -*- coding: utf-8 -*-
import requests

login_url = "https://www.okex.com/v3/users/login/login?loginName=18980028490" #登录地址
login_data = {"areaCode": 86, "loginName": "18980028490", "password": "ZHANGchao2020~8"}#登录信息
headers = {'content-type': 'application/json',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
           'authority': 'www.okex.com',
           'path': '/v3/users/login/login?loginName=18980028490',
           'app-type': 'web',
           'cookie':  '__cfduid=d268f871c1f8ddf6683c1293165f5ee831525785471; locale=zh_CN; _ga=GA1.2.1105539038.1525785471; first_ref=https://www.okex.com/account/login.htm; perm=85E2BB8DDAF5EC8B4DAB9C6429D20733; lp=; _gid=GA1.2.1414655093.1526568686; product=eth_usdt; Hm_lvt_b4e1f9d04a77cfd5db302bc2bcc6fe45=1525785472,1526568686,1526644458; Hm_lpvt_b4e1f9d04a77cfd5db302bc2bcc6fe45=1526645070; ref=https://www.okex.com/',
           'devid': '321a2514-357e-4d3d-9087-e9803eb66cc6',
           'loginname': '18980028490',
           'origin': ' https://www.okex.com',
           'referer': 'https://www.okex.com/account/login',
           'scheme':'https'
          }
r = requests.post(login_url, login_data, headers)
print(r.status_code)
print(r.text)


