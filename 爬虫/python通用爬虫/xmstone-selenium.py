from generalspider import ExhibitorSpiderSelenium
import requests
#起始链接
class xmstoneSpiderSelenium(ExhibitorSpiderSelenium):
    start_urls = ['http://www.stonefair.org.cn/Exhibitor/ExhibitorList.asp']
    # 设置请求头
    headers = {
        'Referer': 'http://www.stonefair.org.cn/Exhibitor/ExhibitorList.asp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        # 'Cookie':Cookie,
    }
    sheetheader = ['序号', '公司名称', '英文名称', '区号', '电话1', '电话2', '传真', '移动电话', '联系人', '邮箱', '网址', '地址', '英文地址', '企业类型',
                   '主营产品', '主营行业', '国家', '城市', 'url']

    # 下一页链接状态：直接是链接、列表、需点击
    next_page_state = 'isList'  # isLink/isList/isClick
    # xpath提取下一页链接
    next_page_xpath = './/*[@title="Next Page"]/a/@href'
    # 下一页链接前缀拼接
    next_page_prefix = 'http://www.stonefair.org.cn/Exhibitor/ExhibitorList.asp?page={}'

    next_page_list = ['http://www.stonefair.org.cn/Exhibitor/ExhibitorList.asp?page={}'.format(page) for page in
                      range(1, 91)]
    ##next_page_list = ['http://www.stonefair.org.cn/Exhibitor/ExhibitorList.asp?page={}'.format(chr(page)) for page in range(ord('a'),ord('z')+1)]
    delaytime = 2
    page = 1  # 断点续采第几页
    rows = 1  # 断点续采第几行

    info_items_xpath = './/tr[@bgcolor]'
    DETIAL_PAGE_STATE = 0

    foldname = 'D:/'  # 保存目录
    filename = '1.xls'  # 保存文件名

    # 采集的数据字段xpath设置,0数据在翻页当前页，1数据在详情页
    companyNameCN_detail = 0
    companyNameCN = './/td[3]/text()'  # 公司名称、
    companyNameEN_detail = 0
    companyNameEN = './/td[2]/text()'  # 英文名称、
    areacode_detail = 0
    areacode = 'xpath'  # 区号
    phone1_detail = 0
    phone1 = 'xpath'  # 电话1
    phone2_detail = 0
    phone2 = 'xpath'  # 电话2
    fax_detail = 0
    fax = 'xpath'  # 传真
    telphone_detail = 0
    telphone = 'xpath'  # 移动电话
    contacts_detail = 0
    contacts = 'xpath'  # 联系人
    email_detail = 0
    email = 'xpath'  # 邮箱
    website_detail = 0
    website = 'xpath'  # 网址
    address_detail = 0
    address = 'xpath'  # 地址
    addressEN_detail = 0
    addressEN = 'xpath'  # 英文地址
    boothNo_detail = 0
    boothNo = './/td[2]/text()'  # 企业类型，放展馆展位号
    industry_detail = 0
    industry = './/td/div/div/div[@class="ProdMCon"]/text()'  # 行业
    product_detail = 0
    product = './/td/div/div/div[@class="ProdTCon"]/text()'  # 产品
    country_detail = 0
    country = './/td[4]/text()'  # 国家
    city_detail = 0
    city = './/td[4]/text()'  # 城市
    pageurl_detail = 0
    pageurl = 'xpath'  # 采集页网址

# if __name__ == "__main__":
xmstoneSpiderSelenium()
print("over")
