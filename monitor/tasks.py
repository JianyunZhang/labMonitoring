from VideoCapture import Device
from cv2 import VideoCapture
from celery import shared_task
from labMonitoring.settings import BASE_DIR
from monitor.models import Camera, Photo, Detection
import os
import time


# 读取系统中摄像头总数，然后将摄像头信息写入数据库
@shared_task
def get_camera_list():
    # 获取接入系统的摄像头，并将信息存入数据库
    print('开始获取接入系统的摄像头：')
    total_camera_num = 0    # 摄像头计数器
    for num in range(0, 9):     # 该系统最多支持9个摄像头
        temp_camera = VideoCapture(num)     # 获取编号为num的摄像头
        res = (temp_camera.isOpened())      # 检测该摄像头能否开启
        temp_camera.release()   # 释放该摄像头
        if res:  # 若该摄像头可以正常开启
            try:  # 若数据库已经有该摄像头的记录，则跳过操作
                Camera.objects.get(id=total_camera_num)
            except Exception as e:  # 若数据库不含该摄像头的记录，则进行添加操作
                Camera.objects.create(id=total_camera_num)
            total_camera_num = total_camera_num + 1  # 摄像头计数器自增
    print('摄像头总数：', total_camera_num)

    # 获取摄像头列表
    camera_list = Camera.objects.all()
    if total_camera_num < len(camera_list):
        for num in range(total_camera_num-1, len(camera_list)-1):
            Camera.objects.filter(id=num).delete()


# 控制设置为启用的摄像头拍照
@shared_task
def photo_capture():
    # 设置摄像头拍照参数
    cam = Device(devnum=0, showVideoWindow=0)
    cam.setResolution(640, 480)
    while True:
        start_time = time.time()
        print('\n正在拍摄照片')
        # 拍摄照片，保存到指定目录
        dir = os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'photo', str(start_time)) + '.jpg'
        print(dir)
        cam.saveSnapshot(dir, timestamp=3, boldfont=1)


# 识别照片中的内容，将识别结果存储到指定路径
@shared_task
def photo_detection():
    return

