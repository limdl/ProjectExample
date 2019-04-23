# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlwt,xlrd,os
from xlutils.copy import copy

class ExhibitionspiderPipelineExcel(object):
    # 创建excel表
    rows = 1
    foldname = 'D:/'  # 保存目录
    filename = '1.xls'  # 保存文件名
    sheetheader = ['序号', '公司名称', '英文名称', '区号', '电话1', '电话2', '传真', '移动电话', '联系人', '邮箱', '网址', '地址', '英文地址', '企业类型',
                   '主营产品', '主营行业', '国家', '城市', 'url']
    def __init__(self):
        if not os.path.exists(self.foldname + self.filename):
            workbook = xlwt.Workbook()
            worksheet = workbook.add_sheet('sheet1')
            # 写入表头
            for h in range(0, len(self.sheetheader)):
                worksheet.write(0, h, self.sheetheader[h])
            workbook.save(self.foldname + self.filename)

    # 写入数据
    def process_item(self,item,spider):
        exhibitorlist = [list(item.values())]
        oldWb = xlrd.open_workbook(self.foldname + self.filename)  # 先打开已存在的表
        newWb = copy(oldWb)  # 复制
        newWs = newWb.get_sheet(0)  # 取sheet表
        for ex in exhibitorlist:
            for col in range(0, len(ex)):
                newWs.write(self.rows, col, ex[col])
            self.rows += 1
        newWb.save(self.foldname + self.filename)
        return item

import sqlite3
class ExhibitionspiderPipelineSqlite(object):
    # 创建excel表
    rows = 1800

    # 写入数据
    def process_item(self,item,spider):
        itemlist = [list(item.values())]
        conn = sqlite3.connect('tyc.db')
        cur = conn.cursor()
        try:
            createsql = '''create table tb_cantonfair2019(
                序号 int,
                公司名称 varchar(500),
                英文名称 varchar(500),
                区号 varchar(10),
                电话1 varchar(100),
                电话2 varchar(100),
                传真 varchar(100),
                移动电话 varchar(100),
                联系人 varchar(100),
                邮箱 varchar(100),
                网址 varchar(1000),
                地址 varchar(2000),
                英文地址 varchar(2000),
                企业类型 varchar(100),
                主营产品 varchar(2000),
                主营行业 varchar(2000),
                国家 varchar(100),
                城市 varchar(100),
                url varchar(1000)
                )
                '''
            conn.execute(createsql)
            conn.commit()
        except:
            ''
        insertsql = '''insert into tb_cantonfair2019 values("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")
        '''.format(itemlist[0], itemlist[1], itemlist[2], itemlist[3], itemlist[4], itemlist[5], itemlist[6], itemlist[7], itemlist[8], itemlist[9], itemlist[10], itemlist[11], itemlist[12],itemlist[13], itemlist[14], itemlist[15], itemlist[16], itemlist[17], itemlist[18])
        conn.execute(insertsql)
        conn.commit()
        cur.close()
        conn.close()
        return item

import pymysql
class ExhibitionspiderPipelineMysql(object):
    # 创建excel表
    rows = 1800

    # 写入数据
    def process_item(self,item,spider):
        itemlist = [list(item.values())]
        dbmysql = pymysql.connect('localhost', 'root', 'root123', 'mysqldatabase', charset='utf8')

        with dbmysql:
            # 用cursor游标建立连接，用于执行查询
            cur = dbmysql.cursor()
            # 类似于其他语言的query函数，execute是python中的执行查询函数
            try:
                createsql = '''create table tb_cantonfair2019(
                    序号 int,
                    公司名称 varchar(500),
                    英文名称 varchar(500),
                    区号 varchar(10),
                    电话1 varchar(100),
                    电话2 varchar(100),
                    传真 varchar(100),
                    移动电话 varchar(100),
                    联系人 varchar(100),
                    邮箱 varchar(100),
                    网址 varchar(1000),
                    地址 varchar(2000),
                    英文地址 varchar(2000),
                    企业类型 varchar(100),
                    主营产品 varchar(2000),
                    主营行业 varchar(2000),
                    国家 varchar(100),
                    城市 varchar(100),
                    url varchar(1000)
                    )
                    '''
                cur.execute(createsql)
                cur.commit()
            except:
                ''
            insertsql = '''insert into tb_cantonfair2019 values({},{},"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")
            '''.format(itemlist[0], itemlist[1], itemlist[2], itemlist[3], itemlist[4], itemlist[5], itemlist[6],
                       itemlist[7], itemlist[8], itemlist[9], itemlist[10], itemlist[11], itemlist[12], itemlist[13],
                       itemlist[14], itemlist[15], itemlist[16], itemlist[17], itemlist[18])
            cur.execute(insertsql)
            cur.commit()
            cur.close()
        dbmysql.close()
        return item


import pymssql
class ExhibitionspiderPipelineMysql(object):
    # 创建excel表
    rows = 1800

    # 写入数据
    def process_item(self,item,spider):
        itemlist = [list(item.values())]
        dbmssql = pymssql.connect('localhost', 'sa', 'sa', 'db_tables', 'utf8')

        with dbmssql:
            # 用cursor游标建立连接，用于执行查询
            cur = dbmssql.cursor()
            # 类似于其他语言的query函数，execute是python中的执行查询函数
            try:
                createsql = '''create table tb_cantonfair2019(
                    序号 int,
                    公司名称 varchar(500),
                    英文名称 varchar(500),
                    区号 varchar(10),
                    电话1 varchar(100),
                    电话2 varchar(100),
                    传真 varchar(100),
                    移动电话 varchar(100),
                    联系人 varchar(100),
                    邮箱 varchar(100),
                    网址 varchar(1000),
                    地址 varchar(2000),
                    英文地址 varchar(2000),
                    企业类型 varchar(100),
                    主营产品 varchar(2000),
                    主营行业 varchar(2000),
                    国家 varchar(100),
                    城市 varchar(100),
                    url varchar(1000)
                    )
                    '''
                cur.execute(createsql)
                cur.commit()
            except:
                ''
            insertsql = '''insert into tb_cantonfair2019 values({},{},"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")
            '''.format(itemlist[0], itemlist[1], itemlist[2], itemlist[3], itemlist[4], itemlist[5], itemlist[6],
                       itemlist[7], itemlist[8], itemlist[9], itemlist[10], itemlist[11], itemlist[12], itemlist[13],
                       itemlist[14], itemlist[15], itemlist[16], itemlist[17], itemlist[18])
            cur.execute(insertsql)
            cur.commit()
            cur.close()
        dbmssql.close()
        return item