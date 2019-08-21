from legalfiles.models import Txt
import os
import legalfiles.processtext.batchdealtext
from config2 import data_file_path
#这个就是业务层，一个个的功能，供表现层调用,持久层不用你写


#保存文本功能，文本从工具函数来，不是前端来
def save_txt(request):
    #获得内容
    files=bat=legalfiles.processtext.batchdealtext.Batchdealtext.files
    #文章标题和内容放进数据库
    for title,content in zip(os.listdir(data_file_path),files):
        #没有该文章标题的文章对象则创建文章对象，有就不创建了
        Txt.objects.get_or_create(title=title, users=request.user)
        #有该文章标题的对象则更新里面的内容，没有就创建这个对象并且顺带content
        Txt.objects.update_or_create(title=title, defaults={"content":content}, users=request.user)



if __name__ == '__main__':
    save_txt()
