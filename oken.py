#coding=utf-8
import time
from splinter.browser import Browser
import requests
import json

price = 0
#登录oken网
def login(browser):
    browser.visit("https://www.okex.com/")
    browser.find_by_id('dialogBtn').click()
    browser.find_link_by_href("/account/login").click()
    browser.find_by_text('我知道了').click()
    browser.find_by_text("手机号").click()
    browser.find_by_name("username").fill("18980028490")
    browser.find_by_name("password").fill("ZHANGchao2020~8")
    browser.find_by_css("button").click()
    time.sleep(10)
    browser.find_by_text("确认").click()
    time.sleep(3)

#获取btc交易详情
def getBtcTrade():
    headers = {
        "authorization": "eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiJleDExMDE1MzU1NTA4MTYwNTJEMEY2MjFFQTlBRjA5NkIxSkxBViIsInVpZCI6IkZBUEU0SWxPYlF5c1haWW95dzBIUHc9PSIsInN0YSI6MCwibWlkIjowLCJpYXQiOjE1MzU1NTA4MTYsImV4cCI6MTUzNjE1NTYxNiwiYmlkIjowLCJkb20iOiJ3d3cub2tleC5jb20iLCJpc3MiOiJva2NvaW4ifQ.JddmytO3Hdkrgj4E5Xwe1fT2Zo9A--R5zsZnuMbksyPBKwNZLnrCF59fdGqxUsYaeckRwJScZYwFkePwr3OKqA"
    }
    url = "https://www.okex.com/v2/c2c-open/tradingOrders/group?digitalCurrencySymbol=btc&legalCurrencySymbol=cny&best=1&exchangeRateLevel=0&paySupport=0"
    try:
        r = requests.get(url, headers=headers, timeout=2)
        requests.adapters.DEFAULT_RETRIES = 5
        if(r.status_code == 200):
             print(json.loads(r.text)["data"]["buyTradingOrders"][3]["exchangeRate"])
             return json.loads(r.text)["data"]["buyTradingOrders"][3]
    except Exception as e:
        print(e)
        return None


def deployTrade(buy):
    js = "window.scrollTo(0,0)"
    browser.execute_script(js)
    browser.find_by_text("发布委托单").first.click()
    time.sleep(1)
    browser.find_by_name("price").fill(round(buy["exchangeRate"]) - 10)
    browser.find_by_css(".release-entrust-box").first.find_by_name("amount").fill("0.05")
    browser.find_by_text("发布买单").click()
    browser.find_by_css(".release-confirm-box").first.find_by_css(".cancel-order").click()

def cancelTrade():
    js = "window.scrollTo(0,document.body.scrollHeight)"
    browser.execute_script(js)
    browser.find_by_text("撤销").last.click()
    browser.find_by_text("确定").click()
    time.sleep(5)

with Browser("chrome") as browser:
    login(browser)
    browser.find_by_text("法币交易").click()
    time.sleep(3)
    browser.find_by_css(".list-main").first.find_by_tag("li")[1].click()
    browser.find_by_text("盘口模式").click()
    browser.find_by_text("我的委托单").click()
    buy = getBtcTrade()
    if(buy != None):
      deployTrade(buy)
      price = round(buy["exchangeRate"]) - 10

    while(True):
        time.sleep(1)
        buy = getBtcTrade()
        if (buy != None):
            if(round(buy["exchangeRate"]) - 10 != price):
                print("价格变动，取消再重新发布")
                cancelTrade()
                deployTrade(buy)
                price = round(buy["exchangeRate"]) - 10


