%currqul="2022q4"
%curryear="2023q4"
%nextyear="2024q4"

'============    額外調整外生參數 ====================================================================================================================================

smpl 2023q1 2023q4
gdp_chn =gdp_chn(-4)*1.05453
gdp_usa =gdp_usa(-4)*1.01112

smpl 2004q1 %currqul
'============  Set up model  ============================================================================================================================================
model model1 
model1.merge eq_goods_cf
model1.merge eq_goods_co
model1.merge eq_ip
model1.merge eq_mgfsales
'model1.merge eq_ex
'model1.merge eq_im
model1.merge eq_lf
model1.merge eq_ru
model1.merge eq_aw_mfg
model1.merge eq_m2
model1.merge eq_m1b
model1.merge eq_mrda
model1.merge eq_rmibon
model1.merge eq_irc
model1.merge eq_iri
model1.merge eq_deposit
model1.merge eq_loan
model1.merge eq_pstock
model1.merge eq_stock_trade

model1.merge eq_price_cpi
model1.merge eq_price_cpizf
model1.merge eq_price_tmuia
model1.merge eq_price_wpi
for %zz co cf cg ip ig ipc ip jj ex im
model1.merge eq_price_p{%zz}
next

model1.merge eq_idtax

'model1.merge eq_dep
'model1.merge eq_jj
'model1.merge eq_adb
'model1.merge eq_gdpmfg
'model1.merge eq_mfp

'@@@ 定義式 @@@
model1.append td=co+cf+cg+ifix+ex+jj 
model1.append le=lf*(1-0.01*ru)
model1.append pdt=gdp/le
model1.append ulc=1000*aw_mfg/pdt
model1.append gdp$ = cp$ + cg$ + ip$ +ipc$+ig$+ jj$ + ex$ - im$ '名目GDP
model1.append cp$ = co$ + cf$                                                       '名目消費
model1.append ifix$ = ip$ + ig$+ipc$                                             '名目資本形成
model1.append jj=jj$*100/pjj
model1.append pgdp = gdp$*100/gdp    'GDP平減指數
model1.append im$ = pim*im/100          '名目進口
model1.append ex$ = pex*ex/100           '名目出口
model1.append ig$ = pig*ig/100             '名目政府固定投資 
model1.append co$ = pco*co/100          '名目消費非食物
model1.append cf$ = pcf*cf/100              '名目消費食物
model1.append pcp = cp$*100/cp        '消費平減指數
model1.append pifix = ifix$*100/ifix        '資本形成平減指數
model1.append cg$ = pcg*cg/100           '名目政府消費
model1.append ipc$ = pipc*ipc/100        '名目公營事業固定投資
model1.append ip$ = pip*ip/100            '名目民間投資

' 各支出之貢獻率
for %zz co cf cg ip ig ipc ifix jj ex im
    model1.append  contrib_{%zz}_q=(p{%zz}_qavg(-4)/pgdp_qavg(-4)*({%zz}-{%zz}(-4))/gdp(-4)+(({%zz}(-4)/gdp(-4))-({%zz}_qavg(-4)/gdp_qavg(-4)))*(p{%zz}_qavg(-4)/pgdp_qavg(-4)-p{%zz}_qavg(-8)/pgdp_qavg(-8)))*100
next
' 實質GDP成長率(連鎖)
model1.append gdp_pcy  = contrib_co_q+contrib_cf_q+contrib_cg_q+contrib_ip_q+contrib_ig_q+contrib_ipc_q+contrib_jj_q+contrib_ex_q-contrib_im_q  
' 實質GDP(連鎖)
model1.append gdp=gdp(-4)*(1+gdp_pcy/100) 


' 消費對總消費貢獻率
for %zz co cf
model1.append contrib_c_{%zz}_q=(p{%zz}_qavg(-4)/pcp_qavg(-4)*({%zz}-{%zz}(-4))/cp(-4)+(({%zz}(-4)/cp(-4))-({%zz}_qavg(-4)/cp_qavg(-4)))*(p{%zz}_qavg(-4)/pcp_qavg(-4)-p{%zz}_qavg(-8)/pcp_qavg(-8)))*100
next

' 各投資對總投資貢獻率
for %zz ipc ig ip
model1.append contrib_i_{%zz}_q=(p{%zz}_qavg(-4)/pifix_qavg(-4)*({%zz}-{%zz}(-4))/ifix(-4)+(({%zz}(-4)/ifix(-4))-({%zz}_qavg(-4)/ifix_qavg(-4)))*(p{%zz}_qavg(-4)/pifix_qavg(-4)-p{%zz}_qavg(-8)/pifix_qavg(-8)))*100
next

model1.append cp=cp(-4)*(contrib_c_co_q+contrib_c_cf_q)/100+cp(-4)
model1.append ifix=ifix(-4)*(contrib_i_ig_q+contrib_i_ip_q+contrib_i_ipc_q)/100+ifix(-4)


' 實質淨出口(連鎖)
model1.append netexport= gdp(-4)*(contrib_ex_q-contrib_im_q)/100+netexport(-4)



'============  Baseline solution ====================================================================================================
model1.scenario "baseline"
model1.solve(s=d,d=s)  

model1.makegraph(a) baseline1 @endog  
model1.makegroup(a) table1 @endog

'============  Constant adjustment ====================================================================================================

model1.addassign(i)  ip pstock m1b m2 co wpi cpi jj  pifix pim pex 

smpl 2023q1 2023q1		
'co_a=0.03459
'ip_a=-0.00079
'ex_a=-0.022
'im_a=0.0315
'cpi_a=0.00249
'wpi_a=0.0197
'm1b_a= -0.0047
'm2_a=0.00033

smpl 2023q2 2023q2		
'co_a=0.04255
'ip_a=-0.0174
'ex_a=-0.01181
'im_a=0.0099
'cpi_a=0.00255
'wpi_a=0.0538
'm1b_a= 0.0244
'm2_a=0.007

smpl 2023q3 2023q3		
'co_a=0.026
'ip_a=-0.0148
'ex_a=0.0356
'im_a=0.04025
'cpi_a=-0.0006
'wpi_a=	-0.033
'm1b_a=	 0.004
'm2_a=0.0075

smpl 2023q4 2023q4	
'co_a= 0.0379
'ip_a=-0.0296
'ex_a=0.03808
'im_a= 0.051398
'cpi_a= 0.0055
'wpi_a=	-0.046
'm1b_a=	 0.001
'm2_a=0.0015

'============  Baseline prediction for NEXT year  ====================================================================================================

smpl 2023q1  2023q4
model1.solve(s=d,d=d)


