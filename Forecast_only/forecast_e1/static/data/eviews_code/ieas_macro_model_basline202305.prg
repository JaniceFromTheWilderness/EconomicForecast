''
' This code is used for Taiwan Economy Forecasting
' and is written by Kian @ IEAS at 201712

%currqul="2022q4"
%curryear="2023q4"
%nextyear="2024q4"
'=========================================================================================================================================================================
' Loading data
workfile q 1962q1 2023q4

read(s=end)  "C:\Users\s7108\Dropbox\pythonProject\Forecast_only\forecast_e1\static\data\11205_raw.xls" 60
read(s=exo)  "C:\Users\s7108\Dropbox\pythonProject\Forecast_only\forecast_e1\static\data\11205_raw.xls" 16

'save D:\SINICA\20171203\output_new.wlf

'=========================================================================================================================================================================
' Some preliminary setup -=ENDOGENOUS=-
smpl @all
series td=co+cf+cg+ifix+ex+jj                     'Total Demand
series rtaxcum=tarrif/imtw$                'Tarrif rate
series le=lf*(1-0.01*ru)                              '就業人口
series pdt=gdp/le                                         '勞動生產力
series ulc=1000*aw_mfg/pdt                      '單位生產勞動成本
series pjj= 100*jj$/jj                                   '存貨變動平減指數

' setting of tariffs (using moving average) and interest rate(重貼現率) -=EXOGENOUS=-
'smpl 2022q1 2022q4
'series rtaxcum=(rtaxcum(-1)+rtaxcum(-2)+rtaxcum(-3)+rtaxcum(-4))/4
'ir=1.375


'=========================================================================================================================================================================
'calculating the contribution to GDP for CO and CF (非食物消費與食物消費)-= In sample=-

smpl 1962q1 %currqul
'計算"年成長率"，q4的地方是年成長率
for %1 cp co cf cg ip ig ipc ifix jj ex im gdp
  series {%1}_ypcy= @pcy(@meansby({%1}, @year))
next
' 各支出"年deflator "
for %zz cp co cf cg ip ig ipc ifix jj ex im gdp
  series {%zz}_qavg = @meansby({%zz}, @year)
  series {%zz}$_qavg = @meansby({%zz}$, @year)
  series p{%zz}_qavg= @meansby({%zz}$_qavg /{%zz}_qavg, @year) '各支出年deflator, 4季的位置數值都是一樣
next
'CO and CF貢獻率
for %zz co cf 
  series contrib_{%zz}_q=(p{%zz}_qavg(-4)/pgdp_qavg(-4)*({%zz}-{%zz}(-4))/gdp(-4)+(({%zz}(-4)/gdp(-4))-({%zz}_qavg(-4)/gdp_qavg(-4)))*(p{%zz}_qavg(-4)/pgdp_qavg(-4)-p{%zz}_qavg(-8)/pgdp_qavg(-8)))*100
next

'CO and CF對C貢獻率
for %zz co cf 
series contrib_c_{%zz}_q=(p{%zz}_qavg(-4)/pcp_qavg(-4)*({%zz}-{%zz}(-4))/cp(-4)+(({%zz}(-4)/cp(-4))-({%zz}_qavg(-4)/cp_qavg(-4)))*(p{%zz}_qavg(-4)/pcp_qavg(-4)-p{%zz}_qavg(-8)/pcp_qavg(-8)))*100
next

'IG, IPC  and IP對IFIX貢獻率
for %zz ipc ig ip
series contrib_i_{%zz}_q=(p{%zz}_qavg(-4)/pifix_qavg(-4)*({%zz}-{%zz}(-4))/ifix(-4)+(({%zz}(-4)/ifix(-4))-({%zz}_qavg(-4)/ifix_qavg(-4)))*(p{%zz}_qavg(-4)/pifix_qavg(-4)-p{%zz}_qavg(-8)/pifix_qavg(-8)))*100
next

'GDP成長率(季) and 淨出口
series gdp_pcy= contrib_cp_q+contrib_cg_q+contrib_ip_q+contrib_ig_q+contrib_ipc_q+contrib_jj_q+contrib_ex_q-contrib_im_q
series netexport=ex-im




'============    Start of  Estimation (2002Q1~2021Q1)   ===========================================================================================================================
smpl 2003q1 %currqul

'@@@    消費   @@@  
' 食物消費
equation eq_goods_cf.cointreg(cov=hac) log(cf) c log(cf(-1)) log(cf(-4)) log(gdp) log(pop) log(pstock) log(cpi) @seas(2) @seas(3) @seas(4) @isperiod("2003q2") @isperiod("2009q1") 
' 非食物消費
equation eq_goods_co.cointreg(trend=linear, cov=hac) log(co) c log(co(-1)) log(co(-4)) irc @pcy(cpizf) log(pstock) @pch(loan) @seas(3) @isperiod("2003q2")  (@isperiod("2008q3")+@isperiod("2008q4")+@isperiod("2009q1")+@isperiod("2009q2"))  'ma(1) ma(2)


'@@@    投資   @@@  
' 民間投資函數
equation eq_ip.cointreg(cov=hac)  log(ip) c log(ip(-1))  log(ip(-4)) _
              log(ig(-1))  log(ig(-2)) irc log(ex) @seas(2) @seas(3) @seas(4)  _
              @isperiod("2003q2") (@isperiod("2008q3")+@isperiod("2008q4")+@isperiod("2009q1")+@isperiod("2009q2")) @isperiod("2011q4") @isperiod("2019q4")  'log(mgf_sale_idx) _

'equation eq_ip.cointreg(TREND=linear, cov=hac)  log(ip) c log(ip(-1)) log(ig) _
'                 iri log(td) @seas(2) @seas(3) @seas(4)  _
'                @isperiod("2003q2") (@isperiod("2008q3")+@isperiod("2008q4")+@isperiod("2009q1")+@isperiod("2009q2")) @isperiod("2011q4")

' Lin(2010) model
'equation eq_ip.ls(n) log(ip) c log(ip(-1)) log(ip(-4)) mgf_sale_idx log(gdp) iri log(ig) _
                   '@isperiod("2003q2") @isperiod("2008q3") @isperiod("2008q4") 'log(bond_trade) log(stock_trade) 

' 製造業銷售
equation eq_mgfsales.cointreg(cov=hac) log(mgf_sale_idx) c log(gdp) @isperiod("2003q2") (@isperiod("2008q3")+@isperiod("2008q4")+@isperiod("2009q1")+@isperiod("2009q2")) (@isperiod("2015q3")+@isperiod("2015q4")+@isperiod("2016q1")) 'ar(1) 

'@@@    貿易部門   @@@ 
' 出口
equation eq_ex.cointreg(cov=hac) log(ex) c log(ex(-1)) log(ex(-2)) log(eroc*wpx/pex)  log(gdp_usa) log(gdp_chn)  @seas(2) @seas(3) @seas(4) (@isperiod("2008q3")+@isperiod("2008q4")+@isperiod("2009q1")+@isperiod("2009q2")) @isperiod("2019q1") 'ar(1) 
'equation eq_ex.ls(n) log(ex) c log(ex(-1)) log(ex(-4)) log(eroc) log(gdpmfg) log(gdp_usa) log(pex) @seas(2) @seas(3) @seas(4) @isperiod("2008q3") @isperiod("2008q4")  @isperiod("2009q1")  ar(1)' log(gdp_chn)

' 進口
equation eq_im.cointreg(trend=linear, cov=hac) log(im) c log(im(-1)) log(im(-4)) log(td) log(ex) log(pim)   eroc*wpx*(1+0.01*rtaxcum)/wpi @seas(2) @seas(3) @seas(4) (@isperiod("2008q3")+@isperiod("2008q4")+@isperiod("2009q1")+@isperiod("2009q2"))  @isperiod("2019q1")  'ar(1) 
'equation eq_im.ls(n) log(im) c log(im(-1)) log(im(-4)) log(gdp) log(wpi/pim)  @seas(2) @seas(3) @seas(4)  @isperiod("2008q4") ar(2) ar(4)

'@@@    勞動部門   @@@ 
'勞動力
equation eq_lf.cointreg(cov=hac) log(lf) c log(pop*lf(-1)/pop(-1)) log(pop*lf(-4)/pop(-4)) @pcy(gdp) @pcy(aw_mfg) @seas(2) @seas(3) @seas(4) 'ar(1) 
'失業率
equation eq_ru.cointreg(cov=hac) ru c ru(-1) ru(-4) mgf_sale_idx/log(gdp) gdp_chn @seas(2) @seas(3) @seas(4) @isperiod("2009q1") @isperiod("2020q1")'ar(1)
'製造業 薪資
equation eq_aw_mfg.ls(n) log(aw_mfg) c log(aw_mfg(-1)) log(aw_mfg(-4)) log(cpi) log(ru) log(pdt) ar(1) @isperiod("2009q1") @seas(2) @seas(3) @seas(4)


'@@@    金融市場   @@@ 
' M2
equation eq_m2.cointreg(cov=hac) log(m2) c log(m2(-1)) log(gdp) irc-ircus d(stock_trade) @seas(2) @seas(3) @seas(4) @isperiod("2007q4") @isperiod("2008q3") @isperiod("2009q1") 

' M1B
equation eq_m1b.cointreg(cov=hac) log(m1b) c log(m1b(-1)) rmibon d(pstock) @pcy(cpi) d(gdp) @seas(2) @seas(3) @seas(4) @isperiod("2008q3") @isperiod("2009q2") 'ar(1)

' 準備貨幣
equation eq_mrda.cointreg(cov=hac) log(mrda) c log(mrda(-1))  log(pstock) log(gdp) log(deposit) @pcy(rmibon) @seas(2) @seas(3) @seas(4) 'ar(1) 

' 隔夜拆款利率
equation eq_rmibon.ls(n) rmibon c rmibon(-1) @pch(cpizf) ir log(pstock)

' 一年定存利率
equation eq_irc.ls(n) irc c ir rmibon ar(1) @seas(2) @seas(3) @seas(4)

' 一般銀行放款基準利率
equation eq_iri.ls(n) iri c ffr rmibon ir ar(1) @seas(2) @seas(3) @seas(4)

' 一般銀行存款餘額
equation eq_deposit.cointreg(cov=hac)  log(deposit) c log(deposit(-1)) irc(-1) d(log(gdp(-1))) 'd(bond_trade)

' 全體貨幣機構放款量
equation eq_loan.cointreg(cov=hac)  @pcy(loan) c @pcy(loan(-1)) @pcy(m1b) iri(-4) @pcy(ip+co+ig) 'ar(1)

' 股價指數
equation eq_pstock.cointreg(trend=linear, cov=hac)  log(pstock) c log(pstock(-1)) log(stock_trade) mgf_sale_idx iri-irc' ar(1)

' 股票交易金額
equation eq_stock_trade.cointreg(trend=linear, cov=hac) log(stock_trade) c log(stock_trade(-1)) log(pstock) d(loan) 'ar(1) 'd(bank_inv_non) ar(1)

'@@@    物價   @@@ 
' 一般物價指數
equation eq_price_cpi.cointreg(cov=hac) log(cpi) c log(cpi(-1)) iri-irc log(wpi) log(cpizf) @pcy(idtax) @isperiod("2009q1") @seas(2) @seas(3) @seas(4)

' 核心物價指數
equation eq_price_cpizf.cointreg(cov=hac) log(cpizf) c  log(cpizf(-1)) d(rmibon) ru log(m2) log(pim) @seas(3) @seas(2) 'ar(1)


' 進口平減指數
equation eq_price_pim.cointreg(cov=hac) log(pim) c log(pim(-1)) log(pim(-4)) (rtaxcum*0.01+1)*tmuia$$*eroc log(poil) log(ipx_jap) @seas(2) @seas(3) @seas(4) @isperiod("2008q4")' ar(1) 

' 出口平減指數
equation eq_price_pex.cointreg(cov=hac) log(pex) c log(pex(-1)) log(pex(-4)) log(wpi) @seas(2) @seas(3) @seas(4) @isperiod("2008q2") @isperiod("2008q3")  ' ar(1) ar(2) ar(4)


' 進口物價指數
equation eq_price_tmuia.cointreg(cov=hac) log(tmuia$$) c log(poil) log(wpx) log(ipx_jap) @seas(2) @seas(3) @seas(4) @isperiod("2008q4") ' ar(1) 


' 躉售物價指數
equation eq_price_wpi.cointreg(cov=hac) log(wpi) c @pcy(ulc) log(pim) log(wpx) @seas(2) @seas(3) @seas(4)'ar(1) 

' 存貨變動平減指數
equation eq_price_pjj.cointreg(cov=hac) pjj c wpi @seas(2) @seas(3) @seas(4) @isperiod("2006q2") 'ar(1)

' pcp=民間消費物價平減指數
equation eq_price_pco.cointreg(cov=hac) log(pco) c log(pco(-1)) log(pco(-4)) log(cpi) @seas(2) @seas(3) @seas(4) 'ar(1)

' pcp=民間消費物價平減指數
equation eq_price_pcf.cointreg(trend=Quadratic, cov=hac) log(pcf) c log(pcf(-1)) log(pcf(-4)) log(cpi) @seas(2) @seas(3) @seas(4) 'ar(1)

' pcg==政府消費物價平減指數
equation eq_price_pcg.cointreg(cov=hac) log(pcg) c log(pcg(-1)) log(pcg(-4))  log(cpi) @seas(2) @seas(3) @seas(4) 'ar(1)

' pig==政府固定投資物價平減指數
equation eq_price_pig.cointreg(cov=hac) log(pig) c log(pig(-1)) log(wpi) @seas(2) @seas(3) @seas(4)  'ar(1)

' pipc=公營事業固定投資物價平減指數
equation eq_price_pipc.cointreg(cov=hac) log(pipc) c log(pipc(-1)) log(pipc(-4)) log(wpi) @seas(4) 'ar(1) 

' pifix=民間固定投資平減指數物價平減指數
equation eq_price_pip.cointreg(cov=hac) log(pip) c log(pip(-1)) log(pip(-4)) log(wpi) log(wpi(-4)) @seas(2) @seas(3) @seas(4) 'ar(1) 

' 間接稅
equation eq_idtax.cointreg(cov=hac) log(idtax) c log(td) idtax(-4)/td(-4) log(mgf_sale_idx) @seas(2) @seas(3) @seas(4)



'其餘設為外生之變數或沒用到之變數
'折舊
'equation eq_dep.ls(n) log(dep) c log(gdp*dep(-1)/gdp(-1)) log(ifix(-3)) log(wpi) log(cpi) @seas(2) @seas(3) @seas(4) ma(1) ma(2)
' 存貨變動
'equation eq_jj.ls(n) jj c jj(-1) iri(-1)-@pchy(cpi(-1)) ifix(-2)+ifix(-3)+ifix(-4) @seas(2)
'equation eq_adb.ls(n) log(bank_inv_non) c log(mrda) rmibon log(pstock) log(loan(-1)) ar(1) ar(2)
'製造業生產毛額
'equation eq_gdpmfg.ls(n) log(gdpmfg) c log(gdp) log(mfp) ma(1) @seas(2) @seas(3) @seas(4)
'技術進步
'equation eq_mfp.ls(n) d(mfp) c log(poil) log(ifix) log(ifix(-1)+ifix(-2)+ifix(-3)+ifix(-4)) @seas(2) @seas(3) @seas(4)
'============    End of  Estimation    =====================================================================================================================================


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
model1.merge eq_ex
model1.merge eq_im
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

model1.addassign(i)  ip pstock m1b m2 co ex im wpi cpi jj  pifix pim pex 

smpl 2023q1 2023q1		
co_a=0.03459
ip_a=-0.00079
ex_a=-0.022
im_a=0.0315
cpi_a=0.00249
wpi_a=0.0197
m1b_a= -0.0047
m2_a=0.00033

smpl 2023q2 2023q2		
co_a=0.04255
ip_a=-0.0174
ex_a=-0.01181
im_a=0.0099
'cpi_a=0.00255
'wpi_a=0.0538
'm1b_a= 0.0244
'm2_a=0.007

smpl 2023q3 2023q3		
co_a=0.026
ip_a=-0.0148
ex_a=0.0356
im_a=0.04025
'cpi_a=-0.0006
'wpi_a=	-0.033
'm1b_a=	 0.004
'm2_a=0.0075

smpl 2023q4 2023q4	
co_a= 0.0379
ip_a=-0.0296
ex_a=0.03808
im_a= 0.051398
'cpi_a= 0.0055
'wpi_a=	-0.046
'm1b_a=	 0.001
'm2_a=0.0015

'============  Baseline prediction for NEXT year  ====================================================================================================

smpl 2023q1  2023q4
model1.solve(s=d,d=d)

'============  Build the table for LINK  and forcaste next year ====================================================================================================


smpl 2011q1 2023q4   '計算年成長率，q4的地方是年成長率
for %1  gdp co cf cp ip ifix ex im netexport gdp$ co$ cf$ cp$ cg$ ip$ ig$ ipc$ ifix$ ex$ im$  jj 
   series  {%1}_ysum  =  @movsum({%1}_0, 4)/1000                   
   series  {%1}_ypcy  =  @pcy({%1}_ysum)
next

smpl 2011q1 2023q4   '計算年成長率，q4的地方是年成長率
for %1  m1b m2
 series {%1}_0={%1}_0/1  
   series  {%1}_ysum  =  @movsum({%1}_0, 4)/4         
   series  {%1}_ypcy  =  @pcy({%1}_ysum)
next

for %1  pgdp pcp pcf pcp pcg pip pig pipc  pifix pex pim cpi wpi 
   series  {%1}_ysum  =  @movsum({%1}_0, 4)/4                      
   series  {%1}_ypcy  =  @pcy({%1}_ysum)
next

for %1  poil eroc gdp_usa gdp_chn  
   series  {%1}_ysum  =  @movsum({%1}, 4)/4                      
   series  {%1}_ypcy  =  @pcy({%1}_ysum)
next

for %1  cg ig ipc 
   series  {%1}_ysum  =  @movsum({%1}, 4)/1000                       
   series  {%1}_ypcy  =  @pcy({%1}_ysum)
next

for %2  2012q1 2012q2 2012q3 2013q1 2013q2 2013q3  2014q1 2014q2 2014q3  2015q1 2015q2 2015q3 2016q1 2016q2 2016q3 2017q1 2017q2 2017q3 2018q1 2018q2 2018q3  2019q1 2019q2 2019q3  2020q1 2020q2 2020q3 2021q1 2021q2 2021q3 2022q1 2022q2 2022q3 2023q1 2023q2 2023q3
      smpl %2  %2
      for %1  gdp co cf cp cg ip ig ipc ifix ex im cpi wpi m1b m2 netexport pgdp pcp pcf pcp pcg pip pig pipc  pifix pex pim gdp$ co$ cf$ cp$ cg$ ip$ ig$ ipc$ ifix$ ex$ im$ gdp_usa gdp_chn jj
      series  {%1}_ypcy  = na
      series  {%1}_ysum =na
   next

next
smpl 2011q1 2023q4
 group LINK_ypcy cp$_ypcy cg$_ypcy ifix$_ypcy ex$_ypcy im$_ypcy gdp$_ypcy cp_ypcy cg_ypcy ifix_ypcy ex_ypcy im_ypcy gdp_ypcy pcp_ypcy pcg_ypcy pifix_ypcy pex_ypcy pim_ypcy pgdp_ypcy poil_ypcy eroc_ypcy cpi_ypcy wpi_ypcy
 group LINK_level cp$_ysum cg$_ysum ifix$_ysum ex$_ysum im$_ysum gdp$_ysum cp_ysum cg_ysum ifix_ysum ex_ysum im_ysum gdp_ysum pcp_ysum pcg_ysum pifix_ysum pex_ysum pim_ysum  pgdp_ysum


smpl 2017q1 2023q4
group Link_table  cp_ypcy cg_ypcy ifix_ypcy ex_ypcy im_ypcy gdp_ypcy pcp_ypcy pcg_ypcy pifix_ypcy pex_ypcy pim_ypcy pgdp_ypcy  cpi_ypcy wpi_ypcy  m1b_ypcy m2_ypcy  gdp_usa_ypcy gdp_chn_ypcy   poil_ypcy eroc_ypcy poil eroc


smpl 2017q1 2023q4
group link_ypcy_pre cp_ypcy cg_ypcy ifix_ypcy ex_ypcy im_ypcy gdp_ypcy pcp_ypcy pcg_ypcy pifix_ypcy pex_ypcy pim_ypcy pgdp_ypcy  cpi_ypcy wpi_ypcy poil_ypcy eroc_ypcy gdp_usa_ypcy 


'============  Build the table for IEAS  ====================================================================================================



smpl 2013q1 2023q4
for %1  gdp co cf cp ip ifix ex im m1b m2 netexport  cpi wpi  
   series  {%1}_pcy  =  @pcy({%1}_0)
next
for %1  gdp_usa gdp_chn wpx ircus ffr ipx_jap pop cg ipc ig jj
   series  {%1}_pcy  =  @pcy({%1})
next
smpl 2022q1 2023q4
group IEAS_ypcy gdp_ypcy cp_ypcy ip_ypcy ex_ypcy im_ypcy netexport_ypcy cpi_ypcy wpi_ypcy m1b_ypcy m2_ypcy eroc_ypcy  poil_ypcy gdp_usa_ypcy gdp_chn_ypcy    
group IEAS_pcy gdp_pcy cp_pcy ip_pcy ex_pcy im_pcy netexport_pcy cpi_pcy wpi_pcy m1b_pcy m2_pcy  gdp_usa_pcy gdp_chn_pcy   eroc poil  wpx ircus ffr ipx_jap pop 

group IEAS_press1 gdp_0 cp_0 cg ifix_0 ip_0 ipc ig jj_0 netexport_0 ex_0 im_0 cpi_0 wpi_0 m1b_0 m2_0 eroc
group IEAS_press2 gdp_pcy cp_pcy cg_pcy ifix_pcy ip_pcy ipc_pcy ig_pcy jj_pcy netexport_pcy ex_pcy im_pcy cpi_pcy wpi_pcy m1b_pcy m2_pcy 
group IEAS_press3 gdp_ysum cp_ysum cg_ysum ifix_ysum ip_ysum ipc_ysum ig_ysum netexport_ysum ex_ysum im_ysum cpi_ysum wpi_ysum m1b_ysum m2_ysum   eroc
group IEAS_press4 gdp_ypcy cp_ypcy cg_ypcy ifix_ypcy ip_ypcy ipc_ypcy ig_ypcy  netexport_ypcy ex_ypcy im_ypcy cpi_ypcy wpi_ypcy m1b_ypcy m2_ypcy

show  IEAS_ypcy

show  IEAS_press2

show  IEAS_press4

	' Export data to Excel
'wfsave(type=excelxml,mode=update) "D:\User_Data\Desktop\0\0 situation.xlsx" range=t2!a1 @smpl 2022q1 2023q4 @keep   IEAS_press2 

'wfsave(type=excelxml,mode=update) "D:\User_Data\Desktop\0\0 situation.xlsx" range=t2!a15 @smpl 2022q1 2023q4 @keep   IEAS_press4


