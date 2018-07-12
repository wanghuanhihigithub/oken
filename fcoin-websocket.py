import gzip
import json
import threading

import websocket
from datetime import datetime
import redis
import time

def create_pool():
    pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0)
    global __redis
    __redis = redis.Redis(connection_pool=pool)
    global __pipe
    __pipe = __redis.pipeline(transaction=True)
    print(__redis, __pipe)

def send_message(ws, message_dict):
    data = json.dumps(message_dict)
    print("sendMessage", data)
    ws.send(data)

def on_message(ws, message):
   print(message)


def on_error(ws, error):
    print("Error: " + str(error))
    error = gzip.decompress(error).decode()
    print(error)


def on_close(ws):
    print("### closed ###")
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "wss://api.huobi.pro/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

def on_open(ws):
    def run(*args):
        data  = {
            'cmd':'req',
            'args':["ticker.btcusdt"],
            'id':'1'

        }
        # # 每2秒请求一次K线图，请求5次
        while(True):
            time.sleep(2)
            send_message(ws, data)
        ws.close()
        print("thread terminating...")

    t = threading.Thread(target=run, args=())
    t.start()

#主程序
if __name__ == "__main__":
    create_pool()
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "wss://ws.fcoin.com/api/v2/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()
