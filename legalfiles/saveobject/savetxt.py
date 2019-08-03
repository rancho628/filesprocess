from legalfiles.models import Txt
import os
import legalfiles.processtext.batchdealtext
from config2 import data_file_path
#这个就是业务层，一个个的功能，供表现层调用



def save_txt():
    files=bat=legalfiles.processtext.batchdealtext.Batchdealtext.files
    #文章标题和内容放进数据库
    for p,f in zip(os.listdir(data_file_path),files):
        Txt.objects.get_or_create(title=p)
        Txt.objects.update_or_create(title=p, defaults={"content":f})



if __name__ == '__main__':
    save_txt()
