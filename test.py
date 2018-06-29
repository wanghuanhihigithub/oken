import fcoin
import time

api = fcoin.authorize('key', 'secret', int(round(time.time() * 1000)))
api.market.get_ticker("ethbtc")
