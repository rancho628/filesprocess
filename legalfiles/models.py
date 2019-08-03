from django.db import models

# Create your models here.
class Tag(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Txt(models.Model):
    # 文章的唯一ID
    txt_id = models.AutoField(primary_key=True)
    # 文章标题
    title = models.TextField()
    # 文章内容
    content = models.TextField()
    #文章标签，多对多
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
