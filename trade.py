# -*- coding: utf-8 -*-
import requests
import json

trade_url = "https://www.okex.com/v2/c2c-open/tradingOrders/group?digitalCurrencySymbol=usdt&legalCurrencySymbol=cny&best=0&exchangeRateLevel=0&paySupport=0"
trade_data = {}
headers = {
    'authorization':'eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiJlYjZhYzY2MS1kNTc0LTQ1YTktOTg2MS00MzkxMzIwMGY0OGVQaU9yIiwidWlkIjoiM2xuNzNkSmxtNXJhQzZIK0RtWG9Rdz09Iiwic3ViIjoiMTg5KioqODQ5MCIsInN0YSI6MCwibWlkIjowLCJpYXQiOjE1MjY2NDY1MTksImV4cCI6MTUyNzI1MTMxOSwiaXNzIjoib2tjb2luIn0.AU-r-xYv8dB-FQS_pLJcwxPALTTzJolqY8NmLf1Cly_dnU-qfIlkTt0u0wRkfnwWLYF4iqD_Xbtruk_a9uwvag',
    'content-type':'application/json',
    'cookie':'__cfduid=d268f871c1f8ddf6683c1293165f5ee831525785471; locale=zh_CN; _ga=GA1.2.1105539038.1525785471; first_ref=https://www.okex.com/account/login.htm; perm=85E2BB8DDAF5EC8B4DAB9C6429D20733; _gid=GA1.2.1414655093.1526568686; Hm_lvt_b4e1f9d04a77cfd5db302bc2bcc6fe45=1525785472,1526568686,1526644458; isLogin=1; product=btc_usdt; lp=/future/trade; Hm_lpvt_b4e1f9d04a77cfd5db302bc2bcc6fe45=1526649066; ref=https://www.okex.com/futureTrade/beforeFuture; _gat_gtag_UA_115738092_1=1',
    'referer':'https://www.okex.com/fiat/c2c',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
}

r = requests.get(trade_url, headers=headers)
print(r.status_code)
print(r.text)
print(json.loads(r.text))
print(type(json.loads(r.text)))
