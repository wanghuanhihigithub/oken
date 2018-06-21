import gzip
import json
import threading

import time
import websocket
from datetime import datetime
from models import HuoBi
import asyncio


def send_message(ws, message_dict):
    data = json.dumps(message_dict).encode()
    print("Sending Message:")
    print(message_dict)
    ws.send(data)

def on_message(ws, message):
    unzipped_data = gzip.decompress(message).decode()
    msg_dict = json.loads(unzipped_data)
    print("Recieved Message: ", datetime.now())
    data = msg_dict["data"]
    new = data[len(data) - 1]
    new["createdTime"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(new)
    HuoBi.save(data)
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


def on_open(ws):
    def run(*args):
        data = {
            "req": "market.btcusdt.kline.1min",
            "id": "id1"
        }
        # # 每2秒请求一次K线图，请求5次
        for i in range(5):
            time.sleep(2)
            send_message(ws, data)
        ws.close()
        print("thread terminating...")

    t = threading.Thread(target=run, args=())
    t.start()

if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "wss://api.huobi.pro/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()