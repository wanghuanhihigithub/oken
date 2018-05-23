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