from bottle import route, run,request
import redis

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

def getFromRedis(coinType, request):
    fromType = request.query.fromType
    toType = request.query.toType
    conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
    return conn.get(coinType + "-" + fromType + "-" + toType)

run(host='localhost', port=9000)