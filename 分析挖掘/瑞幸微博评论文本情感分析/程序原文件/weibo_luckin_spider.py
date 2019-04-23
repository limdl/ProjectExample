#微博爬虫：https://s.weibo.com/,按“瑞幸”搜索
from selenium import webdriver
from lxml import etree
import time,datetime,xlwt,xlrd,os,re
from xlutils.copy import copy
from urllib import parse
                 
def parse_time(time_str):
    if '分钟前' in time_str:
        time_temp = int(time_str.split('分钟前')[0])
        new_time = (datetime.datetime.now() + datetime.timedelta(minutes=time_temp)).strftime("%Y-%m-%d %H:%M")
    elif '今天' in time_str:
        time_temp = time_str.split('今天')[1]
        new_time = (datetime.datetime.now()).strftime("%Y-%m-%d") + ' ' +time_temp
    elif '月' in time_str and '日' in time_str:
        time_temp = time_str.replace('月','-').replace('日','-')
        new_time = (datetime.datetime.now()).strftime("%Y") + '-' +time_temp
    else:
        new_time=''
    return new_time



# 创建excel表
def create_wookbook(sheetheader):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('weibo')
    # 写入表头
    for h in range(0, len(sheetheader)):
        worksheet.write(0, h, sheetheader[h])
    workbook.save('../weibo.xls')


# 写入数据  
def write_into_workbook(rows, content_info_list):
    oldWb = xlrd.open_workbook('../weibo.xls')  # 先打开已存在的表
    newWb = copy(oldWb)  # 复制
    newWs = newWb.get_sheet(0)  # 取sheet表
    for ex in content_info_list:
        for col in range(0, len(ex)):
            newWs.write(rows, col, ex[col])
        rows += 1
    newWb.save('../weibo.xls')
    return rows

def weibo(key_word,user_name,user_key,pages):
#     file_set = open('../采集设置.txt','r')
#     file_read = file_set.read()
#     key_word = re.search(r"(?<=关键词:)(.+?)[\s]",file_read).group(1)
#     user_name = re.search(r"(?<=用户名:)(.+?)[\s]",file_read).group(1)
#     user_key = re.search(r"(?<=密码:)(.+?)[\s]",file_read).group(1)
#     pages = int(re.search(r"(?<=采集页数:)(.+?)[\s]",file_read).group(1))
    dict_weibo ={'q':key_word,'wvr':'6','b':'1','Refer':'SWeibo_box'}

    print('采集关键词:{},采集页数:{}'.format(key_word,pages))
    start_url = 'https://s.weibo.com/weibo?'+parse.urlencode(dict_weibo)
    sheetheader = ['编号', '用户名', '用户链接', '会员类型', '评论内容', '评论时间', '来自','转发','评论','点赞']
    if not os.path.exists('../weibo.xls'):
        create_wookbook(sheetheader)
    rows =1
    driver = webdriver.Chrome()
    driver.get('https://s.weibo.com/')
    time.sleep(2)
    html = etree.HTML(driver.page_source)
    if html.xpath('//*[@id="weibo_top_public"]/div/div/div[3]/div[2]/ul/li[3]/a'):
        driver.find_element_by_xpath('//*[@id="weibo_top_public"]/div/div/div[3]/div[2]/ul/li[3]/a').click()

    time.sleep(2)
    input_user = driver.find_element_by_xpath('.//input[@action-data="text=邮箱/会员帐号/手机号"]')
    time.sleep(2)
    input_user.clear()
    input_user.send_keys(user_name)#输入账号
    time.sleep(2)
    input_key = driver.find_element_by_xpath('.//input[@type="password"]')
    input_key.clear()
    input_key.send_keys(user_key)#输入密码
    driver.find_element_by_xpath('.//span[@class="enter_psw"]/../../div[@class="item_btn"]/a').click() #点击登录
    time.sleep(2)

    for page in range(1,pages+1):
        url = (start_url+'&page={}').format(page)
        driver.get(url)  
        html = etree.HTML(driver.page_source)
        item = html.xpath('.//div[@class="card-wrap" and @action-type="feed_list_item"]')
        content_info = {}
        content_info_list = []
        for i in item:
            # content_info['page'] = page
            content_info['mid'] = "".join(i.xpath('./@mid')).strip()
            content_info['user_name'] = "".join(i.xpath('.//descendant::div[@class="content"]/div/div/a[@class="name"]/@nick-name')).strip()
            content_info['user_link'] = 'https:'+"".join(i.xpath('.//descendant::div[@class="content"]/div/div/a[@class="name"]/@href')).strip().split('?re')[0]
            content_info['user_type'] = "".join(i.xpath('.//descendant::div[@class="content"]/div/div/a[@target="_blank" and @title]/@title')).strip()
            content_info['content_txt'] = "".join(i.xpath('.//descendant::div[@class="content"]/p[@class="txt"][position()=last()]//text()')).strip()
            content_info['content_time'] = "".join(i.xpath('.//descendant::div[@class="content"]/p[@class="from"]/a[@suda-data]/text()')).strip()
            if content_info['content_time'] == '':
                content_info['content_time'] = ''
            else:
                content_info['content_time'] = parse_time(content_info['content_time'])
            content_info['phone_nofollow'] = "".join(i.xpath('.//descendant::div[@class="content"]/p[@class="from"]/a[@rel="nofollow"]/text()')).strip()
            content_info['content_zhuanfa'] = "".join(i.xpath('.//descendant::div[@class="card-act"]/ul/li[2]//text()')).strip().replace('转发','')
            content_info['content_pinglu'] = "".join(i.xpath('.//descendant::div[@class="card-act"]/ul/li[3]//text()')).strip().replace('评论','')
            content_info['content_dianzan'] = "".join(i.xpath('.//descendant::div[@class="card-act"]/ul/li[4]//text()')).strip().replace('赞','')
            
     
            content_info_list.append(list(content_info.values()))
        print(content_info_list)
        rows = write_into_workbook(rows, content_info_list)
        time.sleep(2)
    print('采集完成')
    driver.close()
if __name__ =='__main__':
    key_word = input('请输入采集关键词：')
    user_name = input('请输入微博用户名：')
    user_key = input('请输入微博密码：')
    pages = 50 #采集页数
    weibo(key_word,user_name,user_key,pages)
