from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
from monitor.tasks import get_camera_list
from login import models
from login.models import *
import json
from django.core import serializers
from json import *
import datetime

# login/views.py


# 第一个参数必须是request,该参数封装了用户请求的所有内容
def index(request):
    # render方法接收request作为第一个参数，要渲染的页面为第二个参数，以及需要传递给页面的数据字典作为第三个参数（可以为空）
    return render(request, 'login/index.html')


# 登录界面
def login(request):
    # 如果form通过POST方法发送数据
    if request.method == 'POST':
        # 接收request.POST参数构造form类的实例
        username = request.POST.get('username')
        password = request.POST.get('password')
        typeOfUser = request.POST.get('typeOfUser')

        # 若登录账号种类为学生
        if typeOfUser == 'student':
            try:
                student = Student.objects.get(id=username)
                if student.password == password:
                    user = json.dumps(student, default=lambda obj: obj.__dict__)  # 将学生序列化为JSON(str)
                    user = json.loads(user)   # 将学生反序列化为字典
                    request.session['user'] = user  # 将用户信息传入session，传入前需要序列化为JSON
                    return render(request, 'login/student-index.html')    # 跳转到学生主界面
            except Exception as e:  # 若捕获异常则停止执行
                print('Error:', e)

        # 若登录账号种类为教师
        if typeOfUser == 'teacher':
            try:
                teacher = Teacher.objects.get(id=username)
                if teacher.password == password:
                    user = json.dumps(teacher, default=lambda obj: obj.__dict__)  # 将教师序列化为JSON
                    user = json.loads(user)  # 将教师反序列化为字典
                    request.session['user'] = user  # 将序列化后的用户信息传入session
                    return render(request, 'login/teacher-index.html')  # 跳转到教师主界面
            except Exception as e:  # 若捕获异常则停止执行
                print('Error:', e)

        # 若登录账号种类为管理员
        if typeOfUser == 'admin':
            try:
                admin = Admin.objects.get(id=username)
                if admin.password == password:
                    user = json.dumps(admin, default=lambda obj: obj.__dict__)  # 将管理员序列化为JSON
                    user = json.loads(user)  # 将管理员反序列化为字典
                    request.session['user'] = user  # 将字典传入session
                    return render(request, 'login/admin-index.html')  # 跳转到教师主界面
            except Exception as e:  # 若捕获异常则停止执行
                print('Error:', e)

    return render(request, 'login/login.html')


# 注册页面
def register(request):
    # 如果form通过POST方法发送数据
    if request.method == 'POST':
        # 接受request.POST参数构造form类的实例
        username = request.POST.get('username')
        password = request.POST.get('password')
        typeOfUser = request.POST.get('typeOfUser')

        # 若登录账号种类为学生
        if typeOfUser == 'student':
            try:  # 若数据库已经有该学生的记录，则返回注册界面
                Student.objects.get(id=username)
                return render(request, 'login/register.html')
            except Exception as e:  # 若数据库没有该学生的记录，则增加然后返回登录界面
                Student.objects.create(id=username, password=password)
                return render(request, 'login/login.html')

        # 若注册账号种类为教师
        if typeOfUser == 'teacher':
            try:
                Teacher.objects.get(id=username)
                return render(request, 'login/register.html')
            except Exception as e:
                Teacher.objects.create(id=username, password=password)
                return render(request, 'login/login.html')

    return render(request, 'login/register.html')


def student_index(request):
    return render(request, 'login/student-index.html')


def welcome(request):
    return render(request, 'login/welcome.html')

