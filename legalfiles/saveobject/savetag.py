from legalfiles.models import Tag
import os
import legalfiles.processtext.batchdealtext

def save_tag():
    wordlists = bat = legalfiles.processtext.batchdealtext.Batchdealtext.wordlists
    # 文章标题和内容放进数据库
    for w in wordlists:
        Tag.objects.get_or_create(name=w)
