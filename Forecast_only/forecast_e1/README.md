# 經濟預測網站

## 簡介

這是一個經濟預測分析網站，主要是透過Python的[Django套件](https://www.djangoproject.com/)與[Dash套件](https://dash.plotly.com/)製作。

內容包含進出口預測、重要經濟變數變化、GDP之元素貢獻度等，可直接進行探索與互動式分析。

[[網頁請點此]](http://127.0.0.1:8000/)


### 檔案細節說明
* forecast_e1
  * views.py:
    * function 分別是:
      * Trade_f:進出口預測，對應的檔案-->'forecast_e1/trade_f_web.html'；網址名-->'預測進出口_f'
      * GDPyoy_plotly:GDPyoy堆疊圖，對應的檔案-->'forecast_e1/GDPyoy_web.html' ；網址名-->'GDPyoy堆疊圖'),  # name參數，它是此特定 URL 映射的唯一識別標籤。
