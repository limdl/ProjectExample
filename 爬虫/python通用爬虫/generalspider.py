from lxml import etree
import requests,time,os,re,xlwt,xlrd,json
from xlutils.copy import copy
from selenium import webdriver
# from concurrent import futures
import pymysql #写入mysql数据库
import pymssql #写入mssql数据库
import sqlite3  #写入sqlite数据库
import pymongo

class ExhibitorSpiderBasic():
    # start_urls = ['']

    # # 设置请求头User-Agent
    # User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    # # 设置请求头跨域请求
    # Referer = ''
    # # 设置Cookie
    # Cookie = ''

    # # 下一页链接状态：直接是链接、列表、需点击
    # next_page_state = 'isLink'  # isLink/isList/isClick
    # # xpath提取下一页链接
    # next_page_xpath = 'xpath'
    # # 下一页链接前缀拼接
    # next_page_prefix = ''
    # next_page_list = []
    # ##next_page_list = ['http://www.stonefair.org.cn/Exhibitor/ExhibitorList.asp?page={}'.format(chr(page)) for page in range(ord('a'),ord('z')+1)]

    # info_items_xpath = 'xpath'
    # DETIAL_PAGE_STATE = True

    # foldname = ''  # 保存目录
    # filename = ''  # 保存文件名

    # # 采集的数据字段xpath设置
    # companyNameCN = 'xpath'  # 公司名称、
    # companyNameEN = 'xpath'  # 英文名称、
    # areacode = 'xpath'  # 区号
    # phone1 = 'xpath'  # 电话1
    # phone2 = 'xpath'  # 电话2
    # fax = 'xpath'  # 传真
    # telphone = 'xpath'  # 移动电话
    # contacts = 'xpath'  # 联系人
    # email = 'xpath'  # 邮箱
    # website = 'xpath'  # 网址
    # address = 'xpath'  # 地址
    # addressEN = 'xpath'  # 英文地址
    # boothNo = 'xpath'  # 企业类型，放展馆展位号
    # industry = 'xpath'  # 行业
    # product = 'xpath'  # 产品
    # country = './/td[4]/text()'  # 国家
    # city = 'xpath'  # 城市
    # pageurl = 'xpath'  # 采集页网址
    # headers = {
    #     'Referer': Referer,
    #     'User-Agent': User_Agent,
    #     # 'Cookie':Cookie,
    # }

    def __init__(self):
        if not os.path.exists(self.foldname+self.filename):
            self.create_wookbook(self.foldname, self.filename,self.sheetheader)
        for start_url in self.start_urls:
            next_link = start_url
            while next_link:
                resp = requests.get(next_link, headers=self.headers)
                html = etree.HTML(resp.text)
                print('采集网址:{}'.format(next_link))
                exhibitorlist = self.get_datas(next_link, html)
                print('采集数量:{}'.format(len(exhibitorlist)))
                rows = self.write_into_workbook(self.rows, exhibitorlist, self.foldname, self.filename)
                try:
                    if self.next_page_state == 'isList':
                        next_link = self.next_page_list[self.page]
                        self.page +=1
                    elif self.next_page_state == 'isLink':
                        next_link = self.get_nextlink(html)
                except:
                    next_link = ''
                time.sleep(self.delaytime)
    
    #创建excel表
    def create_wookbook(self,foldname,filename,sheetheader):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('sheet1')
        #写入表头
        for h in range(0,len(self.sheetheader)):
            worksheet.write(0,h,self.sheetheader[h])
        workbook.save(self.foldname + self.filename)
        

    def get_nextlink(self,html):
        try:
            next_link_temp = "".join(html.xpath(self.next_page_xpath))
            next_link = self.next_page_prefix.format(next_link_temp)
            # next_link = next_link.split('page=')[-1]).replace('\'','')
        except:
            next_link = ''
        return next_link

    #网页解析、json、ajax
    def get_datas(self,current_link,html):
        exhibitorlist = []
        exhibitorInfo = {}
        items = html.xpath(self.info_items_xpath)
        for i in items:
            exhibitorInfo['rowId'] = ""
            if self.companyNameCN_detail == 0:
                exhibitorInfo['companynamecn'] = "".join(i.xpath(self.companyNameCN)).strip()
            else:
                exhibitorInfo['companynamecn'] = ""
            if self.companyNameEN_detail == 0:
                exhibitorInfo['companynameen'] = "".join(i.xpath(self.companyNameEN)).strip()
            else:
                exhibitorInfo['companynameen'] = ""
            if self.areacode_detail == 0:
                exhibitorInfo['areacode'] = "".join(i.xpath(self.areacode)).strip()
            else:
                exhibitorInfo['areacode'] = ""
            if self.phone1_detail == 0:
                exhibitorInfo['phone1'] = "".join(i.xpath(self.phone1)).strip()
            else:
                exhibitorInfo['phone1'] = ""
            if self.phone2_detail == 0:
                exhibitorInfo['phone2'] = "".join(i.xpath(self.phone2)).strip()
            else:
                exhibitorInfo['phone2'] = ""
            if self.fax_detail == 0:
                exhibitorInfo['fax'] = "".join(i.xpath(self.fax)).strip()
            else:
                exhibitorInfo['fax'] = ""
            if self.telphone_detail == 0:
                exhibitorInfo['telphone'] = "".join(i.xpath(self.telphone)).strip()
            else:
                exhibitorInfo['telphone'] = ""
            if self.contacts_detail == 0:
                exhibitorInfo['contacts'] = "".join(i.xpath(self.contacts)).strip()
            else:
                exhibitorInfo['contacts'] = ""
            if self.email_detail == 0:
                exhibitorInfo['email'] = "".join(i.xpath(self.email)).strip()
            else:
                exhibitorInfo['email'] = ""
            if self.website_detail == 0:
                exhibitorInfo['website'] = "".join(i.xpath(self.website)).strip()
            else:
                exhibitorInfo['website'] = ""
            if self.address_detail == 0:
                exhibitorInfo['address'] = "".join(i.xpath(self.address)).strip()
            else:
                exhibitorInfo['address'] = ""
            if self.addressEN_detail == 0:
                exhibitorInfo['addressEN'] = "".join(i.xpath(self.addressEN)).strip()
            else:
                exhibitorInfo['addressEN'] = ""
            if self.boothNo_detail == 0:
                exhibitorInfo['boothNo'] = "".join(i.xpath(self.boothNo)).strip()
            else:
                exhibitorInfo['boothNo'] = ""
            if self.product_detail == 0:
                exhibitorInfo['product'] = "".join(i.xpath(self.product)).strip()
            else:
                exhibitorInfo['product'] = ""
            if self.industry_detail == 0:
                exhibitorInfo['industry'] = "".join(i.xpath(self.industry)).strip()
            else:
                exhibitorInfo['industry'] = ""

            if self.country_detail == 0:
                exhibitorInfo['country'] = "".join(i.xpath(self.country)).strip()
            else:
                exhibitorInfo['country'] = ""
            if self.city_detail == 0:
                exhibitorInfo['city'] = "".join(i.xpath(self.city)).strip()
            else:
                exhibitorInfo['city'] = ""
            if self.pageurl_detail == 0:
                exhibitorInfo['url'] = self.next_page_prefix+"".join(i.xpath(self.pageurl )).strip()
            else:
                exhibitorInfo['url'] = ""
            print('明细网址:'+exhibitorInfo['url'])

            if self.DETIAL_PAGE_STATE ==1:
                print(exhibitorInfo['url'])
                resp = requests.get(exhibitorInfo['url'], headers=self.headers)
                html = etree.HTML(resp.text)
                if self.companyNameCN_detail == 1:
                    exhibitorInfo['companynamecn'] = "".join(html.xpath(self.companyNameCN)).strip()
                if self.companyNameEN_detail == 1:
                    exhibitorInfo['companynameen'] = "".join(html.xpath(self.companyNameEN)).strip()
                if self.areacode_detail == 1:
                    exhibitorInfo['areacode'] = "".join(html.xpath(self.areacode)).strip()
                if self.phone1_detail == 1:
                    exhibitorInfo['phone1'] = "".join(html.xpath(self.phone1)).strip()
                if self.phone2_detail == 1:
                    exhibitorInfo['phone2'] = "".join(html.xpath(self.phone2)).strip()
                if self.fax_detail == 1:
                    exhibitorInfo['fax'] = "".join(html.xpath(self.fax)).strip()
                if self.telphone_detail == 1:
                    exhibitorInfo['telphone'] = "".join(html.xpath(self.telphone)).strip()
                if self.contacts_detail == 1:
                    exhibitorInfo['contacts'] = "".join(html.xpath(self.contacts)).strip()
                if self.email_detail == 1:
                    exhibitorInfo['email'] = "".join(html.xpath(self.email)).strip()
                if self.website_detail == 1:
                    exhibitorInfo['website'] = "".join(html.xpath(self.website)).strip()
                if self.address_detail == 1:
                    exhibitorInfo['address'] = "".join(html.xpath(self.address)).strip()
                if self.addressEN_detail == 1:
                    exhibitorInfo['addressEN'] = "".join(html.xpath(self.addressEN)).strip()
                if self.boothNo_detail == 1:
                    exhibitorInfo['boothNo'] = "".join(html.xpath(self.boothNo)).strip()
                if self.industry_detail == 1:
                    exhibitorInfo['industry'] = "".join(html.xpath(self.industry)).strip()
                if self.product_detail == 1:
                    exhibitorInfo['product'] = "".join(html.xpath(self.product)).strip()
                if self.country_detail == 1:
                    exhibitorInfo['country'] = "".join(html.xpath(self.country)).strip()
                if self.city_detail == 1:
                    exhibitorInfo['city'] = "".join(html.xpath(self.city)).strip()
                if self.pageurl_detail == 1:
                    exhibitorInfo['url'] = exhibitorInfo['url']
            #print(list(exhibitorInfo.values()))
            exhibitorlist.append(list(exhibitorInfo.values()))
        return exhibitorlist



    #写入数据
    def write_into_workbook(self,rows,exhibitorlist,foldname,filename):
        oldWb = xlrd.open_workbook(foldname + filename)#先打开已存在的表
        newWb = copy(oldWb)#复制
        newWs = newWb.get_sheet(0)#取sheet表
        for ex in exhibitorlist:
            for col in range(0,len(ex)):
                newWs.write(self.rows,col,ex[col])
            self.rows +=1
        newWb.save(foldname + filename)
        return rows

    def insert_into_mssql(self, exhibitorlist):
        l=exhibitorlist
        dbmssql = pymssql.connect('192.168.1.15','sa','sa','source','utf8')
        with dbmssql:
            cur=dbmssql.cursor()
            insert_sql = '''insert into tb_Exhibitior values("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")
            '''.format(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10],l[11],l[12],l[13],l[14],l[15],l[16],l[17],l[18])
            cur.execute(insert_sql)
            cur.commit()
            cur.close()
        dbmssql.close()


class ExhibitorSpiderJson():
    # start_urls = ['']

    # # 设置请求头User-Agent
    # User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    # # 设置请求头跨域请求
    # Referer = ''
    # # 设置Cookie
    # Cookie = ''

    # # 下一页链接状态：直接是链接、列表、需点击
    # next_page_state = 'isLink'  # isLink/isList/isClick
    # # xpath提取下一页链接
    # next_page_xpath = 'xpath'
    # # 下一页链接前缀拼接
    # next_page_prefix = ''
    # next_page_list = []
    # ##next_page_list = ['http://www.stonefair.org.cn/Exhibitor/ExhibitorList.asp?page={}'.format(chr(page)) for page in range(ord('a'),ord('z')+1)]

    # info_items_xpath = 'xpath'
    # DETIAL_PAGE_STATE = True

    # foldname = ''  # 保存目录
    # filename = ''  # 保存文件名

    # # 采集的数据字段xpath设置
    # companyNameCN = 'xpath'  # 公司名称、
    # companyNameEN = 'xpath'  # 英文名称、
    # areacode = 'xpath'  # 区号
    # phone1 = 'xpath'  # 电话1
    # phone2 = 'xpath'  # 电话2
    # fax = 'xpath'  # 传真
    # telphone = 'xpath'  # 移动电话
    # contacts = 'xpath'  # 联系人
    # email = 'xpath'  # 邮箱
    # website = 'xpath'  # 网址
    # address = 'xpath'  # 地址
    # addressEN = 'xpath'  # 英文地址
    # boothNo = 'xpath'  # 企业类型，放展馆展位号
    # industry = 'xpath'  # 行业
    # product = 'xpath'  # 产品
    # country = './/td[4]/text()'  # 国家
    # city = 'xpath'  # 城市
    # pageurl = 'xpath'  # 采集页网址
    # headers = {
    #     'Referer': Referer,
    #     'User-Agent': User_Agent,
    #     # 'Cookie':Cookie,
    # }

    def __init__(self):
        if not os.path.exists(self.foldname+self.filename):
            self.create_wookbook(self.foldname, self.filename,self.sheetheader)
        next_link = ' '
        while next_link:
            if self.next_page_state == 'isList':
                try:
                    next_link = self.next_page_list[self.page-1]
                    resp = requests.get(next_link, headers=self.headers)
                    html = json.loads(resp.text)
                    exhibitorlist = self.get_datas(next_link, html)
                    rows = self.write_into_workbook(self.rows, exhibitorlist, self.foldname, self.filename)
                except:
                    next_link = ''
                self.page += 1
            print(next_link)
            time.sleep(self.delaytime)

    # 创建excel表
    def create_wookbook(self, foldname, filename, sheetheader):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('sheet1')
        # 写入表头
        for h in range(0, len(self.sheetheader)):
            worksheet.write(0, h, self.sheetheader[h])
        workbook.save(self.foldname + self.filename)

    # 网页解析、json、ajax
    def get_datas(self, current_link, html):
        exhibitorlist = []
        exhibitorInfo = {}
        items = html['hits']
        for i in items:
            exhibitorInfo['rowId'] = ""
            if self.companyNameCN_detail == 0:
                exhibitorInfo['companynamecn'] = i['hits'][0]['name']
            else:
                exhibitorInfo['companynamecn'] = ""
            if self.companynameen_detail == 0:
                exhibitorInfo['companynameen'] = "".join(
                    html.xpath(self.companyNameEN)).strip()
            else:
                exhibitorInfo['companynameen'] = ""
            if self.areacode_detail == 0:
                exhibitorInfo['areacode'] = "".join(html.xpath(self.areacode)).strip()
            else:
                exhibitorInfo['areacode'] = ""
            if self.phone1_detail == 0:
                exhibitorInfo['phone1'] = "".join(html.xpath(self.phone1)).strip()
            else:
                exhibitorInfo['phone1'] = ""
            if self.phone2_detail == 0:
                exhibitorInfo['phone2'] = "".join(html.xpath(self.phone2)).strip()
            else:
                exhibitorInfo['phone2'] = ""
            if self.fax_detail == 0:
                exhibitorInfo['fax'] = "".join(html.xpath(self.fax)).strip()
            else:
                exhibitorInfo['fax'] = ""
            if self.telphone_detail == 0:
                exhibitorInfo['telphone'] = "".join(html.xpath(self.telphone)).strip()
            else:
                exhibitorInfo['telphone'] = ""
            if self.contacts_detail == 0:
                exhibitorInfo['contacts'] = "".join(html.xpath(self.contacts)).strip()
            else:
                exhibitorInfo['contacts'] = ""
            if self.email_detail == 0:
                exhibitorInfo['email'] = "".join(html.xpath(self.email)).strip()
            else:
                exhibitorInfo['email'] = ""
            if self.website_detail == 0:
                exhibitorInfo['website'] = "".join(html.xpath(self.website)).strip()
            else:
                exhibitorInfo['website'] = ""
            if self.address_detail == 0:
                exhibitorInfo['address'] = "".join(html.xpath(self.address)).strip()
            else:
                exhibitorInfo['address'] = ""
            if self.addressEN_detail == 0:
                exhibitorInfo['addressEN'] = "".join(html.xpath(self.addressEN)).strip()
            else:
                exhibitorInfo['addressEN'] = ""
            if self.boothNo_detail == 0:
                exhibitorInfo['boothNo'] = "".join(html.xpath(self.boothNo)).strip()
            else:
                exhibitorInfo['boothNo'] = ""
            if self.product_detail == 0:
                exhibitorInfo['product'] = "".join(html.xpath(self.product)).strip()
            else:
                exhibitorInfo['product'] = ""
            if self.industry_detail == 0:
                exhibitorInfo['industry'] = "".join(html.xpath(self.industry)).strip()
            else:
                exhibitorInfo['industry'] = ""
            if self.country_detail == 0:
                exhibitorInfo['country'] = "".join(html.xpath(self.country)).strip()
            else:
                exhibitorInfo['country'] = ""
            if self.city_detail == 0:
                exhibitorInfo['city'] = "".join(html.xpath(self.city)).strip()
            else:
                exhibitorInfo['city'] = ""
            exhibitorInfo['url'] = current_link

            if self.DETIAL_PAGE_STATE == 1:
                resp = requests.get(current_link, headers=self.headers)
                html = etree.HTML(resp.text)
                if self.companyNameCN_detail == 1:
                    exhibitorInfo['companynamecn'] = "".join(
                        html.xpath(self.companyNameCN)).strip()
                if self.companynameen_detail == 1:
                    exhibitorInfo['companynameen'] = "".join(
                        html.xpath(self.companyNameEN)).strip()
                if self.areacode_detail == 1:
                    exhibitorInfo['areacode'] = "".join(html.xpath(self.areacode)).strip()
                if self.phone1_detail == 1:
                    exhibitorInfo['phone1'] = "".join(html.xpath(self.phone1)).strip()
                if self.phone2_detail == 1:
                    exhibitorInfo['phone2'] = "".join(html.xpath(self.phone2)).strip()
                if self.fax_detail == 1:
                    exhibitorInfo['fax'] = "".join(html.xpath(self.fax)).strip()
                if self.telphone_detail == 1:
                    exhibitorInfo['telphone'] = "".join(html.xpath(self.telphone)).strip()
                if self.contacts_detail == 1:
                    exhibitorInfo['contacts'] = "".join(html.xpath(self.contacts)).strip()
                if self.email_detail == 1:
                    exhibitorInfo['email'] = "".join(html.xpath(self.email)).strip()
                if self.website_detail == 1:
                    exhibitorInfo['website'] = "".join(html.xpath(self.website)).strip()
                if self.address_detail == 1:
                    exhibitorInfo['address'] = "".join(html.xpath(self.address)).strip()
                if self.addressEN_detail == 1:
                    exhibitorInfo['addressEN'] = "".join(html.xpath(self.addressEN)).strip()
                if self.boothNo_detail == 1:
                    exhibitorInfo['boothNo'] = "".join(html.xpath(self.boothNo)).strip()
                if self.product_detail == 1:
                    exhibitorInfo['product'] = "".join(html.xpath(self.product)).strip()
                if self.industry_detail == 1:
                    exhibitorInfo['industry'] = "".join(html.xpath(self.industry)).strip()
                if self.country_detail == 1:
                    exhibitorInfo['country'] = "".join(html.xpath(self.country)).strip()
                if self.city_detail == 1:
                    exhibitorInfo['city'] = "".join(html.xpath(self.city)).strip()

            exhibitorlist.append(list(exhibitorInfo.values()))
        return exhibitorlist

    # 写入数据
    def write_into_workbook(self, rows, exhibitorlist, foldname, filename):
        oldWb = xlrd.open_workbook(foldname + filename)  # 先打开已存在的表
        newWb = copy(oldWb)  # 复制
        newWs = newWb.get_sheet(0)  # 取sheet表
        for ex in exhibitorlist:
            for col in range(0, len(ex)):
                newWs.write(rows, col, ex[col])
            self.rows += 1
        newWb.save(foldname + filename)
        return rows

class ExhibitorSpiderSelenium():

    def __init__(self):
        global driver
        driver = webdriver.Chrome()
        for start_url in self.start_urls:
            next_link = start_url
            if not os.path.exists(self.foldname + self.filename):
                self.create_wookbook(self.foldname, self.filename, self.sheetheader)
            for start_url in self.start_urls:
                next_link = start_url
                while next_link:
                    driver.get(next_link)
                    html = etree.HTML(driver.page_source)
                    while True:
                        if html.xpath(self.info_items_xpath):
                            break
                        else:
                            time.sleep(2)
                            html = etree.HTML(driver.page_source)
                    print('采集网址:{}'.format(next_link))
                    exhibitorlist = self.get_datas(next_link, html)
                    print('采集数量:{}'.format(len(exhibitorlist)))
                    rows = self.write_into_workbook(self.rows, exhibitorlist, self.foldname, self.filename)
                    try:
                        if self.next_page_state == 'isList':
                            next_link = self.next_page_list[self.page]
                            self.page += 1
                        elif self.next_page_state == 'isLink':
                            next_link = self.get_nextlink(html)
                    except:
                        next_link = ''
                    time.sleep(self.delaytime)

    # 创建excel表
    def create_wookbook(self, foldname, filename, sheetheader):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('sheet1')
        # 写入表头
        for h in range(0, len(self.sheetheader)):
            worksheet.write(0, h, self.sheetheader[h])
        workbook.save(self.foldname + self.filename)

    def get_nextlink(self,html):
        try:
            next_link_temp = "".join(html.xpath(self.next_page_xpath))
            next_link = self.next_page_prefix.format(next_link_temp)
            # next_link = next_link.split('page=')[-1]).replace('\'','')
        except:
            next_link = ''
        return

    # 网页解析、json、ajax
    def get_datas(self,current_link,html):
        exhibitorlist = []
        exhibitorInfo = {}
        items = html.xpath(self.info_items_xpath)
        for i in items:
            exhibitorInfo['rowId'] = ""
            if self.companyNameCN_detail == 0:
                exhibitorInfo['companynamecn'] = "".join(i.xpath(self.companyNameCN)).strip()
            else:
                exhibitorInfo['companynamecn'] = ""
            if self.companyNameEN_detail == 0:
                exhibitorInfo['companynameen'] = "".join(i.xpath(self.companyNameEN)).strip()
            else:
                exhibitorInfo['companynameen'] = ""
            if self.areacode_detail == 0:
                exhibitorInfo['areacode'] = "".join(i.xpath(self.areacode)).strip()
            else:
                exhibitorInfo['areacode'] = ""
            if self.phone1_detail == 0:
                exhibitorInfo['phone1'] = "".join(i.xpath(self.phone1)).strip()
            else:
                exhibitorInfo['phone1'] = ""
            if self.phone2_detail == 0:
                exhibitorInfo['phone2'] = "".join(i.xpath(self.phone2)).strip()
            else:
                exhibitorInfo['phone2'] = ""
            if self.fax_detail == 0:
                exhibitorInfo['fax'] = "".join(i.xpath(self.fax)).strip()
            else:
                exhibitorInfo['fax'] = ""
            if self.telphone_detail == 0:
                exhibitorInfo['telphone'] = "".join(i.xpath(self.telphone)).strip()
            else:
                exhibitorInfo['telphone'] = ""
            if self.contacts_detail == 0:
                exhibitorInfo['contacts'] = "".join(i.xpath(self.contacts)).strip()
            else:
                exhibitorInfo['contacts'] = ""
            if self.email_detail == 0:
                exhibitorInfo['email'] = "".join(i.xpath(self.email)).strip()
            else:
                exhibitorInfo['email'] = ""
            if self.website_detail == 0:
                exhibitorInfo['website'] = "".join(i.xpath(self.website)).strip()
            else:
                exhibitorInfo['website'] = ""
            if self.address_detail == 0:
                exhibitorInfo['address'] = "".join(i.xpath(self.address)).strip()
            else:
                exhibitorInfo['address'] = ""
            if self.addressEN_detail == 0:
                exhibitorInfo['addressEN'] = "".join(i.xpath(self.addressEN)).strip()
            else:
                exhibitorInfo['addressEN'] = ""
            if self.boothNo_detail == 0:
                exhibitorInfo['boothNo'] = "".join(i.xpath(self.boothNo)).strip()
            else:
                exhibitorInfo['boothNo'] = ""
            if self.product_detail == 0:
                exhibitorInfo['product'] = "".join(i.xpath(self.product)).strip()
            else:
                exhibitorInfo['product'] = ""
            if self.industry_detail == 0:
                exhibitorInfo['industry'] = "".join(i.xpath(self.industry)).strip()
            else:
                exhibitorInfo['industry'] = ""

            if self.country_detail == 0:
                exhibitorInfo['country'] = "".join(i.xpath(self.country)).strip()
            else:
                exhibitorInfo['country'] = ""
            if self.city_detail == 0:
                exhibitorInfo['city'] = "".join(i.xpath(self.city)).strip()
            else:
                exhibitorInfo['city'] = ""
            if self.pageurl_detail == 0:
                exhibitorInfo['url'] = self.next_page_prefix+"".join(i.xpath(self.pageurl)).strip()
            else:
                exhibitorInfo['url'] = ""
            print('详细页网址：'+exhibitorInfo['url'])

            if self.DETIAL_PAGE_STATE ==1:
                driver.get(exhibitorInfo['url'])
                html = etree.HTML(driver.page_source)
                while True:
                    if html.xpath(self.companyNameCN) or html.xpath(self.companyNameEN):
                        break
                    else:
                        time.sleep(2)
                        html = etree.HTML(driver.page_source)

                if self.companyNameCN_detail == 1:
                    exhibitorInfo['companynamecn'] = "".join(html.xpath(self.companyNameCN)).strip()
                if self.companyNameEN_detail == 1:
                    exhibitorInfo['companynameen'] = "".join(html.xpath(self.companyNameEN)).strip()
                if self.areacode_detail == 1:
                    exhibitorInfo['areacode'] = "".join(html.xpath(self.areacode)).strip()
                if self.phone1_detail == 1:
                    exhibitorInfo['phone1'] = "".join(html.xpath(self.phone1)).strip()
                if self.phone2_detail == 1:
                    exhibitorInfo['phone2'] = "".join(html.xpath(self.phone2)).strip()
                if self.fax_detail == 1:
                    exhibitorInfo['fax'] = "".join(html.xpath(self.fax)).strip()
                if self.telphone_detail == 1:
                    exhibitorInfo['telphone'] = "".join(html.xpath(self.telphone)).strip()
                if self.contacts_detail == 1:
                    exhibitorInfo['contacts'] = "".join(html.xpath(self.contacts)).strip()
                if self.email_detail == 1:
                    exhibitorInfo['email'] = "".join(html.xpath(self.email)).strip()
                if self.website_detail == 1:
                    exhibitorInfo['website'] = "".join(html.xpath(self.website)).strip()
                if self.address_detail == 1:
                    exhibitorInfo['address'] = "".join(html.xpath(self.address)).strip()
                if self.addressEN_detail == 1:
                    exhibitorInfo['addressEN'] = "".join(html.xpath(self.addressEN)).strip()
                if self.boothNo_detail == 1:
                    exhibitorInfo['boothNo'] = "".join(html.xpath(self.boothNo)).strip()
                if self.industry_detail == 1:
                    exhibitorInfo['industry'] = "".join(html.xpath(self.industry)).strip()
                if self.product_detail == 1:
                    exhibitorInfo['product'] = "".join(html.xpath(self.product)).strip()
                if self.country_detail == 1:
                    exhibitorInfo['country'] = "".join(html.xpath(self.country)).strip()
                if self.city_detail == 1:
                    exhibitorInfo['city'] = "".join(html.xpath(self.city)).strip()
                if self.pageurl_detail == 1:
                    exhibitorInfo['url'] = exhibitorInfo['url']

            print(list(exhibitorInfo.values()))
            exhibitorlist.append(list(exhibitorInfo.values()))
        return exhibitorlist

        # 写入数据
    def write_into_workbook(self, rows, exhibitorlist, foldname, filename):
        oldWb = xlrd.open_workbook(foldname + filename)  # 先打开已存在的表
        newWb = copy(oldWb)  # 复制
        newWs = newWb.get_sheet(0)  # 取sheet表
        for ex in exhibitorlist:
            for col in range(0, len(ex)):
                newWs.write(rows, col, ex[col])
            self.rows += 1
        newWb.save(foldname + filename)
        return rows
# if __name__ == "__main__":
#     ExhibitorSpider()
#     print("over")


