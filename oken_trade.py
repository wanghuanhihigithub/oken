import requests
import json
from datetime import datetime

headers = {
    #"authorization":"eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiJleDExMDE1MzU1NTA4MTYwNTJEMEY2MjFFQTlBRjA5NkIxSkxBViIsInVpZCI6IkZBUEU0SWxPYlF5c1haWW95dzBIUHc9PSIsInN0YSI6MCwibWlkIjowLCJpYXQiOjE1MzYwNDEwNTEsImV4cCI6MTUzNjY0NTg1MSwiYmlkIjowLCJkb20iOiJ3d3cub2tleC5jb20iLCJpc3MiOiJva2NvaW4ifQ.dyBsu9g7VzrsUxCTq5lG18EylVmY0iC_pQmLu_k8NYfEfgXDM7Crwx1YT2AMy-7GAtZRCa0zUwTXfUcJwFvWIw"
}
url = "https://www.okex.com/v3/c2c/tradingOrders/book?side=all&baseCurrency=btc&quoteCurrency=cny&userType=certified&paymentMethod=all"


r = requests.get(url, headers=headers, timeout=2)
data = json.loads(r.text)["data"]["sell"]
for i in data:
    print(i)

