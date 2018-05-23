#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

' url handlers '

from coroweb import get, post

from models import Usdt
from config import configs
import requests
import json

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()

@get('/usdts')
def api_get_usdts():
    trade_url = "https://www.okex.com/v2/c2c-open/tradingOrders/group?digitalCurrencySymbol=usdt&legalCurrencySymbol=cny&best=0&exchangeRateLevel=0&paySupport=0"
    headers = {
        'authorization': '',
        'content-type': 'application/json',
        'cookie': '__cfduid=d268f871c1f8ddf6683c1293165f5ee831525785471; locale=zh_CN; _ga=GA1.2.1105539038.1525785471; first_ref=https://www.okex.com/account/login.htm; perm=85E2BB8DDAF5EC8B4DAB9C6429D20733; _gid=GA1.2.1414655093.1526568686; Hm_lvt_b4e1f9d04a77cfd5db302bc2bcc6fe45=1525785472,1526568686,1526644458; isLogin=1; product=btc_usdt; lp=/future/trade; Hm_lpvt_b4e1f9d04a77cfd5db302bc2bcc6fe45=1526649066; ref=https://www.okex.com/futureTrade/beforeFuture; _gat_gtag_UA_115738092_1=1',
        'referer': 'https://www.okex.com/fiat/c2c',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
    r = requests.get(trade_url, headers=headers)
    usdts = json.loads(r.text)
    for i in usdts["data"]["buyTradingOrders"]:
        yield from Usdt.save(dict2obj(Usdt(), i))
    usdts = yield from Usdt.findAll()
    return usdts

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