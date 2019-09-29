from django import template
from django.db.models.aggregates import Count
from legalfiles.models import Tag
from ..models import Txt
#from __future__ import unicode_literals
from xpinyin import Pinyin
#from pypinyin import lazy_pinyin

register = template.Library()


@register.simple_tag
#返回对应文章的所有标签.
def get_txttags(mytxt_id):
    txttags=[]
    txt_tag = Txt.objects.filter(txt_id=mytxt_id).values_list("tags")
    for tag_id in txt_tag:
        # mytags_id.add(tag_id[0])
        if tag_id[0]!=None:
           txttags.append(Tag.objects.get(id=tag_id[0]).name)
    return txttags



