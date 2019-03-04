from django.db import models

# Create your models here.

class UserInfo(models.Model):
    #创建user，pwd两个字段，最大长度32，类型为char
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)