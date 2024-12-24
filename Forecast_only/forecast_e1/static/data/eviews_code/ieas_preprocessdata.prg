''
' This code is used for Taiwan Economy Forecasting
' and is written by Kian @ IEAS at 201712

%currqul="2022q4"
%curryear="2023q4"
%nextyear="2024q4"
'=========================================================================================================================================================================
' Loading data
'workfile q 1962q1 2023q4

'read(s=end)  "D:\11205_raw.xls" 60
'read(s=exo)  "D:\11205_raw.xls" 16

'save D:\SINICA\20171203\output_new.wlf

'=========================================================================================================================================================================
' Some preliminary setup -=ENDOGENOUS=-
smpl @all
series td=co+cf+cg+ifix+ex+jj                     'Total Demand
series rtaxcum=tarrif/imtw$                'Tarrif rate
series le=lf*(1-0.01*ru)                              '�N�~�H�f
series pdt=gdp/le                                         '�ҰʥͲ��O
series ulc=1000*aw_mfg/pdt                      '���Ͳ��Ұʦ���
series pjj= 100*jj$/jj                                   '�s�f�ܰʥ������

' setting of tariffs (using moving average) and interest rate(���K�{�v) -=EXOGENOUS=-
'smpl 2022q1 2022q4
'series rtaxcum=(rtaxcum(-1)+rtaxcum(-2)+rtaxcum(-3)+rtaxcum(-4))/4
'ir=1.375


'=========================================================================================================================================================================
'calculating the contribution to GDP for CO and CF (�D�������O�P�������O)-= In sample=-

smpl 1962q1 %currqul
'�p��"�~�����v"�Aq4���a��O�~�����v
for %1 cp co cf cg ip ig ipc ifix jj ex im gdp
  series {%1}_ypcy= @pcy(@meansby({%1}, @year))
next
' �U��X"�~deflator "
for %zz cp co cf cg ip ig ipc ifix jj ex im gdp
  series {%zz}_qavg = @meansby({%zz}, @year)
  series {%zz}$_qavg = @meansby({%zz}$, @year)
  series p{%zz}_qavg= @meansby({%zz}$_qavg /{%zz}_qavg, @year) '�U��X�~deflator, 4�u����m�ƭȳ��O�@��
next
'CO and CF�^�m�v
for %zz co cf 
  series contrib_{%zz}_q=(p{%zz}_qavg(-4)/pgdp_qavg(-4)*({%zz}-{%zz}(-4))/gdp(-4)+(({%zz}(-4)/gdp(-4))-({%zz}_qavg(-4)/gdp_qavg(-4)))*(p{%zz}_qavg(-4)/pgdp_qavg(-4)-p{%zz}_qavg(-8)/pgdp_qavg(-8)))*100
next

'CO and CF��C�^�m�v
for %zz co cf 
series contrib_c_{%zz}_q=(p{%zz}_qavg(-4)/pcp_qavg(-4)*({%zz}-{%zz}(-4))/cp(-4)+(({%zz}(-4)/cp(-4))-({%zz}_qavg(-4)/cp_qavg(-4)))*(p{%zz}_qavg(-4)/pcp_qavg(-4)-p{%zz}_qavg(-8)/pcp_qavg(-8)))*100
next

'IG, IPC  and IP��IFIX�^�m�v
for %zz ipc ig ip
series contrib_i_{%zz}_q=(p{%zz}_qavg(-4)/pifix_qavg(-4)*({%zz}-{%zz}(-4))/ifix(-4)+(({%zz}(-4)/ifix(-4))-({%zz}_qavg(-4)/ifix_qavg(-4)))*(p{%zz}_qavg(-4)/pifix_qavg(-4)-p{%zz}_qavg(-8)/pifix_qavg(-8)))*100
next

'GDP�����v(�u) and �b�X�f
series gdp_pcy= contrib_cp_q+contrib_cg_q+contrib_ip_q+contrib_ig_q+contrib_ipc_q+contrib_jj_q+contrib_ex_q-contrib_im_q
series netexport=ex-im


