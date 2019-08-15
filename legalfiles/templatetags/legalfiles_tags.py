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
        #把一个个标签的拼音和名字组合起来，list是一个元组列表
        list.append((pin.get_pinyin(tag.name),tag.name))
    #默认按照元组的第一个元素排序
    list.sort()
    temp_list = []
    #排序完的列表的长度
    length=len(list)
    for i in range(length):
        if i>0:
            #如果首字母和前一个相同，加进去temp
           if list[i][0][0]==list[i-1][0][0]:
              temp_list.append(list[i][1])
              #到了结尾了，别忘了弄进去ret，之前忽略了
              if i==length-1:
                  ret[list[i][0][0]] = temp_list
            #发现不相同，就是新的首字母开启，旧字母作为key，temp这个列表作为内容，放进去ret
           else:
              #保存旧字母的
              ret[list[i-1][0][0]]=temp_list
              #清空
              temp_list=[]
              temp_list.append(list[i][1])
        else:
            #第一个，那就开辟
            temp_list.append(list[i][1])
    #返回一个key是首字母，value是列表的字典
    return ret



