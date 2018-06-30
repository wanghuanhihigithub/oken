from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os
import requests
import json
import redis

scheduler = BlockingScheduler()

#全局的header
headers = {
    'authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiIxMDA1OTIzZi05ODVmLTQyMDItYjNjYi1mMzA5ZjcxZWYxNjlXeUt4IiwidWlkIjoiM2xuNzNkSmxtNXJhQzZIK0RtWG9Rdz09Iiwic3ViIjoiMTg5KioqODQ5MCIsInN0YSI6MCwibWlkIjowLCJpYXQiOjE1MzAzMjY4NTMsImV4cCI6MTUzMDkzMTY1MywiYmlkIjowLCJpc3MiOiJva2NvaW4ifQ.lj-YqBqo6R8sfGzaYQ0n5GINdAh7gHX-h_q9959PMHfBWCIhsuvD_z48X3PCha6gPYu-E1Q4-CLEFSYXy__49A',
    'content-type': 'application/json',
    'cookie': '__cfduid=d268f871c1f8ddf6683c1293165f5ee831525785471; locale=zh_CN; _ga=GA1.2.1105539038.1525785471; first_ref=https://www.okex.com/account/login.htm; perm=85E2BB8DDAF5EC8B4DAB9C6429D20733; _gid=GA1.2.1414655093.1526568686; Hm_lvt_b4e1f9d04a77cfd5db302bc2bcc6fe45=1525785472,1526568686,1526644458; isLogin=1; product=btc_usdt; lp=/future/trade; Hm_lpvt_b4e1f9d04a77cfd5db302bc2bcc6fe45=1526649066; ref=https://www.okex.com/futureTrade/beforeFuture; _gat_gtag_UA_115738092_1=1',
    'referer': 'https://www.okex.com/fiat/c2c',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
}

@scheduler.scheduled_job('interval', seconds=1)
def getFromVsTo():
    trade_url = "https://www.okex.com/v2/futures/market/indexTicker?symbol=f_usd_btc"
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