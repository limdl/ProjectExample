from generalspider import ExhibitorSpiderJson
from lxml import etree
import requests,os,time,json
#起始链接
class hkhousewarefairSpider(ExhibitorSpiderJson):
    foldname = 'D:/'  # 保存目录
    filename = '2.xls'  # 保存文件名

    start_urls = ['https://api-fair.hktdc.com/fair-company/v1/companies?language=en&fairSymbol=hkhousewarefair&page=1&pageItem=20&dfcPathId=']
    # 设置请求头
    headers = {
        # 'Referer': '',
        'origin': 'https: // event.hktdc.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        # 'Cookie':Cookie,
    }
    #数据表表头
    sheetheader = ['序号', '公司名称', '英文名称', '区号', '电话1', '电话2', '传真', '移动电话', '联系人', '邮箱', '网址', '地址', '英文地址', '企业类型',
                   '主营产品', '主营行业', '国家', '城市', 'url']
    #下一页链接状态：直接是链接、列表、需点击
    next_page_state = 'isList'#isLink/isList/isClick
    # xpath提取下一页链接
    # next_page_xpath = './/span[@class="active"]/following-sibling::*[1]/text()'
    # 下一页链接前缀拼接
    next_page_prefix = start_urls[0]
    # next_page_list = [start_urls[0].format(page) for page in range(46, 51)]
    # next_page_list = ['http://www.stonefair.org.cn/Exhibitor/ExhibitorList.asp?page={}'.format(chr(page)) for page in range(ord('a'),ord('z')+1)]
    page = 46 #断点续采第几页
    rows = 1  #断点续采第几行
    delaytime = 2
    # info_items_xpath = './/div[@class="item_list cf"]'
    DETIAL_PAGE_STATE = 0 #1翻页，0无需翻页

    # 采集的数据字段xpath设置,0数据在翻页当前页，1数据在详情页
    companyNameCN_detail = 0
    # companyNameCN = './/div/div/a/h3/text()'  # 公司名称、
    companyNameEN_detail = 0
    # companyNameEN = './/div/div/a/h3/text()'  # 英文名称、
    areacode_detail = 0
    # areacode = 'xpath'  # 区号
    phone1_detail = 0
    # phone1 = './/p[text()="电话号码"]/../p[2]'  # 电话1
    phone2_detail = 0
    # phone2 = 'xpath'  # 电话2
    fax_detail = 0
    fax = 'xpath'  # 传真
    telphone_detail = 0
    # telphone = 'xpath'  # 移动电话
    contacts_detail = 0
    contacts = 'xpath'  # 联系人
    email_detail = 0
    # email = 'xpath'  # 邮箱
    website_detail = 0
    # website = './/p[text()="公司网址"]/../p[2]'  # 网址
    address_detail = 0
    # address = './/p[@class="notranslate OneLinkNoTx"]/text()'  # 地址
    addressEN_detail = 0
    # addressEN = 'xpath'  # 英文地址
    boothNo_detail = 0
    # boothNo = './/div/div/div/p/span/span/a/text()'  # 企业类型，放展馆展位号
    industry_detail = 0
    # industry = './/p[text()="行业"]/../p[2]'  # 行业
    product_detail = 0
    # product = './/div/div[2]/div/span/text()'  # 产品
    country_detail = 0
    # country = './/div/div[1]/div/text()'  # 国家
    city_detail = 0
    # city = 'xpath'  # 城市

    # pageurl = 'xpath'  # 采集页网址
    def __init__(self):
        for start_url in self.start_urls:
            next_page_prefix = start_url.replace('page=1','page={}')
            next_page_list = [next_page_prefix.format(page) for page in range(1, 51)]
            if not os.path.exists(self.foldname+self.filename):
                self.create_wookbook(self.foldname, self.filename,self.sheetheader)
            next_link = ' '
            while next_link:
                if self.next_page_state == 'isList':
                    try:
                        next_link = next_page_list[self.page-1]
                        resp = requests.get(next_link, headers=self.headers)
                        html = json.loads(resp.text)
                        exhibitorlist = self.get_datas(next_link, html)
                        rows = self.write_into_workbook(self.rows, exhibitorlist, self.foldname, self.filename)
                    except:
                        next_link =''
                    self.page +=1
                print(next_link)
                time.sleep(self.delaytime)

    def get_datas(self, current_link, html):
        exhibitorlist = []
        exhibitorInfo = {}
        items = html['hits']
        for i in items:
            exhibitorInfo['rowId'] = ''
            try:
                exhibitorInfo['companynamecn'] = i['hits'][0]['name']
            except:
                exhibitorInfo['companynamecn'] = ''
            try:
                exhibitorInfo['companynameen'] = i['hits'][0]['name']
            except:
                exhibitorInfo['companynameen'] = ''
            try:
                exhibitorInfo['areacode'] = ''
            except:
                exhibitorInfo['areacode'] = ''
            try:
                exhibitorInfo['phone1'] = i['hits'][0]['telephone']
            except:
                exhibitorInfo['phone1'] = ''
            try:
                exhibitorInfo['phone2'] = ''
            except:
                exhibitorInfo['phone2'] = ''
            try:
                exhibitorInfo['fax'] = i['hits'][0]['fax']
            except:
                exhibitorInfo['fax'] = ''
            try:
                exhibitorInfo['telphone'] = ''
            except:
                exhibitorInfo['telphone'] = ''
            try:
                exhibitorInfo['contacts'] = ''
            except:
                exhibitorInfo['contacts'] = ''
            try:
                exhibitorInfo['email'] = ''
            except:
                exhibitorInfo['email'] = ''
            try:
                exhibitorInfo['website'] = i['hits'][0]['website']
            except:
                exhibitorInfo['website'] = ''
            try:
                exhibitorInfo['address'] = i['hits'][0]['companyAddress']
            except:
                exhibitorInfo['address'] = ''
            try:
                exhibitorInfo['addressEN'] = i['hits'][0]['companyAddress']
            except:
                exhibitorInfo['addressEN'] = ''
            try:
                exhibitorInfo['boothNo'] = i['hits'][0]['boothNumber'][0]['boothNumber']
            except:
                exhibitorInfo['boothNo'] = ''
            try:
                exhibitorInfo['product'] = i['hits'][0]['productCategory']
            except:
                exhibitorInfo['product'] = ''
            try:
                exhibitorInfo['industry'] = ";".join(i['hits'][0]['industry'])
            except:
                exhibitorInfo['industry'] = ''
            try:
                exhibitorInfo['country'] = i['hits'][0]['country']
            except:
                exhibitorInfo['country'] = ''
            try:
                exhibitorInfo['city'] = ''
            except:
                exhibitorInfo['city'] = ""
            try:
                exhibitorInfo['url'] = "https://api-fair.hktdc.com/fair-company/v1/companies/fair/hkhousewarefair/exhibitor/{}/en".format(i['hits'][0]['id'])
            except:
                exhibitorInfo['url'] = ''
            exhibitorlist.append(list(exhibitorInfo.values()))
        return exhibitorlist

if __name__ == "__main__":
    hkhousewarefairSpider()
    print("over")
