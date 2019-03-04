from django.shortcuts import render
from login import models  # 导入models文件

# Create your views here.


def index(request): #第一个参数必须是request,该参数封装了用户请求的所有内容

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 将数据保存到数据库
        models.UserInfo.objects.create(user=username, pwd=password)

    # 从数据库中读取所有数据，注意缩进
    user_list = models.UserInfo.objects.all()
    # return HttpResponse('Hello World!')    #不能直接返回字符串，要使用HttpResponse类封装才能被HTTP协议识别
    return render(request, 'index.html', {'data': user_list})#render方法使用数据字典和请求元数据，渲染一个指定的HTML模板。其众多数据中，第一个参数必须是request第二个是模板
    #将用户列表作为上下文参数供render渲染index页面