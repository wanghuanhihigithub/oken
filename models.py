#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for Usdt
'''

__author__ = 'Wang Huan'

from orm import Model, StringField, BooleanField, FloatField, IntegerField,DateTimeField,TextField,MediumTextField
import time, uuid


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

#usdt详情类
class SysSetting(Model):
    __table__ = 'sys_setting'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    enableSms = BooleanField()
    smsSendInterval = IntegerField()
    smsReceiver = StringField(ddl='varchar(100)')

class SmsLog(Model):
    __table__ = 'sms_log'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    lastSendTime = StringField(ddl='varchar(100)')

class CoinProfit(Model):
    __table__ = 'coin'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    fromType = StringField(ddl='varchar(10)')
    toType = StringField(ddl='varchar(10)')
    fromMinSalePrice = FloatField()
    fromMaxBuyPrice = FloatField()
    toMinSalePrice = FloatField()
    toMaxBuyPrice = FloatField()
    lastVs = FloatField()
    buy = FloatField()
    sell = FloatField()
    fromJson = MediumTextField()
    toJson = MediumTextField()
    vsJson = StringField(ddl='varchar(1000)')
    fromToProfit = FloatField()
    toFromProfit = FloatField()
    createdTime = StringField(ddl='varchar(100)')