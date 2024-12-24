"""
1. 在終端機確認可執行：
python3 /home/ubuntu/pythonProject/Forecast_only/forecast_e1/crontab.py
2. crontab -e指令進入Crontab的編輯模式
3. 按鍵盤上的Insert鍵，切換Insert或Replace模式，加入指令：
#使電腦在每天凌晨一點執行該指定檔案
0 1 * * * python3 /home/ubuntu/pythonProject/Forecast_only/forecast_e1/crontab.py
"""

import os
import requests
curr_path = os.getcwd()
print(f"當前路徑{curr_path}")
os.chdir('/home/ubuntu/pythonProject/Forecast_only/forecast_e1')
new_curr_path = os.getcwd()
print(f"更改當前路徑為{new_curr_path}")

token = 'KAszeh91PePA1azdJMrP1QOy2T79aYsTZtv5b8AM75v' #j line通知之權杖
def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code

# 進出口預測所需資料 -------------------------------------------
from funs_class import * #進出口預測相關
result_path ='/home/ubuntu/pythonProject/Forecast_only/forecast_e1/static/data'
# 台灣總體統計資料之文件檔名稱
URL_txt = result_path + '/tw_URL.txt'
# 讀入已存有的 Taiwan data
tw_data = pd.read_csv(result_path + '/taiwan_data.csv', index_col=0,
                      parse_dates=True)  # 如果CSV文件中要設為index的日期字符串為標準格式，則可以直接透過parse_dates=True 確保正確解析日期成為DatetimeIndex
# 讀入已存有的 fred 資料
fred_data = pd.read_csv(result_path + '/fred_data.csv', index_col=0, parse_dates=True)
model = TradeForecast(result_path, tw_data, fred_data=[fred_data])
model.Get_new_data(URL_txt)

lineNotifyMessage(token, f'AWS 順利更新進出口資料檔！台灣資料最後一期為{tw_data.index[-1].date()}，FRED資料最後一期為{fred_data.index[-1].date()}')

# 例行性刪除資料(使資料不要過度累積） -------------------------------------------
import shutil
path = '/home/ubuntu/pythonProject/Forecast_only/forecast_e1/static/data/temporary_data'
# 先強制刪除資料夾
shutil.rmtree(path)
print(f"刪除{path}成功")
# 再重建同名資料夾
os.mkdir(path)
print(f"重建{path}成功")
lineNotifyMessage(token, f'AWS 順利進行例行性資料夾重整！資料夾為{path}')

