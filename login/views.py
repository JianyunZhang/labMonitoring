from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from labMonitoring.settings import BASE_DIR
from django.contrib import auth
from django.shortcuts import redirect
from django import forms
from monitor.tasks import get_camera_list
from login import models
from captcha.fields import CaptchaField
from .forms import CaptchaForm
from login.models import *

import json
import os
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
    # 如果通过GET方法请求该URL,将界面返回
    if request.method == 'GET':
        return render(request, 'login/login.html')
    # 如果form通过POST方法发送数据
    elif request.method == 'POST':
        # 获取AJAX上传的数据，获取对象为JSON
        user = request.POST.get('user')
        # 将密码反序列化为字典
        user = json.loads(user)

        username = user['username']
        password = user['password']
        user_type = user['typeOfUser']  # 接收的用户种类
        print('收到上传内容：', username, password, user_type)

        # 若登录账号种类为学生
        if user_type == 'student':
            try:
                student = Student.objects.get(id=username)
                if student.password == password:    # 如果账号密码正确
                    student = json.dumps(student, default=lambda obj: obj.__dict__)  # 将学生序列化为JSON(str)
                    student = json.loads(student)   # 将学生反序列化为字典
                    request.session['student'] = student  # 将用户信息传入session，传入前需要序列化为JSON
                    return JsonResponse({"msg": "student"})    # 传值给AJAX，跳转到学生主界面
                else:   # 若密码不匹配
                    return JsonResponse({"msg": "failed"})
            except Exception as e:  # 若捕获异常则停止执行,返回false
                print('Error:', e)
                return JsonResponse({"msg": "failed"})

        # 若登录账号种类为教师
        if user_type == 'teacher':
            try:
                teacher = Teacher.objects.get(id=username)
                if teacher.password == password:
                    teacher = json.dumps(teacher, default=lambda obj: obj.__dict__)  # 将教师序列化为JSON
                    teacher = json.loads(teacher)  # 将教师反序列化为字典
                    request.session['teacher'] = teacher  # 将序列化后的用户信息传入session
                    return JsonResponse({"msg": "teacher"})  # 传值给AJAX，跳转到教师主界面
                else:   # 若密码不匹配
                    return JsonResponse({"msg": "failed"})
            except Exception as e:  # 若捕获异常则停止执行
                print('Error:', e)
                return JsonResponse({"msg": "failed"})

        # 若登录账号种类为管理员
        if user_type == 'admin':
            try:
                admin = Admin.objects.get(id=username)
                if admin.password == password:  # 若密码匹配
                    admin = json.dumps(admin, default=lambda obj: obj.__dict__)  # 将管理员序列化为JSON
                    admin = json.loads(admin)  # 将管理员反序列化为字典
                    request.session['admin'] = admin  # 将字典传入session
                    return JsonResponse({'msg': 'admin'})  # 传值给AJAX，跳转到管理员页面
                else:   # 若密码不匹配
                    return JsonResponse({"msg": "failed"})
            except Exception as e:  # 若捕获异常则停止执行
                print('Error:', e)
                return JsonResponse({"msg": "failed"})


# 注册页面login/register.html
def register(request):
    # 如果通过GET方法请求该URL
    if request.method == 'GET':
        return render(request, 'login/register.html')
    # 如果form通过POST方法发送数据
    elif request.method == 'POST':
        # 获取AJAX上传的数据，获取对象为JSON
        user = request.POST.get('user')
        # 将密码反序列化为字典
        user = json.loads(user)

        username = user['username']
        password = user['password']
        user_type = user['typeOfUser']  # 接收的用户种类

        # 若登录账号种类为学生
        if user_type == 'student':
            try:  # 若数据库已经有该学生的记录，则返回注册界面
                student = Student.objects.get(id=username)
                if(student is not None):
                    print('该学生账号已存在，无法重新注册！')
                    return JsonResponse({"msg": "failed"})
            except Exception as e:  # 若数据库没有该学生的记录，则增加然后返回登录界面
                print(e)
                print('创建学生账号')
                Student.objects.create(id=username, password=password)
                return JsonResponse({"msg": "success"})

        # 若注册账号种类为教师
        if user_type == 'teacher':
            try:
                teacher = Teacher.objects.get(id=username)
                if (teacher is not None):
                    print('该教师账号已存在，无法重新注册！')
                    return JsonResponse({"msg": "failed"})
            except Exception as e:
                print(e)
                print('创建教师账号')
                Teacher.objects.create(id=username, password=password)
                return JsonResponse({"msg": "success"})


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
            # 查询操作，取出搜索框输入的id，姓名
            student_id = request.GET.get('student_id')
            student_class_no = request.GET.get('student_class_no')
            student_name = request.GET.get('student_name')
            try:
                # 从数据库中模糊查询，查出学生列表，按照班级号排序
                student_list = Student.objects.filter(id__contains=student_id, class_no__contains=student_class_no, name__contains=student_name).order_by('class_no')
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


# 管理员查看教师列表login/admin-list-teacher.html
def admin_list_teacher(request):
    if request.method == 'GET':
        if 'search' in request.GET:
            # 查询操作，取出搜索框输入的id，姓名
            teacher_id = request.GET.get('teacher_id')
            teacher_name = request.GET.get('teacher_name')
            try:
                # 从数据库中模糊查询，查出教师列表，按照班级号排序
                teacher_list = Teacher.objects.filter(id__contains=teacher_id, name__contains=teacher_name).order_by('school')
                print('查找结果：', teacher_list)
            except Exception as e:
                print('没有查询到结果！id =', teacher_id)
                print(e)
                teacher_list = []

            # 分页操作
            # 将数据按照规定每页显示 5 条, 进行分割
            paginator = Paginator(teacher_list, 5)
            page = request.GET.get('page')
            try:
                teacher_list = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                teacher_list = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            # 将结果返回到页面
            return render(request, 'login/admin-list-teacher.html', {"teacher_list": teacher_list})
        else:
            # 从数据库中查询教师列表
            teacher_list = Teacher.objects.all().order_by('school')
            print('当前教师列表：', teacher_list)
            # 分页操作
            # 将数据按照规定每页显示 5 条, 进行分割
            paginator = Paginator(teacher_list, 5)
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page')
            try:
                teacher_list = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                teacher_list = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            # 将结果返回到页面
            return render(request, 'login/admin-list-teacher.html', {"teacher_list": teacher_list})
    elif request.method == 'POST':  # 删除教师操作
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        teacher_id = request.POST.get('id')
        # 删除数据库中的记录
        Teacher.objects.filter(id=teacher_id).delete()
        print('删除教师成功！id =', teacher_id)
        return HttpResponse('教师信息删除成功')


# 管理员查看教师详情login/admin-check-teacher.html
def admin_check_teacher(request):
    if request.method == 'GET':
        teacher_id = request.GET.get('id')
        # 从数据库中查询该学生的数据
        teacher = Teacher.objects.get(id=teacher_id)
        # 将教师类转换为字典
        teacher_dict = json.loads(json.dumps(teacher, default=lambda obj: obj.__dict__))
        # 打印选中的教师数据
        print(teacher_dict)
        return render(request, 'login/admin-check-teacher.html', {'teacher_dict': teacher_dict})
    elif request.method == 'POST':
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        teacher = request.POST.get('teacher')
        # 将教师信息反序列化为字典
        teacher = json.loads(teacher)
        print('收到上传的内容：', teacher)
        # 将上传结果保存到数据库
        try:
            Teacher.objects.filter(id=teacher['id']).update(name=teacher['name'], email=teacher['email'], phone=teacher['phone'], school=teacher['school'], department=teacher['department'], title=teacher['title'])
            print('教师信息修改成功！id=', teacher['id'])
        except Exception as e:
            print('教师信息修改失败！id=', teacher['id'])
            print(e)
        return HttpResponse()


# 管理员查看管理员列表login/admin-list-admin.html
def admin_list_admin(request):
    if request.method == 'GET':
        if 'search' in request.GET:
            # 查询操作，取出搜索框输入的id，姓名
            admin_id = request.GET.get('admin_id')
            admin_name = request.GET.get('admin_name')
            try:
                # 从数据库中模糊查询，查出学生列表，按照班级号排序
                admin_list = Admin.objects.filter(id__contains=admin_id, name__contains=admin_name).order_by('department')
                print('查找结果：', admin_list)
            except Exception as e:
                print('没有查询到结果！id =', admin_id)
                print(e)
                admin_list = []

            # 分页操作
            # 将数据按照规定每页显示 5 条, 进行分割
            paginator = Paginator(admin_list, 5)
            page = request.GET.get('page')
            try:
                admin_list = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                admin_list = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            # 将结果返回到页面
            return render(request, 'login/admin-list-admin.html', {"admin_list": admin_list})
        else:
            # 从数据库中查询教师列表
            admin_list = Admin.objects.all().order_by('department')
            print('当前管理员列表：', admin_list)
            # 分页操作
            # 将数据按照规定每页显示 5 条, 进行分割
            paginator = Paginator(admin_list, 5)
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page')
            try:
                admin_list = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                admin_list = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            # 将结果返回到页面
            return render(request, 'login/admin-list-admin.html', {"admin_list": admin_list})


# 管理员查看管理员详情login/admin-check-admin.html
def admin_check_admin(request):
    if request.method == 'GET':
        admin_id = request.GET.get('id')
        # 从数据库中查询该管理员的数据
        admin = Admin.objects.get(id=admin_id)
        # 将管理员类转换为字典
        admin_dict = json.loads(json.dumps(admin, default=lambda obj: obj.__dict__))
        # 打印选中的管理员数据
        print(admin_dict)
        return render(request, 'login/admin-check-admin.html', {'admin_dict': admin_dict})


# 管理员添加管理员login/admin-add-admin.html
def admin_add_admin(request):
    if request.method == 'GET':
        return render(request, 'login/admin-add-admin.html')
    if request.method == 'POST':    # 接收AJAX响应，添加管理员账号
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        admin = request.POST.get('admin')
        # 将管理员反序列化为字典
        admin = json.loads(admin)
        print('收到上传的内容：', admin)
        # 将上传结果保存到数据库
        try:
            Admin.objects.create(id=admin['id'], password=admin['password'], name=admin['name'], email=admin['email'], phone=admin['phone'], department=admin['department'])
            print('管理员账号创建成功！id =', admin['id'])
            return JsonResponse({"msg": "success"})
        except Exception as e:
            print('管理员账号创建失败！id =', admin['id'])
            print(e)
        return JsonResponse({"msg": "failed"})


# 管理员查看实验室列表login/admin-list-laboratory.html
def admin_list_laboratory(request):
    if request.method == 'GET':
        if 'search' in request.GET:
            # 查询操作，取出搜索框输入的名称，单位
            laboratory_name = request.GET.get('laboratory_name')
            laboratory_department = request.GET.get('laboratory_department')
            try:
                # 从数据库中模糊查询，查出实验室列表，按照序号排序
                laboratory_list = Laboratory.objects.filter(name__contains=laboratory_name, department__contains=laboratory_department).order_by('-id')
                print('查找结果：', laboratory_list)
            except Exception as e:
                print('没有查询到结果！name =', laboratory_name)
                print(e)
                laboratory_list = []

            # 分页操作
            # 将数据按照规定每页显示 5 条, 进行分割
            paginator = Paginator(laboratory_list, 5)
            page = request.GET.get('page')
            try:
                laboratory_list = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                laboratory_list = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            # 将结果返回到页面
            return render(request, 'login/admin-list-laboratory.html', {"laboratory_list": laboratory_list})
        else:
            # 从数据库中查询实验室列表
            laboratory_list = Laboratory.objects.all().order_by('-id')
            print('当前实验室列表：', laboratory_list)
            # 分页操作
            # 将数据按照规定每页显示 5 条, 进行分割
            paginator = Paginator(laboratory_list, 5)
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page')
            try:
                laboratory_list = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                laboratory_list = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            # 将结果返回到页面
            return render(request, 'login/admin-list-laboratory.html', {"laboratory_list": laboratory_list})
    elif request.method == 'POST':  # 删除教师操作
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        laboratory_id = request.POST.get('id')
        # 删除数据库中的记录
        Laboratory.objects.filter(id=laboratory_id).delete()
        print('删除实验室成功！id =', laboratory_id)
        return HttpResponse('实验室信息删除成功')


# 管理员添加实验室login/admin-add-laboratory.html
def admin_add_laboratory(request):
    if request.method == 'GET':
        return render(request, 'login/admin-add-laboratory.html')
    if request.method == 'POST':    # 接收AJAX响应，添加实验室
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        name = request.POST.get("name")
        department = request.POST.get("department")
        location = request.POST.get('location')
        note = request.POST.get('note')
        # 将上传的数据创建字典
        laboratory = {'name': name, 'department': department, 'location': location, 'note': note, 'photo_url': ''}
        # 获取上传的文件
        file = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None

        print('收到上传的内容：', laboratory)
        # 获取当前时间
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        # 将上传的文件保存到服务器本地
        url = os.path.join(BASE_DIR, 'login', 'static', 'login', 'laboratory_photo', laboratory['name'] + '-' + now_time + '.jpg')
        print('照片保存路径：', url)
        # 将文件写入指定位置
        if not file:  # 如果没有接收到文件
            print('没有接收到照片！')
            return JsonResponse({"msg": "failed"})
        destination = open(url, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in file.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        print('照片保存成功！')

        # 设置照片访问路径
        substr = os.path.join(BASE_DIR, 'login')
        url = url.replace(substr, '')  # 替换子串,形成照片访问路径
        laboratory['photo_url'] = url
        print('照片访问路径：', url)

        # 将信息存入数据库
        try:
            Laboratory.objects.create(name=laboratory['name'], department=laboratory['department'], location=laboratory['location'], note=laboratory['note'], photo_url=laboratory['photo_url'])
            print('实验室创建成功！name =', laboratory['name'])
            return JsonResponse({"msg": "success"})
        except Exception as e:
            print('实验室创建失败！name =', laboratory['name'])
            print(e)
        return JsonResponse({"msg": "failed"})


# 管理员查看实验室详情login/admin-check-laboratory.html
def admin_check_laboratory(request):
    if request.method == 'GET':
        laboratory_id = request.GET.get('id')
        # 从数据库中查询该实验室的数据
        laboratory = Laboratory.objects.get(id=laboratory_id)
        # 将实验室类转换为字典
        laboratory_dict = json.loads(json.dumps(laboratory, default=lambda obj: obj.__dict__))
        # 打印选中的实验室数据
        print(laboratory_dict)
        return render(request, 'login/admin-check-laboratory.html', {'laboratory_dict': laboratory_dict})
    elif request.method == 'POST':
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        id = request.POST.get("id")
        name = request.POST.get("name")
        department = request.POST.get("department")
        location = request.POST.get('location')
        note = request.POST.get('note')
        # 将上传的数据创建字典
        laboratory = {'id': id, 'name': name, 'department': department, 'location': location, 'note': note, 'photo_url': ''}
        # 获取上传的文件
        file = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        print('收到上传的内容：', laboratory)

        # 获取当前时间
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        # 将上传的文件保存到服务器本地
        url = os.path.join(BASE_DIR, 'login', 'static', 'login', 'laboratory_photo', laboratory['name'] + '-' + now_time + '.jpg')
        print('照片保存路径：', url)
        # 将文件写入指定位置
        if not file:  # 如果没有接收到文件
            print('没有接收到照片！')
            Laboratory.objects.filter(id=laboratory['id']).update(name=laboratory['name'], department=laboratory['department'], location=laboratory['location'], note=laboratory['note'])
            return JsonResponse({"msg": "success"})
        destination = open(url, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in file.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        print('照片保存成功！')

        # 设置照片访问路径
        substr = os.path.join(BASE_DIR, 'login')
        url = url.replace(substr, '')  # 替换子串,形成照片访问路径
        laboratory['photo_url'] = url
        print('照片访问路径：', url)

        # 将信息存入数据库
        try:
            Laboratory.objects.filter(id=laboratory['id']).update(name=laboratory['name'], department=laboratory['department'], location=laboratory['location'], note=laboratory['note'], photo_url=laboratory['photo_url'])
            print('实验室修改成功！name =', laboratory['name'])
            return JsonResponse({"msg": "success"})
        except Exception as e:
            print('实验室创建失败！name =', laboratory['name'])
            print(e)
            return JsonResponse({"msg": "failed"})


# 管理员查看实验设备列表login/admin-list-instrument.html
def admin_list_instrument(request):
    if request.method == 'GET':
        if 'search' in request.GET:
            # 查询操作，取出搜索框输入的名称，单位
            instrument_name = request.GET.get('instrument_name')
            instrument_laboratory_name = request.GET.get('instrument_laboratory_name')
            try:
                # 从数据库中模糊查询，查出实验室列表，按照序号排序
                instrument_list = Instrument.objects.filter(name__contains=instrument_name, laboratory_name__contains=instrument_laboratory_name).order_by('-id')
                print('查找结果：', instrument_list)
            except Exception as e:
                print('没有查询到结果！name =', instrument_name)
                print(e)
                instrument_list = []

            # 分页操作
            # 将数据按照规定每页显示 5 条, 进行分割
            paginator = Paginator(instrument_list, 5)
            page = request.GET.get('page')
            try:
                instrument_list = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                instrument_list = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            # 将结果返回到页面
            return render(request, 'login/admin-list-instrument.html', {"instrument_list": instrument_list})
        else:
            # 从数据库中查询实验设备列表
            instrument_list = Instrument.objects.all().order_by('-id')
            print('当前实验设备列表：', instrument_list)
            # 分页操作
            # 将数据按照规定每页显示 5 条, 进行分割
            paginator = Paginator(instrument_list, 5)
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page')
            try:
                instrument_list = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                instrument_list = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            # 将结果返回到页面
            return render(request, 'login/admin-list-instrument.html', {"instrument_list": instrument_list})
    elif request.method == 'POST':  # 删除教师操作
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        instrument_id = request.POST.get('id')
        # 删除数据库中的记录
        Instrument.objects.filter(id=instrument_id).delete()
        print('删除实验设备成功！id =', instrument_id)
        return HttpResponse('实验设备删除成功')


# 管理员添加实验设备login/admin-add-instrument.html
def admin_add_instrument(request):
    if request.method == 'GET':
        # 从数据库中查出实验室列表，返回给前端页面
        laboratory_list = Laboratory.objects.all()
        return render(request, 'login/admin-add-instrument.html', {'laboratory_list': laboratory_list})
    if request.method == 'POST':    # 接收AJAX响应，添加实验设备
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        name = request.POST.get("name")
        laboratory_name = request.POST.get("laboratory_name")
        laboratory_id = Laboratory.objects.filter(name=laboratory_name)[0].id
        category = request.POST.get("category")
        note = request.POST.get('note')
        date = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')

        # 将上传的数据创建字典
        instrument = {'laboratory_id': laboratory_id, 'laboratory_name': laboratory_name, 'name': name, 'category': category, 'note': note, 'date': date, 'photo_url': ''}
        # 获取上传的文件
        file = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None

        print('收到上传的内容：', instrument)
        # 获取当前时间
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        # 将上传的文件保存到服务器本地
        url = os.path.join(BASE_DIR, 'login', 'static', 'login', 'instrument_photo', instrument['name'] + '-' + now_time + '.jpg')
        print('照片保存路径：', url)
        # 将文件写入指定位置
        if not file:  # 如果没有接收到文件
            print('没有接收到照片！')
            return JsonResponse({"msg": "failed"})
        destination = open(url, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in file.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        print('照片保存成功！')

        # 设置照片访问路径
        substr = os.path.join(BASE_DIR, 'login')
        url = url.replace(substr, '')  # 替换子串,形成照片访问路径
        instrument['photo_url'] = url
        print('照片访问路径：', url)

        # 将信息存入数据库
        try:
            Instrument.objects.create(laboratory_id=instrument['laboratory_id'], laboratory_name=instrument['laboratory_name'], name=instrument['name'], category=instrument['category'], note=instrument['note'], date=instrument['date'], photo_url=instrument['photo_url'])
            print('实验设备创建成功！name =', instrument['name'])
            return JsonResponse({"msg": "success"})
        except Exception as e:
            print('实验设备创建失败！name =', instrument['name'])
            print(e)
        return JsonResponse({"msg": "failed"})


def student_home(request):
    return render(request, 'login/student-home.html')

