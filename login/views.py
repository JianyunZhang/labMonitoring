from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
from login import models

# Create your views here.

def index(request): #第一个参数必须是request,该参数封装了用户请求的所有内容
    pass
    return render(request, 'login/index.html')#render方法接收request作为第一个参数，要渲染的页面为第二个参数，以及需要传递给页面的数据字典作为第三个参数（可以为空）

# login/views.py

def login(request):
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())

def register(request):
    pass
    return render(request, 'login/register.html')

def logout(request):
    pass
    return redirect("/index/")