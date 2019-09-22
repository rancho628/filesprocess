from legalfiles.models import Tag
import os
import legalfiles.processtext.batchdealtext

def add_tag(request,tag_name):
    #没有这个标签就创建
    Tag.objects.get_or_create(name=tag_name, users=request.user)
