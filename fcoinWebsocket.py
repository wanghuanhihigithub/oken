import gzip
import json
import threading

import websocket
import redis
import time
from datetime import datetime

#fcoin币的Ws接口
fcoin_ws_url = "wss://ws.fcoin.com/api/v2/ws"

def create_pool():
    pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0)
    global __redis
    __redis = redis.Redis(connection_pool=pool)
    global __pipe
    __pipe = __redis.pipeline(transaction=True)
    print(__redis, __pipe)

def on_message(ws, message):
    data = json.loads(message)["data"]
    type = data["type"]
    redisKey = None;
    if('ticker.btcusdt'== type):
        redisKey = "fcoin-usdt-btc"
    if("ticker.ethusdt" == type):
        redisKey = "fcoin-usdt-eth"

    if(redisKey != None):
       ticker = data["ticker"]
       ticker.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
       __redis.set(redisKey, ticker)
       __pipe.execute()


def on_error(ws, error):
    print("Error: " + str(error))
    error = gzip.decompress(error).decode()
    print(error)


def on_close(ws):
    print("### closed ###")
    runFcoinWs()

def on_open(ws):
    def run(*args):
        #每2秒请求一次K线图，请求5次
        while(True):
            time.sleep(2)
            ws.send(json.dumps({'cmd': 'req', 'args': ["ticker.btcusdt"], 'id': '1'}))
            ws.send(json.dumps({'cmd': 'req', 'args': ["ticker.ethusdt"], 'id': '1'}))
        ws.close()
        print("thread terminating...")

    t = threading.Thread(target=run, args=())
    t.start()

def runFcoinWs():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
       fcoin_ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

#主程序
if __name__ == "__main__":
    create_pool()
    runFcoinWs()
