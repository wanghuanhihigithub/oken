#!/usr/bin/env python3
# -*- coding: utf-8 -*-



__author__ = 'Wang Huan'

' url handlers '

from coroweb import get

import logging; logging.basicConfig(level=logging.INFO)

import redis
import requests
import json
import datetime
from datetime import datetime

@get("/api/coinsVs")
def api_getCoinsVs():
   return getFromVsTo()

def getFromVsTo():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
    print(conn.get(now))
    if(conn.get(now) != None):
        return conn.get(now)
    trade_url = "https://www.okex.com/v2/futures/market/indexTicker?symbol=f_usd_btc"
    r = requests.get(trade_url)
    if (r.status_code == 200):
        text = json.loads(r.text)
        text["createdTime"] = now
        conn.set(now, text)
        return text

@get("/api/huobiCoinsVs")
def api_getHuobiCoinsVs():
    conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
    return conn.get("usdt-btc")

