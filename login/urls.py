from django.urls import path
# 需要先导入App中的views文件
from login import views

# 添加路由信息，重点是路由表达式和后面的视图函数
urlpatterns = [
    # 导入login app路由路径
    path('', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('admin-home/', views.admin_home),  # 管理员功能页面
    path('admin-check-self/', views.admin_check_self),
    path('admin-welcome/', views.admin_welcome),

]
