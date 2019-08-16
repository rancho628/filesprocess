#coding:utf-8

from django.db import models
from django.urls import reverse
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class Tag(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)

    class Meta(AbstractUser.Meta):
        pass


class Txt(models.Model):
    # 文章的唯一ID
    txt_id = models.AutoField(primary_key=True)
    # 文章标题
    title = models.TextField()
    # 文章内容
    content = models.TextField()
    #文章标签，多对多
    tags = models.ManyToManyField(Tag, blank=True)
    users = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('legalfiles:detail', kwargs={'txt_id': self.txt_id})








