from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os
import requests
import json
import redis

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', seconds=1)
def getFromVsTo():
    trade_url = "https://www.okex.com/api/v1/ticker.do?symbol=" + "usdt" + "_" + "btc"
    r = requests.get(trade_url)
    if (r.status_code == 200):
        text = json.loads(r.text)
        if(("error_code" in text) == False):
            text["createdTime"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(text, "===", datetime.now())
            conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
            conn.set('oken-usdt-btc', text)


#主程序
if __name__ == "__main__":
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except Exception:
        scheduler.shutdown()