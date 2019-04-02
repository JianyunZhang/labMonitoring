from django.urls import path
# 需要先导入App中的views文件
from login import views

# 添加路由信息，重点是路由表达式和后面的视图函数
urlpatterns = [
    # 导入login app路由路径
    path('login/', views.login),
    path('register/', views.register),
    path('student-index/', views.student_index),
]
