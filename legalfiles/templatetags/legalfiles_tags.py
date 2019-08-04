from django import template
from django.db.models.aggregates import Count
from legalfiles.models import Tag
from ..models import Txt
#from __future__ import unicode_literals
from xpinyin import Pinyin
from pypinyin import lazy_pinyin

register = template.Library()


@register.simple_tag
def get_tags():
    tags=Tag.objects.all()

    pin = Pinyin()
    ret={}
    list=[]
    for tag in tags:
        list.append((pin.get_pinyin(tag.name),tag.name))
    list.sort()
    temp_list = []
    for i in range(len(list)):
        if i>0:
           if list[i][0][0]==list[i-1][0][0]:
              temp_list.append(list[i][1])
           else:
              ret[list[i-1][0][0]]=temp_list
              temp_list=[]
              temp_list.append(list[i][1])
        else:
            temp_list.append(list[i][1])

    return ret



