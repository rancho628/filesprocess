from django.shortcuts import render
from legalfiles.models import Txt
# Create your views here.
from django.http import HttpResponse
import os
import legalfiles.processtext.batchdealtext
from django.http import HttpResponseRedirect



def index(request):
    wordlists, featWords = legalfiles.processtext.batchdealtext.processFile()

    txts = Txt.objects.all()

    return render(request, 'legalfiles/index.html', {
        'wordlists': wordlists,
        'featWords': featWords,
        'txts': txts
    })

def to_upload(request):
    return render(request, 'legalfiles/upload.html')

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
    return HttpResponse("上传成功! 请关闭窗口")


def to_process(request):
    return render(request, 'legalfiles/processfiles.html')


def process_file(request):
    # if request.method == "POST":
    wordlists, featWords = legalfiles.processtext.batchdealtext.processFile()

    #return HttpResponse("处理文件成功! 请关闭窗口")


def get_detail_page(request, txt_id):
    all_txt = Txt.objects.all()
    curr_txt = None
    previous_index = 0
    next_index = 0
    previous_txt = None
    next_txt = None
    for index, txt in enumerate(all_txt):
        if index == 0:
            previous_index = 0
            next_index = index + 1
        elif index == len(all_txt) - 1:
            previous_index = index - 1
            next_index = index
        else:
            previous_index = index - 1
            next_index = index + 1
        if txt.txt_id == txt_id:
            curr_txt = txt
            previous_txt = all_txt[previous_index]
            next_txt = all_txt[next_index]
            break

    section_list = curr_txt.content.split('\n')
    return render(request, 'legalfiles/detail.html',
                  {
                      'curr_txt': curr_txt,
                      'section_list': section_list,
                      'previous_txt': previous_txt,
                      'next_txt': next_txt
                  }
                  )
