from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import os
import legalfiles.processtext.batchdealtext
from django.http import HttpResponseRedirect


def to_upload(request):
    return render(request, 'upload.html')


def upload_file(request):
    # if request.method == "POST":    # 请求方法为POST时，进行处理
    myFile = request.FILES.getlist("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None

    # if not myFile:
    #     return HttpResponse("no files for upload!")

    for f in myFile:
        destination = open('legalfiles\\files\\' + f.name, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
    return HttpResponseRedirect('/legalfiles/to_process/')


def to_process(request):
    return render(request, 'processfiles.html')


def process_file(request):
    # if request.method == "POST":
    wordlist = legalfiles.processtext.batchdealtext.processFile()
    return render(request, 'processfiles.html', {
          'wordlist': wordlist
    })
