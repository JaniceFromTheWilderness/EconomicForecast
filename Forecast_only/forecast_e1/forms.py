from django import forms
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    captcha = CaptchaField(
        error_messages={ #錯誤訊息提示
            'invalid': '驗證碼錯誤'
        },
        label="驗證碼",
    )
#------------------------------------------------------------------
def CHOICES(list):
    CHOICES = []  # 設定選項
    for c in list:
        if c != 0:
            CHOICES.append([c, c])
    return CHOICES
def CHOICES2(list,list2):
    CHOICES = []  # 設定選項
    for c,a in zip(list,list2):
        if c != 0:
            CHOICES.append([c, a])
    return CHOICES

#預測目標選擇
RESULTS_list = ['進口','出口']
RESULTS_CHOICES = CHOICES(RESULTS_list)



#年份選擇
this_year = datetime.date.today().year #找到今天的日期
Y_list =  [i for i in range(this_year - 20, this_year + 2)]
Y_list2 = [' {} 年 '.format(i) for i in range(this_year - 20, this_year + 2)]
YEARS_CHOICES = CHOICES2(Y_list,Y_list2)

#月份選擇
this_month = datetime.date.today().month
M_list =  [i for i in range(1,13)]
M_list2 = [' {} 月 '.format(i) for i in range(1,13)]
Month_CHOICES = CHOICES2(M_list,M_list2)




class TradeSearchForm(forms.Form):
    #results_by = forms.ChoiceField(label="欲預測的目標",choices=RESULTS_CHOICES) # 選項設定
    forecast_H = forms.IntegerField(label="輸入欲預測的期數：", max_value=24, min_value=1)
    forecast_year = forms.ChoiceField(initial=[this_year,],label="選擇欲預測的起始年份：",choices = YEARS_CHOICES)
    forecast_month = forms.ChoiceField(initial=[this_month,],label="選擇欲預測的起始月份：", choices = Month_CHOICES)
    forecast_H2 = forms.IntegerField(label="輸入欲對照的預測結果(old)，是往前推幾期：", max_value=24, min_value=1)

withFred_l1 = ['a.單純使用台灣資料','b.加入Fred資料']
withFred_l2 = ['without_fred','with_fred']

withFred_CHOICES = CHOICES2(withFred_l2,withFred_l1)
state_CHOICES = CHOICES(['level','growth rate'])
class EviewsForm(forms.Form):
    withFred_c1 = forms.ChoiceField(initial=['單純使用台灣資料',],label="解釋變數資料：",choices = withFred_CHOICES)
    state_c1 = forms.ChoiceField(initial=['growth rate',],label="解釋變數型態：", choices = state_CHOICES)
    withFred_c2 = forms.ChoiceField(initial=['單純使用台灣資料',],label="解釋變數資料：",choices = withFred_CHOICES)
    state_c2 = forms.ChoiceField(initial=['growth rate',],label="解釋變數型態：", choices = state_CHOICES)