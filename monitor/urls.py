from django.urls import path
# 需要先导入App中的views文件
from monitor import views

# 添加路由信息，重点是路由表达式和后面的视图函数
urlpatterns = [
    # 导入camera app路由路径
    path('control/', views.control),
    path('photo/', views.photo),
    path('detection/', views.detection),
    path('camera-edit/', views.camera_edit),
    path('photo-show/',  views.photo_show),
    path('detection-show/',  views.detection_show),
    path('admin-check-setting/', views.admin_check_setting),  # 管理员修改设定
    path('admin-list-camera/', views.admin_list_camera),    # 管理员查看摄像头列表
    path('admin-check-camera/', views.admin_check_camera),  # 管理员修改摄像头信息
    path('admin-list-photo/', views.admin_list_photo),  # 管理员查看照片列表
    path('admin-check-photo/', views.admin_check_photo),    # 管理员查看照片原图
    path('admin-check-photo-detection/', views.admin_check_photo_detection),  # 管理员查看对象检测结果
    path('admin-check-photo-prediction/', views.admin_check_photo_prediction),  # 管理员查看照片预测结果
    path('admin-detection-photo/', views.admin_detection_photo),  # 管理员手动执行物体检测操作
    path('admin-prediction-photo/', views.admin_prediction_photo),  # 管理员手动执行图像预测操作
]
