#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for Usdt
'''

__author__ = 'Wang Huan'

from orm import Model, StringField, BooleanField, FloatField, IntegerField

#usdt详情类
class Usdt(Model):
    __table__ = 'usdt'

    acceptOrder = BooleanField()
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
    clientName = StringField(ddl='varchar(50)')
    clientPaymentSecondsAvg = StringField(ddl='varchar(20)')
    completedAmount = FloatField()
    completedOrderQuantity = IntegerField()
    completedOrderTotal = FloatField()
    createdDate = IntegerField()
    digitalCurrencySymbol = StringField(ddl='varchar(20)')
    exchangeRate = FloatField()
    exchangeRateDeviateTooFar = BooleanField()
    existPhone = BooleanField()
    floatRate = IntegerField()
    frozenAmount = IntegerField()
    index = IntegerField()
    isBuy = BooleanField()
    legalCurrencySymbol = StringField(ddl='varchar(20)')
    maxPlacePrice = IntegerField()
    minKycLevel = IntegerField()
    minPlacePrice = FloatField()
    publicTradingOrderId = IntegerField(primary_key=True)
    type = IntegerField()
