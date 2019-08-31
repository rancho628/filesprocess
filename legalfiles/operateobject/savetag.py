from legalfiles.models import Tag
import os
import legalfiles.processtext.batchdealtext

def save_tag(request):
    #获得标签
    tags  = legalfiles.processtext.batchdealtext.Batchdealtext.featwords
    #tags是一个字典列表
    for tag in tags:
        #tag是一个字典
        for t in tag:
          #这个函数已经有自动去重复功能,如果已经有了就不创建了
          Tag.objects.get_or_create(name=t, users=request.user)
