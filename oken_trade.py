import requests
import json

headers = {
    "authorization":"eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiJleDExMDE1MzU1NTA4MTYwNTJEMEY2MjFFQTlBRjA5NkIxSkxBViIsInVpZCI6IkZBUEU0SWxPYlF5c1haWW95dzBIUHc9PSIsInN0YSI6MCwibWlkIjowLCJpYXQiOjE1MzU1NTA4MTYsImV4cCI6MTUzNjE1NTYxNiwiYmlkIjowLCJkb20iOiJ3d3cub2tleC5jb20iLCJpc3MiOiJva2NvaW4ifQ.JddmytO3Hdkrgj4E5Xwe1fT2Zo9A--R5zsZnuMbksyPBKwNZLnrCF59fdGqxUsYaeckRwJScZYwFkePwr3OKqA"
}
url = "https://www.okex.com/v2/c2c-open/tradingOrders/group?digitalCurrencySymbol=btc&legalCurrencySymbol=cny&best=0&exchangeRateLevel=0&paySupport=0"

while(True):
    r = requests.get(url, headers=headers, timeout=10)
    print(r.status_code)
    print(json.loads(r.text)["data"]["buyTradingOrders"][0]["exchangeRate"])