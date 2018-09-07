from bottle import route, run,request
import redis
import requests
import json


@route("/api/oken")
def get_oken():
    return getFromRedis("oken", request)


@route("/api/huoBi")
def get_huoBi():
   return getFromRedis("huoBi", request)


@route("/api/fcoin")
def get_fcoin():
   return getFromRedis("fcoin", request)


@route("/api/coinEx")
def get_coinEx():
    return getFromRedis("coinEx", request)


@route("/api/oken/change")
def getOkenChange():
    side = request.query.side
    url = "https://www.okex.com/v3/c2c/tradingOrders/book?side=all&baseCurrency=" + request.query.baseCurrency + "&quoteCurrency=cny&userType=certified&paymentMethod=all"
    r = requests.get(url, timeout=2)
    data = json.loads(r.text)["data"]["buy"]
    if("sell" == side):
        data = json.loads(r.text)["data"]["sell"]
    for i in data:
        if(i["creator"]["nickName"] == request.query.nickName):
            #if(i["quoteMinAmountPerOrder"] == int(request.query.quoteMinAmountPerOrder)):
            return i
    return None


def getFromRedis(coinType, request):
    fromType = request.query.fromType
    toType = request.query.toType
    conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
    return conn.get(coinType + "-" + fromType + "-" + toType)


run(host='localhost', port=9000)