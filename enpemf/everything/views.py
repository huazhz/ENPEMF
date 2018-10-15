from django.shortcuts import render
import time
import json
import random

# Create your views here.

def index(request):
    if request.POST:
        print(request.POST['file_date'])

    nh_value = []
    min_nh = []
    max_nh = []

    ah_value = []
    min_ah = []
    max_ah = []

    timeline = []

    for x in range(0, 90):
        timeline.append(x)

    value = [[],[],[],[],[],[],[],[],[]]
    for x in value:
        for j in range(0, 9):
            for k in range(0, 10):
                value[j].append(random.randint(0, j))
        ah_value.append(x)
        nh_value.append(x)

    min_temp = []
    max_temp = []
    for x in ah_value:
        min_temp.append(min(x))
        max_temp.append(max(x))
    min_ah = min(min_temp)
    max_ah = max(max_temp)

    min_temp = []
    max_temp = []
    for x in nh_value:
        min_temp.append(min(x))
        max_temp.append(max(x))
    min_nh = min(min_temp)
    max_nh = max(max_temp)

    return render(request, 'index.html',
                  {
                      'current_time': str(time.strftime("%Y-%m-%d", time.localtime())),
                      'form_label': '检索日期',
                      'button_label': '检索',
                      'button_information': '检索数据的时间间隔为一分钟，请正确选择日期后进行数据检索',
                      'timeline': json.dumps(timeline),
                      'ah_value': json.dumps(ah_value),
                      'nh_value': json.dumps(nh_value),
                      'min_ah': json.dumps(min_ah),
                      'max_ah': json.dumps(max_ah),
                      'min_nh': json.dumps(min_nh),
                      'max_nh': json.dumps(max_nh),
                   })



def download(request):
    return render(request, 'download.html',
                  {
                      'current_time': str(time.strftime("%Y-%m-%d", time.localtime())),
                      'form_label': '下载日期',
                      'button_label': '下载',
                      'button_information': '下载数据的时间间隔为一秒钟，请正确选择日期后进行数据下载',

                   })