from VideoCapture import Device
from cv2 import VideoCapture
from celery import shared_task
from labMonitoring.settings import BASE_DIR
from imageai.Detection import ObjectDetection
from monitor.models import Camera, Photo, Detection
import os
import time
import datetime


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
                print(e)
                Camera.objects.create(id=total_camera_num)
            total_camera_num = total_camera_num + 1  # 摄像头计数器自增
    print('摄像头总数：', total_camera_num)

    # 获取摄像头列表
    camera_list = Camera.objects.all()
    if total_camera_num < len(camera_list):
        for num in range(total_camera_num-1, len(camera_list)-1):
            Camera.objects.filter(id=num).delete()


# 指定摄像头拍照并将照片存入数据库
@shared_task
def photo_capture_by_id(camera_id):
    # 从数据库中获取摄像头列表
    camera_list = list(Camera.objects.all().order_by('id'))
    # 检查摄像头列表中相机的状态
    for camera in camera_list:
        # 如果工作状况设置为是，则进行拍照操作
        if camera.id is camera_id:
            print('当前拍照的摄像头为:', camera)
            # 设置摄像头拍照参数
            cam = Device(devnum=int(camera.id), showVideoWindow=0)
            cam.setResolution(640, 480)
            # 获取当前时间
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            print('\n正在拍摄照片')
            # 拍摄照片，保存到指定目录
            url = os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'photo', 'cam' + camera.id + '-' + now_time + '.jpg')
            print('摄像头id=', camera.id, '照片存储路径', url)
            cam.saveSnapshot(url, timestamp=3, boldfont=1, quality=50)
            # 将照片信息存入数据库
            Photo.objects.create(time=now_time, camera_id=camera.id, location=camera.location, is_processed=False, url=url)


# 控制设置为启用的摄像头拍照
@shared_task
def photo_capture():
    # 从数据库中获取摄像头列表
    camera_list = list(Camera.objects.all().order_by('id'))
    print('camera_list:', camera_list)
    # 检查摄像头列表中相机的状态
    for camera in camera_list:
        # 如果工作状况设置为是，则进行拍照操作
        if camera.is_working:
            # 设置摄像头拍照参数
            cam = Device(devnum=int(camera.id), showVideoWindow=0)
            cam.setResolution(640, 480)
            # 获取当前时间
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            print('\n正在拍摄照片')
            # 拍摄照片，保存到指定目录
            url = os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'photo', 'cam' + camera.id + '-' + now_time + '.jpg')
            print('摄像头id=', camera.id, '照片存储路径', url)
            cam.saveSnapshot(url, timestamp=3, boldfont=1, quality=50)
            # 将照片信息存入数据库
            Photo.objects.create(time=now_time, camera_id=camera.id, location=camera.location, is_processed=False, url=url)


# 识别照片中的内容，将识别结果存储到指定路径
@shared_task
def photo_detection():
    # 从数据库中获取照片列表
    photo_list = list(Photo.objects.all().order_by('-time'))
    print('photo_list', photo_list)

    # 设置预测模型，有以下三种
    detector = ObjectDetection()
    # YOLO-tiny
    # detector.setModelTypeAsTinyYOLOv3()  #设置需要使用的模型
    # detector.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'yolo-tiny.h5'))

    # YOLO
    # detector.setModelTypeAsYOLOv3()
    # detector.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'yolo.h5'))

    # RetinaNet
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'resnet50_coco_best_v2.0.1.h5'))

    # 加载模型
    detector.loadModel()

    # 遍历照片列表，如果照片没有被识别则进行识别操作
    for photo in photo_list:
        if photo.is_processed is False:
            start_time = time.time()  # 开始计时
            # 将检测后的结果保存为新图片
            detections = detector.detectObjectsFromImage(input_image=photo.url, output_image_path=photo.url.replace('photo', 'detection'))
            end_time = time.time()   # 结束计时
            # 输出照片中物体列表
            for eachObject in detections:
                print('--------------------------------')
                print('照片的识别结果为：')
                print(eachObject['name'] + ':' + str(eachObject["percentage_probability"]))
                print('--------------------------------')
            # 输出耗费总时间
            print('识别照片所耗时间：', end_time - start_time, 's')
            # 将检测结果保存到数据库
            Photo.objects.filter(id=photo.id).update(is_processed=True, url_processed=photo.url.replace('photo', 'detection'))

