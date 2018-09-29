# coding=utf-8
import time
from splinter.browser import Browser
import requests
import json

# oken网自动改价软件，本地记录上次发布时的价格
price = 0
authorization = "eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiJleDExMDE1Mzc0NDk0OTUzMzM5N0REREY2QTg1NEJDOTc1bUNldiIsInVpZCI6IkZBUEU0SWxPYlF5c1haWW95dzBIUHc9PSIsInN0YSI6MCwibWlkIjowLCJpYXQiOjE1MzgxODQ1MzYsImV4cCI6MTUzODc4OTMzNiwiYmlkIjowLCJkb20iOiJ3d3cub2tleC5jb20iLCJpc3MiOiJva2NvaW4ifQ.jriSXCtUhSd3r-RAKJXaWCPmO_AjXhTdyJZMKaOeHhzhU5M-LfEvBnkaLIom7kpgE2uz8fBoaWtYA6gXvAPu4w"
headers = {"authorization": authorization}
url = "https://www.okex.com/v2/c2c-open/tradingOrders/group?digitalCurrencySymbol=btc&legalCurrencySymbol=cny" \
      "&best=1&exchangeRateLevel=0&paySupport=0"
# 对标用户
personIndex = 3
# 和对标用户的价格差异
priceVariance = 10


# 登录oken网
def login():
    browser.visit("https://www.okex.com/")
    browser.find_by_id('dialogBtn').click()
    browser.find_link_by_href("/account/login").click()
    browser.find_by_text('我知道了').click()
    browser.find_by_text("手机号").click()
    browser.find_by_name("username").fill("18980028490")
    browser.find_by_name("password").fill("11111~8")
    browser.find_by_css("button").click()
    time.sleep(10)
    browser.find_by_text("确认").click()
    time.sleep(3)


# 获取btc交易详情
def get_btc_price():
    try:
        r = requests.get(url, headers=headers, timeout=2)
        requests.adapters.DEFAULT_RETRIES = 5
        if 200 == r.status_code:
            return json.loads(r.text)["data"]["buyTradingOrders"][personIndex]
    except Exception as e:
        print(e)
        return None


# 发布BTC买单
def deploy_btc_buy(buy):
    browser.find_by_text("法币交易").click()
    time.sleep(2)
    browser.find_by_css(".list-main").first.find_by_tag("li")[1].click()
    js = "window.scrollTo(0,0)"
    browser.execute_script(js)
    browser.find_by_text("发布委托单").first.click()
    time.sleep(1)
    browser.find_by_name("price").fill(round(buy["exchangeRate"]) - priceVariance)
    browser.find_by_css(".release-entrust-box").first.find_by_name("amount").fill("0.05")
    browser.find_by_text("发布买单").click()
    browser.find_by_css(".release-confirm-box").first.find_by_css(".cancel-order").click()
    print("btc第", personIndex, "价格", buy["exchangeRate"], "当前发布买价", round(buy["exchangeRate"]) - priceVariance)


# 取消Btc买单
def cancel_btc_buy():
    browser.find_by_text("法币交易").click()
    time.sleep(2)
    browser.find_by_css(".list-main").first.find_by_tag("li")[1].click()
    browser.find_by_text("盘口模式").click()
    js = "window.scrollTo(0,document.body.scrollHeight)"
    browser.execute_script(js)
    browser.find_by_text("我的委托单").click()
    browser.find_by_text("撤销").last.click()
    browser.find_by_text("确定").click()


# 判断是否能取消btc买入订单 True需要取消 False不需要取消
# 1.当前没有买入订单
# 2.买入订单的状态已经发生变化
# 3.对标用户的买入价格 - priceVariance < 当前发布价格
def can_cancel_btc_buy(person_price):
    if 0 == price:
        return False
    if person_price - priceVariance < price:
        return False
    return True


with Browser("chrome") as browser:
    login(browser)
    while True:
        buy = get_btc_price()
        if buy is not None:
            tempPrice = round(buy["exchangeRate"]) - priceVariance
            if can_cancel_btc_buy(buy["exchangeRate"]):
                print("价格变动，取消再重新发布")
                cancel_btc_buy()
                deploy_btc_buy(buy)
            price = tempPrice
            time.sleep(3)


