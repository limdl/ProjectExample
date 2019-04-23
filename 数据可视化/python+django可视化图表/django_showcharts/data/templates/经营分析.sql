select top 10
客户编号=saclId
,客户名称=saclName
,成交展会=(select prName from tb_Product where prId=saprId)
,省份=(select prNameCN from tb_Province where prId=(select ciPrId from tb_City where ciId=(select clAreaId from tb_ClientMain where clId=saclId)))
,城市=(select ciNameCN from tb_City where ciId=(select clAreaId from tb_ClientMain where clId=saclId))

,举办国家=(select ctNameCN from tb_Country where ctId=(select piValueI from tb_ProductInfo where piprId=saprId and pitpId=(select tpId from tb_PTProperty where tpptId=(select prType from tb_Product where prId=saprId) and tpName='举办国家')))
,举办城市=(select ciNameCN from tb_City where ciId=(select piValueI from tb_ProductInfo where piprId=saprId and pitpId=(select tpId from tb_PTProperty where tpptId=(select prType from tb_Product where prId=saprId) and tpName='举办城市')))
,展位面积=saArea
,随团人数=saGroupNum
,成交金额=cast(totalYingShou as float)

from v_SalesAuditList a
where sassId=3047 and sasdId not in(1044,1047,1049,1054,1055,1058,1060,1062,1068,1070,1072,1076,1077,1079)
--and saBocDate between '2017-01-01' and '2017-12-31 23:59:59'
and left((select prName from tb_Product where prId=saprId),4)='2018'


--营业额完成情况
select sum(cast(totalYingShou as float))/10000 from v_SalesAuditList 
where sassId=3047 and sasdId not in(1044,1047,1049,1054,1055,1058,1060,1062,1068,1070,1072,1076,1077,1079)
and left((select prName from tb_Product where prId=saprId),4)='2018'


--各月营业额
select 月份=convert(varchar(7),saBocDate,120) 
,营业额=sum(cast(totalYingShou as float))/10000 
from v_SalesAuditList 
where sassId=3047 and sasdId not in(1044,1047,1049,1054,1055,1058,1060,1062,1068,1070,1072,1076,1077,1079) 
and left((select prName from tb_Product where prId=saprId),4)='2018' and year(saBocDate)=2018 
group by convert(varchar(7),saBocDate,120)


--客户城市分布
select
省份=(select convert(nvarchar(20),replace(prNameCN,'市','')) from tb_Province where prId=(select ciPrId from tb_City where ciId=clAreaId))
,城市=(select convert(nvarchar(20),replace(ciNameCN,'市','')) from tb_City where ciId=clAreaId)
,数量=count(1)
from tb_ClientMain
where clId in(select saclId from v_SalesAuditList 
			  where sassId=3047 and sasdId not in(1044,1047,1049,1054,1055,1058,1060,1062,1068,1070,1072,1076,1077,1079)
			  and left((select prName from tb_Product where prId=saprId),4)='2018'
			  )
group by clAreaId
order by 数量 desc

select
省份=prNameCN
,数量=(select count(1) from tb_ClientMain
	   where (select ciPrId from tb_City where ciId=clAreaId)=prId
	   and clId in(select saclId from v_SalesAuditList
				  where sassId=3047 and sasdId not in(1044,1047,1049,1054,1055,1058,1060,1062,1068,1070,1072,1076,1077,1079)
				  and left((select prName from tb_Product where prId=saprId),4)='2018'
				  )
	  )
from tb_Province
where prNameCN<>'其他'
order by 数量 desc


select 
                城市=(select convert(nvarchar(20),ciNameCN) from tb_City where ciId=clAreaId) 
                ,数量=count(1) 
                from tb_ClientMain 
                where clId in(select saclId from v_SalesAuditList 
                              where sassId=3047 
                              and sasdId not in(1044,1047,1049,1054,1055,1058,1060,1062,1068,1070,1072,1076,1077,1079)
                and left((select prName from tb_Product where prId=saprId),4)='2018'
                )
				and (select convert(nvarchar(20),ciNameCN) from tb_City where ciId=clAreaId)<>'海阳市'
                group by clAreaId 
                order by 数量 desc

--成交客户画像
--省份、城市、行业、展会、摊位类型
select top 1 展会行业,数量=count(1) from(
select 
展会行业=(select in_Name_CN from tb_Industry where cast(in_Code as int)=(select piValueI from tb_ProductInfo where piprId=saprId and pitpId=(select tpId from tb_PTProperty where tpptId=(select prType from tb_Product where prId=saprID) and tpName='展会行业')))
from v_SalesAuditList a
where sassId=3047 and sasdId not in(1044,1047,1049,1054,1055,1058,1060,1062,1068,1070,1072,1076,1077,1079)
--and saBocDate between '2017-01-01' and '2017-12-31 23:59:59'
and left((select prName from tb_Product where prId=saprId),4)='2018'
)a
group by 展会行业
order by 数量 desc

select top 1
成交展会=replace(replace((select prName from tb_Product where prId=saprId),'2018年',''),'览会','')
,数量=count(1)
from v_SalesAuditList a
where sassId=3047 and sasdId not in(1044,1047,1049,1054,1055,1058,1060,1062,1068,1070,1072,1076,1077,1079)
--and saBocDate between '2017-01-01' and '2017-12-31 23:59:59'
and left((select prName from tb_Product where prId=saprId),4)='2018'
group by saprId
order by 数量 desc