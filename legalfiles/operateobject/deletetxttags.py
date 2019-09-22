import os
import django


os.environ['DJANGO_SETTINGS_MODULE'] = 'filesprocess.settings'
django.setup()

from legalfiles.models import Txt,Tag
#这个就是业务层，一个个的功能，供表现层调用

def delete_txttags(request,tag,txt=' '):
    #删除全局标签，url的txt是空格
    if txt==' ':
        obj_tag = Tag.objects.filter(name=tag).first()
        if obj_tag != None:
            obj_tag.txt_set.clear()
    #删除特定文章的标签
    else:
        obj_tag = Tag.objects.filter(name=tag, users=request.user).first()
        obj_txt = Txt.objects.filter(title=txt, users=request.user).first()
        obj_txt.tags.remove(obj_tag)

        #看一个这个标签还有没有文章使用，没有就删掉
        if obj_tag.txt_set.all():
            pass
        else:
            Tag.objects.filter(name=obj_tag.name,users=request.user).delete()



if __name__ == '__main__':
    delete_txttags('北京市')

