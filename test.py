import json
import urllib
import urllib2

if(__name__=="__main__"):
    url_of_eos_next_week = "https://www.okex.com/api/v1/future_depth.do?symbol=eos_usdt&contract_type=next_week&size=1" #EOS次周合约市场深度API地址
    req_eos_next_week = urllib2.Request(url_of_eos_next_week)
    req_eos_next_week.add_header("Content-Type","application/x-www-form-urlencoded")
    req_eos_next_week.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36")
    res_eos_next_week=urllib2.urlopen(req_eos_next_week, timeout=2)
    json_res_eos_next_week = json.loads(res_eos_next_week.read().decode("utf-8"))
    #json_res_eos_next_week即为EOS次周合约价格信息