from django.shortcuts import render
from django.http import  HttpResponse
import os
import datetime
import pymysql
import json

# Create your views here.
def home(request):
    timeline, ah_value, nh_value = find(
        r"SELECT create_data,receive_msg FROM gprs_receive WHERE create_data LIKE '%:00'")
    current_time = datetime.date.today()
    min_ah = min(ah_value)
    max_ah = max(ah_value)
    min_nh = min(nh_value)
    max_nh = max(nh_value)
    if request.POST:
        filedate = request.POST['filedate']
    return render(request, 'home.html',
                      {
                          'current_time':str(current_time),
                          'timeline':json.dumps(timeline),
                          'ah_value':json.dumps(ah_value),
                          'nh_value':json.dumps(nh_value),
                          'min_ah':json.dumps(min_ah),
                          'max_ah':json.dumps(max_ah),
                          'min_nh':json.dumps(min_nh),
                          'max_nh':json.dumps(max_nh),
                      }
                  )


def download(request):
    '''数据下载'''
    timeline, ah_value, nh_value = [],[],[]
    filedate = None
    if request.POST:
        #   接收文件日期，并检索数据 bv
        filedate = request.POST['filedate']
        if filedate == '':
            return render(request, 'download.html',
                          {
                              'input_info': '请输入需要下载的数据所在日期（例如：2016-06-07）'
                          }
                          )
        timeline, ah_value, nh_value = find(
            r"SELECT create_data,receive_msg FROM gprs_receive WHERE create_data LIKE '"+filedate+r"%'")
        if len(timeline) == 0:
            #   未检索到数据时
            return render(request, 'download.html',
                          {
                              'input_info': '数据不存在或输入日期格式错误'
                          }
                          )
        if len(timeline) != 0:
              # 写入文件
            with open(filedate+'.txt', 'w') as file_object:
                file_object.write("         TIME         AH   NH\n")
                i = 0
                while i < len(timeline):
                    file_object.write(timeline[i] + ",")
                    file_object.write(str(ah_value[i]) + ",")
                    file_object.write(str(nh_value[i]) + "\n")
                    i = i + 1
            file = open(filedate+'.txt','rb')
            response = HttpResponse(file)
            # 删除临时存储的文件
            if(os.path.exists(filedate+'.txt')):
                os.remove(filedate+'.txt')
            response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
            response['Content-Disposition'] = 'attachment;filename='+filedate+'.txt'
            return response

    return render(request, 'download.html',
                    {
                        'input_info': '请输入需要下载的数据所在日期（例如：2016-06-07）'
                    }
                  )


def descriprion(request):
    return render(request,'description.html')


def find(commond):
    '''根据命令查询相关字段'''
    db = pymysql.connect('123.207.7.51', 'root', 'root', 'lsq_gprs')  # 连接对象
    cursor = db.cursor()  # 游标对象
    cursor.execute(commond)
    data = cursor.fetchall()
    db.close()

    ah_value = []
    nh_value = []
    time = []
    i = 0
    while i < len(data):
        time.append(str(data[i][0]))
        value = str(data[i][1]).split(' ')
        nh_value.append(int(value[0][1:]))
        ah_value.append(int(value[1]))
        i = i + 1
    return time, ah_value, nh_value
