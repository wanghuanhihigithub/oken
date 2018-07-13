import gzip
import json
import threading

import websocket
import redis
import time

#OKEN币ws地址
oken_ws_url = "wss://real.okex.com:10441/websocket"
#火币ws地址
huoBi_ws_url = "wss://api.huobi.pro/ws"

#创建数据库连接池
def create_pool():
    pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0)
    global __redis
    __redis = redis.Redis(connection_pool=pool)
    global __pipe
    __pipe = __redis.pipeline(transaction=True)
    print(__redis, __pipe)

#OKEN币接收Usdt和Btc变更
def on_message(ws, message):
    message =  json.loads(message)[0]
    print(message)
    redisKey = None
    if("ok_sub_spot_btc_usdt_ticker" == message["channel"]):
        redisKey = "oken-usdt-btc"

    if("ok_sub_spot_eth_usdt_ticker" == message["channel"]):
        redisKey = "oken-usdt-eth"

    if(redisKey != None):
        ''' __redis.set('redisKey', json.loads(message)[0]["data"])
        __pipe.execute()'''

#oken币发生异常
def on_error(ws, error):
    print("ws报错: ", str(error))

#oken币开启ws代码
def on_open(ws):
    def run(*args):
        # # 每2秒请求一次K线图，请求5次
        while(True):
            time.sleep(2)
            ws.send("{'event':'addChannel','channel':'ok_sub_spot_btc_usdt_ticker','binary':'0'}")
            ws.send("{'event':'addChannel','channel':'ok_sub_spot_eth_usdt_ticker','binary':'0'}")
        ws.close()
        print("thread terminating...")

    t = threading.Thread(target=run, args=())
    t.start()

def on_close(ws):
    print("oken ### closed ###")
    #runOkenWs()

#开启OKEN币Ws
def runOkenWs():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        oken_ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

def huobi_on_open(ws):
    def run(*args):

        # # 每2秒请求一次K线图，请求5次
        while (True):
            time.sleep(2)
            ws.send(json.dumps({"req": "market.btcusdt.kline.1min", "id": "id1"}).encode())
            ws.send(json.dumps({"req": "market.ethusdt.kline.1min", "id": "id1"}).encode())
        ws.close()
        print("thread terminating...")

    t = threading.Thread(target=run, args=())
    t.start()

def huobi_on_message(ws, message):
    unzipped_data = gzip.decompress(message).decode()
    msg_dict = json.loads(unzipped_data)
    print(msg_dict)

def huoBi_on_close():
    print("huoBi ### closed ###")
    # runHuoBiWs()


#开启火币Ws
def runHuoBiWs():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        huoBi_ws_url,
        on_open=huobi_on_open,
        on_message=huobi_on_message,
        on_error=on_error,
        on_close=huoBi_on_close
    )
    ws.run_forever()

#主程序
if __name__ == "__main__":
    create_pool()
    runOkenWs()
    runHuoBiWs()
