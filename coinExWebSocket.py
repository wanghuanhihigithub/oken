import json
import threading

import websocket
import redis
import time

#coinEx币的Ws接口
coinEx_ws_url = "wss://socket.coinex.com"

def create_pool():
    pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0)
    global __redis
    __redis = redis.Redis(connection_pool=pool)
    global __pipe
    __pipe = __redis.pipeline(transaction=True)
    print(__redis, __pipe)

def on_message(ws, message):
   print(message)


def on_error(ws, error):
    print("Error: " + str(error))


def on_close(ws):
    print("### closed ###")
    #runCoinExWs()

def on_open(ws):
    def run(*args):
        #每2秒请求一次K线图，请求5次
        while(True):
            time.sleep(2)
            ws.send(json.dumps({'method': 'state.query', 'params': ["BTCBCH",86400], 'id': '15'}))
            #ws.send(json.dumps({'cmd': 'req', 'args': ["ticker.ethusdt"], 'id': '1'}))
        ws.close()
        print("thread terminating...")

    t = threading.Thread(target=run, args=())
    t.start()

def runCoinExWs():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        coinEx_ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

#主程序
if __name__ == "__main__":
    create_pool()
    runCoinExWs()
