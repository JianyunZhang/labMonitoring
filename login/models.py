# login/models.py
from django.db import models


# Create your models here.
class Student(models.Model):    # 学生类
    id = models.CharField(primary_key=True, max_length=30)  # 学号
    password = models.CharField(max_length=30)  # 密码
    name = models.CharField(max_length=30)  # 姓名
    sex = models.CharField(max_length=30, choices=(('male', '男'), ('female', '女'), ))  # 性别
    email = models.EmailField()  # 邮箱
    phone = models.CharField(max_length=30)    # 电话号码
    school = models.CharField(max_length=30)    # 学院
    specialty = models.CharField(max_length=30)  # 专业
    class_no = models.CharField(max_length=30)  # 班级


class Teacher(models.Model):  # 教师类
    id = models.CharField(primary_key=True, max_length=30)  # 工号
    password = models.CharField(max_length=30)  # 密码
    name = models.CharField(max_length=30)  # 姓名
    sex = models.CharField(max_length=30, choices=(('male', '男'), ('female', '女'), ))  # 性别
    email = models.EmailField()  # 邮箱
    phone = models.CharField(max_length=30)  # 电话号码
    school = models.CharField(max_length=30)  # 学院
    department = models.CharField(max_length=30)  # 部门
    title = models.CharField(max_length=30)  # 职称


class Admin(models.Model):  # 管理员类
    id = models.CharField(primary_key=True, max_length=30)  # 账号
    password = models.CharField(max_length=30)  # 密码
    name = models.CharField(max_length=30)  # 姓名
    email = models.EmailField()  # 邮箱
    phone = models.CharField(max_length=30)  # 电话号码
    department = models.CharField(max_length=30)  # 部门


class Laboratory(models.Model):   # 实验室类
    id = models.AutoField(primary_key=True, auto_created=True)  # id
    name = models.CharField(max_length=30)  # 名称
    department = models.CharField(max_length=30)    # 所在单位
    location = models.CharField(max_length=30)  # 所在位置
    note = models.CharField(max_length=100)  # 说明
    photo_url = models.CharField(default='', max_length=200)   # 照片URL地址


class Instrument(models.Model):     # 仪器类
    id = models.AutoField(primary_key=True, auto_created=True)  # id
    laboratory_id = models.CharField(max_length=30)    # 所属实验室id
    laboratory_name = models.CharField(max_length=30)   # 所属实验室名称
    name = models.CharField(max_length=30)  # 名称
    category = models.CharField(max_length=30)  # 类别
    note = models.CharField(max_length=100)  # 说明
    date = models.CharField(max_length=100)  # 投入使用时间
    photo_url = models.CharField(default='', max_length=200)   # 照片URL地址


class Course(models.Model):  # 开设实验课程类
    id = models.AutoField(primary_key=True, auto_created=True)  # 课程id
    name = models.CharField(max_length=30)  # 课程名
    teacher_id = models.CharField(max_length=30)  # 教师id
    teacher_name = models.CharField(max_length=30)   # 教师名
    laboratory_id = models.CharField(max_length=30)    # 实验室id
    laboratory_name = models.CharField(max_length=30)   # 实验室名称
    location = models.CharField(max_length=30)  # 上课地址
    note = models.CharField(max_length=100)  # 课程说明
    add_time = models.DateTimeField(auto_now=True)  # 加入时间
    file_url = models.CharField(default='', max_length=200)  # 教学大纲URL地址


class Select(models.Model):  # 学生选课类
    id = models.AutoField(primary_key=True, auto_created=True)  # 选课号
    student_id = models.CharField(max_length=30)  # 学生id
    student_name = models.CharField(max_length=30)  # 学生姓名
    course_id = models.CharField(max_length=30)  # 课程id
    course_name = models.CharField(max_length=30)  # 课程名
    teacher_id = models.CharField(max_length=30)  # 教师id
    teacher_name = models.CharField(max_length=30)  # 教师姓名
    select_time = models.DateTimeField(auto_now=True)   # 选课操作时间
    score = models.CharField(max_length=10)  # 课程得分


class Assignment(models.Model):  # 课程作业类
    id = models.AutoField(primary_key=True, auto_created=True)  # 选课号
    student_id = models.CharField(max_length=30)  # 学生id
    student_name = models.CharField(max_length=30)  # 学生姓名
    course_id = models.CharField(max_length=30)  # 课程id
    course_name = models.CharField(max_length=30)  # 课程名
    teacher_id = models.CharField(max_length=30)  # 教师id
    teacher_name = models.CharField(max_length=30)  # 教师姓名
    title = models.CharField(max_length=30)  # 作业标题
    put_time = models.DateTimeField(auto_now=True)  # 作业下发时间
    add_time = models.DateTimeField  # 作业提交时间
    file_url = models.CharField(default='', max_length=200)  # 提交内容URL地址
    score = models.CharField(max_length=10)  # 得分
