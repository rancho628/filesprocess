from django import template
from django.db.models.aggregates import Count
from legalfiles.models import Tag
from ..models import Txt

register = template.Library()


@register.simple_tag
def get_tags():
    return Tag.objects.all()

