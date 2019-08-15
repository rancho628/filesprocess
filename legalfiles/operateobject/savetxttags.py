from legalfiles.models import Txt,Tag
import os
import legalfiles.processtext.batchdealtext
from config2 import data_file_path
#这个就是业务层，一个个的功能，供表现层调用

def save_txttags():
    #tags是一个字典列表(字典是列表的元素)
    tags= legalfiles.processtext.batchdealtext.Batchdealtext.featwords

    titles=os.listdir(data_file_path)

    for title, tag in zip(titles, tags):
       #拿到txt对象，肯定有的
       obj_txt = Txt.objects.get(title=title)
       #每个txt有自己的标签字典，tag是一个字典
       for t in tag:
           #标签拿出来（肯定有，刚放进去），拿出来是为了拿到它的主键
           obj_tag = Tag.objects.get(name=t)
           #这个会自动去重复的，如果里面有文章id和标签id一样的数据，就不会加了
           obj_txt.tags.add(obj_tag.id)



