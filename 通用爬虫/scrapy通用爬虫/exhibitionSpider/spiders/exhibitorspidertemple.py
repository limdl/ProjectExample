# -*- coding: utf-8 -*-
import scrapy

from lxml import etree
import requests, time, os, re, xlwt, xlrd, json
from xlutils.copy import copy
from selenium import webdriver

class ExhibitorSpiderBasic(scrapy.Spider):
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
    def parse(self, response):
        items = response.xpath(self.info_items_xpath)
        item = {}
        print('采集网址:{}'.format(response.url))
        for i in items:
            item['rowId'] = ""
            if self.companyNameCN_detail == 0:
                item['companynamecn'] = "".join(i.xpath('normalize-space(' + self.companyNameCN + ')').extract()).strip()
            else:
                item['companynamecn'] = ""
            if self.companyNameEN_detail == 0:
                item['companynameen'] = "".join(i.xpath('normalize-space(' + self.companyNameEN + ')').extract()).strip()
            else:
                item['companynameen'] = ""
            if self.areacode_detail == 0:
                item['areacode'] = "".join(i.xpath('normalize-space(' + self.areacode + ')').extract()).strip()
            else:
                item['areacode'] = ""
            if self.phone1_detail == 0:
                item['phone1'] = "".join(i.xpath('normalize-space(' + self.phone1 + ')').extract()).strip()
            else:
                item['phone1'] = ""
            if self.phone2_detail == 0:
                item['phone2'] = "".join(i.xpath('normalize-space(' + self.phone2 + ')').extract()).strip()
            else:
                item['phone2'] = ""
            if self.fax_detail == 0:
                item['fax'] = "".join(i.xpath('normalize-space(' + self.fax + ')').extract()).strip()
            else:
                item['fax'] = ""
            if self.telphone_detail == 0:
                item['telphone'] = "".join(i.xpath('normalize-space(' + self.telphone + ')').extract()).strip()
            else:
                item['telphone'] = ""
            if self.contacts_detail == 0:
                item['contacts'] = "".join(i.xpath('normalize-space(' + self.contacts + ')').extract()).strip()
            else:
                item['contacts'] = ""
            if self.email_detail == 0:
                item['email'] = "".join(i.xpath('normalize-space(' + self.email + ')').extract()).strip()
            else:
                item['email'] = ""
            if self.website_detail == 0:
                item['website'] = "".join(i.xpath('normalize-space(' + self.website + ')').extract()).strip()
            else:
                item['website'] = ""
            if self.address_detail == 0:
                item['address'] = "".join(i.xpath('normalize-space(' + self.address + ')').extract()).strip()
            else:
                item['address'] = ""
            if self.addressEN_detail == 0:
                item['addressEN'] = "".join(i.xpath('normalize-space(' + self.addressEN + ')').extract()).strip()
            else:
                item['addressEN'] = ""
            if self.boothNo_detail == 0:
                item['boothNo'] = "".join(i.xpath('normalize-space(' + self.boothNo + ')').extract()).strip()
            else:
                item['boothNo'] = ""
            if self.product_detail == 0:
                item['product'] = "".join(i.xpath('normalize-space(' + self.product + ')').extract()).strip()
            else:
                item['product'] = ""
            if self.industry_detail == 0:
                item['industry'] = "".join(i.xpath('normalize-space(' + self.industry + ')').extract()).strip()
            else:
                item['industry'] = ""

            if self.country_detail == 0:
                item['country'] = "".join(i.xpath('normalize-space(' + self.country + ')').extract()).strip()
            else:
                item['country'] = ""
            if self.city_detail == 0:
                item['city'] = "".join(i.xpath('normalize-space(' + self.city + ')').extract()).strip()
            else:
                item['city'] = ""
            if self.pageurl_detail == 0:
                item['url'] = "".join(i.xpath('normalize-space(' + self.pageurl + ')').extract()).strip()
            else:
                item['url'] = ""
            # print(list(item.values()))
            if self.DETIAL_PAGE_STATE == 1:
                yield scrapy.Request(item['url'], callback=self.parse_detail_page, meta=item)
            else:
                # print(list(item.values()))
                yield item
        try:
            if self.next_page_state == 'isList':
                next_link = self.next_page_list[self.page]
                self.page += 1
            elif self.next_page_state == 'isLink':
                next_link_temp = "".join(response.xpath(self.next_page_xpath))
                next_link = self.next_page_prefix.format(next_link_temp)
        except:
            next_link = ''
        if next_link:
            yield scrapy.Request(next_link, callback=self.parse)

    def parse_detail_page(self, response):
        item = response.meta
        if self.companyNameCN_detail == 1:
            item['companynamecn'] = "".join(response.xpath('normalize-space(' + self.companyNameCN + ')').extract()).strip()
        if self.companynameen_detail == 1:
            item['companynameen'] = "".join(response.xpath('normalize-space(' + self.companyNameEN + ')').extract()).strip()
        if self.areacode_detail == 1:
            item['areacode'] = "".join(response.xpath('normalize-space(' + self.areacode + ')').extract()).strip()
        if self.phone1_detail == 1:
            item['phone1'] = "".join(response.xpath('normalize-space(' + self.phone1 + ')').extract()).strip()
        if self.phone2_detail == 1:
            item['phone2'] = "".join(response.xpath('normalize-space(' + self.phone2 + ')').extract()).strip()
        if self.fax_detail == 1:
            item['fax'] = "".join(response.xpath('normalize-space(' + self.fax + ')').extract()).strip()
        if self.telphone_detail == 1:
            item['telphone'] = "".join(response.xpath('normalize-space(' + self.telphone + ')').extract()).strip()
        if self.contacts_detail == 1:
            item['contacts'] = "".join(response.xpath('normalize-space(' + self.contacts + ')').extract()).strip()
        if self.email_detail == 1:
            item['email'] = "".join(response.xpath('normalize-space(' + self.email + ')').extract()).strip()
        if self.website_detail == 1:
            item['website'] = "".join(response.xpath('normalize-space(' + self.website + ')').extract()).strip()
        if self.address_detail == 1:
            item['address'] = "".join(response.xpath('normalize-space(' + self.address + ')').extract()).strip()
        if self.addressEN_detail == 1:
            item['addressEN'] = "".join(response.xpath('normalize-space(' + self.addressEN + ')').extract()).strip()
        if self.boothNo_detail == 1:
            item['boothNo'] = "".join(response.xpath('normalize-space(' + self.boothNo + ')').extract()).strip()
        if self.industry_detail == 1:
            item['industry'] = "".join(response.xpath('normalize-space(' + self.industry + ')').extract()).strip()
        if self.product_detail == 1:
            item['product'] = "".join(response.xpath('normalize-space(' + self.product + ')').extract()).strip()
        if self.country_detail == 1:
            item['country'] = "".join(response.xpath('normalize-space(' + self.country + ')').extract()).strip()
        if self.city_detail == 1:
            item['city'] = "".join(response.xpath('normalize-space(' + self.city + ')').extract()).strip()
        if self.pageurl_detail == 1:
            item['url'] = response.meta['url']
        return item


class ExhibitorSpiderJson(scrapy.Spider):

    def __init__(self):
        if not os.path.exists(self.foldname + self.filename):
            self.create_wookbook(self.foldname, self.filename, self.sheetheader)
        next_link = ' '
        while next_link:
            if self.next_page_state == 'isList':
                try:
                    next_link = self.next_page_list[self.page - 1]
                    resp = requests.get(next_link, headers=self.headers)
                    html = json.loads(resp.text)
                    exhibitorlist = self.get_datas(next_link, html)
                    rows = self.write_into_workbook(self.rows, exhibitorlist, self.foldname, self.filename)
                except:
                    next_link = ''
                self.page += 1
            print(next_link)
            time.sleep(self.delaytime)

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
                    html.xpath('normalize-space(' + self.companyNameEN + ')')).strip()
            else:
                exhibitorInfo['companynameen'] = ""
            if self.areacode_detail == 0:
                exhibitorInfo['areacode'] = "".join(html.xpath('normalize-space(' + self.areacode + ')')).strip()
            else:
                exhibitorInfo['areacode'] = ""
            if self.phone1_detail == 0:
                exhibitorInfo['phone1'] = "".join(html.xpath('normalize-space(' + self.phone1 + ')')).strip()
            else:
                exhibitorInfo['phone1'] = ""
            if self.phone2_detail == 0:
                exhibitorInfo['phone2'] = "".join(html.xpath('normalize-space(' + self.phone2 + ')')).strip()
            else:
                exhibitorInfo['phone2'] = ""
            if self.fax_detail == 0:
                exhibitorInfo['fax'] = "".join(html.xpath('normalize-space(' + self.fax + ')')).strip()
            else:
                exhibitorInfo['fax'] = ""
            if self.telphone_detail == 0:
                exhibitorInfo['telphone'] = "".join(html.xpath('normalize-space(' + self.telphone + ')')).strip()
            else:
                exhibitorInfo['telphone'] = ""
            if self.contacts_detail == 0:
                exhibitorInfo['contacts'] = "".join(html.xpath('normalize-space(' + self.contacts + ')')).strip()
            else:
                exhibitorInfo['contacts'] = ""
            if self.email_detail == 0:
                exhibitorInfo['email'] = "".join(html.xpath('normalize-space(' + self.email + ')')).strip()
            else:
                exhibitorInfo['email'] = ""
            if self.website_detail == 0:
                exhibitorInfo['website'] = "".join(html.xpath('normalize-space(' + self.website + ')')).strip()
            else:
                exhibitorInfo['website'] = ""
            if self.address_detail == 0:
                exhibitorInfo['address'] = "".join(html.xpath('normalize-space(' + self.address + ')')).strip()
            else:
                exhibitorInfo['address'] = ""
            if self.addressEN_detail == 0:
                exhibitorInfo['addressEN'] = "".join(html.xpath('normalize-space(' + self.addressEN + ')')).strip()
            else:
                exhibitorInfo['addressEN'] = ""
            if self.boothNo_detail == 0:
                exhibitorInfo['boothNo'] = "".join(html.xpath('normalize-space(' + self.boothNo + ')')).strip()
            else:
                exhibitorInfo['boothNo'] = ""
            if self.product_detail == 0:
                exhibitorInfo['product'] = "".join(html.xpath('normalize-space(' + self.product + ')')).strip()
            else:
                exhibitorInfo['product'] = ""
            if self.industry_detail == 0:
                exhibitorInfo['industry'] = "".join(html.xpath('normalize-space(' + self.industry + ')')).strip()
            else:
                exhibitorInfo['industry'] = ""
            if self.country_detail == 0:
                exhibitorInfo['country'] = "".join(html.xpath('normalize-space(' + self.country + ')')).strip()
            else:
                exhibitorInfo['country'] = ""
            if self.city_detail == 0:
                exhibitorInfo['city'] = "".join(html.xpath('normalize-space(' + self.city + ')')).strip()
            else:
                exhibitorInfo['city'] = ""
            exhibitorInfo['url'] = current_link

            if self.DETIAL_PAGE_STATE == 1:
                resp = requests.get(current_link, headers=self.headers)
                html = etree.HTML(resp.text)
                if self.companyNameCN_detail == 1:
                    exhibitorInfo['companynamecn'] = "".join(
                        html.xpath('normalize-space(' + self.companyNameCN + ')')).strip()
                if self.companynameen_detail == 1:
                    exhibitorInfo['companynameen'] = "".join(
                        html.xpath('normalize-space(' + self.companyNameEN + ')')).strip()
                if self.areacode_detail == 1:
                    exhibitorInfo['areacode'] = "".join(html.xpath('normalize-space(' + self.areacode + ')')).strip()
                if self.phone1_detail == 1:
                    exhibitorInfo['phone1'] = "".join(html.xpath('normalize-space(' + self.phone1 + ')')).strip()
                if self.phone2_detail == 1:
                    exhibitorInfo['phone2'] = "".join(html.xpath('normalize-space(' + self.phone2 + ')')).strip()
                if self.fax_detail == 1:
                    exhibitorInfo['fax'] = "".join(html.xpath('normalize-space(' + self.fax + ')')).strip()
                if self.telphone_detail == 1:
                    exhibitorInfo['telphone'] = "".join(html.xpath('normalize-space(' + self.telphone + ')')).strip()
                if self.contacts_detail == 1:
                    exhibitorInfo['contacts'] = "".join(html.xpath('normalize-space(' + self.contacts + ')')).strip()
                if self.email_detail == 1:
                    exhibitorInfo['email'] = "".join(html.xpath('normalize-space(' + self.email + ')')).strip()
                if self.website_detail == 1:
                    exhibitorInfo['website'] = "".join(html.xpath('normalize-space(' + self.website + ')')).strip()
                if self.address_detail == 1:
                    exhibitorInfo['address'] = "".join(html.xpath('normalize-space(' + self.address + ')')).strip()
                if self.addressEN_detail == 1:
                    exhibitorInfo['addressEN'] = "".join(html.xpath('normalize-space(' + self.addressEN + ')')).strip()
                if self.boothNo_detail == 1:
                    exhibitorInfo['boothNo'] = "".join(html.xpath('normalize-space(' + self.boothNo + ')')).strip()
                if self.product_detail == 1:
                    exhibitorInfo['product'] = "".join(html.xpath('normalize-space(' + self.product + ')')).strip()
                if self.industry_detail == 1:
                    exhibitorInfo['industry'] = "".join(html.xpath('normalize-space(' + self.industry + ')')).strip()
                if self.country_detail == 1:
                    exhibitorInfo['country'] = "".join(html.xpath('normalize-space(' + self.country + ')')).strip()
                if self.city_detail == 1:
                    exhibitorInfo['city'] = "".join(html.xpath('normalize-space(' + self.city + ')')).strip()

            exhibitorlist.append(list(exhibitorInfo.values()))
        return exhibitorlist

class ExhibitorSpiderSelenium(scrapy.Spider):

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
                    exhibitorlist = self.get_datas(next_link, html)
                    print('采集网址:{},采集数量:{}'.format(next_link, len(exhibitorlist)))
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

    def get_nextlink(self, html):
        try:
            next_link_temp = "".join(html.xpath(self.next_page_xpath))
            next_link = self.next_page_prefix.format(next_link_temp)
            # next_link = next_link.split('page=')[-1]).replace('\'','')
        except:
            next_link = ''
        return

    # 网页解析、json、ajax
    def get_datas(self, current_link, html):
        exhibitorlist = []
        exhibitorInfo = {}
        items = html.xpath(self.info_items_xpath)
        for i in items:
            exhibitorInfo['rowId'] = ""
            if self.companyNameCN_detail == 0:
                exhibitorInfo['companynamecn'] = "".join(i.xpath('normalize-space(' + self.companyNameCN + ')')).strip()
            else:
                exhibitorInfo['companynamecn'] = ""
            if self.companyNameEN_detail == 0:
                exhibitorInfo['companynameen'] = "".join(i.xpath('normalize-space(' + self.companyNameEN + ')')).strip()
            else:
                exhibitorInfo['companynameen'] = ""
            if self.areacode_detail == 0:
                exhibitorInfo['areacode'] = "".join(i.xpath('normalize-space(' + self.areacode + ')')).strip()
            else:
                exhibitorInfo['areacode'] = ""
            if self.phone1_detail == 0:
                exhibitorInfo['phone1'] = "".join(i.xpath('normalize-space(' + self.phone1 + ')')).strip()
            else:
                exhibitorInfo['phone1'] = ""
            if self.phone2_detail == 0:
                exhibitorInfo['phone2'] = "".join(i.xpath('normalize-space(' + self.phone2 + ')')).strip()
            else:
                exhibitorInfo['phone2'] = ""
            if self.fax_detail == 0:
                exhibitorInfo['fax'] = "".join(i.xpath('normalize-space(' + self.fax + ')')).strip()
            else:
                exhibitorInfo['fax'] = ""
            if self.telphone_detail == 0:
                exhibitorInfo['telphone'] = "".join(i.xpath('normalize-space(' + self.telphone + ')')).strip()
            else:
                exhibitorInfo['telphone'] = ""
            if self.contacts_detail == 0:
                exhibitorInfo['contacts'] = "".join(i.xpath('normalize-space(' + self.contacts + ')')).strip()
            else:
                exhibitorInfo['contacts'] = ""
            if self.email_detail == 0:
                exhibitorInfo['email'] = "".join(i.xpath('normalize-space(' + self.email + ')')).strip()
            else:
                exhibitorInfo['email'] = ""
            if self.website_detail == 0:
                exhibitorInfo['website'] = "".join(i.xpath('normalize-space(' + self.website + ')')).strip()
            else:
                exhibitorInfo['website'] = ""
            if self.address_detail == 0:
                exhibitorInfo['address'] = "".join(i.xpath('normalize-space(' + self.address + ')')).strip()
            else:
                exhibitorInfo['address'] = ""
            if self.addressEN_detail == 0:
                exhibitorInfo['addressEN'] = "".join(i.xpath('normalize-space(' + self.addressEN + ')')).strip()
            else:
                exhibitorInfo['addressEN'] = ""
            if self.boothNo_detail == 0:
                exhibitorInfo['boothNo'] = "".join(i.xpath('normalize-space(' + self.boothNo + ')')).strip()
            else:
                exhibitorInfo['boothNo'] = ""
            if self.product_detail == 0:
                exhibitorInfo['product'] = "".join(i.xpath('normalize-space(' + self.product + ')')).strip()
            else:
                exhibitorInfo['product'] = ""
            if self.industry_detail == 0:
                exhibitorInfo['industry'] = "".join(i.xpath('normalize-space(' + self.industry + ')')).strip()
            else:
                exhibitorInfo['industry'] = ""

            if self.country_detail == 0:
                exhibitorInfo['country'] = "".join(i.xpath('normalize-space(' + self.country + ')')).strip()
            else:
                exhibitorInfo['country'] = ""
            if self.city_detail == 0:
                exhibitorInfo['city'] = "".join(i.xpath('normalize-space(' + self.city + ')')).strip()
            else:
                exhibitorInfo['city'] = ""
            if self.pageurl_detail == 0:
                exhibitorInfo['url'] = "".join(i.xpath('normalize-space(' + self.pageurl + ')')).strip()
            else:
                exhibitorInfo['url'] = ""

            if self.DETIAL_PAGE_STATE == 1:
                resp = requests.get(exhibitorInfo['url'], headers=self.headers)
                html = etree.HTML(resp.text)
                if self.companyNameCN_detail == 1:
                    exhibitorInfo['companynamecn'] = "".join(
                        html.xpath('normalize-space(' + self.companyNameCN + ')')).strip()
                if self.companynameen_detail == 1:
                    exhibitorInfo['companynameen'] = "".join(
                        html.xpath('normalize-space(' + self.companyNameEN + ')')).strip()
                if self.areacode_detail == 1:
                    exhibitorInfo['areacode'] = "".join(html.xpath('normalize-space(' + self.areacode + ')')).strip()
                if self.phone1_detail == 1:
                    exhibitorInfo['phone1'] = "".join(html.xpath('normalize-space(' + self.phone1 + ')')).strip()
                if self.phone2_detail == 1:
                    exhibitorInfo['phone2'] = "".join(html.xpath('normalize-space(' + self.phone2 + ')')).strip()
                if self.fax_detail == 1:
                    exhibitorInfo['fax'] = "".join(html.xpath('normalize-space(' + self.fax + ')')).strip()
                if self.telphone_detail == 1:
                    exhibitorInfo['telphone'] = "".join(html.xpath('normalize-space(' + self.telphone + ')')).strip()
                if self.contacts_detail == 1:
                    exhibitorInfo['contacts'] = "".join(html.xpath('normalize-space(' + self.contacts + ')')).strip()
                if self.email_detail == 1:
                    exhibitorInfo['email'] = "".join(html.xpath('normalize-space(' + self.email + ')')).strip()
                if self.website_detail == 1:
                    exhibitorInfo['website'] = "".join(html.xpath('normalize-space(' + self.website + ')')).strip()
                if self.address_detail == 1:
                    exhibitorInfo['address'] = "".join(html.xpath('normalize-space(' + self.address + ')')).strip()
                if self.addressEN_detail == 1:
                    exhibitorInfo['addressEN'] = "".join(html.xpath('normalize-space(' + self.addressEN + ')')).strip()
                if self.boothNo_detail == 1:
                    exhibitorInfo['boothNo'] = "".join(html.xpath('normalize-space(' + self.boothNo + ')')).strip()
                if self.industry_detail == 1:
                    exhibitorInfo['industry'] = "".join(html.xpath('normalize-space(' + self.industry + ')')).strip()
                if self.product_detail == 1:
                    exhibitorInfo['product'] = "".join(html.xpath('normalize-space(' + self.product + ')')).strip()
                if self.country_detail == 1:
                    exhibitorInfo['country'] = "".join(html.xpath('normalize-space(' + self.country + ')')).strip()
                if self.city_detail == 1:
                    exhibitorInfo['city'] = "".join(html.xpath('normalize-space(' + self.city + ')')).strip()
                if self.pageurl_detail == 1:
                    exhibitorInfo['url'] = exhibitorInfo['url']

            exhibitorlist.append(list(exhibitorInfo.values()))
        return exhibitorlist






