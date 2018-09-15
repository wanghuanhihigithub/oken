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
    conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
    data = conn.get("oken-" + side)
    if(data == None):
        return None
    data = data["data"]["buy"]
    if("sell" == side):
        data = data["data"]["sell"]
    for i in data:
        if(i["creator"]["nickName"] == request.query.nickName):
            return i
    return None


def getFromRedis(coinType, request):
    fromType = request.query.fromType
    toType = request.query.toType
    conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
    return conn.get(coinType + "-" + fromType + "-" + toType)


@route("/api/ubit/btc")
def get_coinEx():
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    r = requests.get(url, timeout=2)
    if(r.status_code == 200):
        return r.text
    return None

run(host='localhost', port=9000)