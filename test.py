import fcoin
import time

api = fcoin.authorize('key', 'secret', int(round(time.time() * 1000)))
t = api.market.get_ticker("ethbtc")
print(t)
