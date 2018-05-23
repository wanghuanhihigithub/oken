import websocket

def on_message(ws, message):
    print("接收数据===")
    print(message)

def on_error(ws, error):
    print("发送异常")
    print(error)

def on_close(ws):
    print("###closed###")

def on_oppen(ws):
    print("###open###")
    ws.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_depth_this_week_20'}")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws  = websocket.WebSocketApp('wss://real.okcoin.com:10440/websocket/okcoinapi',
                                on_open = on_oppen,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.run_forever()