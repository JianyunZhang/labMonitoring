# login/models.py

from django.db import models

# Create your models here.
class Student(models.Model):    # 学生类
    id = models.CharField(primary_key=True, max_length=30)  # 学号
    password = models.CharField(max_length=30)  # 密码
    name = models.CharField(max_length=30)  # 姓名
    sex = models.CharField(max_length=30, choices=(('male', '男'), ('female', '女'), ), default='男')  # 性别
    email = models.EmailField(unique=True)  # 邮箱
    phone = models.CharField(max_length=30, unique=True)    # 电话号码
    school = models.CharField(max_length=30)    # 学院
    specialty = models.CharField(max_length=30)  # 专业
    class_no = models.CharField(max_length=30)  # 班级
    register_time = models.DateTimeField(auto_now_add=True)     # 注册时间

class Teacher(models.Model):    #教师类
    id = models.CharField(primary_key=True, max_length=30)  # 工号
    password = models.CharField(max_length=30)  # 密码
    name = models.CharField(max_length=30)  # 姓名
    sex = models.CharField(max_length=30, choices=(('male', '男'), ('female', '女'), ), default='男')  # 性别
    email = models.EmailField(unique=True)  # 邮箱
    phone = models.CharField(max_length=30, unique=True)     # 电话号码
    school = models.CharField(max_length=30)  # 学院
    department = models.CharField(max_length=30)  # 部门
    title = models.CharField(max_length=30)  # 职称
    register_time = models.DateTimeField(auto_now_add=True)  # 注册时间

class Admin(models.Model):    #管理员类
    id = models.CharField(primary_key=True, max_length=30)  # 账号
    password = models.CharField(max_length=30)  # 密码
    name = models.CharField(max_length=30)  # 姓名
    email = models.EmailField(unique=True)  # 邮箱
    phone = models.CharField(max_length=30, unique=True)     # 电话号码
    department = models.CharField(max_length=30)  # 部门