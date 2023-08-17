import twstock
import time
import requests

# 自訂發送 Line Notify 通知形式
def lineNotify(token, msg):
    headers = {
        "Authorization": "Bearer " + token,  
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {"message": msg}
    url = "https://notify-api.line.me/api/notify"
    notify = requests.post(url, headers = headers, data = payload)
    return notify.status_code

# 自訂發送 Line Notify 通知內容
def sendLine(mode, real_price, counter_line, token):
    print("鴻海目前股價：" + str(real_price))
    if mode == 1: # 股價高點
        message = "現在股價為" + str(real_price) + "元，可以賣出股票！"
    else: # 股價低點(mode == 2)
        message = "現在股價為" + str(real_price) + "元，可以買進股票！"
    
    code = lineNotify(token, message)
    if code == 200:
        counter_line += 1
        print("第" + str(counter_line) + "次發送訊息。")
    else:
        print("發送訊息失敗！")
    return counter_line

my_token = "QNKVe2w9YJqUB4c4gBCXJLrPcxmM3PZZx82YUNJRj4v"
counter_line = 0
counter_error = 0

print("程式開始執行！")
# 不斷監視股價
while True:
    real_data = twstock.realtime.get("2317")
    if real_data["success"]:
        real_price = real_data["realtime"]["latest_trade_price"] # 目前股價
        if real_price != "-":
            if float(real_price) >= 100.0:
                counter_line = sendLine(1, real_price, counter_line, my_token)
            elif float(real_price) <= 60.0:
                counter_line = sendLine(2, real_price, counter_line, my_token)
            # 發送3次訊息即結束
            if counter_line >= 3:
                print("程式結束！")
                break
            # 每5分鐘讀取一次資料並發送訊息
            # 每次讀取資料延遲2秒
            for i in range(300):
                time.sleep(5)
    else:
        print("資料讀取錯誤，錯誤原因：" + real_data["rtmessage"])
        counter_error += 1
        # 最多發送3次錯誤訊息
        if counter_error >= 3:
            print("程式結束！")
            break
