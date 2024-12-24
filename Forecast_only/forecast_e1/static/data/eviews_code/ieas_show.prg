%currqul="2022q4"
%curryear="2023q4"
%nextyear="2024q4"

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
