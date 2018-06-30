#!/usr/bin/env python3
# -*- coding: utf-8 -*-



__author__ = 'Wang Huan'

' url handlers '

from coroweb import get

import logging; logging.basicConfig(level=logging.INFO)

import redis

@get("/api/coinsVs")
def api_getCoinsVs():
    conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
    return conn.get("oken-usdt-btc")

@get("/api/huobiCoinsVs")
def api_getHuobiCoinsVs():
    conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
    return conn.get("usdt-btc")

