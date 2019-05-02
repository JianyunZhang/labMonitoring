from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.contrib import auth
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
    if request.method == 'GET':
        return render(request, 'login/index.html')


# 登录界面login/login.html
def login(request):
    # 如果通过GET方法请求该URL
    if request.method == 'GET':
        return render(request, 'login/login.html')
    # 如果form通过POST方法发送数据
    elif request.method == 'POST':
        # 接收request.POST参数构造form类的实例
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('typeOfUser')  # 接收的用户种类

        # 若登录账号种类为学生
        if user_type == 'student':
            try:
                student = Student.objects.get(id=username)
                if student.password == password:    # 如果账号密码正确
                    user = json.dumps(student, default=lambda obj: obj.__dict__)  # 将学生序列化为JSON(str)
                    user = json.loads(user)   # 将学生反序列化为字典
                    request.session['user'] = user  # 将用户信息传入session，传入前需要序列化为JSON
                    return render(request, 'login/student-home.html')    # 跳转到学生主界面
            except Exception as e:  # 若捕获异常则停止执行
                print('Error:', e)

        # 若登录账号种类为教师
        if user_type == 'teacher':
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
        if user_type == 'admin':
            try:
                admin = Admin.objects.get(id=username)
                if admin.password == password:
                    admin = json.dumps(admin, default=lambda obj: obj.__dict__)  # 将管理员序列化为JSON
                    admin = json.loads(admin)  # 将管理员反序列化为字典
                    request.session['admin'] = admin  # 将字典传入session
                    return render(request, 'login/admin-home.html')  # 跳转到教师主界面
            except Exception as e:  # 若捕获异常则停止执行
                print('Error:', e)


# 注册页面login/register.html
def register(request):
    # 如果通过GET方法请求该URL
    if request.method == 'GET':
        return render(request, 'login/register.html')
    # 如果form通过POST方法发送数据
    elif request.method == 'POST':
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
                print('该教师账号已存在，无法重新注册！')
                return render(request, 'login/register.html')
            except Exception as e:
                Teacher.objects.create(id=username, password=password)
                print('教师账号注册成功！')
                return render(request, 'login/login.html')


# 管理员功能页面login/admin-home.html
def admin_home(request):
    if request.method == 'GET':
        return render(request, 'login/admin-home.html')


# 管理员查看个人账户信息页面login/admin-check-self.html
# @csrf_exempt
def admin_check_self(request):
    if request.method == 'GET':
        return render(request, 'login/admin-check-self.html')
    elif request.method == 'POST':
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        admin = request.POST.get('admin')
        # 将管理员反序列化为字典
        admin = json.loads(admin)
        print('收到上传的内容：', admin)
        # 将上传结果保存到数据库
        try:
            Admin.objects.filter(id=admin['id']).update(password=admin['password'], name=admin['name'], email=admin['email'], phone=admin['phone'], department=admin['department'])
            print('管理员个人信息修改成功！id=', admin['id'])
            request.session['admin'] = admin  # 将修改后的admin字典传入session
        except Exception as e:
            print('管理员个人信息修改失败！id=', admin['id'])
            print(e)
        return HttpResponse()


# 管理员修改账号密码页面login/admin-change-password.html
# @csrf_exempt
def admin_change_password(request):
    if request.method == 'GET':
        return render(request, 'login/admin-change-password.html')
    elif request.method == 'POST':
        # 获取AJAX上传的数据，获取对象为JSON
        password = request.POST.get('password')
        # 将密码反序列化为字典
        password = json.loads(password)
        print('收到上传的内容：', password)

        # 从session中读出目前的用户信息
        admin = request.session['admin']
        # 校验密码
        if admin['password'] == password['pre_password']:    # 若原密码匹配，将上传结果保存到数据库
            try:
                Admin.objects.filter(id=admin['id']).update(password=password['new_password'])
                admin['password'] = password['new_password']
                print('管理员密码修改成功！id =', admin['id'])
                request.session['admin'] = admin  # 将修改后的admin字典传入session
                return JsonResponse({"msg": "success"})
            except Exception as e:
                print('管理员密码修改失败！id =', admin['id'])
                print(e)
                # 如果这样返回，两边都不需要进行json的序列化与反序列化，ajax接受的直接是一个对象
                return JsonResponse({"msg": "failed"})
        elif admin['password'] != password['pre_password']:  # 若原密码不匹配，则修改失败
            # 传文本给前端Ajax
            print('密码不匹配，修改失败！')
            return JsonResponse({"msg": "failed"})


# 管理员欢迎页面login/admin-welcome.html
def admin_welcome(request):
    if request.method == 'GET':
        return render(request, 'login/admin-welcome.html')


# 管理员查看学生列表login/admin-list-student.html
def admin_list_student(request):
    if request.method == 'GET':
        if 'search' in request.GET:
            # 查询操作，取出搜索框输入的id
            student_id = request.GET.get('student_id')
            try:
                # 从数据库中模糊查询，查出学生列表，按照班级号排序
                student_list = Student.objects.filter(id__contains=student_id).order_by('class_no')
                print('查找结果：', student_list)
            except Exception as e:
                print('没有查询到结果！id =', student_id)
                print(e)
                student_list = []

            # 分页操作
            # 将数据按照规定每页显示 5 条, 进行分割
            paginator = Paginator(student_list, 5)
            page = request.GET.get('page')
            try:
                student_list = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                student_list = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            # 将结果返回到页面
            return render(request, 'login/admin-list-student.html', {"student_list": student_list})
        else:
            # 从数据库中查询学生列表
            student_list = Student.objects.all().order_by('class_no')
            print('当前学生列表：', student_list)
            # 分页操作
            # 将数据按照规定每页显示 5 条, 进行分割
            paginator = Paginator(student_list, 5)
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page')
            try:
                student_list = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                student_list = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            # 将结果返回到页面
            return render(request, 'login/admin-list-student.html', {"student_list": student_list})
    elif request.method == 'POST':  # 删除学生操作
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        student_id = request.POST.get('id')
        # 删除数据库中的记录
        Student.objects.filter(id=student_id).delete()
        print('删除学生成功！id =', student_id)
        return HttpResponse('学生信息删除成功')


# 管理员查看学生详情login/admin-check-student.html
def admin_check_student(request):
    if request.method == 'GET':
        student_id = request.GET.get('id')
        # 从数据库中查询该学生的数据
        student = Student.objects.get(id=student_id)
        # 将学生类转换为字典
        student_dict = json.loads(json.dumps(student, default=lambda obj: obj.__dict__))
        # 打印选中的学生数据
        print(student_dict)
        return render(request, 'login/admin-check-student.html', {'student_dict': student_dict})
    elif request.method == 'POST':
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        student = request.POST.get('student')
        # 将学生信息反序列化为字典
        student = json.loads(student)
        print('收到上传的内容：', student)
        # 将上传结果保存到数据库
        try:
            Student.objects.filter(id=student['id']).update(name=student['name'], email=student['email'], phone=student['phone'], school=student['school'], specialty=student['specialty'], class_no=student['class_no'])
            print('学生信息修改成功！id=', student['id'])
        except Exception as e:
            print('学生信息修改失败！id=', student['id'])
            print(e)
        return HttpResponse()


def student_home(request):
    return render(request, 'login/student-home.html')

