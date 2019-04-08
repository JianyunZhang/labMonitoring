from django.urls import path
# 需要先导入App中的views文件
from monitor import views

# 添加路由信息，重点是路由表达式和后面的视图函数
urlpatterns = [
    # 导入camera app路由路径
    path('control/', views.control),
    path('photo/', views.photo),
    path('detection/', views.detection)
]