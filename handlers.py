#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Wang Huan'

' url handlers '

from coroweb import get, post

from models import CoinProfit
from config import configs
import requests
import json

from  decimal import Decimal

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret


#全局的header
headers = {
    'authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiJiZjk5YzNkMS02YWU3LTQ5ZDgtYTM5Yi01MTdkNjY5ZDJlYTRka1hhIiwidWlkIjoiM2xuNzNkSmxtNXJhQzZIK0RtWG9Rdz09Iiwic3ViIjoiMTg5KioqODQ5MCIsInN0YSI6MCwibWlkIjowLCJpYXQiOjE1MjczMTA0ODYsImV4cCI6MTUyNzkxNTI4NiwiaXNzIjoib2tjb2luIn0.pelyCGEJOl3X4qs0N6bl4W7gST5M4X95Aq-PogB5TNGUHgjUA2wEuI1sJ2NnH0p9Q-IatfyZp5ZkoTgalMaNpg',
    'content-type': 'application/json',
    'cookie': '__cfduid=d268f871c1f8ddf6683c1293165f5ee831525785471; locale=zh_CN; _ga=GA1.2.1105539038.1525785471; first_ref=https://www.okex.com/account/login.htm; perm=85E2BB8DDAF5EC8B4DAB9C6429D20733; _gid=GA1.2.1414655093.1526568686; Hm_lvt_b4e1f9d04a77cfd5db302bc2bcc6fe45=1525785472,1526568686,1526644458; isLogin=1; product=btc_usdt; lp=/future/trade; Hm_lpvt_b4e1f9d04a77cfd5db302bc2bcc6fe45=1526649066; ref=https://www.okex.com/futureTrade/beforeFuture; _gat_gtag_UA_115738092_1=1',
    'referer': 'https://www.okex.com/fiat/c2c',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
}

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()

@get('/usdts')
def api_get_usdts():
    #获取btcPrice
    btcPrice = getBtcPrice()
    #获取btc最低卖价
    btcMinSalePrice = getMinSalePrice(btcPrice)
    #获取btc最高买入价
    btcMaxBuyPrice = getMaxBuyPrice(btcPrice)
    btcVsUsdt = getBtcVsUsdt()
    btcVsUsdt_low = btcVsUsdt["ticker"]["buy"]
    usdtPrice = getUsdtPrice()
    # 获取usdt最低卖价
    usdtMinSalePrice = getMinSalePrice(usdtPrice)
    # 获取usdt最高买入价
    usdtMaxBuyPrice = getMaxBuyPrice(usdtPrice)
    print("50000/usdt最低买价/usdt-btc的个数 * btc的最高卖价- 50000 - 100")
    fromToProfit = 50000 * Decimal(btcMaxBuyPrice) / Decimal(btcVsUsdt_low) /Decimal(usdtMinSalePrice) -50000 - 100
    print("usdt-btc的最大利润", (50000 * Decimal(btcMaxBuyPrice) / Decimal(btcVsUsdt_low) /Decimal(usdtMinSalePrice) -50000 - 100))
    print("50000/btc最低买价 * usdt-btc的个数 * usdt的最高卖价-50000 - 100")
    toFromProfit = 50000 / Decimal(btcMinSalePrice) * Decimal(btcVsUsdt_low) * Decimal(usdtMaxBuyPrice) -50000 -100
    coinProfit = CoinProfit()
    coinProfit.fromType = "usdt"
    coinProfit.toType = "btc"
    coinProfit.fromMaxBuyPrice = usdtMaxBuyPrice
    coinProfit.fromMinSalePrice = usdtMinSalePrice
    coinProfit.toMaxBuyPrice = btcMaxBuyPrice
    coinProfit.toMinSalePrice = btcMinSalePrice
    coinProfit.fromJson = json.dumps(usdtPrice)
    coinProfit.toJson = json.dumps(btcPrice)
    coinProfit.vsJson = json.dumps(btcVsUsdt)
    coinProfit.buy = btcVsUsdt["ticker"]["buy"]
    coinProfit.sell = btcVsUsdt["ticker"]["sell"]
    coinProfit.lastVs = btcVsUsdt["ticker"]["last"]
    coinProfit.fromToProfit = fromToProfit
    coinProfit.toFromProfit = toFromProfit
    yield from CoinProfit.save(coinProfit)
    return (yield from CoinProfit.findAll(orderBy='createdTime desc'))

# 将class转dict,以_开头的属性不要
def props(obj):
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not callable(value) and not name.startswith('_'):
            pr[name] = value
    return pr
# 将class转dict,以_开头的也要
def props_with_(obj):
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not callable(value):
            pr[name] = value
    return pr


# dict转obj，先初始化一个obj
def dict2obj(obj,dict):
    obj.__dict__.update(dict)
    return obj


#获取usdt的买入/卖出价
def getUsdtPrice():
    trade_url = "https://www.okex.com/v2/c2c-open/tradingOrders/group?digitalCurrencySymbol=usdt&legalCurrencySymbol=cny&best=0&exchangeRateLevel=0&paySupport=0"
    r = requests.get(trade_url, headers=headers)
    return json.loads(r.text)


#获取btc和usdt的数量对比
def getBtcVsUsdt():
    trade_url = "https://www.okex.com/api/v1/ticker.do?symbol=btc_usdt"
    r = requests.get(trade_url, headers=headers)
    return json.loads(r.text)

def getBtcPrice():
    trade_url = "https://www.okex.com/v2/c2c-open/tradingOrders/group?digitalCurrencySymbol=btc&legalCurrencySymbol=cny&best=0&exchangeRateLevel=0&paySupport=0"
    r = requests.get(trade_url, headers=headers)
    return json.loads(r.text)

def getMaxBuyPrice(priceList):
    for i in priceList["data"]["buyTradingOrders"]:
        return i['exchangeRate']

def getMinSalePrice(priceList):
    minPrice = 0
    for i in priceList["data"]["sellTradingOrders"]:
        minPrice = i['exchangeRate']
    return minPrice