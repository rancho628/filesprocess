from legalfiles.models import Txt,Tag
import os
import legalfiles.processtext.batchdealtext
from config2 import data_file_path
#这个就是业务层，一个个的功能，供表现层调用



def save_txttags():
    #tags是一个字典列表
    tags= legalfiles.processtext.batchdealtext.Batchdealtext.featwords

    titles=os.listdir(data_file_path)

    for title, tag in zip(titles, tags):
        #拿到txt对象
       obj_txt = Txt.objects.filter(title=title).first()
       #每个txt有自己的标签字典，tag是一个字典
       for t in tag:
           #如果有这个标签，拿出来，没有则创建
           obj_tag, created=Tag.objects.get_or_create(name=t)
           obj_txt.tags.add(obj_tag.id)



