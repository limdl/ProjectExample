from generalspider import ExhibitorSpiderJson
import requests,time,os,xlwt,xlrd,json

class cantonfair2019_Spider(ExhibitorSpiderJson):
    #账号、密码
    loginID = ''
    token = ''


    #开始链接，请求获取行业
    start_url = 'http://webapi.cantonfair.org.cn/?loginID=&token=&interfaceEnum=ExhibitorListWAP&Source=3&ipAddress=&bizData=%7B%22IsCN%22%3A1%2C%22PageSize%22%3A10%2C%22OrderBy%22%3A2%2C%22CategoryNo%22%3A%22%22%2C%22KeyWord%22%3A%22%22%2C%22CurrentPage%22%3A1%7D'

    #各行业api，{'CategoryNo': '411', 'Name': '电子消费品及信息产品', 'Count': 702}，参数：数量，行业编号，请求获取行业展商列表
    productCategorys_api = 'http://webapi.cantonfair.org.cn/?loginID=&token=&interfaceEnum=ExhibitorListWAP&Source=3&ipAddress=&bizData=%7B%22IsCN%22%3A1%2C%22PageSize%22%3A{}%2C%22OrderBy%22%3A2%2C%22CategoryNo%22%3A%22{}%22%2C%22KeyWord%22%3A%22%22%2C%22CurrentPage%22%3A1%7D'

    #展商详情页api，获取明细，参数：展商编号，9142193783
    detail_page_api = 'http://webapi.cantonfair.org.cn/?loginID={}&token={}&interfaceEnum=ExhibitorDetailWAP&Source=3&ipAddress=&bizData=%7B%22IsCN%22%3A1%2C%22ExhibitorID%22%3A%22{}%22%2C%22IsAD%22%3A%220%22%2C%22CorpType%22%3A%221%22%7D'

    # 设置请求头
    headers = {
        'Referer': 'http://m.cantonfair.org.cn/m/widget/page/preview-exhibitor-search.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }

    foldname = 'D:/'  # 保存目录
    filename = '2.xls'  # 保存文件名
    sheetheader = ['industry', 'boothNo', 'CorpName','Http', 'product', 'CorpAddress', 'Telephone', 'Email', 'Fax', 'Linkman','url','CorpDesc']
    rows = 1
    delaytime = 0.1
	
    def __init__(self):
        if not os.path.exists(self.foldname + self.filename):
            self.create_wookbook(self.foldname, self.filename, self.sheetheader)
        resp = requests.get(self.start_url, headers=self.headers)
        html = json.loads(resp.text)

        # print(html['ReturnData']['ProductCategorys'][0:2])
        for i in html['ReturnData']['ProductCategorys'][:]:
            # exhibitorlist['industry'] = i['Name']
            # print(exhibitorlist['industry'])
            # # i['Count']
            industry_resp = requests.get(self.productCategorys_api.format(i['Count'], i['CategoryNo']), headers=self.headers)
            industry_html = json.loads(industry_resp.text)
            for c in industry_html['ReturnData']['CorpList'][:]:
                exhibitorlist = []
                exhibitorInfo = {}
                # print(c)
                detail_resp = requests.get(self.detail_page_api.format(self.loginID,self.token,c['ID']), headers=self.headers)
                datail_html = json.loads(detail_resp.text)
                # print(datail_html)
                # exhibitorInfo['boothPhase'] = '第{}期'.format(datail_html['ReturnData']['BOOTHINFO'][0]['phase'])
                exhibitorInfo['industry'] = i['Name']
                exhibitorInfo['boothNo'] = ";".join(["{} {}".format(bn['CategoryName'],bn['Booth']) for bn in datail_html['ReturnData']['BOOTHINFO']])
                exhibitorInfo['CorpName'] = datail_html['ReturnData']['CorpName']
                exhibitorInfo['Http'] = datail_html['ReturnData']['Http']
                exhibitorInfo['product'] = datail_html['ReturnData']['AreaInfo']
                exhibitorInfo['CorpAddress'] = datail_html['ReturnData']['CorpAddress']
                exhibitorInfo['Telephone'] = datail_html['ReturnData']['Telephone']
                exhibitorInfo['Email'] = datail_html['ReturnData']['Email']
                exhibitorInfo['Fax'] = datail_html['ReturnData']['Fax']
                exhibitorInfo['Linkman'] = datail_html['ReturnData']['Linkman']
                exhibitorInfo['url'] = 'http://i.cantonfair.org.cn/cn/Company/Index?corpid={}&corptype=1&ad=0'.format(c['ID'])
                exhibitorInfo['CorpDesc'] = datail_html['ReturnData']['CorpDesc']
                exhibitorlist = [list(exhibitorInfo.values())]
                print(i['Name'],exhibitorInfo['CorpName'],exhibitorInfo['url'])
                rows = self.write_into_workbook(self.rows, exhibitorlist, self.foldname, self.filename)
                time.sleep(self.delaytime)

if __name__ == "__main__":
    cantonfair2019_Spider()
    print("over")
