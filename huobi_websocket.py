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

def send_message(ws, message_dict):
    data = json.dumps(message_dict).encode()
    ws.send(data)

def on_message(ws, message):
    unzipped_data = gzip.decompress(message).decode()
    msg_dict = json.loads(unzipped_data)
    if("data" in msg_dict):
        data = msg_dict["data"]
        new = data[len(data) - 1]
        new["createdTime"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #conn.set('usdt-btc', new)
        __redis.set('new',new)
        __pipe.execute()
        if 'ping' in msg_dict:
            data = {
                "pong": msg_dict['ping']
            }
            send_message(ws, data)


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
        data = {
            "req": "market.btcusdt.kline.1min",
            "id": "id1"
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
        "wss://api.huobi.pro/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()
