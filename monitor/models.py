# monitor/models.py
from django.db import models


# Create your models here.
class Camera(models.Model):  # 摄像头
    id = models.CharField(primary_key=True, max_length=30)  # id
    is_working = models.BooleanField(default=False)  # 是否启用
    name = models.CharField(max_length=30)  # 名称
    location = models.CharField(max_length=30)   # 地点
    photo_quality = models.IntegerField(default=100)  # 照片质量（0-100）


class Photo(models.Model):  # 拍摄照片
    id = models.AutoField(primary_key=True)  # id
    time = models.DateTimeField(auto_now=True)  # 拍摄时间
    camera_id = models.CharField(default='', max_length=30)  # 摄像头id
    camera_name = models.CharField(default='', max_length=30)  # 摄像头名称
    location = models.CharField(max_length=30)  # 拍摄地点
    is_detected = models.BooleanField(default=False)  # 是否完成对象检测
    url_detected = models.CharField(default='', max_length=200)  # 对象检测结果图片URL
    detection_model = models.CharField(default='', max_length=30)  # 对象检测使用的模型
    detection_speed = models.CharField(default='', max_length=30)   # 对象检测速度
    is_predicted = models.BooleanField(default=False)  # 是否完成图像预测
    list_predicted = models.CharField(default='', max_length=200)  # 图像预测结果（字符串列表）
    prediction_model = models.CharField(default='', max_length=30)  # 图像预测使用的模型
    prediction_speed = models.CharField(default='', max_length=30)  # 图像预测速度
    is_phone = models.BooleanField(default=False)  # 是否含有手机
    url = models.CharField(default='', max_length=200)   # URL地址


class Detection(models.Model):  # 识别结果
    id = models.CharField(primary_key=True, max_length=30)  # id
    time = models.DateTimeField(auto_now=True)  # 拍摄时间
    location = models.CharField(max_length=30)  # 拍摄地点
    is_phone = models.BooleanField(default=False)  # 图中是否含有手机
    url = models.CharField(default='', max_length=200)   # URL地址


class Setting(models.Model):  # 用户设置
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=30)  # 用户id
    user_name = models.CharField(max_length=30)  # 用户姓名
    is_auto_detecting = models.BooleanField(default=False)  # 自动对象检测是否开启
    is_auto_predicting = models.BooleanField(default=False)  # 自动图像预测是否开启
    detection_model = models.CharField(default='RetinaNet', max_length=30)  # 设置对象检测模型
    detection_speed = models.CharField(default='normal', max_length=30)  # 设置对象检测速度
    prediction_model = models.CharField(default='SqueezeNet', max_length=30)  # 设置图像预测模型
    prediction_speed = models.CharField(default='normal', max_length=30)  # 设置图像预测速度
