from django.shortcuts import render,HttpResponse
from datetime import datetime
import pygal
import json
from .models import Data
from pyecharts import Bar

def render_html(request):
    #
    # # 针对title，将类型全部查询出来
    # titles = Data.objects.values_list('title')
    # titles = {title[0] for title in titles}
    #
    # # for title in titles:
    # #     info = Data.objects.filter(title=title).order_by('-create_time')[:10]
    #
    # # infos = Data.objects.all().order_by('-create_time')[:10]
    #
    # # info_list = [(info.create_time, info.number) for info in infos]
    # # title = infos[0].title
    #
    # datetimeline = pygal.DateTimeLine(
    #     x_label_rotation=35, truncate_label=-1,
    #     x_value_formatter=lambda dt: dt.strftime('%d, %b %Y at %I:%M:%S %p'))
    #
    #
    # for title in titles:
    #     infos = Data.objects.filter(title=title).order_by('-create_time')[:10]
    #     datetimeline.add(title, [(info.create_time, info.number) for info in infos])
    # # datetimeline.add("Serie", [(datetime(2013, 1, 2, 12, 0), 300),])
    # # datetimeline.add(title, info_list)
    # return render(request,'data.html',{'chart':datetimeline})

    # #pagal文档：http://www.pygal.org/en/stable/documentation/types/bar.html
    # attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    # v1 = [5, 20, 36, 10, 75, 90]
    # v2 = [10, 25, 8, 60, 20, 80]
    # bar = Bar("柱状图数据堆叠示例")
    # bar.add("商家A", attr, v1, is_stack=True)
    # bar.add("商家B", attr, v2, is_stack=True)

    # chart = pygal.Line()
    # chart.x_labels = 'Red', 'Blue', 'Green'
    # chart.add('line', [.0002, .0005, .00035])

    return render(request, 'render.html')

def post_data(request):
    if request.method != 'POST':
        return HttpResponse('Error 403',status=403)


    """
    {
        'data':[
                {'title':'Python3教程','number':245},
                {'title':'Xpath','number':2},
                {'title':'Django','number':16},
                {'title':'Scrapy','number':256},
                ......
            ],
    }
    """
    try:
        info = json.loads(request.body)
        data = info['data']
        for da in data:
            title = da['title']
            number = da['number']
            Data.objects.create(title=title,number=number)
            # 使用Data model 进行数据的保存
    except:
        return HttpResponse('Error 400', status=400)

    return HttpResponse('OK 200',status=200)
