from django.db import models

# Create your models here.
class Txt(models.Model):
    # 文章的唯一ID
    txt_id = models.AutoField(primary_key=True)
    # 文章标题
    title = models.TextField()
    # 文章的主要内容
    content = models.TextField()

    def __str__(self):
        return self.title