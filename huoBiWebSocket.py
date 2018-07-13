import gzip
import json
import threading

import websocket
from datetime import datetime
import time
import redis

#火币ws地址
huobi_ws_url = "wss://api.huobi.pro/ws"

#创建数据库连接池
def create_pool():
    pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0)
    global __redis
    __redis = redis.Redis(connection_pool=pool)
    global __pipe
    __pipe = __redis.pipeline(transaction=True)
    print(__redis, __pipe)

def on_message(ws, message):
    unzipped_data = gzip.decompress(message).decode()
    msg_dict = json.loads(unzipped_data)
    for i in msg_dict:
        if(i != "data"):
            print(i,"===", msg_dict[i])
    '''if("data" in msg_dict):
        data = msg_dict["data"]
        new = data[len(data) - 1]
        new["createdTime"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("new", new)
        __redis.set('usdt-btc', new)
        __pipe.execute()'''



def on_error(ws, error):
    print("Error: " + str(error))
    error = gzip.decompress(error).decode()
    print(error)


def on_close(ws):
    print("### closed ###")
    #runHuoBiWebsocket()

def on_open(ws):
    def run(*args):
        # # 每2秒请求一次K线图，请求5次
        while(True):
            time.sleep(2)
            ws.send(json.dumps({"req": "market.btcusdt.kline.1min", "id": "id1"}).encode())
            ws.send(json.dumps({"req": "market.ethusdt.kline.1min", "id": "id1"}).encode())
        ws.close()
        print("thread terminating...")

    t = threading.Thread(target=run, args=())
    t.start()

#运行火币ws
def runHuoBiWebsocket():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        huobi_ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

#主程序
if __name__ == "__main__":
    create_pool()
    runHuoBiWebsocket()
