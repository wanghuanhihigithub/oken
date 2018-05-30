#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for Usdt
'''

__author__ = 'Wang Huan'

from orm import Model, StringField, BooleanField, FloatField, IntegerField
import time, uuid

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

#usdt详情类
class Usdt(Model):
    __table__ = 'usdt'

    acceptOrder = BooleanField()
    # 数量
    availableAmount = FloatField()
    availableFromTime = StringField(ddl='varchar(20)')
    availableToTime = StringField(ddl='varchar(20)')
    best = IntegerField()
    blacker = BooleanField()
    canPlaceOrder = BooleanField()
    clientAvgCompletedTime = StringField(ddl='varchar(20)')
    clientAvgPaidTime = StringField(ddl='varchar(20)')
    clientCancelledOrderQuantity = IntegerField()
    clientCompletedOrderQuantity = IntegerField()
    clientCompletionSecondsAvg = StringField(ddl='varchar(20)')
    clientId = IntegerField()
    clientKycLevel = StringField(ddl='varchar(20)')
    # 委托人
    clientName = StringField(ddl='varchar(50)')
    clientPaymentSecondsAvg = StringField(ddl='varchar(20)')
    completedAmount = FloatField()
    completedOrderQuantity = IntegerField()
    # 所有金额
    completedOrderTotal = FloatField()
    createdDate = IntegerField()
    digitalCurrencySymbol = StringField(ddl='varchar(20)')
    # 价格
    exchangeRate = FloatField()
    exchangeRateDeviateTooFar = BooleanField()
    existPhone = BooleanField()
    floatRate = IntegerField()
    frozenAmount = IntegerField()
    index = IntegerField()
    # isBuy为false表示是卖出的单子 true表示是买入的订单
    isBuy = BooleanField()
    legalCurrencySymbol = StringField(ddl='varchar(20)')
    #单笔限额-高
    maxPlacePrice = IntegerField()
    minKycLevel = IntegerField()
    #单笔限额-低
    minPlacePrice = FloatField()
    publicTradingOrderId = IntegerField(primary_key=True)
    type = IntegerField()

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
    fromJson = StringField(ddl='varchar(1000)')
    toJson = StringField(ddl='varchar(1000)')
    vsJson = StringField(ddl='varchar(1000)')
    fromToProfit = FloatField()
    toFromProfit = FloatField()
    createdTime = FloatField(default=time.time)