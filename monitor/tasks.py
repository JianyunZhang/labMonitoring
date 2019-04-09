from VideoCapture import Device
from cv2 import VideoCapture
from celery import shared_task
from labMonitoring.settings import BASE_DIR
import os
import time


# 读取系统中摄像头总数，然后将摄像头信息写入数据库
@shared_task
def get_camera_list():
    print('开始获取接入系统的摄像头：')
    total_camera_num = 0
    for num in range(0, 99):
        temp_camera = VideoCapture(num)
        res = (temp_camera.isOpened())
        temp_camera.release()
        if res:
            total_camera_num = total_camera_num + 1
    print('摄像头总数：', total_camera_num)


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

