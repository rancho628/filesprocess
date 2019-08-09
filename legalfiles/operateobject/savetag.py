from legalfiles.models import Tag
import os
import legalfiles.processtext.batchdealtext

def save_tag():
    #获得标签
    tags  = legalfiles.processtext.batchdealtext.Batchdealtext.featwords
    #tag是一个字典列表
    for tag in tags:
        for t in tag:
          #这个函数已经有自动去重复功能
          Tag.objects.get_or_create(name=t)
