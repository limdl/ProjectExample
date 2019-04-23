#情感评分分析
from aip import AipNlp
import csv,re
import pandas as pd
import numpy as np

""" 你的 APPID AK SK """
# 利用百度云提供的API接口实现情感分析
# https://cloud.baidu.com/product/nlp/sentiment_classify
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

#清洗Unicode编码字符串https://www.jianshu.com/p/4958bcdea12a
def illegal_char(s):
    s = re.compile( \
        u"[^"
        u"\u4e00-\u9fa5"
        u"\u0041-\u005A"
        u"\u0061-\u007A"
        u"\u0030-\u0039"
        u"\u3002\uFF1F\uFF01\uFF0C\u3001\uFF1B\uFF1A\u300C\u300D\u300E\u300F\u2018\u2019\u201C\u201D\uFF08\uFF09\u3014\u3015\u3010\u3011\u2014\u2026\u2013\uFF0E\u300A\u300B\u3008\u3009"
        u"\!\@\#\$\%\^\&\*\(\)\-\=\[\]\{\}\\\|\;\'\:\"\,\.\/\<\>\?\/\*\+"
        u"]+").sub('', s)
    return s


# 对读入的数据进行情感分析，将其得到的结果解析成标准JSON格式数据，并保存在一个新的dict中
def senti_anlaly(text):
    text = illegal_char(text)
    data = client.sentimentClassify(text)
    sentiment =data['items'][0]['positive_prob']
    return sentiment

datas = pd.read_excel('weibo_luckin.xls',sheet_name='weibo',header=0,encoding = "gbk")
sentiments = []
for s in list(datas['评论内容']):
    sentiments.append(senti_anlaly(s))
