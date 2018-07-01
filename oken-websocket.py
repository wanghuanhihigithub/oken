
import websocket
import sys
import zlib

def on_open(self):
    # subscribe okcoin.com spot ticker
    self.send({'event':'addChannel','channel':'ok_sub_spot_usd_btc_ticker','binary':0})

def on_message(self, evt):
    data = inflate(evt)  # data decompress
    print(data)

def inflate(data):
    decompress = zlib.decompressobj(
        -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated


def on_error(self, evt):
    print(evt)


def on_close(self, evt):
    print('DISCONNECT')


if __name__ == "__main__":
    url = "wss://real.okcoin.com:10440/websocket/okcoinapi"  # if okcoin.cn  change url wss://real.okcoin.cn:10440/websocket/okcoinapi
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
