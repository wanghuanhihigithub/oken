import redis
import threading
import requests
import json

def create_pool():
    pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0)
    global __redis
    __redis = redis.Redis(connection_pool=pool)
    global __pipe
    __pipe = __redis.pipeline(transaction=True)
    print(__redis, __pipe)

def fun_timer():
    get_coinEx("btc","usdt")
    get_coinEx("eth","usdt")
    global timer
    timer = threading.Timer(3,fun_timer)
    timer.start()

def get_coinEx(toType, fromType):
    trade_url = "https://api.coinex.com/v1/market/ticker?market=" + toType + fromType
    try:
        r = requests.get(trade_url, timeout=2)
        if (r.status_code == 200):
            text = json.loads(r.text)
            redisKey = "coinEx-usdt-btc"
            if("eth" == toType):
                redisKey = "coinEx-usdt-eth"
            __redis.set(redisKey, text)
            __pipe.execute()
    except Exception  as e:
        print("coinEx获取行情失败", e)

#主程序
if __name__ == "__main__":
    create_pool()
    timer = threading.Timer(1, fun_timer)  # 首次启动
    timer.start()
