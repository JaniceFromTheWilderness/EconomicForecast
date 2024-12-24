%currqul="2022q4"
%curryear="2023q4"
%nextyear="2024q4"

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
'equation eq_ex.cointreg(cov=hac) log(ex) c log(ex(-1)) log(ex(-2)) log(eroc*wpx/pex)  log(gdp_usa) log(gdp_chn)  @seas(2) @seas(3) @seas(4) (@isperiod("2008q3")+@isperiod("2008q4")+@isperiod("2009q1")+@isperiod("2009q2")) @isperiod("2019q1") 'ar(1) 
'equation eq_ex.ls(n) log(ex) c log(ex(-1)) log(ex(-4)) log(eroc) log(gdpmfg) log(gdp_usa) log(pex) @seas(2) @seas(3) @seas(4) @isperiod("2008q3") @isperiod("2008q4")  @isperiod("2009q1")  ar(1)' log(gdp_chn)

' 進口
'equation eq_im.cointreg(trend=linear, cov=hac) log(im) c log(im(-1)) log(im(-4)) log(td) log(ex) log(pim)   eroc*wpx*(1+0.01*rtaxcum)/wpi @seas(2) @seas(3) @seas(4) (@isperiod("2008q3")+@isperiod("2008q4")+@isperiod("2009q1")+@isperiod("2009q2"))  @isperiod("2019q1")  'ar(1) 
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


