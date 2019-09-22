import os
import django


os.environ['DJANGO_SETTINGS_MODULE'] = 'filesprocess.settings'
django.setup()
from legalfiles.models import Tag
import legalfiles.processtext.batchdealtext
from legalfiles.operateobject import deletetxttags

def delete_tag(request,tag):
    #先删除多对多表的数据
    deletetxttags.delete_txttags(request,tag)
    #再删除标签
    Tag.objects.filter(name=tag,users=request.user).delete()

if __name__ == '__main__':
    delete_tag('北京市')
