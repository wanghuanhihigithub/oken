#oken网自动取消,暂停
import requests
import json

#暂停接单/开始接单 True开始接单 False暂停接单
def startOrStopTrade():
    headers = {"authorization": "eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiJjNTY0N2M4MS1jZDljLTRkN2YtYmM3MC1iZGI2YjRlMjhiODNiamVqIiwidWlkIjoiM2xuNzNkSmxtNXJhQzZIK0RtWG9Rdz09Iiwic3ViIjoiMTg5KioqODQ5MCIsInN0YSI6MCwibWlkIjowLCJpYXQiOjE1MzM2NDAwMzUsImV4cCI6MTUzNDI0NDgzNSwiYmlkIjowLCJkb20iOiJ3d3cub2tleC5jb20iLCJpc3MiOiJva2NvaW4ifQ.nOLePYEBLt7ODHC75CQOeloAtDkxpIcNHO1YFwn5JYxc0A6nPhgNV9znzuLvayTrsEyBQ7sSSfpI30x56oGW7Q",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36",
               "content-type": "application/json"
               }
    url = "https://www.okex.com/v2/c2c-open/tradingOrder/accept-order"
    r = requests.post(url, data={"acceptOrder": True}, headers=headers)
    print(r.status_code)
    print(r.text)


#取消订单
def cancelTrade():
    headers = {
        "authorization": "eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiJjNTY0N2M4MS1jZDljLTRkN2YtYmM3MC1iZGI2YjRlMjhiODNiamVqIiwidWlkIjoiM2xuNzNkSmxtNXJhQzZIK0RtWG9Rdz09Iiwic3ViIjoiMTg5KioqODQ5MCIsInN0YSI6MCwibWlkIjowLCJpYXQiOjE1MzM2NDAwMzUsImV4cCI6MTUzNDI0NDgzNSwiYmlkIjowLCJkb20iOiJ3d3cub2tleC5jb20iLCJpc3MiOiJva2NvaW4ifQ.nOLePYEBLt7ODHC75CQOeloAtDkxpIcNHO1YFwn5JYxc0A6nPhgNV9znzuLvayTrsEyBQ7sSSfpI30x56oGW7Q",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36",
        "accept": "application/json"
    }
    url = "https://www.okex.com/v2/c2c-open/tradingOrder/180807195411825/cancel"
    print("取消订单")
    r = requests.post(url,data={}, timeout=2, headers=headers)
    print(r.status_code)
    print(r.text)

if __name__ == "__main__":
    startOrStopTrade()