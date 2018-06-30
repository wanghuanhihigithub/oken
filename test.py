from bottle import route, run
import redis
import requests
import json
import datetime
from datetime import datetime

@route("/api/coinsVs")
def api_getCoinsVs():
   return getFromVsTo()

def getFromVsTo():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
    #if(conn.exists(now)):
       #return conn.get(now)
    trade_url = "https://www.okex.com/v2/futures/market/indexTicker?symbol=f_usd_btc"
    r = requests.get(trade_url)
    if (r.status_code == 200):
        text = json.loads(r.text)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        text["createdTime"] = now
        #conn.set(now, text)
        return text

run(host='localhost', port=9000)