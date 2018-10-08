from django.shortcuts import render
from django.http import  HttpResponse
import os
import datetime
import pymysql
import json


def home(request):
    '''主页'''
    timeline, ah_value, nh_value = [],[],[]
    min_ah,min_nh,max_ah,max_nh = [],[],[],[]
    filedate = None
    #   收到表单提交
    if request.POST:
        filedate = request.POST['filedate']
        #   搜索框未输入
        if filedate == '':
            return render(request, 'home.html',
                          {
                              'input_warning':'alert alert-danger alert-dismissible',
                              'close_button':'X',
                              'information':'错误！未输入数据所在日期。',
                              'timeline': json.dumps(timeline),
                              'ah_value': json.dumps(ah_value),
                              'nh_value': json.dumps(nh_value),
                              'min_ah': json.dumps(min_ah),
                              'max_ah': json.dumps(max_ah),
                              'min_nh': json.dumps(min_nh),
                              'max_nh': json.dumps(max_nh),
                              'current_time': str(datetime.date.today()),
                          }
                          )
        timeline, ah_value, nh_value = find(
                r"SELECT create_data,receive_msg FROM gprs_receive WHERE create_data LIKE '"+filedate+r"%:00'")
        #   未检索到数据文件
        if len(timeline) == 0:
            return render(request, 'home.html',
                          {
                              'input_warning':'alert alert-danger alert-dismissible',
                              'close_button':'X',
                              'information':'错误！未检索到数据或输入日期格式错误。',
                              'timeline': json.dumps(timeline),
                              'ah_value': json.dumps(ah_value),
                              'nh_value': json.dumps(nh_value),
                              'min_ah': json.dumps(min_ah),
                              'max_ah': json.dumps(max_ah),
                              'min_nh': json.dumps(min_nh),
                              'max_nh': json.dumps(max_nh),
                              'current_time': str(datetime.date.today()),
                          }
                          )
        #   成功检索到数据文件
        if len(timeline) != 0:
            min_ah = min(ah_value)
            max_ah = max(ah_value)
            min_nh = min(nh_value)
            max_nh = max(nh_value)
            return render(request, 'home.html',
                              {
                                  'input_warning': 'alert alert-success alert-dismissible',
                                  'close_button': 'X',
                                  'information': '恭喜！成功检索数据并完成数据可视化。',
                                  'timeline': json.dumps(timeline),
                                  'ah_value': json.dumps(ah_value),
                                  'nh_value': json.dumps(nh_value),
                                  'min_ah': json.dumps(min_ah),
                                  'max_ah': json.dumps(max_ah),
                                  'min_nh': json.dumps(min_nh),
                                  'max_nh': json.dumps(max_nh),
                                  'current_time': str(datetime.date.today()),
                              }
                          )
    #   正常启动或刷新home
    return render(request, 'home.html',
                  {
                      'timeline': json.dumps(timeline),
                      'ah_value': json.dumps(ah_value),
                      'nh_value': json.dumps(nh_value),
                      'min_ah': json.dumps(min_ah),
                      'max_ah': json.dumps(max_ah),
                      'min_nh': json.dumps(min_nh),
                      'max_nh': json.dumps(max_nh),
                      'current_time': str(datetime.date.today()),
                  }
                  )

def download(request):
    '''数据下载页面'''
    timeline, ah_value, nh_value = [],[],[]
    filedate = None
    if request.POST:
        filedate = request.POST['filedate']
        #   未输入日期
        if filedate == '':
            return render(request, 'download.html',
                          {
                              'input_warning':'alert alert-danger alert-dismissible',
                              'close_button':'X',
                              'information':'错误！未输入数据所在日期。',
                              'current_time': str(datetime.date.today()),
                          }
                          )
        timeline, ah_value, nh_value = find(
            r"SELECT create_data,receive_msg FROM gprs_receive WHERE create_data LIKE '" + filedate + r"%'")
        #   未检索到数据
        if len(timeline) == 0:
            return render(request, 'download.html',
                          {
                              'input_warning': 'alert alert-danger alert-dismissible',
                              'close_button': 'X',
                              'information': '错误！未检索到数据或输入日期格式错误。',
                              'current_time': str(datetime.date.today()),
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
                      'current_time': str(datetime.date.today()),
                  }
                  )

def find(commond):
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
