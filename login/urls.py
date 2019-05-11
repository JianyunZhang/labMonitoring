from django.urls import path
# 需要先导入App中的views文件
from login import views

# 添加路由信息，重点是路由表达式和后面的视图函数
urlpatterns = [
    # 导入login app路由路径
    path('', views.index),  # 系统首页
    path('document/', views.document),  # 文档展示界面
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
    path('admin-list-laboratory/', views.admin_list_laboratory),  # 管理员查看实验室列表
    path('admin-add-laboratory/', views.admin_add_laboratory),  # 管理员添加实验室
    path('admin-check-laboratory/', views.admin_check_laboratory),  # 管理员修改实验室
    path('admin-list-instrument/', views.admin_list_instrument),  # 管理员查看实验仪器列表
    path('admin-add-instrument/', views.admin_add_instrument),  # 管理员添加实验仪器
    path('admin-check-instrument/', views.admin_check_instrument),  # 管理员查看实验仪器
    path('admin-list-course/', views.admin_list_course),  # 管理员查看课程列表
    path('admin-list-select/', views.admin_list_select),  # 管理员查看选课列表
    path('teacher-home/', views.teacher_home),  # 教师功能页面
    path('teacher-check-self/', views.teacher_check_self),  # 教师查看个人信息
    path('teacher-change-password/', views.teacher_change_password),  # 教师修改账号密码
    path('teacher-welcome/', views.teacher_welcome),    # 教师欢迎界面
    path('teacher-list-course/', views.teacher_list_course),  # 教师查看课程列表
    path('teacher-add-course/', views.teacher_add_course),  # 教师新增课程
    path('teacher-check-course/', views.teacher_check_course),  # 教师查看已发布课程
    path('teacher-list-select/', views.teacher_list_select),  # 教师查看学生选课列表
    path('student-home/', views.student_home),  # 学生功能页面
    path('student-check-self/', views.student_check_self),  # 学生查看个人信息
    path('student-change-password/', views.student_change_password),  # 学生修改账号密码
    path('student-welcome/', views.student_welcome),  # 学生欢迎界面
    path('student-list-course/', views.student_list_course),  # 学生选课列表
]
