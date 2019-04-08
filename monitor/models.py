# monitor/models.py
from django.db import models


# Create your models here.
class Camera(models.Model):  # 摄像头类
    id = models.CharField(primary_key=True, max_length=30)  # 序号
    name = models.CharField(max_length=30)  # 名称
    location = models.CharField(max_length=30)   # 地点


class Photo(models.Model):  # 照片类
    id = models.CharField(primary_key=True, max_length=30)  # id
    time = models.DateTimeField(auto_now=True)  # 拍摄时间
    location = models.CharField(max_length=30)  # 拍摄地点
    is_processed = models.BooleanField(default=False)   # 是否识别完成
    url = models.URLField   # URL地址


class Detection(models.Model):  # 识别后的照片类
    id = models.CharField(primary_key=True, max_length=30)  # id
    time = models.DateTimeField(auto_now=True)  # 拍摄时间
    location = models.CharField(max_length=30)  # 拍摄地点
    url = models.URLField  # URL地址
