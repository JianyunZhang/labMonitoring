from django.urls import path
# 需要先导入App中的views文件
from login import views

# 添加路由信息，重点是路由表达式和后面的视图函数
urlpatterns = [
    # 导入login app路由路径
    path('', views.index),  # 系统首页
    path('login/', views.login),  # 登录界面
    path('register/', views.register),  # 注册界面
    path('admin-home/', views.admin_home),  # 管理员功能页面
    path('admin-check-self/', views.admin_check_self),  # 管理员查看个人信息
    path('admin-change-password/', views.admin_change_password),  # 管理员修改账号密码
    path('admin-welcome/', views.admin_welcome),    # 管理员欢迎界面
    path('admin-list-student/', views.admin_list_student),  # 管理员查看学生列表
    path('admin-check-student/', views.admin_check_student),  # 管理员查看学生详情
    path('admin-list-teacher/', views.admin_list_teacher),  # 管理员查看教师列表
    path('admin-check-teacher/', views.admin_check_teacher),  # 管理员查看教师详情
    path('admin-list-admin/', views.admin_list_admin),  # 管理员查看管理员列表
    path('admin-check-admin/', views.admin_check_admin),  # 管理员查看管理员详情
    path('admin-add-admin/', views.admin_add_admin),  # 管理员添加管理员
]
