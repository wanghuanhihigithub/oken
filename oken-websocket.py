import gzip
import json
import threading

import websocket
from datetime import datetime
import redis
import time

def send_message(ws, message_dict):
    ws.send("{'event':'addChannel','channel':'ok_sub_spot_btc_usdt_ticker','binary':'0'}")

def on_message(ws, message):
    print("on_message")
    print(message)
    print(message[0]["data"]["last"])


def on_error(ws, error):
    print("Error: " + str(error))
    error = gzip.decompress(error).decode()
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        # # 每2秒请求一次K线图，请求5次
        while(True):
            time.sleep(2)
            ws.send("{'event':'addChannel','channel':'ok_sub_spot_btc_usdt_ticker','binary':'0'}")
        ws.close()
        print("thread terminating...")

    t = threading.Thread(target=run, args=())
    t.start()

#主程序
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "wss://real.okex.com:10441/websocket",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()
