from haystack import indexes
from .models import Txt


#定义索引类,指定对于某个类的某些数据建立索引
class TxtIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    # 针对哪张表进行查询
    def get_model(self):
        return Txt

    # 针对哪些行进行查询
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
