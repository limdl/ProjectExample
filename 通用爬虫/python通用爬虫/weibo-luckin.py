import requests
from lxml import etree
import time,datetime,sqlite3
import pandas as pd

class weibo_luckin():
    start_url = 'https://s.weibo.com/weibo?q=%E7%91%9E%E5%B9%B8%E5%92%96%E5%95%A1&typeall=1&suball=1&Refer=SWeibo_box&page={}'

    Cookie = 'SINAGLOBAL=9296706455372.553.1547262203437; un=limjixian@sina.com; login_sid_t=27eef2c50ab2112f3e1f77297590ee46; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=4033969224363.172.1554722884154; ULV=1554722884161:30:3:1:4033969224363.172.1554722884154:1554299775131; WBtopGlobal_register_version=edef3632d17f5fb3; webim_unReadCount=%7B%22time%22%3A1554724743828%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D; UOR=,,login.sina.com.cn; SCF=Agr8b1rSoBW-eFPEELcsy2XIh2vjjxIJ_BaNtezU2mgWOgguVXn9qiE50945aFHOteI4uVBnucfjHH0L83b3QDw.; SUB=_2A25xr0mIDeRhGedN71IT9ibOyD6IHXVS3TxArDV8PUNbmtBeLUH2kW9NWqZJG4GCSkYOmBLUaKA9AdCmmbjWXEmE; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5-E986C8gQIb9ai00PVS.i5JpX5K2hUgL.Fo20Sh5ESonEe0z2dJLoI7LPqgp.9g4eIgRt; SUHB=00xoKHdbfogWCZ; ALF=1555330230; SSOLoginState=1554725336; WBStorage=201904082100|undefined'

    headers = {
        'Host':'s.weibo.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Cookie':Cookie,
    }

    def __init__(self):
        
    
    def parse_time(self,time_str):
        if '分钟前' in time_str:
            time_temp = int(time_str.split('分钟前')[0])
            new_time = (datetime.datetime.now() + datetime.timedelta(minutes=time_temp)).strftime("%Y-%m-%d %H:%M")
        elif '今天' in time_str:
            time_temp = time_str.split('今天')[1]
            new_time = (datetime.datetime.now()).strftime("%Y-%m-%d") + ' ' +time_temp
        elif '月' in time_str and '日' in time_str:
            time_temp = time_str.replace('月','-').replace('日','-')
            new_time = (datetime.datetime.now()).strftime("%Y") + '-' +time_temp
        return new_time

    def insert_sql(self,content_info):
        conn = sqlite3.connect('weibo.db')
        cur = conn.cursor()

        try:
            create_sql = '''create table tb_weibo(
            mid varchar(20),
            user_name varchar(100),
            user_link varchar(500),
            user_type varchar(20),
            content_txt varchar(8000),
            content_time varchar(20),
            phone_nofollow varchar(100)
            )'''
            cur.execute(create_sql)
        except:
            select_sql = 'select mid from tb_weibo'
            cur.execute(select_sql)
            datas = pd.DataFrame(cur.fetchall())

            mid_list = list(datas[0])
            print(mid_list)
            if content_info['mid'] in mid_list:
                insert_type = 'break'
            else:
                print('*************************************************************************')
                l = list(content_info.values())
                insert_sql = 'insert into tb_weibo values("{}","{}","{}","{}","{}","{}","{}")'.format(l[0],l[1],l[2],l[3],l[4],l[5],l[6])
                cur.execute(insert_sql)
                conn.commit()
                insert_type = 'continue'
        conn.close()
        return insert_type

    for page in range(1,3):
        url = start_url.format(page)
        resp = requests.get(start_url,headers=headers)
        html = etree.HTML(resp.text)
        item = html.xpath('.//div[@class="card-wrap" and @action-type="feed_list_item"]')
        content_info = {}
        for i in item:
            # content_info['page'] = page
            content_info['mid'] = "".join(i.xpath('./@mid')).strip()
            content_info['user_name'] = "".join(i.xpath('.//descendant::div[@class="content"]/div/div/a[@class="name"]/@nick-name')).strip()
            content_info['user_link'] = 'https:'+"".join(i.xpath('.//descendant::div[@class="content"]/div/div/a[@class="name"]/@href')).strip().split('?refer')[0]
            content_info['user_type'] = "".join(i.xpath('.//descendant::div[@class="content"]/div/div/a[@target="_blank" and @title]/@title')).strip()
            content_info['content_txt'] = "".join(i.xpath('.//descendant::div[@class="content"]/p[@class="txt"][position()=last()]//text()')).strip()
            content_info['content_time'] = parse_time("".join(i.xpath('.//descendant::div[@class="content"]/p[@class="from"]/a[@suda-data]/text()')).strip())
            content_info['phone_nofollow'] = "".join(i.xpath('.//descendant::div[@class="content"]/p[@class="from"]/a[@rel="nofollow"]/text()')).strip()

            insert_type = insert_sql(content_info)
            print(insert_type)
            print(list(content_info.values()))
        time.sleep(2)

