import fcoin
import time

api = fcoin.authorize('key', 'secret')
t = api.get_ticker("ethbtc")
#t = api.market.get_ticker("ethbtc")
print(t)
