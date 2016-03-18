# coding: utf-8
from django.db import models
from django.utils import timezone
#管理列表
class manage(models.Model):
    name = models.CharField(verbose_name="名称",max_length=100,unique=True)
    url = models.URLField()
    ops_manage = models.CharField('属于运维', choices=(('0','yes'),('1','no')),max_length=1)

    def __unicode__(self):
        return self.name

class findpasswd(models.Model):
    key = models.CharField(verbose_name="找回密码KEY",max_length=150,unique=True)
    status = models.IntegerField(verbose_name="KEY状态",max_length=1,default=0)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    username = models.CharField(verbose_name="用户名", max_length=100)

