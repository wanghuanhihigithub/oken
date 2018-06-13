#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Wang Huan'

' url handlers '

from coroweb import get, post

from models import CoinProfit,SysSetting, SmsLog
from config import configs
import requests
import json

from decimal import Decimal
from datetime import datetime
import logging; logging.basicConfig(level=logging.INFO)
import asyncio
from apis import Page
from urllib import request

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

#全局的header
headers = {
    'authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiI4MzEzMzExOC1mZmE4LTRhNmUtODEzYS1hOTg4Y2FjMDVlNWJYQ2tOIiwidWlkIjoiM2xuNzNkSmxtNXJhQzZIK0RtWG9Rdz09Iiwic3ViIjoiMTg5KioqODQ5MCIsInN0YSI6MCwibWlkIjowLCJpYXQiOjE1Mjg4NTU0MTYsImV4cCI6MTUyOTQ2MDIxNiwiaXNzIjoib2tjb2luIn0.oUbH0k5-0vY5jehWg1F7KtvIcDCo8o-274LNBYvYCL1sfV_QWW7eDVI-qq3u5MyxPl9ixoPuXG3Ckzq1NWWnfA',
    'content-type': 'application/json',
    'cookie': '__cfduid=d268f871c1f8ddf6683c1293165f5ee831525785471; locale=zh_CN; _ga=GA1.2.1105539038.1525785471; first_ref=https://www.okex.com/account/login.htm; perm=85E2BB8DDAF5EC8B4DAB9C6429D20733; _gid=GA1.2.1414655093.1526568686; Hm_lvt_b4e1f9d04a77cfd5db302bc2bcc6fe45=1525785472,1526568686,1526644458; isLogin=1; product=btc_usdt; lp=/future/trade; Hm_lpvt_b4e1f9d04a77cfd5db302bc2bcc6fe45=1526649066; ref=https://www.okex.com/futureTrade/beforeFuture; _gat_gtag_UA_115738092_1=1',
    'referer': 'https://www.okex.com/fiat/c2c',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
}

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()

@get('/api/coins')
def api_get_coins():
    return (yield from CoinProfit.findAll(orderBy='createdTime desc', limit=(0, 10)))

@post('/api/setting/{id}')
def api_update_setting(id, request, *, enableSms, smsSendInterval, smsReceiver):
    setting = yield from SysSetting.find(id)
    setting.enableSms = enableSms
    setting.smsSendInterval = smsSendInterval
    setting.smsReceiver = smsReceiver
    yield from setting.update()
    return setting

@get('/api/setting/{id}')
def api_get_setting(*, id):
    setting = yield from SysSetting.find(id)
    return setting

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p

@get('/api/coins/params')
def api_get_coins_by_params(*, page='1',createdTimeStart='',createdTimeEnd=''):
    where = 'createdTime>\'' + createdTimeStart + '\' and createdTime<\'' + createdTimeEnd + "\' and (fromToProfit > 0 || toFromProfit > 0)"
    page_index = get_page_index(page)
    num = yield from CoinProfit.findNumber('count(id)', where=where)
    page = Page(num, page_index)
    if num == 0:
       coins = []
    else:
       coins = yield from CoinProfit.findAll(where=where, orderBy='createdTime desc', limit=(page.offset, page.limit))
    return {
        'page': page,
        'coins': coins
    }

def getMaxBuyPrice(priceList):
    for i in priceList["data"]["buyTradingOrders"]:
        return i['exchangeRate']

def getMinSalePrice(priceList):
    minPrice = 0
    for i in priceList["data"]["sellTradingOrders"]:
        minPrice = i['exchangeRate']
    return minPrice

@asyncio.coroutine
def getCoinProfit(fromPrice, fromType, fromMinSalePrice, fromMaxBuyPrice, toType):
    # 获取toType的法币交易价格
    toPrice = getCoinPrice(toType)
    # 获取btc最低卖价
    toMinSalePrice = getMinSalePrice(toPrice)
    # 获取btc最高买入价
    toMaxBuyPrice = getMaxBuyPrice(toPrice)
    fromVsTo = getFromVsTo(fromType, toType)
    fromVsTo_buy = fromVsTo["ticker"]["buy"]
    fromToProfit = 50000 * Decimal(toMaxBuyPrice) / Decimal(fromVsTo_buy) / Decimal(fromMinSalePrice) - 50000 - 100
    toFromProfit = 50000 / Decimal(toMinSalePrice) * Decimal(fromVsTo_buy) * Decimal(fromMaxBuyPrice) - 50000 - 100
    coinProfit = CoinProfit()
    coinProfit.fromType = fromType
    coinProfit.toType = toType
    coinProfit.fromMaxBuyPrice = fromMaxBuyPrice
    coinProfit.fromMinSalePrice = fromMinSalePrice
    coinProfit.toMaxBuyPrice = toMaxBuyPrice
    coinProfit.toMinSalePrice = toMinSalePrice
    #coinProfit.fromJson = json.dumps(fromPrice)
    #coinProfit.toJson = json.dumps(toPrice)
    #coinProfit.vsJson = json.dumps(fromVsTo)
    coinProfit.fromJson = ''
    coinProfit.toJson =''
    coinProfit.vsJson = ''
    coinProfit.buy = fromVsTo["ticker"]["buy"]
    coinProfit.sell = fromVsTo["ticker"]["sell"]
    coinProfit.lastVs = fromVsTo["ticker"]["last"]
    coinProfit.fromToProfit = Decimal(fromToProfit).quantize(Decimal('0.00'))
    coinProfit.toFromProfit = Decimal(toFromProfit).quantize(Decimal('0.00'))
    coinProfit.createdTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(coinProfit)
    yield from sendSms(coinProfit)
    yield from CoinProfit.save(coinProfit)


def getFromVsTo(fromType, toType):
    # 获取btc和usdt的数量对比
    trade_url = "https://www.okex.com/api/v1/ticker.do?symbol=" + toType + "_" + fromType
    r = requests.get(trade_url, headers=headers)
    if (r.status_code != 200):
        logging.info('请求oken网数据异常', r.text)
    return json.loads(r.text)

#根据币种类型获取币种价格
def getCoinPrice(coinType):
    trade_url = "https://www.okex.com/v2/c2c-open/tradingOrders/group?digitalCurrencySymbol=" + coinType + "&legalCurrencySymbol=cny&best=0&exchangeRateLevel=0&paySupport=0"
    r = requests.get(trade_url, headers=headers)
    if(r.status_code != 200):
        logging.info('请求oken网数据异常', r.text)
    return json.loads(r.text)


@asyncio.coroutine
def fun_timer():
    print(datetime.now(),'Hello Timer!')
    # 先获取usdt价格作为基准价格
    fromType = "usdt"
    fromPrice = getCoinPrice(fromType)
    print(fromPrice)
    # 获取fromType最低卖价
    fromMinSalePrice = getMinSalePrice(fromPrice)
    # 获取fromType最高买入价
    fromMaxBuyPrice = getMaxBuyPrice(fromPrice)
    yield from getCoinProfit(fromPrice, fromType, fromMinSalePrice, fromMaxBuyPrice, "btc")
    yield from getCoinProfit(fromPrice, fromType, fromMinSalePrice, fromMaxBuyPrice, "eos")
    yield from getCoinProfit(fromPrice, fromType, fromMinSalePrice, fromMaxBuyPrice, "eth")
    #global timer
    #timer = threading.Timer(2, fun_timer)
    #timer.start()

@asyncio.coroutine
def sendSms(coinProfit):

    #如果利润为0 不发送短信
    if((coinProfit.fromToProfit < 0) & (coinProfit.toFromProfit < 0)):
        return
    #如果不允许发送短信返回
    setting = yield from SysSetting.find("1")
    if(setting.enableSms != 1):
        return
    #如果没有电话号码收件人
    if(setting.smsReceiver.strip()==''):
        return

    #如果是在已经发送的时间范围内
    smsLog = yield from SmsLog.find("1")
    if(smsLog.lastSendTime != ""):
        if(datetime.now().time() - datetime.strptime(smsLog.lastSendTime,'%Y-%m-%d %H:%M:%S' )< setting.smsSendInterval * 60 * 1000):
            return

    host = 'https://fesms.market.alicloudapi.com'
    path = '/smsmsg'
    appcode = '9fc05d770b0445fe8bc096753f6bef93'
    param = coinProfit.createdTime.replace(" ","(") + "|" + coinProfit.fromType + "|" + coinProfit.toType + "|" + str(coinProfit.fromToProfit)
    if (coinProfit.fromToProfit < 0):
        param = coinProfit.createdTime.replace(" ", "(") + "|" + coinProfit.toType + "|" + coinProfit.fromType + "|" + str(
            coinProfit.toFromProfit)
    querys = 'param=' + param + "&phone=" + setting.smsReceiver + '&sign=1&skin=9303'
    url = host + path + '?' + querys

    req = request.Request(url)
    req.add_header('Authorization', 'APPCODE ' + appcode)

    with request.urlopen(req) as f:
        if(f.status == 200):
            smsLog.lastSendTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
