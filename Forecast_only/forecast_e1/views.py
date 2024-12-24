from django.shortcuts import render ,redirect
from django.contrib.auth.forms import UserCreationForm #來開發網站的註冊功能。
from django.contrib.auth import authenticate, login, logout #來驗證使用者所輸入的帳號及密碼是否正確
from django.contrib.auth.decorators import login_required #防止使用者在沒有進行登入的動作時，直接透過網址存取首頁
from .forms import *
import numpy as np
import pandas as pd
from django.contrib import messages #
from dash import Dash, dcc, html, Input, Output,State, ctx, callback,dash_table
from datetime import date
import time
from dateutil.relativedelta  import relativedelta as rd# 可以用於計算時間差，支持年、月、日、週、時、分、秒等
from plotly.subplots import make_subplots #繪製子圖用
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False # 使坐標軸刻度表簽正常顯示正負號
import seaborn as sns; sns.set()
from .funs_class import * #進出口預測相關
from .ieas_funs import * #歷史資料作圖相關
from multiprocessing import Process, Pool
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import quandl
quandl.ApiConfig.api_key = '9zC5CombxV_sj2aKogz1'
from dateutil.relativedelta import relativedelta as rd
from datetime import datetime



import urllib.request
from urllib.request import urlopen
import ssl
import json
import os
from django.conf import settings
ssl._create_default_https_context = ssl._create_unverified_context


# 取得資料夾中的所有檔案的函式  =======================================
def file_list(path, sort_by='time', descending=True):
    """
    獲取目錄中的檔案列表，並根據需求排序。

    Args:
        path (str): 檔案路徑。
        sort_by (str): 排序依據，'name' 表示按檔案名稱排序，'time' 表示按修改時間排序。
        descending (bool): 是否降序排列， False（升序）。

    Returns:
        list: 排序後的檔案列表。
    """
    files = os.listdir(path)

    if sort_by == 'name':
        files = sorted(files, key=lambda x: x, reverse=descending)  # 根據檔名排序
    elif sort_by == 'time':
        files = sorted(
            files,
            key=lambda x: os.path.getmtime(os.path.join(path, x)),
            reverse=descending  # 按修改時間排序
        )
    else:
        raise ValueError("Invalid value for sort_by. Use 'name' or 'time'.")

    return files


# ====================================================
result_path = os.path.join(settings.BASE_DIR, 'forecast_e1/static/data/')
temporary_path =os.path.join(settings.BASE_DIR, 'forecast_e1/static/data/temporary_data/')
#data
#=======================================================================================================================
#@login_required(login_url="Login")
def home(request):
     #首頁
    return render(request, 'forecast_e1/home2.html', locals())



#@login_required(login_url="Login")
def ieas1(request):
    """ #歷史月資料 """
    """
    today = date.today()
    
    for i in range(0, 60): #若當日資料沒有則回推最近日期之資料
        today = today - rd(days=i)
        excel_file = result_path + '/簡報數據' + today.strftime('%Y') + today.strftime('%b') + str(today.day) + '.xlsx'
        if os.path.exists(excel_file):
            break
        else:
            print(f"The file '{excel_file}' does not exist.")
    """
    for file in file_list(result_path):
        if '簡報數據' in file and file.endswith('.xlsx'):
            excel_file = os.path.join(result_path, file)
            break


    tw_datam = pd.read_excel(excel_file, sheet_name='彙整月', header=[0], index_col=[0], na_values=['-', '－'],
                             parse_dates=[0])
    tw_dataq = pd.read_excel(excel_file, sheet_name='彙整季', header=[0, 1], index_col=[0], na_values='-',
                             parse_dates=[0])
    tw_datamt = pd.read_excel(excel_file, sheet_name='月資料說明', header=[0], index_col=[0], na_values=['-', '－'],
                              parse_dates=[0])
    tw_dataqt = pd.read_excel(excel_file, sheet_name='季資料說明', header=[0], index_col=[0], na_values='-',
                              parse_dates=[0])
    # model = ieas_project(result_path, excel_file,fightml_path)
    model = ieas_project(excel_file,result_path, tw_datam, tw_dataq, tw_datamt, tw_dataqt, temporary_path)
    ieas_Dashm = model.Dash_Chart_n(model.tw_datam, '月資料', 'ieas_Dashm')
    text_title = '月資料'

    return render(request, 'forecast_e1/ieas_web1.html', locals())

#@login_required(login_url="Login")
def ieas2(request):
    """ #歷史季資料 """

    for file in file_list(result_path):
        if '簡報數據' in file and file.endswith('.xlsx'):
            excel_file = os.path.join(result_path, file)
            break

    tw_datam = pd.read_excel(excel_file, sheet_name='彙整月', header=[0], index_col=[0], na_values=['-', '－'],
                             parse_dates=[0])
    tw_dataq = pd.read_excel(excel_file, sheet_name='彙整季', header=[0, 1], index_col=[0], na_values='-',
                             parse_dates=[0])
    tw_datamt = pd.read_excel(excel_file, sheet_name='月資料說明', header=[0], index_col=[0], na_values=['-', '－'],
                              parse_dates=[0])
    tw_dataqt = pd.read_excel(excel_file, sheet_name='季資料說明', header=[0], index_col=[0], na_values='-',
                              parse_dates=[0])

    tw_dataq.index.name = ('Unnamed: 0_level_0', 'Indicator')
    tw_dataq_colori = tw_dataq.columns.tolist()
    tw_dataq_colmix = ['{}_{}'.format(col[0], col[1]) for col in tw_dataq_colori]  # 將雙層columns name降為一層
    tw_dataq.columns = tw_dataq_colmix
    # tw_dataq.loc[:, '貢獻率_國外淨需求-減：商品及服務輸入'] = tw_dataq.loc[:, '貢獻率_國外淨需求-減：商品及服務輸入'] * -1#貢獻率_貢獻度國外淨需求-減：商品及服務輸入
    tw_dataq.loc[:, '貢獻率_貢獻度國外淨需求-減：商品及服務輸入'] = tw_dataq.loc[:,
                                                                   '貢獻率_貢獻度國外淨需求-減：商品及服務輸入'] * -1  # 貢獻率_貢獻度國外淨需求-減：商品及服務輸入

    model = ieas_project(excel_file,result_path, tw_datam, tw_dataq,tw_datamt, tw_dataqt,temporary_path)
    text_title = '季資料'
    ieas_Dashq = model.Dash_Chart_n(model.tw_dataq,text_title,'ieas_Dashq')



    return render(request, 'forecast_e1/ieas_web2.html', locals())

def ieas3(request):
    """ #歷史日資料 """

    for file in file_list(result_path):
        if '簡報數據' in file and file.endswith('.xlsx'):
            excel_file = os.path.join(result_path, file)
            break

    tw_datam = pd.read_excel(excel_file, sheet_name='彙整月', header=[0], index_col=[0], na_values=['-', '－'],
                             parse_dates=[0])
    tw_dataq = pd.read_excel(excel_file, sheet_name='彙整季', header=[0, 1], index_col=[0], na_values='-',
                             parse_dates=[0])
    tw_datamt = pd.read_excel(excel_file, sheet_name='月資料說明', header=[0], index_col=[0], na_values=['-', '－'],
                              parse_dates=[0])
    tw_dataqt = pd.read_excel(excel_file, sheet_name='季資料說明', header=[0], index_col=[0], na_values='-',
                              parse_dates=[0])
    # model = ieas_project(result_path, excel_file,fightml_path)
    model = ieas_project(excel_file,result_path, tw_datam, tw_dataq, tw_datamt, tw_dataqt, temporary_path)
    ieas_Dashd = model.Dash_Chart_n(model.tw_datam, '日資料', 'ieas_Dashd')#model.tw_datam要改！！
    text_title = '日資料'

    return render(request, 'forecast_e1/ieas_web3.html', locals())


#@login_required(login_url="Login")
def Trade_f(request):
    """ #預測進出口 """
    # 台灣總體統計資料之文件檔名稱
    URL_txt = result_path + '/tw_URL.txt'
    # 讀入已存有的 Taiwan data
    tw_data = pd.read_csv(result_path + '/taiwan_data.csv', index_col=0,
                          parse_dates=True)  # 如果CSV文件中要設為index的日期字符串為標準格式，則可以直接透過parse_dates=True 確保正確解析日期成為DatetimeIndex
    # 讀入已存有的 fred 資料
    fred_data = pd.read_csv(result_path + '/fred_data.csv', index_col=0, parse_dates=True)

    search_form = TradeSearchForm(request.POST or None)  # 將表單呈現為 HTML 文件
    model = TradeForecast(result_path, tw_data, fred_data=[fred_data])
    # 資料最後的時間
    tw_data_last = tw_data.index[-1].date()
    fred_data_last = fred_data.index[-1].date()
    print('***the latest date of the data:***', '\nX:', tw_data_last, '\nFred:', fred_data_last)
    tw_data_lastTtext = '臺灣主計總處統計資料最後一期時間為' + datetime.strftime(tw_data_last, '%Y{y}%m{m}').format(y='年',m='月') + \
                        '，且有' + str(len(tw_data)) + '筆可用資料'
    fred_data_lastTtext = '美聯儲經濟數據(FRED)資料最後一期時間為' + datetime.strftime(fred_data_last, '%Y{y}%m{m}').format(y='年',m='月')+ \
                          '，且有' + str(len(fred_data)) + '筆可用資料'
    if request.method == 'POST':
        model.Get_new_clear_data(tw_data,fred_data)  # 得整理好的資料
        forecast_year = int(request.POST.get('forecast_year'))
        forecast_month = int(request.POST.get('forecast_month'))
        forecast_from = date(forecast_year,forecast_month,1)
        H = int(request.POST.get('forecast_H'))
        H2 = int(request.POST.get('forecast_H2'))
        # 預測未來時，in_sample的時間終點，基於tw_data_last會大於fred_data_last的特性建立:
        if forecast_from <= fred_data_last:  # 舉例:在2022/10/14當下，fred_data_last為8月，則forecast_from為8月時，in-sample需為7月
            t_process_f = forecast_from - rd(months=1)  # in-sample的最後一期時間，為預測起始期的前一期
            t_process_f_with_fred = forecast_from - rd(months=1)
        elif (forecast_from > fred_data_last) & (
                forecast_from <= tw_data_last):  # (記得要括號，不然會出錯)輸入的欲預測時間forecast_from為9月，超出fred_data_last8月，則不管怎樣fred_data之in-sample都是fred_data_last8月
            t_process_f = forecast_from - rd(months=1)
            t_process_f_with_fred = fred_data_last  # in-sample 直接等於資料最後時間
        else:  # 只會發生在輸入的欲預測時間，超出兩個data_last，則不管怎樣兩個in-sample都是fdata_last
            t_process_f = tw_data_last
            t_process_f_with_fred = fred_data_last
        print('***the latest date of the In-sample data:***', '\nwithout Fred:', t_process_f, '\nwith Fred:',
              t_process_f_with_fred)

        # ----------------------------------------------------------------------
        fred_data = model.fred_data
        t_process_f2 = t_process_f - rd(months=H2)
        t_process_f_with_fred2 = t_process_f_with_fred - rd(months=H2)

        for key, name in zip([model.r_im, model.r_ex], ['im', 'ex']):
            print('預測',name)
            start = time.time()
            forecasts = {}
            forecasts['forecast_without_fred_f'] = pd.concat(
                [model.forecast(key, 'level', t_process_f, t_process_f, H)[3].iloc[:, 0].to_frame(),
                 model.forecast(key, 'growth rate', t_process_f, t_process_f, H)[3].iloc[:, :]], axis=1)

            forecasts['forecast_with_fred_f'] = pd.concat(
                [model.forecast(key, 'level', t_process_f_with_fred, t_process_f_with_fred, H, fred_data=fred_data)[3].iloc[:,0].to_frame(),
                 model.forecast(key, 'growth rate', t_process_f_with_fred, t_process_f_with_fred, H, fred_data=fred_data)[3].iloc[:, :]], axis=1)
            forecasts['forecast_without_fred_f_old'] = pd.concat(
                [model.forecast(key, 'level', t_process_f2, t_process_f2, H)[3].iloc[:, 0].to_frame(),
                 model.forecast(key, 'growth rate',  t_process_f2, t_process_f2, H)[3].iloc[:, :]], axis=1)
            forecasts['forecast_with_fred_f_old'] = pd.concat(
                [model.forecast(key, 'level',  t_process_f_with_fred2, t_process_f_with_fred2, H, fred_data=fred_data)[3].iloc[:,0].to_frame(),
                 model.forecast(key, 'growth rate',  t_process_f_with_fred2, t_process_f_with_fred2, H, fred_data=fred_data)[3].iloc[:, :]], axis=1)
            globals()['forecasts_' + name] = forecasts
            end = time.time()
            print('費時:',format(end - start))

        # ----------------------------------------------------------------------
        Y_list = ['real', 'f_level', 'f', 'f_level_with_freddata', 'f_with_freddata' \
            , 'f_level_old', 'f_old', 'f_level_with_freddata_old', 'f_with_freddata_old']
        Yn_list = ['real', 'forecast(level)', 'forecast', 'forecast(level) with fred data', 'forecast with fred data' \
            , 'forecast(level)_old', 'forecast_old', 'forecast(level) with fred data_old',
                   'forecast with fred data_old']

        option_Y = [{'label': Yn_list[i], 'value': Y_list[i]} for i in range(len(Y_list))]
        result_test = forecasts_im['forecast_without_fred_f']['real'].dropna(how='any', axis=0)
        date_list = pd.date_range(start=result_test.index[0], end=(result_test.index[-1]+rd(months=(H+1))), freq='MS') #.strftime('%y-%m-%d')
        T = len(date_list)
        now = datetime.now()
        #file_time = datetime.strftime(now, '%Y-%m-%d %H{H}').format(H='點')
        file_time = datetime.strftime(now, '%Y-%m-%d')
        file_title = '預測折線圖'
        # ----------------------------------------------------------------------

        app = DjangoDash('TradeDash_f', external_stylesheets=[dbc.themes.BOOTSTRAP])
        app.css.append_css({'external_url': '/static/css/freestyle.css'})
        app.layout = dbc.Container([
            html.Br(),
            html.Br(),
            html.H4('進出口預測'),
            html.Br(),
            dbc.Row([
            html.Br(),
            dbc.Row([
                html.P("選擇欲呈現出的目標:"),
                dbc.RadioItems(
                    id='selection',
                    options=["進口", "出口"],
                    value="進口",  # 預設選項
                    switch=True,
                    labelCheckedStyle={"color": "rgb(255,99,71)"},
                    inline=True,
                )
            ]),
            html.Br(),  # 空行
            html.P('選擇欲呈現出的結果:'),
            dbc.Row([
                html.Div([
                    html.Div(html.P(
                        html.A(
                            html.Button('全選', className='Button2'),
                            id="line_all",
                            n_clicks=0,
                        )
                    ), style={'display': 'inline-table'}),  # 呈現並排
                    html.Div(html.P(
                        html.A(
                            html.Button('取消選取', className='Button2'),
                            id="line_notall",
                            n_clicks=0,
                        ))
                        ,className='px-2', style={'display': 'inline-table'}),
                    html.Div(html.P(
                        '(後四個為往前幾期開始預測的對照組)',
                        style={ 'color': '#178CA4'}), className='px-2', style={'display': 'inline-table'})
                ]),
            ]),

                dbc.Row([
                    dbc.Checklist(  # 欲選擇的
                        id='line_y1',
                        options=option_Y[1:5],
                        value=Y_list[1:5],
                        labelCheckedStyle={'color': 'rgb(255,99,71)'},
                        inline=True,
                    ),
                ]),
                dbc.Row([
                    dbc.Checklist(  # 欲選擇的
                        id='line_y2',
                        options=option_Y[5:],
                        value=Y_list[5:],
                        labelCheckedStyle={'color': 'rgb(255,99,71)'},
                        inline=True,
                    ),


                ]),

            html.Br(),  # 空行
            html.Br(),
            dbc.Row([
                html.Br(),  # 空行
                html.Div(
                    [
                        dbc.Button(
                            "打開隱藏資料",
                            id="collapse-button",
                            className="mb-3 Button1",
                            color="primary",
                            n_clicks=0,
                            # 可設定預設值 is_open=True顯示內容和is_open=False隱藏內容
                        ),
                        dbc.Collapse(
                            html.Div(

                                [html.P(
                                    '(可以透過點選欄位名稱最左邊的上下箭頭按鈕, 來達到升降冪排序)',
                                    style={'color': '#178CA4'}),
                                    html.P(
                                        '(可以在 filter data... 部份直接輸入條件式做即時搜尋,舉例：在 Date 欄位輸入 >=2000-03)',
                                        style={'color': '#178CA4'}),

                                    dash_table.DataTable(
                                        id='table-editing-simple',
                                        editable=False,  # 是否可以編輯表格
                                        filter_action="native",
                                        export_format='xlsx',
                                        export_headers='display',
                                        merge_duplicate_headers=True,
                                        page_action='native',
                                        page_current=0,
                                        page_size=24,
                                        sort_action='native',
                                        # sort_action='custom'適用於表頭固定名稱~並在回調中定義應該如何進行排序（sort_by輸入和data輸出在哪裡）
                                        sort_mode='multi',  # 對於多列排序 ;  默認'single'按單個列執行排序
                                        sort_by=[],
                                        style_cell={'textAlign': 'left'},
                                        # 向左對齊 (補充:“cell”是整個表格，“header”只是標題行，“data”只是數據行)
                                        style_as_list_view=True,  # 將表格樣式化為列表
                                        style_header={  # 標題的列表的 CSS 樣式
                                            'backgroundColor': '#178CA4',
                                            'color': 'rgb(255, 255, 255)',
                                            'fontWeight': 'bold',
                                            # 'border': '1px solid pink' #邊框
                                        },
                                        style_data={  # 數據行的 CSS 樣式
                                            'backgroundColor': 'rgb(240,248,255)',
                                            'border': '1px solid pink'
                                        },
                                        style_filter={  # 過濾器單元格的 CSS 樣式
                                            'backgroundColor': 'rgb(255,240,245)',
                                            'border': '1px solid pink'
                                        }
                                    ),
                                ]),
                            id="collapse",
                            is_open=False,
                        ),
                    ]
                ),
                html.Br(),  # 空行
                html.Div(
                    [
                        dbc.Button(
                            "動態調整圖形",
                            id="collapse-button_fig",
                            className="Button1",
                            color="primary",
                            n_clicks=0,

                            # 可設定預設值 is_open=True顯示內容和is_open=False隱藏內容
                        ),

                        dbc.Collapse(
                            html.Div([
                                html.P(),
                                html.Div([
                                    html.P('日期範圍 '),
                                    dcc.RangeSlider(0, T, 1, count=1,
                                                    marks={i: date_list[i].strftime('%Y-%m') for i in range(0, T, 48)},
                                                    # y兩位數的年份表示（00-99）; % Y四位數的年份表示（000-9999）
                                                    # value=[T-(H*3),T], #預設值
                                                    value=[0, T],  # 預設值
                                                    id='date_range_slider'),
                                ], style={"display": "grid", "grid-template-columns": "7% 88%","padding-bottom":"10px"}),

                                html.Div([
                                    html.P('長度 '),
                                    dcc.Slider(id='SliderHeight', min=600, max=900, step=20, value=870,
                                               marks={x: str(x) for x in [600, 700, 800, 900]}),
                                ], style={"display": "grid", "grid-template-columns": "5% 90%"}),
                                html.Div([
                                    html.P('寬度 '),
                                    dcc.Slider(id='SliderWidth', min=800, max=1500, step=20, value=900,
                                               marks={x: str(x) for x in
                                                      [800, 900, 1000, 1100, 1200, 1300, 1400, 1500]}),
                                ], style={"display": "grid", "grid-template-columns": "5% 90%"}),
                            ]),
                            id="collapse_fig",
                            is_open=False,
                        ),
                    ], style={"text-align": "right"}),
                html.Br(),  # 空行
                html.Br(),  # 空行
                html.P(
                    html.A(
                        html.Button("下載互動式圖檔", className='Button1'),
                        id="download",
                        style={"text-align": "right"}), style={"text-align": "right"}),
                dcc.Download(id='download_1'),
                html.P("( 圖形右上方隱藏選單內有 PNG 檔載點與重置圖形紐 )",
                       style={"text-align": "right", "font-weight": "bold"}),  #
                html.Div([
                                            dcc.Loading(dcc.Graph(id="graph",
                                                                  config={
                                                                          "displaylogo": False,
                                                                      'scrollZoom': False,
                                                                          'toImageButtonOptions': {'filename': "{}_{}_{}".format('進出口', file_title, file_time)},
                                                                          # 'scrollZoom': True 滑鼠滾輪縮放開起
                                                                          }),
                                                        type="graph"),  # 改預設"cube" 為 "graph",
                                        ], style={'height': '1300px'}),

            ]),
            ]),
            ],className="",style={'max-width': '100%','max-height': '100%',"margin-right": "1%", "margin-left": "1%"})

        @app.callback(
            Output("collapse_fig", "is_open"),
            [Input("collapse-button_fig", "n_clicks")],
            [State("collapse_fig", "is_open")],
        )
        def toggle_collapse(n, is_open):
            if n:
                return not is_open
            return is_open



        @app.callback(
            Output("line_y1", "value"),
            Output("line_y2", "value"),
            Input("line_all", "n_clicks"),
            Input("line_notall", "n_clicks"),
            State('line_y1', 'options'),
            #State('line_y1', 'value'),
            State('line_y2', 'options'),
            #State('line_y2', 'value'),
            State("line_all", "n_clicks_timestamp"),
            State("line_notall", "n_clicks_timestamp"),
            prevent_initial_call=True)  # prevent_initial_call=True 使不被預設先按了按鈕
        def update_dropdowns(n,n2, options1, options2, timestamp1, timestamp2): #, options_value1, options_value2
            if timestamp1 is None:
                timestamp1 = 0
            if timestamp2 is None:
                timestamp2 = 0
            print(n, '***', timestamp1)
            print('******************')
            print(n2, '***', timestamp2)
            last_n_id = max([(timestamp1, 'n'), (timestamp2, 'n2')])[1]
            if last_n_id == 'n'  : #or (options_value1 == all_values1 & options_value2 == all_values2)
                # 獲取所有選項的值
                all_values1 = [option['value'] for option in options1]
                all_values2 = [option['value'] for option in options2]
                # 就讓所有選項被納入
                value1 = all_values1
                value2 = all_values2
            elif last_n_id == "n2":
                value1 = []
                value2 = []
                #value1 = [i for i in options_value1] if type(options_value1) == list else  [options_value1]
                #value2 = [i for i in options_value2] if type(options_value2) == list else  [options_value2]

            return value1,value2

        @app.callback(
            Output("collapse", "is_open"),
            [Input("collapse-button", "n_clicks")],
            [State("collapse", "is_open")],
        )
        def toggle_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        @app.callback(
            Output("graph", "figure"),
            Output('table-editing-simple', 'data'),
            Output('table-editing-simple', 'columns'),
            Output('table-editing-simple', 'style_data_conditional'),

            Input("selection", "value"),
            Input('line_y1', 'value'),
            Input('line_y2', 'value'),
            Input('date_range_slider', 'value'),
            Input('SliderHeight', 'value'),
            Input('SliderWidth', 'value'),
            )
        def display_animated_graph(selection, line_ys1,line_ys2,date_range,height,width):
            line_ys = []
            for ys in [line_ys1, line_ys2]:
                if ys != []:
                    ys_list = [ys] if type(ys) != list else ys
                    line_ys.extend(ys_list)
            line_ys.insert(0,'real') #real一定出現
            #---------------------------------------------------------------
            forecasts = forecasts_im if selection == '進口' else forecasts_ex

            result_0 = forecasts['forecast_without_fred_f']['real'].dropna(how='any', axis=0)
            result_1 = forecasts['forecast_without_fred_f']['forecast(level)_0'].dropna(how='any', axis=0)[-(H + 1):]
            result_2 = forecasts['forecast_without_fred_f']['forecast_0'].dropna(how='any', axis=0)[-(H + 1):]
            result_3 = forecasts['forecast_with_fred_f']['forecast(level)_0'].dropna(how='any', axis=0)[-(H + 1):]
            result_4 = forecasts['forecast_with_fred_f']['forecast_0'].dropna(how='any', axis=0)[-(H + 1):]
            result_1_old = forecasts['forecast_without_fred_f_old']['forecast(level)_0'].dropna(how='any', axis=0)[-(H + 1):]
            result_2_old = forecasts['forecast_without_fred_f_old']['forecast_0'].dropna(how='any', axis=0)[-(H + 1):]
            result_3_old = forecasts['forecast_with_fred_f_old']['forecast(level)_0'].dropna(how='any', axis=0)[-(H + 1):]
            result_4_old = forecasts['forecast_with_fred_f_old']['forecast_0'].dropna(how='any', axis=0)[-(H + 1):]
            resultnamedict = {}  # 對資料名稱用
            marker1 = 'circle'
            marker2 = 'triangle-up'
            marker_size1 = 7
            marker_size2 = 7
            # dash_list = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
            dash0 = 'solid'
            dash1 = 'longdash'
            dash2 = 'dashdot'
            dash3 = 'dot'
            linewidth2 = 1.5
            resultnamedict['real'] = {'data': result_0, 'Y_name': 'real', 'color': 'dimgray', 'linewidth': 2,
                                      'marker': marker1, 'marker_size': 0, 'dash': dash0}

            resultnamedict['f_level'] = {'data': result_1, 'Y_name': 'forecast(level)', 'color': 'royalblue',
                                         'linewidth': 2, 'marker': marker1, 'marker_size': marker_size1, 'dash': dash0}
            resultnamedict['f_level_with_freddata'] = {'data': result_3, 'Y_name': 'forecast(level) with fred data',
                                                       'color': 'dodgerblue', 'linewidth': 2, 'marker': marker2,
                                                       'marker_size': marker_size1, 'dash': dash1}

            resultnamedict['f'] = {'data': result_2, 'Y_name': 'forecast', 'color': 'crimson', 'linewidth': 2,
                                   'marker': marker1, 'marker_size': marker_size1, 'dash': dash0}
            resultnamedict['f_with_freddata'] = {'data': result_4, 'Y_name': 'forecast with fred data',
                                                 'color': 'indianred', 'linewidth': 2, 'marker': marker2,
                                                 'marker_size': marker_size1, 'dash': dash1}

            resultnamedict['f_level_old'] = {'data': result_1_old, 'Y_name': 'forecast(level)_old',
                                             'color': 'rgb(107,142,35)', 'linewidth': linewidth2, 'marker': marker1,
                                             'marker_size': marker_size2, 'dash': dash2}
            resultnamedict['f_level_with_freddata_old'] = {'data': result_3_old,
                                                           'Y_name': 'forecast(level) with fred data_old',
                                                           'color': 'rgb(189,183,107)', 'linewidth': linewidth2,
                                                           'marker': marker2, 'marker_size': marker_size2,
                                                           'dash': dash3}

            resultnamedict['f_old'] = {'data': result_2_old, 'Y_name': 'forecast_old', 'color': 'rgb(147,112,219)',
                                       'linewidth': linewidth2, 'marker': marker1, 'marker_size': marker_size2, 'dash': dash2}
            resultnamedict['f_with_freddata_old'] = {'data': result_4_old, 'Y_name': 'forecast with fred data_old',
                                                     'color': 'rgb(221,160,221)', 'linewidth': linewidth2, 'marker': marker2,
                                                     'marker_size': marker_size2, 'dash': dash3}

            #--------------------------------------------------------------
            draw_data = pd.DataFrame()
            draw_data_columns = []
            fig = go.Figure()
            for key in line_ys:
                data = resultnamedict[key]['data'].iloc[date_range[0]:] if key=='real' else resultnamedict[key]['data']
                Y_name = resultnamedict[key]['Y_name']
                color = resultnamedict[key]['color']
                lwidth = resultnamedict[key]['linewidth']
                symbols = resultnamedict[key]['marker']
                marker_size = resultnamedict[key]['marker_size']
                dash = resultnamedict[key]['dash']
                draw_data_columns.append(Y_name)
                draw_data = pd.merge(draw_data, data.to_frame(),
                                     left_index=True, right_index=True, how='outer')
                draw_data.columns = draw_data_columns

                fig.add_trace(go.Scatter(x=data.index, y=data, name=Y_name,
                                         marker_symbol=symbols, marker_size=marker_size,
                                         line=dict(color=color, width=lwidth, dash=dash)))
                #fig.update_layout()
                fig.update_traces(hovertemplate='%{x} <br> %{y:.3%}', )  # 自行定義標籤
            #draw_data = draw_data.iloc[date_range[0]:date_range[1],:]
            draw_data = draw_data.iloc[:date_range[1], :]
            # Set title
            fig.update_layout(
                title={
                    'text': selection,
                    'y': 0.95,  # 位置
                    'x': 0.5,
                    'xanchor': 'center',  # 相對位置
                    'yanchor': 'top'}
                , legend=dict(orientation="h",  # 水平顯示
                              y=1.15, x=1,
                              xanchor="right",  # 設置圖例的水平位置(極限點)
                              yanchor="top"  # 設置圖例的垂直位置(極限點)
                              )
                , autosize=True
            ,height = height  # 設置繪圖的高度（以像素為單位）
            , width = width
                , margin=dict(b=30,  # 設置下邊距（以像素為單位）
                              t=160,  # 設置上邊距（以像素為單位）
                              l=30,  # 設置左邊距（以像素為單位）
                              r=30,  # 設置右邊距（以像素為單位）
                              )
                # ,xaxis_title = 'Dates' #橫軸軸標籤
                , font=dict(size=16)  # 設置字體大小
                , template='plotly_white'  # 換默認模板
                # "plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"
                , hovermode="x"
            )
            # Add range slider
            fig.update_layout(
                xaxis=dict(

                    rangeslider=dict(
                        visible=True,
                        autorange=False, #確定是否根據輸入數據計算範圍滑塊範圍。如果提供了 `range`，則 `autorange` 設置為“False”。
                        #range=date_list[date_range[0]:date_range[1]], 錯誤

                        bgcolor='rgb(255,228,225)', #設置範圍滑塊的背景顏色 rgb(255,250,250) rgb(255,228,225)
                        thickness=0.09, #範圍滑塊的高度佔繪圖區域總高度的%
                    ),
                    range=[draw_data.index[0], draw_data.index[-1]+rd(months=1)],  # 設置範圍滑塊的範圍。如果未設置，則默認為完整的 x 軸範圍。#+rd(months=1)
                    rangeslider_range=[draw_data.index[0], draw_data.index[-1]+rd(months=1)], #+rd(months=1)
                    type="date",
                )
            )

            draw_data = draw_data.dropna(how='all')
            draw_data.index = draw_data.index.strftime("%Y-%m")#-%d
            draw_data = draw_data.rename_axis('Date').reset_index()
            data = draw_data
            # fig.write_html(apppath + "最近一次執行的進出口互動式圖形.html")
            data_col_name = data.columns.values.tolist()
            table_columns = [{'id': col, 'name': col, 'deletable': True, 'renamable': True} for col in
                             data_col_name]

            table_data = [dict(Model=i, **{col: data.iloc[i][col] for col in data_col_name})
                          for i in range(len(data))]
            style_data_conditional = (
                [
                    {
                        'if': {'row_index': 'odd'},  # 數據行樣式 且控制偶數行
                        'backgroundColor': 'rgb(176,224,230)',
                    }
                ]
            )
            title = file_title
            fig.write_html(temporary_path+"/{}_{}_{}.html".format(selection, title, file_time), config= {'displaylogo': False})
            return (fig, table_data, table_columns, style_data_conditional)

        @app.callback(
            Output('download_1', 'data'),
            Input("selection", "value"),
            Input('download', 'n_clicks'), prevent_initial_call=True)
        def download_html(selection,n):
            title = file_title
            return dcc.send_file(temporary_path+"/{}_{}_{}.html".format(selection, title,file_time))  # 從本機傳送出去

        TradeDash_f = app
    else:
        messages.warning(request, "<  請填選完整資料，並按下運算以進行估計 >")
    text_title = '進出口預測'
    return render(request, 'forecast_e1/trade_f_web.html', locals())

#@login_required(login_url="Login")
def Trade_Coef_heatmap(request):
    """ # 進出口預測係數熱力地圖 """
    forecast_from = date(date.today().year, date.today().month, 1)  # 這個月第一天
    H=12
    # 台灣總體統計資料之文件檔名稱
    URL_txt = result_path + '/tw_URL.txt'
    # 讀入已存有的 Taiwan data
    tw_data = pd.read_csv(result_path + '/taiwan_data.csv', index_col=0,
                          parse_dates=True)  # 如果CSV文件中要設為index的日期字符串為標準格式，則可以直接透過parse_dates=True 確保正確解析日期成為DatetimeIndex
    # 讀入已存有的 fred 資料
    fred_data = pd.read_csv(result_path + '/fred_data.csv', index_col=0, parse_dates=True)
    # ==============================================
    if request.method == 'POST':
        model = TradeForecast(result_path, tw_data, fred_data=[fred_data])
        model.Get_new_clear_data(tw_data,fred_data)  # 得到整理好的資料
        # 整理過後，資料最後的時間
        tw_data_last = model.tw_data.index[-1].date()
        fred_data_last = model.fred_data.index[-1].date()
        print('***the latest date of the data:***', '\nX:', tw_data_last, '\nFred:', fred_data_last)

        # 預測未來時，in_sample的時間終點，基於tw_data_last會大於fred_data_last的特性建立:
        if forecast_from <= fred_data_last:  # 舉例:在2022/10/14當下，fred_data_last為8月，則forecast_from為8月時，in-sample需為7月
            t_process_f = forecast_from - rd(months=1)  # in-sample的最後一期時間，為預測起始期的前一期
            t_process_f_with_fred = forecast_from - rd(months=1)
        elif (forecast_from > fred_data_last) & (
                forecast_from <= tw_data_last):  # (記得要括號，不然會出錯)輸入的欲預測時間forecast_from為9月，超出fred_data_last8月，則不管怎樣fred_data之in-sample都是fred_data_last8月
            t_process_f = forecast_from - rd(months=1)
            t_process_f_with_fred = fred_data_last  # in-sample 直接等於資料最後時間
        else:  # 只會發生在輸入的欲預測時間，超出兩個data_last，則不管怎樣兩個in-sample都是fdata_last
            t_process_f = tw_data_last
            t_process_f_with_fred = fred_data_last

        print('***the latest date of the In-sample data:***', '\nwithout Fred:', t_process_f, '\nwith Fred:',
              t_process_f_with_fred)
        start = time.time()  # 開始測量執行時間
        [ex_result,ex_forecasts,ex_x_coefs] = model.Get_allForecast(model.r_ex,   t_process_f, t_process_f_with_fred, H)
        [im_result,im_forecasts,im_x_coefs] = model.Get_allForecast(model.r_im,   t_process_f, t_process_f_with_fred, H)
        end = time.time()  # 結束測量執行時間
        print('預測總共花費時間：', end - start)
        withFred_l1 = ['a.單純使用台灣資料', 'b.加入Fred資料']
        withFred_l2 = ['without_fred', 'with_fred']
        option_Fred = [{'label': withFred_l1[i], 'value': withFred_l2[i]} for i in range(len(withFred_l1))]
        # --------------------------------------------------------------------------------
        now = datetime.now()
        file_time = datetime.strftime(now, '%Y-%m-%d')
        # ----------------------------------------------------------------------------
        app = DjangoDash('TradeHeatmapDash_f', external_stylesheets=[dbc.themes.BOOTSTRAP])
        app.css.append_css({'external_url': '/static/css/freestyle.css'})
        app.layout = dbc.Container([
            html.Br(),
            html.Br(),
            html.H4('進出口預測之迴歸係數'),
            html.Br(),

                html.P("選擇欲呈現出的預測目標:"),
                dbc.RadioItems(
                    id='selection',
                    options=["進口", "出口"],
                    value="進口",  # 預設選項
                    switch=True,
                    labelCheckedStyle={"color": "rgb(255,99,71)"},
                    inline=True,
                ),
            html.Br(),  # 空行
            html.P('選擇解釋變數資料:'),

                    dbc.RadioItems(  # 欲選擇的
                        id='withfred',
                        options=option_Fred,
                        value=withFred_l2[0],
                        switch=True,
                        labelCheckedStyle={'color': 'rgb(255,99,71)'},
                        inline=True,
                    ),

                html.Br(),  # 空行
                html.P('選擇解釋變數型態:'),
                dbc.Row([
                    dbc.RadioItems(  # 欲選擇的
                        id='state',
                        options=['level', 'growth rate'],
                        value='level',
                        switch=True,
                        labelCheckedStyle={'color': 'rgb(255,99,71)'},
                        inline=True,
                    ),


                ]),

            html.Br(),  # 空行
            html.Br(),
            dbc.Row([
                html.Br(),  # 空行
                html.Div(
                    [
                        dbc.Button(
                            "打開隱藏資料",
                            id="collapse-button",
                            className="mb-3 Button1",
                            color="primary",
                            n_clicks=0,
                            # 可設定預設值 is_open=True顯示內容和is_open=False隱藏內容
                        ),
                        dbc.Collapse(
                            html.Div(
                                [   html.P(
                                        '(可以透過點選欄位名稱最左邊的上下箭頭按鈕, 來達到升降冪排序)',
                                        style={'color': '#178CA4'}),
                                    html.P(
                                        '(可以在 filter data... 部份直接輸入條件式做即時搜尋, 舉例：在預測第1期欄位輸入 >0)',
                                        style={'color': '#178CA4'}),
                                    html.P('(資料表中, 橘色底色與紫色底色分別代表該欄位前、後百分之時十的數值)',
                                           style={'color': '#178CA4'}),
                                    dash_table.DataTable(
                                        id='table-editing-simple',
                                        editable=False,  # 是否可以編輯表格
                                        filter_action="native",
                                        export_format='xlsx',
                                        export_headers='display',
                                        merge_duplicate_headers=True,
                                        page_action='native',
                                        page_current=0,
                                        page_size=25,
                                        sort_action='native',
                                        # sort_action='custom'適用於表頭固定名稱~並在回調中定義應該如何進行排序（sort_by輸入和data輸出在哪裡）
                                        sort_mode='multi',  # 對於多列排序 ;  默認'single'按單個列執行排序
                                        sort_by=[],
                                        style_cell={'textAlign': 'left'},
                                        # 向左對齊 (補充:“cell”是整個表格，“header”只是標題行，“data”只是數據行)
                                        style_as_list_view=True,  # 將表格樣式化為列表
                                        style_header={  # 標題的列表的 CSS 樣式
                                            'backgroundColor': '#178CA4',
                                            'color': 'rgb(255, 255, 255)',
                                            'fontWeight': 'bold',
                                            # 'border': '1px solid pink' #邊框
                                        },
                                        style_data={  # 數據行的 CSS 樣式
                                            'backgroundColor': 'rgb(240,248,255)',
                                            'border': '1px solid pink'
                                        },
                                        style_filter={  # 過濾器單元格的 CSS 樣式
                                            'backgroundColor': 'rgb(255,240,245)',
                                            'border': '1px solid pink'
                                        }
                                    ),
                                ]),
                            id="collapse",
                            is_open=False,
                        ),
                    ]
                ),
                html.Div(
                    [
                        dbc.Button(
                            "動態調整圖形大小",
                            id="collapse-button_fig",
                            className="Button1",
                            color="primary",
                            n_clicks=0,

                            # 可設定預設值 is_open=True顯示內容和is_open=False隱藏內容
                        ),

                        dbc.Collapse(
                            html.Div([
                                html.P(),
                                html.Div([
                                    html.P('長度 '),
                                    dcc.Slider(id='SliderHeight', min=700, max=2700, step=25, value=1300,
                                               marks={x: str(x) for x in
                                                      [700, 1000, 1300, 1500, 1800, 2100, 2400, 2700]}),
                                ], style={"display": "grid", "grid-template-columns": "5% 90%"}),
                                html.Div([
                                    html.P('寬度 '),
                                    dcc.Slider(id='SliderWidth', min=800, max=1200, step=25, value=880,
                                               marks={x: str(x) for x in [800, 900, 1000, 1100, 1200]}),
                                ], style={"display": "grid", "grid-template-columns": "5% 90%"}),
                            ]),
                            id="collapse_fig",
                            is_open=False,
                        ),
                    ], style={"text-align": "right"}),
                html.Br(),  # 空行
                html.Br(),  # 空行


                html.Br(),  # 空行
                html.P(
                    html.A(
                        html.Button("下載互動式圖檔", className='Button1'),
                        id="download",
                        style={"text-align": "right"}), style={"text-align": "right"}),
                dcc.Download(id='download_1'),
                html.P("( 圖形右上方隱藏選單內有 PNG 檔載點與重置圖形紐 )",
                       style={"text-align": "right", "font-weight": "bold"}),  #
                html.Div([
                                            dcc.Loading(dcc.Graph(id="graph",
                                                                  config={"displaylogo": False,
                                                                          'scrollZoom': False,
                                                                          'toImageButtonOptions': {
                                                                              'filename': "進出口_迴歸係數熱力圖_{}".format(
                                                                                                              file_time)}}),
                                                        type="graph"),  # 改預設"cube" 為 "graph",
                                        ], style={'height': '1000px'}),

            ]),
            ],className="",style={'max-width': '98%','max-height': '100%',"margin-right": "1%", "margin-left": "1%"})


        @app.callback(
            Output("collapse_fig", "is_open"),
            [Input("collapse-button_fig", "n_clicks")],
            [State("collapse_fig", "is_open")],
        )
        def toggle_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        @app.callback(
            Output("collapse", "is_open"),
            [Input("collapse-button", "n_clicks")],
            [State("collapse", "is_open")],
        )
        def toggle_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        @app.callback(
            Output("graph", "figure"),
            Output('table-editing-simple', 'data'),
            Output('table-editing-simple', 'columns'),
            Output('table-editing-simple', 'style_data_conditional'),
            Input("selection", "value"),
            Input('withfred', 'value'),
            Input('state', 'value'),
            Input('SliderHeight', 'value'),
            Input('SliderWidth', 'value'),
            )
        def display_animated_graph(selection, withfred,state,height,width):
            x_coefs = im_x_coefs if selection == '進口' else ex_x_coefs
            X = model.newX
            fred_c = 'forecast_without_fred_f' if 'without' in withfred else 'forecast_with_fred_f'
            idx2 = 0 if state == 'level' else 1
            coef = x_coefs[fred_c][idx2][0, :, :]
            coef = pd.DataFrame(coef, columns=X.columns, index=range(1, 13)).T if 'without' in withfred else pd.DataFrame(coef, columns=list(X.columns) + list(model.fred_data.columns), index=range(1, 13)).T
            figu_name = '預測' + selection + '之迴歸係數熱力圖<br><sup>(變數型態為' + state + ')</sup><br><br>'

            fig = px.imshow(coef, color_continuous_scale='RdBu_r', color_continuous_midpoint=0)
            fig.update_layout(
                title={
                    'text': figu_name,
                    'y': 0.95,  # 位置
                    'x': 0.5,
                    'xanchor': 'center',  # 相對位置
                    'yanchor': 'top'}
                , yaxis=dict(

                )
                , xaxis=dict(
                    title="預測期數",  # 橫軸軸標籤
                    dtick=1,  # 步長
                )

                , autosize=True
                , height=height  # 設置繪圖的高度（以像素為單位）
                , width=width  # 設置繪圖的高度（以像素為單位）
                , margin=dict( #b=30,  # 設置下邊距（以像素為單位）
                              t=120,  # 設置上邊距（以像素為單位）
                          #    l=30,  # 設置左邊距（以像素為單位）
                            #  r=40,  # 設置右邊距（以像素為單位）
                              )
                , font=dict(size=16)  # 設置字體大小
                , template='plotly_white'  # 換默認模板

                , hovermode="x"
            )

            fig.update_traces(hovertemplate='預測第%{x}期 <br> 變數「%{y}」之<br> 迴歸係數為 %{z}', )  # 自行定義標籤

            #(fig,data) = Model.figu_heatmap2( 'forecast_without_fred_f',state, figu_name, -2, 2,figsize=(10,30))
            data = coef.rename_axis('預測'+selection+'的變數').reset_index()
            for h in range(1,13):
                data.rename(columns={h : '預測第'+str(h)+'期'}, inplace=True)
            # fig.write_html(apppath + "最近一次執行的進出口互動式圖形.html")
            data_col_name = data.columns.values.tolist()
            table_columns = [{'id': col, 'name': col, 'deletable': True, 'renamable': True} for col in
                             data_col_name]
            table_data = [dict(Model=i, **{col: data.iloc[i][col] for col in data_col_name})
                          for i in range(len(data))]
            style_data_conditional = (
                    [
                        {
                            'if': {'row_index': 'odd'},  # 數據行樣式 且控制偶數行
                            'backgroundColor': 'rgb(176,224,230)',
                        }
                    ] +
                    [
                        {
                            'if': {
                                'filter_query': '{{{}}} >= {}'.format(col, float(value)),
                                'column_id': col
                            },
                            'backgroundColor': 'rgb(255,127,80)',
                            'color': 'white'
                        } for (col, value) in data.iloc[:, 1:].quantile(0.9).items()
                    ] +
                    [
                        {
                            'if': {
                                'filter_query': '{{{}}} <= {}'.format(col, float(value)),
                                'column_id': col
                            },
                            'backgroundColor': 'rgb(218,112,214)',
                            'color': 'white'
                        } for (col, value) in data.iloc[:, 1:].quantile(0.1).items()
                    ]
            )
            fig.write_html(temporary_path+"/{}_迴歸係數熱力圖_{}.html".format(selection, file_time), config= {'displaylogo': False})
            return (fig, table_data, table_columns, style_data_conditional)

        @app.callback(
            Output('download_1', 'data'),
            Input('download', 'n_clicks'),
            State("selection", "value"),
            prevent_initial_call=True)
        def download_html(n,selection):
            return dcc.send_file(temporary_path+"/{}_迴歸係數熱力圖_{}.html".format(selection,   file_time))  # 從本機傳送出去


        TradeHeatmapDash_f = app
    else:
        messages.warning(request, "< 請點擊開始運算以進行估計 >")

    text_title = '進出口預測之迴歸係數'
    return render(request, 'forecast_e1/trade_heatmap_web.html', locals())


#=======================================================================================================================

""" 
def sign_up(request):
     #帳號密碼註冊 
    #form = UserCreationForm()
    form = RegisterForm() #自訂的註冊表單

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  # 重新導向到登入畫面
    context = {
        'form': form
    }
    return render(request, 'forecast_e1/register.html', context)



def sign_in(request):
     #登入 
    login_form = LoginForm()
    # 生成驗證碼
    hashkey = CaptchaStore.generate_key()
    imgage_url = captcha_image_url(hashkey)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        vcode = request.POST.get('vcode')
        vcode_key = request.POST.get('hashkey')
        # 验证查询数据库生成正确的码
        get_captcha = CaptchaStore.objects.get(hashkey=vcode_key)
        try:
            user = models.User.objects.get(name=username)
            login(request, user)
            return redirect('/')  # 重新導向到首頁
        except:
            message = '帳號不存在！'
            return render(request, 'forecast_e1/login.html', locals())
        if user.password == password:
            # 将用户输入值小写后与数据库查询的response值对比：
            if vcode.lower() == get_captcha.response:
                return redirect('/')
            else:
                message = '驗證碼不正確！'
                return render(request, 'forecast_e1/login.html', locals())
        else:
            message = '密碼不正確！'
            return render(request, 'forecast_e1/login.html', locals())

    context = {
        'form': login_form
    }

    return render(request, 'forecast_e1/login.html', locals())


def log_out(request):
     #登出 
    logout(request)
    return redirect('/login') #重新導向到登入畫面

"""
