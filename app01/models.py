from django.db import models

# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length=32,verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱')
    age = models.IntegerField(verbose_name='年龄')


class Role(models.Model):
    caption = models.CharField(max_length=32,verbose_name='角色名')