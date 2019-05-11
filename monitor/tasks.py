from VideoCapture import Device
from cv2 import VideoCapture
from celery import shared_task
from labMonitoring.settings import BASE_DIR
from imageai.Detection import ObjectDetection
from imageai.Prediction import ImagePrediction
from monitor.models import Camera, Photo, Detection
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from login.models import *
from monitor.models import Setting
from keras.backend import clear_session
from tensorflow import keras
import os
import time
import datetime
import tensorflow as tf


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

    # 删除多余的摄像头
    camera_list = Camera.objects.all()
    if total_camera_num < len(camera_list):
        for num in range(total_camera_num-1, len(camera_list)-1):
            Camera.objects.filter(id=num).delete()


# 指定摄像头拍照并将照片存入数据库
@shared_task
def photo_capture_by_id(camera_id):
    # 从数据库中获取该摄像头
    camera = Camera.objects.get(id=camera_id)
    print('当前拍照的摄像头为 id =', camera.id)
    # 设置摄像头拍照参数
    cam = Device(devnum=int(camera.id), showVideoWindow=0)
    cam.setResolution(640, 480)
    # 获取当前时间
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    print('\n正在拍摄照片')
    # 拍摄照片，保存到指定目录
    url = os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'photo', 'cam' + camera.id + '-' + now_time + '.jpg')
    print('摄像头id =', camera.id, '照片存储路径', url)
    cam.saveSnapshot(url, timestamp=3, boldfont=1, quality=camera.photo_quality)
    # 将照片信息存入数据库
    Photo.objects.create(time=now_time, camera_id=camera.id, camera_name=camera.name, location=camera.location, url=url)


# 控制设置为启用的摄像头拍照
@shared_task
def photo_capture():
    # 从数据库中获取摄像头列表
    camera_list = Camera.objects.all().order_by('id')
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
            cam.saveSnapshot(url, timestamp=3, boldfont=1, quality=camera.photo_quality)
            # 将照片信息存入数据库
            Photo.objects.create(time=now_time, camera_id=camera.id, camera_name=camera.name, location=camera.location, url=url)


# 自动对象检测，将识别照片存储到指定路径
@shared_task
def photo_detection():
    # 从数据库中获取设置
    setting = Setting.objects.get(id=1)
    # 若自动识别功能为True，则启动自动识别
    if setting.is_auto_detecting:
        # 从数据库中获取照片列表
        photo_list = Photo.objects.all().order_by('-time')

        # 创建ObjectDetection类的新实例
        detector = ObjectDetection()

        # 按照用户设置对象检测的算法和模型
        if setting.detection_model == 'TinyYOLOv3':
            # YOLO-tiny
            detector.setModelTypeAsTinyYOLOv3()
            detector.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'yolo-tiny.h5'))
        elif setting.detection_model == 'YOLOv3':
            # YOLO
            detector.setModelTypeAsYOLOv3()
            detector.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'yolo.h5'))
        elif setting.detection_model == 'RetinaNet':
            # RetinaNet
            detector.setModelTypeAsRetinaNet()
            detector.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'resnet50_coco_best_v2.0.1.h5'))

        # ImageAI 为对象检测任务添加了速度调节参数detection_speed
        # 可用的检测速度是 “normal”(default), “fast”, “faster” , “fastest” and “flash”
        # 只需要在调用loadModel()函数时指定参数detection_speed的值为你想要的速度模式即可
        detector.loadModel(detection_speed=setting.detection_speed)  # 载入检测模型

        # 定义一个新变量custom_objects = detector.CustomObjects()
        # 其中将一些物品属性设置为True，这是为了告诉模型只检测设置为True的对象
        custom_objects = detector.CustomObjects(cell_phone=True, remote=True, laptop=True, toaster=True, keyboard=True, book=True)

        # 进行自动操作
        # 遍历照片列表，如果照片没有被识别则进行识别操作
        for photo in photo_list:
            if photo.is_detected is False:
                # 开始计时
                start_time = time.time()
                # 将检测后的结果保存为新图片
                # 调用detector.detectCustomObjectsFromImage()函数并传入定义的变量custom_objects来指定我们需要从图像中识别的对象
                # 然后该函数返回一个字典数组，每个字典包含图像中检测到的对象信息，字典中的对象信息有name（对象类名）和 percentage_probability（概率）
                # 它的工作原理是将检测到的对象返回到数组中，然后利用数组中的数据在每个对象上绘制矩形标记来生成新图像
                # minimum_percentage_probability参数用于设定设定预测概率的阈值，其默认值为50（范围在0-100之间）
                # 如果保持默认值，这意味着只有当百分比概率大于等于50时，该函数才会返回检测到的对象
                detections = detector.detectCustomObjectsFromImage(minimum_percentage_probability=25, custom_objects=custom_objects, input_image=photo.url, output_image_path=photo.url.replace('photo', 'detection'))
                # 结束计时
                end_time = time.time()
                # 输出照片中物体列表
                for eachObject in detections:
                    # 若照片中物体含有手机，则将is_phone置为True
                    if eachObject['name'] == 'cell phone':
                        photo.is_phone = True
                    # 输出识别结果
                    print(eachObject['name'] + ':' + str(eachObject["percentage_probability"]))
                print('--------------------------------')
                # 输出耗费总时间
                print('对象检测所耗时间：', end_time - start_time, 's')
                # 将图片的对象检测结果保存到数据库
                Photo.objects.filter(id=photo.id).update(is_detected=True, url_detected=photo.url.replace('photo', 'detection'), is_phone=photo.is_phone, detection_model=setting.detection_model, detection_speed=setting.detection_speed)


# 指定图片id，检测算法，检测速度，进行对象检测操作，将识别照片存储到指定路径
@shared_task
def photo_detection_by_id(photo_id, detection_model, detection_speed):
    # 从数据库中获取设置
    # setting = Setting.objects.get(id=1)

    # 从数据库中获取指定id的照片
    photo = Photo.objects.get(id=photo_id)

    # 创建ObjectDetection类的新实例
    detector = ObjectDetection()

    # 重复预测时，为了避免切换模型的错误，需要清理model底层tensorflow的session中的数据
    # if tf.Session():
    #    keras.backend.clear_session()

    # 按照用户设置对象检测的算法和模型
    if detection_model == 'TinyYOLOv3':
        # YOLO-tiny
        detector.setModelTypeAsTinyYOLOv3()
        detector.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'yolo-tiny.h5'))
    elif detection_model == 'YOLOv3':
        # YOLO
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'yolo.h5'))
    elif detection_model == 'RetinaNet':
        # RetinaNet
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'resnet50_coco_best_v2.0.1.h5'))

    # ImageAI 为对象检测任务添加了速度调节参数detection_speed
    # 可用的检测速度是 “normal”(default), “fast”, “faster” , “fastest” and “flash”
    # 只需要在调用loadModel()函数时指定参数detection_speed的值为你想要的速度模式即可
    detector.loadModel(detection_speed=detection_speed)  # 载入检测模型

    # 定义一个新变量custom_objects = detector.CustomObjects()
    # 其中将一些物品属性设置为True，这是为了告诉模型只检测设置为True的对象
    custom_objects = detector.CustomObjects(cell_phone=True, remote=True, laptop=True, toaster=True, keyboard=True, book=True)

    # 开始计时
    start_time = time.time()
    # 将检测后的结果保存为新图片
    # 调用detector.detectCustomObjectsFromImage()函数并传入定义的变量custom_objects来指定我们需要从图像中识别的对象
    # 然后该函数返回一个字典数组，每个字典包含图像中检测到的对象信息，字典中的对象信息有name（对象类名）和 percentage_probability（概率）
    # 它的工作原理是将检测到的对象返回到数组中，然后利用数组中的数据在每个对象上绘制矩形标记来生成新图像
    detections = detector.detectCustomObjectsFromImage(custom_objects=custom_objects, input_image=photo.url, output_image_path=photo.url.replace('photo', 'detection'))
    # 结束计时
    end_time = time.time()
    # 输出照片中物体列表
    for eachObject in detections:
        # 若照片中物体含有手机，则将is_phone置为True
        if eachObject['name'] == 'cell phone':
            photo.is_phone = True
        # 输出识别结果
        print(eachObject['name'] + ':' + str(eachObject["percentage_probability"]))
    print('--------------------------------')
    # 输出耗费总时间
    print('对象检测所耗时间：', end_time - start_time, 's')
    # 将图片的对象检测结果保存到数据库
    Photo.objects.filter(id=photo.id).update(is_detected=True, url_detected=photo.url.replace('photo', 'detection'), is_phone=photo.is_phone, detection_model=detection_model, detection_speed=detection_speed)


# 自动图像预测，将预测结果存入数据库
@shared_task
def photo_predicting():
    # 从数据库中获取设置
    setting = Setting.objects.get(id=1)
    print('进入图像预测模块')
    # 若自动识别功能为True，则启动自动识别
    if setting.is_auto_predicting:
        print('开始图像预测')
        # 从数据库中获取照片列表
        photo_list = Photo.objects.all().order_by('-id')

        # 对ImagePrediction类进行了实例化
        prediction = ImagePrediction()

        # 按照用户设置预测算法和模型
        if setting.prediction_model == 'SqueezeNet':
            # SqueezeNet（文件大小：4.82 MB，预测时间最短，精准度适中）
            prediction.setModelTypeAsSqueezeNet()
            prediction.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'squeezenet_weights_tf_dim_ordering_tf_kernels.h5'))  # 设置了模型文件的路径
        elif setting.prediction_model == 'RetinaNet':
            # ResNet50 by Microsoft Research （文件大小：98 MB，预测时间较快，精准度高）
            prediction.setModelTypeAsResNet()
            prediction.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'resnet50_weights_tf_dim_ordering_tf_kernels.h5'))
        elif setting.prediction_model == 'InceptionV3':
            # InceptionV3 by Google Brain team （文件大小：91.6 MB，预测时间慢，精度更高）
            prediction.setModelTypeAsInceptionV3()
            prediction.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'inception_v3_weights_tf_dim_ordering_tf_kernels.h5'))
        elif setting.prediction_model == 'DenseNet':
            # DenseNet121 by Facebook AI Research （文件大小：31.6 MB，预测时间较慢，精度最高）
            prediction.setModelTypeAsDenseNet()  # 调用了.setModelTypeAsResNet()函数将预测对象的模型类型设置为DenseNet
            prediction.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'DenseNet-BC-121-32.h5'))

        # ImageAI 为图像预测任务添加了预测速度调节功能，最多可使预测时间缩短60％
        # 可选的速度模式有normal(default), fast, faster , fastest
        # 只需要在调用loadModel()函数时指定参数prediction_speed的值为你想要的速度模式即可
        prediction.loadModel(prediction_speed=setting.prediction_speed)  # 载入预测模型

        # 进行自动操作
        # 遍历照片列表，如果照片没有被识别则进行识别操作
        for photo in photo_list:
            if photo.is_detected is False:
                # 开始计时
                start_time = time.time()
                # 预测图片，以及结果输出数目
                # 在下面的代码中，我们定义了两个变量，他们的值将由所调用的函数predictImage()返回
                # 其中predictImage()函数接受了两个参数，一个是指定要进行图像预测的图像文件路径
                # 另一个参数result_count用于设置我们想要预测结果的数量（该参数的值可选1 to 100）
                # 最后，predictImage()函数将返回预测的对象名和相应的百分比概率（percentage_probabilities）
                predictions, probabilities = prediction.predictImage(image_input=photo.url, result_count=5)
                # 结束计时
                end_time = time.time()
                # 输出预测结果
                result = ''
                for eachPrediction, eachProbability in zip(predictions, probabilities):
                    print(eachPrediction + " : " + result(eachProbability))
                    # 用字符串暂存预测结果
                    result = result + eachPrediction + " : " + result(eachProbability) + "<br>"
                    # 若照片中物体含有手机，则将is_phone置为True
                    if eachPrediction == 'cell phone':
                        photo.is_phone = True
                print('--------------------------------')
                # 输出耗费总时间
                print('对象检测所耗时间：', end_time - start_time, 's')
                # 将图片的预测结果保存到数据库
                Photo.objects.filter(id=photo.id).update(is_predicted=True, list_predicted=result, is_phone=photo.is_phone, prediction_model=setting.prediction_model, prediction_speed=setting.prediction_speed)


# 按照给出的照片id，算法模型，执行速度，进行图像预测操作，将预测结果存入数据库
@shared_task
def photo_predicting_by_id(photo_id, prediction_model, prediction_speed):
    # 从数据库中获取设置
    # setting = Setting.objects.get(id=1)
    # 从数据库中获取照片列表
    photo = Photo.objects.get(id=photo_id)

    # 对ImagePrediction类进行了实例化
    prediction = ImagePrediction()

    # 按照用户设置预测算法和模型
    if prediction_model == 'SqueezeNet':
        # SqueezeNet（文件大小：4.82 MB，预测时间最短，精准度适中）
        prediction.setModelTypeAsSqueezeNet()
        prediction.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'squeezenet_weights_tf_dim_ordering_tf_kernels.h5'))  # 设置了模型文件的路径
    elif prediction_model == 'RetinaNet':
        # ResNet50 by Microsoft Research （文件大小：98 MB，预测时间较快，精准度高）
        prediction.setModelTypeAsResNet()
        prediction.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'resnet50_weights_tf_dim_ordering_tf_kernels.h5'))
    elif prediction_model == 'InceptionV3':
        # InceptionV3 by Google Brain team （文件大小：91.6 MB，预测时间慢，精度更高）
        prediction.setModelTypeAsInceptionV3()
        prediction.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'inception_v3_weights_tf_dim_ordering_tf_kernels.h5'))
    elif prediction_model == 'DenseNet':
        # DenseNet121 by Facebook AI Research （文件大小：31.6 MB，预测时间较慢，精度最高）
        prediction.setModelTypeAsDenseNet()  # 调用了.setModelTypeAsResNet()函数将预测对象的模型类型设置为DenseNet
        prediction.setModelPath(os.path.join(BASE_DIR, 'monitor', 'static', 'monitor', 'CNN', 'DenseNet-BC-121-32.h5'))

    # ImageAI 为图像预测任务添加了预测速度调节功能，最多可使预测时间缩短60％
    # 可选的速度模式有normal(default), fast, faster , fastest
    # 只需要在调用loadModel()函数时指定参数prediction_speed的值为你想要的速度模式即可
    prediction.loadModel(prediction_speed=prediction_speed)  # 载入预测模型

    # 开始计时
    start_time = time.time()
    # 预测图片，以及结果输出数目
    # 在下面的代码中，我们定义了两个变量，他们的值将由所调用的函数predictImage()返回
    # 其中predictImage()函数接受了两个参数，一个是指定要进行图像预测的图像文件路径
    # 另一个参数result_count用于设置我们想要预测结果的数量（该参数的值可选1 to 100）
    # 最后，predictImage()函数将返回预测的对象名和相应的百分比概率（percentage_probabilities）
    predictions, probabilities = prediction.predictImage(image_input=photo.url, result_count=5)
    # 结束计时
    end_time = time.time()
    # 输出预测结果
    result = ''
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        print(eachPrediction + " : " + result(eachProbability))
        # 用字符串暂存预测结果
        result = result + eachPrediction + " : " + result(eachProbability) + "<br>"
        # 若照片中物体含有手机，则将is_phone置为True
        if eachPrediction is 'cell phone':
            photo.is_phone = True
    print('--------------------------------')
    # 输出耗费总时间
    print('对象检测所耗时间：', end_time - start_time, 's')
    # 将图片的预测结果保存到数据库
    Photo.objects.filter(id=photo.id).update(is_predicted=True, list_predicted=result, is_phone=photo.is_phone, prediction_model=prediction_model, prediction_speed=prediction_speed)
