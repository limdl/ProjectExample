import pandas as pd
import pymssql
from pyecharts import Gauge, Liquid, Line, Bar, Geo, Map, WordCloud, Page

dbmssql = pymssql.connect('localhost', 'sa', 'sa', 'db_tables', 'utf8')

with dbmssql:
    cur = dbmssql.cursor()
    cur.execute("select sum(cast(totalYingShou as float))/10000 from v_SalesAuditList \
                where sassId=3047 and sasdId not in(1044,1047,1049,1054,1055,1058,1060,1062,1068,1070,1072,1076,1077,1079)\
                and left((select prName from tb_Product where prId=saprId),4)='2018'"
                )
    totalYingShou = cur.fetchall()[0][0]
    totalYingTarget = 25000

    cur.execute("select 月份=convert(varchar(7),saBocDate,120) \
                ,营业额=sum(cast(totalYingShou as float))/10000 \
                from v_SalesAuditList \
                where sassId=3047 and sasdId not in(1044,1047,1049,1054,1055,1058,1060,1062,1068,1070,1072,1076,1077,1079) \
                and left((select prName from tb_Product where prId=saprId),4)='2018' and year(saBocDate)=2018 \
                group by convert(varchar(7),saBocDate,120)"
                )
    totalYingShouByMonth = pd.DataFrame(cur.fetchall())

    cur.execute("select \
                省份=convert(nvarchar(10),prNameCN) \
                ,数量=(select count(1) from tb_ClientMain\
                       where (select ciPrId from tb_City where ciId=clAreaId)=prId \
                       and clId in(select saclId from v_SalesAuditList \
                                   where sassId=3047 \
                                   and sasdId not in(1044,1047,1049,1054,1055,1058,1060,1062,1068,1070,1072,1076,1077,1079) \
                                   and left((select prName from tb_Product where prId=saprId),4)='2018'\
                                   )\
                      )\
                from tb_Province \
                where prNameCN<>'其他' \
                order by 数量 desc"
                )
    provienceClients = pd.DataFrame(cur.fetchall())

    cur.execute("select top 150\
                城市=(select convert(nvarchar(20),replace(ciNameCN,'市','')) from tb_City where ciId=clAreaId) \
                ,数量=count(1) \
                from tb_ClientMain \
                where clId in(select saclId from v_SalesAuditList \
                              where sassId=3047 \
                              and sasdId not in(1044,1047,1049,1054,1055,1058,1060,1062,1068,1070,1072,1076,1077,1079)\
                and left((select prName from tb_Product where prId=saprId),4)='2018'\
                )\
                and (select convert(nvarchar(20),ciNameCN) from tb_City where ciId=clAreaId) not in('海阳市','宁国市') \
                group by clAreaId \
                order by 数量 desc"
                )
    cityClients = pd.DataFrame(cur.fetchall())
    fujianClients = cityClients.loc[cityClients[0].isin(['厦门', '泉州', '福州', '漳州', '莆田', '宁德', '龙岩', '三明', '南平'])]

    cur.execute("select top 150\
                城市=(select convert(nvarchar(20),replace(ciNameCN,'市','')) from tb_City where ciId=clAreaId) \
                ,数量=count(1) \
                from tb_ClientMain \
                where clId in(select saclId from v_SalesAuditList \
                              where sassId=3047 \
                              and sasdId not in(1044,1047,1049,1054,1055,1058,1060,1062,1068,1070,1072,1076,1077,1079)\
                and left((select prName from tb_Product where prId=saprId),4)='2018'\
                )\
                and (select convert(nvarchar(20),ciNameCN) from tb_City where ciId=clAreaId) not in('海阳市','宁国市') \
                group by clAreaId \
                order by 数量 desc"
                )

    #     cur.execute()
    #     datas = pd.DataFrame(cur.fetchall())

    cur.close()
dbmssql.close()

liquid = Liquid("营业额完成情况", width=1000, height=320)
liquid.add("", [round(totalYingShou / totalYingTarget, 2), 0.5, 0.4, 0.3], is_liquid_outline_show=False)

gauge = Gauge("项目完成情况", width=1000, height=320)
gauge.add("", "完成率", 90)

x_month = [i + '月' for i in list(totalYingShouByMonth[0])]
y_totalYingShou = [round(i, 2) for i in list(totalYingShouByMonth[1])]
bar = Bar("各月营业额分布(万)", width=1000, height=320)
bar.add("", x_month, y_totalYingShou)

provienceClientNum = list(provienceClients[1])
attr = [str.replace('市', '') for str in list(provienceClients[0])]
map_provience = Map("客户省份分布", width=1000, height=600)
map_provience.add("", attr, provienceClientNum, maptype='china')
# map_provience.add("", attr, provienceClientNum, maptype="china"
#         , is_visualmap=True, is_label_show=True, is_map_symbol_show=False, visual_text_color="#000"
#         , visual_range=[0, 800]  # http://pyecharts.org/#/zh-cn/charts_configure?id=visualmap
#         , visual_range_color=['#FFF0F5', '#FF1493', '#d94e5d']  ##默认['#50a3ba', '#eac763', '#d94e5d']
#         # 颜色编码http://xh.5156edu.com/page/z1015m9220j18754.html
#         )

fujianClientNum = list(fujianClients[1])
attr = [str + '市' for str in list(fujianClients[0])]
map_fujian = Map("福建客户分布", width=1000, height=500)
map_fujian.add(
    "", attr, fujianClientNum, maptype="福建", is_visualmap=True, visual_text_color="#000"
    , visual_range=[0, 200]  # http://pyecharts.org/#/zh-cn/charts_configure?id=visualmap
    , is_label_show=True
    , is_map_symbol_show=False
    , visual_range_color=['#FFFFFF', '#FF1493', '#d94e5d']  ##默认['#50a3ba', '#eac763', '#d94e5d']
)
map_fujian

cityClientNum = list(cityClients[1])
attr = list(cityClients[0])
geo = Geo("客户城市分布", width=1000, height=600,
          title_color="#fff"
          # ,title_pos="center"
          , background_color="#404a59",
          )
geo.add("", attr, cityClientNum, type='effectScatter', is_random=True,
        effect_scale=4, effect_brushtype='stroke', effect_period=4,
        # effect效果 http://pyecharts.org/#/zh-cn/charts_base
        is_visualmap=True, is_map_symbol_show=False, visual_text_color="#000",
        visual_range=[0, 200],
        geo_cities_coords={'阿城': ['', ''], },
        symbol_size=4,

        #     is_piecewise=True,
        #     visual_split_number=5,
        )

name = ['广东', '深圳', '建材', '美国', '供应商', '员工人数100-500人', '注册资本500-1000万'
    , '国外参展', '国内参展', '品牌客户'
        ]
value = [781, 202, 909, 145, 50, 90, 45, 8, 11, 5]

wordcloud = WordCloud("客户画像", width=1000, height=350)
wordcloud.add("", name, value, shape='diamond')

page = Page()
page.add(liquid)
page.add(gauge)
page.add(bar)
# page.add(map_provience)
page.add(map_fujian)
# page.add(geo)
page.add(wordcloud)
page.render()