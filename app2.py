from bottle import route, run
import redis
import requests
import json
import datetime
from datetime import datetime
from fcoin import Fcoin

@route("/api/coinsVs")
def api_getCoinsVs():
        return getFromVsTo()

@route("/api/huobiCoinsVs")
def api_getHuobiCoinsVs():
    conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
    return conn.get("usdt-btc")


@route("/api/fcoinVs")
def api_getFcoinVs():
    fcoin = Fcoin(api_key, api_secret)
    ticket = fcoin.get_ticket("btcusdt")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ticket["createdTime"] = now
    return ticket


@route("/api/coinEx")
def api_getCoinEx():
    trade_url = "https://api.coinex.com/v1/market/ticker?market=btcusdt"
    r = requests.get(trade_url, timeout=2)
    if (r.status_code == 200):
        text = json.loads(r.text)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        text["createdTime"] = now
        return text


def getFromVsTo():
    trade_url = "https://www.okex.com/api/v1/ticker.do?symbol=btc_usdt"
    r = requests.get(trade_url, timeout=2)
    if (r.status_code == 200):
        text = json.loads(r.text)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        text["createdTime"] = now
        return text

api_key = "dcda9f2b36584b7d81f9eeb7f3465e7e"
api_secret = "78bff669d4f24c2f85f17c0b71c52f37"

run(host='localhost', port=9001)