from django import template
from django.db.models.aggregates import Count
from legalfiles.models import Tag
from ..models import Txt
#

register = template.Library()


@register.simple_tag
def get_tags():
    tags=Tag.objects.all()

    # t=[]
    # for tag in tags:
    #     t.append(tag.name)
    # b = [''.join(lazy_pinyin(_)) for _ in t]
    # b.sort()
    # print(b)

    return tags

