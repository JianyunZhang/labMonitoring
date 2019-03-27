from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
from login import models

# Create your views here.

#第一个参数必须是request,该参数封装了用户请求的所有内容
def index(request):
    pass
    # render方法接收request作为第一个参数，要渲染的页面为第二个参数，以及需要传递给页面的数据字典作为第三个参数（可以为空）
    return render(request, 'login/index.html')

# login/views.py
def login(request):
    pass
    return render(request, 'login/login.html')

def register(request):
    pass
    return render(request, 'login/register.html')

def logout(request):
    pass
    return redirect('/index/')