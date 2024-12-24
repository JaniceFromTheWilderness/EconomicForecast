from django.urls import path
from . import views
from django.urls import include
urlpatterns = [
    path('', views.home, name='首頁'),
    path('1', views.ieas1, name='月資料'),
    path('2', views.ieas2, name='季資料'),
    path('3', views.ieas3, name='日資料'),
    path('trade_f', views.Trade_f, name='預測進出口_f'),
    path('heatmap', views.Trade_Coef_heatmap, name='係數熱力地圖'),
    #path('register', views.sign_up, name='Register'),  ＃帳號註冊頁面
    #path('login', views.sign_in, name='Login'), ＃登入頁面
    #path('logout', views.log_out, name='Logout'), ＃登出頁面
    path('captcha/', include('captcha.urls') ) #由於使用了二級路由機制，需要在頂部from django.urls import include。
]