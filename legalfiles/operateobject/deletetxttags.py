import os
import django


os.environ['DJANGO_SETTINGS_MODULE'] = 'filesprocess.settings'
django.setup()

from legalfiles.models import Txt,Tag

#这个就是业务层，一个个的功能，供表现层调用

def delete_txttags(tag):
    #拿到标签对象
    obj_tag = Tag.objects.filter(name=tag).first()
    if obj_tag != None:
        obj_tag.txt_set.clear()






    # obj_txt = Txt.objects.get(title='倪利刚与马北明合伙协议纠纷一审民事判决书.docx')
    # p=obj_txt.tags.all()





if __name__ == '__main__':
    delete_txttags('北京市')

