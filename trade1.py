# -*- coding: utf-8 -*-
import requests
import json

#获取btc和usdt币币交易比例
#trade_url ="https://www.okex.com/api/v1/ticker.do?symbol=btc_usdt"
trade_url = "https://www.okex.com/v2/futures/market/indexTickerAll.do"
trade_url = "https://www.okex.com/v2/c2c-open/tradingOrders/group?digitalCurrencySymbol=btc&legalCurrencySymbol=cny&best=0&exchangeRateLevel=0&paySupport=0"
trade_data = {}
trade_url = "https://www.okex.com/api/v1/ticker.do?symbol=btc_usdt"
headers = {
    'authorization':'eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiJiZjk5YzNkMS02YWU3LTQ5ZDgtYTM5Yi01MTdkNjY5ZDJlYTRka1hhIiwidWlkIjoiM2xuNzNkSmxtNXJhQzZIK0RtWG9Rdz09Iiwic3ViIjoiMTg5KioqODQ5MCIsInN0YSI6MCwibWlkIjowLCJpYXQiOjE1MjczMTA0ODYsImV4cCI6MTUyNzkxNTI4NiwiaXNzIjoib2tjb2luIn0.pelyCGEJOl3X4qs0N6bl4W7gST5M4X95Aq-PogB5TNGUHgjUA2wEuI1sJ2NnH0p9Q-IatfyZp5ZkoTgalMaNpg',
    'content-type':'application/json',
    'cookie':'__cfduid=d268f871c1f8ddf6683c1293165f5ee831525785471; locale=zh_CN; _ga=GA1.2.1105539038.1525785471; first_ref=https://www.okex.com/account/login.htm; perm=85E2BB8DDAF5EC8B4DAB9C6429D20733; _gid=GA1.2.1414655093.1526568686; Hm_lvt_b4e1f9d04a77cfd5db302bc2bcc6fe45=1525785472,1526568686,1526644458; isLogin=1; product=btc_usdt; lp=/future/trade; Hm_lpvt_b4e1f9d04a77cfd5db302bc2bcc6fe45=1526649066; ref=https://www.okex.com/futureTrade/beforeFuture; _gat_gtag_UA_115738092_1=1',
    'referer':'https://www.okex.com/fiat/c2c',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
}
r = requests.get(trade_url, headers=headers)
btcPrice = json.loads(r.text)
minBtcPrice = 0
print(btcPrice)
for i in btcPrice["data"]["sellTradingOrders"]:
    minBtcPrice = i['exchangeRate']
    print(minBtcPrice)
print(minBtcPrice)
##for i in json.loads(r.text)['data']:
       # print(i['coinName'], i['last'] * i['usdCnyRate'])
        #print(round(i['last'] * i['usdCnyRate'], 2))

