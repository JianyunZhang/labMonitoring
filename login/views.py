from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
from login import models

# login/views.py

# 第一个参数必须是request,该参数封装了用户请求的所有内容
def login(request):
    # render方法接收request作为第一个参数，要渲染的页面为第二个参数，以及需要传递给页面的数据字典作为第三个参数（可以为空）
    return render(request, 'login/login.html')

def register(request):
    return render(request, 'login/register.html')
