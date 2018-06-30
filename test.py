import fcoin

api = fcoin.authorize('dcda9f2b36584b7d81f9eeb7f3465e7e', '78bff669d4f24c2f85f17c0b71c52f37')
t = api.get_ticker("ethbtc")
#t = api.market.get_ticker("ethbtc")
print(t)
