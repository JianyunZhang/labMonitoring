from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from labMonitoring.settings import BASE_DIR
from login.models import *
from monitor.models import *
from monitor.tasks import get_camera_list
from monitor.tasks import photo_capture_by_id
from monitor.tasks import photo_detection_by_id
from monitor.tasks import photo_predicting_by_id
import time
import datetime
import json
import os
# Create your views here.
# monitor/views.py


def control(request):
    # 如果form通过POST方法发送数据
    if request.method == 'POST':
        # 获取传入的摄像机id
        camera_id = request.GET.get('id')
        photo_capture_by_id.delay(camera_id)

    # 获取相机列表
    camera_list = list(Camera.objects.all().order_by('id'))
    # print(camera_list)
    # 将相机列表中的数据转换为字典
    for num in range(0, len(camera_list)):
        camera_list[num] = json.loads(json.dumps(camera_list[num], default=lambda obj: obj.__dict__))
    # print(camera_list)
    return render(request, 'monitor/control.html', {'camera_data': camera_list})


# 照片列表页面
def photo(request):
    # 获取照片列表
    photo_list = list(Photo.objects.all().order_by('-time'))
    substr = os.path.join(BASE_DIR, 'monitor')
    for photo in photo_list:
        photo.url = photo.url.replace(substr, '')  # 替换子串
        photo.url_processed = photo.url_processed.replace(substr, '')  # 替换子串
        photo.url_processed = photo.url_processed.replace('photo', 'detection')
    # 列表中的元素转换为字典
    for num in range(0, len(photo_list)):
        photo_list[num] = {'id': photo_list[num].id, 'time': photo_list[num].time, 'location': photo_list[num].location, 'is_processed': photo_list[num].is_processed, 'camera_id': photo_list[num].camera_id, 'url': photo_list[num].url, 'url_processed': photo_list[num].url_processed}

    return render(request, 'monitor/photo.html', {'photo_data': photo_list})


# 识别结果页面
def detection(request):
    # 获取照片列表
    photo_list = list(Photo.objects.filter(is_processed=True).order_by('-time'))
    substr = os.path.join(BASE_DIR, 'monitor')
    for photo in photo_list:
        photo.url = photo.url.replace(substr, '')  # 替换子串
        photo.url_processed = photo.url_processed.replace(substr, '')  # 替换子串
        photo.url_processed = photo.url_processed.replace('photo', 'detection')
    # 列表中的元素转换为字典
    for num in range(0, len(photo_list)):
        photo_list[num] = {'id': photo_list[num].id, 'time': photo_list[num].time, 'location': photo_list[num].location,
                           'is_processed': photo_list[num].is_processed, 'camera_id': photo_list[num].camera_id,
                           'url': photo_list[num].url, 'url_processed': photo_list[num].url_processed}

    return render(request, 'monitor/detection.html', {'photo_data': photo_list})


# 修改相机属性页面
def camera_edit(request):
    # 如果form通过POST方法发送数据
    if request.method == 'POST':
        # 接收request.POST参数构造form类的实例
        camera_id = request.GET.get('id')
        camera_name = request.POST.get('name')
        camera_location = request.POST.get('location')
        if request.POST.get('is_working') == '开启':
            camera_is_working = True
        elif request.POST.get('is_working') == '关闭':
            camera_is_working = False
        print('接收的摄像头id:', camera_id, 'name:', camera_name, 'location:', camera_location, 'is_working:', camera_is_working)
        # 修改数据库中数据
        Camera.objects.filter(id=camera_id).update(name=camera_name, location=camera_location, is_working=camera_is_working)
        # 从数据库中查询该相机的数据
        camera = Camera.objects.get(id=camera_id)
        # 将相机类转换为字典
        camera_dict = json.loads(json.dumps(camera, default=lambda obj: obj.__dict__))
        return render(request, 'monitor/camera-edit.html', {'camera_dict': camera_dict})

    # 先获取传入的相机id
    camera_id = request.GET.get('id')
    # 从数据库中查询该相机的数据
    camera = Camera.objects.get(id=camera_id)
    # 将相机类转换为字典
    camera_dict = json.loads(json.dumps(camera, default=lambda obj: obj.__dict__))
    print('接收的摄像头id:', camera_id)
    return render(request, 'monitor/camera-edit.html', {'camera_dict': camera_dict})


# 显示相片原图页面
def photo_show(request):
    # 先获取传入的照片id
    photo_id = request.GET.get('id')
    # 从数据库中查询图片
    photo = Photo.objects.get(id=photo_id)
    # 替换字串
    substr = os.path.join(BASE_DIR, 'monitor')
    photo.url = photo.url.replace(substr, '')  # 替换子串
    photo.url_processed = photo.url_processed.replace(substr, '')  # 替换子串
    photo.url_processed = photo.url_processed.replace('photo', 'detection')
    # 将图片类转换为字典
    photo_dict = {'id': photo.id, 'time': photo.time, 'location': photo.location, 'is_processed': photo.is_processed, 'camera_id': photo.camera_id, 'url': photo.url, 'url_processed': photo.url_processed}

    print('传入的图片URL:', photo.url)
    return render(request, 'monitor/photo-show.html', {'photo_data': photo_dict})


# 显示识别结果原图页面
def detection_show(request):
    # 先获取传入的照片id
    photo_id = request.GET.get('id')
    # 从数据库中查询图片
    photo = Photo.objects.get(id=photo_id)
    # 替换字串
    substr = os.path.join(BASE_DIR, 'monitor')
    photo.url = photo.url.replace(substr, '')  # 替换子串
    photo.url_processed = photo.url_processed.replace(substr, '')  # 替换子串
    photo.url_processed = photo.url_processed.replace('photo', 'detection')
    # 将图片类转换为字典
    photo_dict = {'id': photo.id, 'time': photo.time, 'location': photo.location, 'is_processed': photo.is_processed,
                  'camera_id': photo.camera_id, 'url': photo.url, 'url_processed': photo.url_processed}
    print('传入的识别结果URL:', photo.url_processed)
    return render(request, 'monitor/detection-show.html', {'photo_data': photo_dict})


# 修改设定项页面
def admin_check_setting(request):
    if request.method == 'GET':
        # 从数据库查出当前的设定
        setting = Setting.objects.get(id=1)
        # 将设定类转换为字典
        setting_dict = json.loads(json.dumps(setting, default=lambda obj: obj.__dict__))
        return render(request, 'monitor/admin-check-setting.html', {'setting_dict': setting_dict})
    elif request.method == 'POST':
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        setting = request.POST.get('setting')
        # 将设定信息反序列化为字典
        setting = json.loads(setting)
        print('收到上传的内容：', setting)
        # 将上传结果保存到数据库
        try:
            Setting.objects.filter(id=setting['id']).update(is_auto_detecting=setting['is_auto_detecting'], is_auto_predicting=setting['is_auto_predicting'], detection_model=setting['detection_model'], detection_speed=setting['detection_speed'], prediction_model=setting['prediction_model'], prediction_speed=setting['prediction_speed'])
            print('设置修改成功！id =', setting['id'])
            return JsonResponse({"msg": "success"})
        except Exception as e:
            print('设置修改失败！id =', setting['id'])
            print(e)
            return JsonResponse({"msg": "failed"})


# 管理员查看摄像头列表界面
def admin_list_camera(request):
    if request.method == 'GET':
        # 探测接入系统的摄像头
        get_camera_list()
        # 从数据库中查询摄像头列表
        camera_list = Camera.objects.all().order_by('-id')
        print('当前摄像头列表：', camera_list)
        # 分页操作
        # 将数据按照规定每页显示 5 条, 进行分割
        paginator = Paginator(camera_list, 5)
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            camera_list = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            camera_list = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        # 将结果返回到页面
        return render(request, 'monitor/admin-list-camera.html', {"camera_list": camera_list})
    elif request.method == 'POST':  # 拍照操作
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        camera_id = request.POST.get('id')
        # 执行拍照操作
        photo_capture_by_id(camera_id)
        print('拍照成功！id =', camera_id)
        return JsonResponse({"msg": "success"})


# 管理员修改摄像头信息monitor/admin-check-camera.html
def admin_check_camera(request):
    if request.method == 'GET':
        # 获取修改的摄像头id
        camera_id = request.GET.get('id')
        # 从数据库查出该摄像头
        camera = Camera.objects.get(id=camera_id)
        # 从数据库中查询实验室列表
        laboratory_list = Laboratory.objects.all()
        # 将摄像头转换为字典
        camera_dict = json.loads(json.dumps(camera, default=lambda obj: obj.__dict__))
        # 打印选中的摄像头数据
        print('接收到摄像头信息：', camera_dict)
        return render(request, 'monitor/admin-check-camera.html', {'camera_dict': camera_dict, 'laboratory_list': laboratory_list})
    elif request.method == 'POST':
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        camera = request.POST.get('camera')
        # 将摄像头信息反序列化为字典
        camera = json.loads(camera)
        print('收到上传的内容：', camera)
        # 将上传结果保存到数据库
        try:
            Camera.objects.filter(id=camera['id']).update(name=camera['name'], location=camera['location'], is_working=camera['is_working'], photo_quality=camera['photo_quality'])
            print('摄像头信息修改成功！id=', camera['id'])
            return JsonResponse({"msg": "success"})
        except Exception as e:
            print('摄像头信息修改失败！id=', camera['id'])
            print(e)
            return JsonResponse({"msg": "failed"})


# 管理员查看照片列表monitor/admin-list-photo.html
def admin_list_photo(request):
    if request.method == 'GET':
        if 'search' in request.GET:
            # 查询操作，取出搜索框输入的相机名称，拍摄地点，是否被对象检测，图像预测，是否包含手机
            photo_camera = request.GET.get('photo_camera')
            photo_location = request.GET.get('photo_location')
            is_detected = request.GET.get('is_detected')
            if is_detected is None:
                is_detected = False
            is_predicted = request.GET.get('is_predicted')
            if is_predicted is None:
                is_predicted = False
            is_phone = request.GET.get('is_phone')
            if is_phone is None:
                is_phone = False

            print(is_detected, is_predicted, is_phone)
            try:
                # 从数据库中模糊查询，查出照片列表，按照序号排序
                photo_list = Photo.objects.filter(camera_name__contains=photo_camera, location__contains=photo_location, is_detected=is_detected, is_predicted=is_predicted, is_phone=is_phone).order_by('-id')
                # 替换photo中url的字串
                substr = os.path.join(BASE_DIR, 'monitor')
                for photo in photo_list:
                    photo.url = photo.url.replace(substr, '')  # 替换图片URL中的子串
                    if photo.url_detected:
                        photo.url_detected = photo.url_detected.replace(substr, '')   # 替换检测结果中的子串
                        photo.url_detected = photo.url_detected.replace('photo', 'detection')
                print('查找结果：', photo_list)
            except Exception as e:
                print('没有查询到结果！')
                print(e)
                photo_list = []

            # 分页操作
            # 将数据按照规定每页显示 5 条, 进行分割
            paginator = Paginator(photo_list, 5)
            page = request.GET.get('page')
            try:
                photo_list = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                photo_list = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            # 将结果返回到页面
            return render(request, 'monitor/admin-list-photo.html', {"photo_list": photo_list})
        else:
            # 从数据库中查询实验设备列表
            photo_list = Photo.objects.all().order_by('-id')
            # 替换photo中url的字串
            substr = os.path.join(BASE_DIR, 'monitor')
            for photo in photo_list:
                photo.url = photo.url.replace(substr, '')  # 替换图片URL中的子串
                if photo.is_detected:
                   photo.url_detected = photo.url_detected.replace(substr, '')  # 替换检测结果中的子串
                   photo.url_detected = photo.url_detected.replace('photo', 'detection')
            print('当前照片列表：', photo_list)
            # 分页操作
            # 将数据按照规定每页显示 5 条, 进行分割
            paginator = Paginator(photo_list, 5)
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page')
            try:
                photo_list = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                photo_list = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            # 将结果返回到页面
            return render(request, 'monitor/admin-list-photo.html', {"photo_list": photo_list})
    elif request.method == 'POST':  # 删除照片操作
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        photo_id = request.POST.get('id')
        # 删除数据库中的记录
        Photo.objects.filter(id=photo_id).delete()
        print('删除照片成功！id =', photo_id)
        return JsonResponse({"msg": "success"})


# 管理员查看照片详情monitor/admin-check-photo
def admin_check_photo(request):
    if request.method == 'GET':
        # 先获取传入的照片id
        photo_id = request.GET.get('id')
        # 从数据库中查询图片
        photo = Photo.objects.get(id=photo_id)
        # 替换url子串
        substr = os.path.join(BASE_DIR, 'monitor')
        photo.url = photo.url.replace(substr, '')  # 替换子串
        if photo.is_detected:
            photo.url_detected = photo.url_detected.replace(substr, '')  # 替换物体检测结果URL子串
            photo.url_detected = photo.url_detected.replace('photo', 'detection')
        # 将照片转换为字典
        photo_dict = {'id': photo.id, 'time': photo.time, 'location': photo.location, 'camera_id': photo.camera_id, 'url': photo.url, 'is_detected': photo.is_detected, 'is_predicted': photo.is_predicted, 'list_predicted': photo.list_predicted, 'url_detected': photo.url_detected, 'is_phone': photo.is_phone, 'camera_name': photo.camera_name, 'detection_model': photo.detection_model, 'prediction_model': photo.prediction_model, 'detection_speed': photo.detection_speed, 'prediction_speed': photo.prediction_speed}
        return render(request, 'monitor/admin-check-photo.html', {'photo_dict': photo_dict})


# 管理员查看对象检测结果详情monitor/admin-check-photo-detection
def admin_check_photo_detection(request):
    if request.method == 'GET':
        # 先获取传入的照片id
        photo_id = request.GET.get('id')
        # 从数据库中查询图片
        photo = Photo.objects.get(id=photo_id)
        # 替换字串
        substr = os.path.join(BASE_DIR, 'monitor')
        photo.url = photo.url.replace(substr, '')  # 替换照片URL子串
        photo.url_detected = photo.url_detected.replace(substr, '')  # 替换物体检测结果URL子串
        photo.url_detected = photo.url_detected.replace('photo', 'detection')
        # 将照片转换为字典
        photo_dict = {'id': photo.id, 'time': photo.time, 'location': photo.location, 'camera_id': photo.camera_id, 'url': photo.url, 'is_detected': photo.is_detected, 'is_predicted': photo.is_predicted, 'list_predicted': photo.list_predicted, 'url_detected': photo.url_detected, 'is_phone': photo.is_phone, 'camera_name': photo.camera_name, 'detection_model': photo.detection_model, 'prediction_model': photo.prediction_model, 'detection_speed': photo.detection_speed, 'prediction_speed': photo.prediction_speed}
        return render(request, 'monitor/admin-check-photo-detection.html', {'photo_dict': photo_dict})


# 管理员查看图像预测结果详情monitor/admin-check-photo-prediction
def admin_check_photo_prediction(request):
    if request.method == 'GET':
        # 先获取传入的照片id
        photo_id = request.GET.get('id')
        # 从数据库中查询图片
        photo = Photo.objects.get(id=photo_id)
        # 将照片转换为字典
        photo_dict = {'id': photo.id, 'time': photo.time, 'location': photo.location, 'camera_id': photo.camera_id, 'url': photo.url, 'is_detected': photo.is_detected, 'is_predicted': photo.is_predicted, 'list_predicted': photo.list_predicted, 'url_detected': photo.url_detected, 'is_phone': photo.is_phone, 'camera_name': photo.camera_name, 'detection_model': photo.detection_model, 'prediction_model': photo.prediction_model, 'detection_speed': photo.detection_speed, 'prediction_speed': photo.prediction_speed}
        return render(request, 'monitor/admin-check-photo-prediction.html', {'photo_dict': photo_dict})


# 管理员按照传入的图片id，算法模型，执行速度等，手动执行对象检测操作monitor/admin-detection-photo
def admin_detection_photo(request):
    if request.method == 'GET':
        # 先获取传入的照片id
        photo_id = request.GET.get('id')
        # 从数据库中查询图片
        photo = Photo.objects.get(id=photo_id)
        # 替换图片url子串
        substr = os.path.join(BASE_DIR, 'monitor')
        photo.url = photo.url.replace(substr, '')  # 替换图片url子串
        if photo.is_predicted:
            photo.url_detected = photo.url_detected.replace(substr, '')  # 替换物体检测结果URL子串
            photo.url_detected = photo.url_detected.replace('photo', 'detection')
        # 将照片转换为字典
        photo_dict = {'id': photo.id, 'time': photo.time, 'location': photo.location, 'camera_id': photo.camera_id,
                      'url': photo.url, 'is_detected': photo.is_detected, 'is_predicted': photo.is_predicted,
                      'list_predicted': photo.list_predicted, 'url_detected': photo.url_detected,
                      'is_phone': photo.is_phone, 'camera_name': photo.camera_name,
                      'detection_model': photo.detection_model, 'prediction_model': photo.prediction_model,
                      'detection_speed': photo.detection_speed, 'prediction_speed': photo.prediction_speed}
        return render(request, 'monitor/admin-detection-photo.html', {'photo_dict': photo_dict})
    if request.method == 'POST':
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        photo_id = request.POST.get('id')
        detection_model = request.POST.get('detection_model')
        detection_speed = request.POST.get('detection_speed')
        print('photo_id:', photo_id, 'detection_model:', detection_model, 'detection_speed:', detection_speed)
        # 启动对象检测操作
        try:
            # 执行对象检测操作
            photo_detection_by_id(photo_id=int(photo_id), detection_model=detection_model, detection_speed=detection_speed)
            return JsonResponse({"msg": "success"})
        except Exception as e:
            print('手动执行对象检测操作失败！')
            print(e)
            return JsonResponse({"msg": "failed"})


# 管理员按照传入的图片id，算法模型，执行速度等，手动执行图像预测操作monitor/admin-prediction-photo
def admin_prediction_photo(request):
    if request.method == 'GET':
        # 先获取传入的照片id
        photo_id = request.GET.get('id')
        # 从数据库中查询图片
        photo = Photo.objects.get(id=photo_id)
        # 替换图片url子串
        substr = os.path.join(BASE_DIR, 'monitor')
        photo.url = photo.url.replace(substr, '')  # 替换图片url子串
        if photo.is_predicted:
            photo.url_detected = photo.url_detected.replace(substr, '')  # 替换物体检测结果URL子串
            photo.url_detected = photo.url_detected.replace('photo', 'detection')
        # 将照片转换为字典
        photo_dict = {'id': photo.id, 'time': photo.time, 'location': photo.location, 'camera_id': photo.camera_id,
                      'url': photo.url, 'is_detected': photo.is_detected, 'is_predicted': photo.is_predicted,
                      'list_predicted': photo.list_predicted, 'url_detected': photo.url_detected,
                      'is_phone': photo.is_phone, 'camera_name': photo.camera_name,
                      'detection_model': photo.detection_model, 'prediction_model': photo.prediction_model,
                      'detection_speed': photo.detection_speed, 'prediction_speed': photo.prediction_speed}
        return render(request, 'monitor/admin-prediction-photo.html', {'photo_dict': photo_dict})
    if request.method == 'POST':
        # 获取AJAX上传的数据，GET上传的数据用request.args获取，POST上传的数据用request.form获取，获取对象为JSON
        photo_id = request.POST.get('id')
        prediction_model = request.POST.get('prediction_model')
        prediction_speed = request.POST.get('prediction_speed')
        print('photo_id:', photo_id, 'prediction_model:', prediction_model, 'prediction_speed:', prediction_speed)
        # 启动对象检测操作
        try:
            # 执行对象检测操作
            photo_predicting_by_id(photo_id=int(photo_id), prediction_model=prediction_model, prediction_speed=prediction_speed)
            return JsonResponse({"msg": "success"})
        except Exception as e:
            print('手动执行图像预测操作失败！')
            print(e)
            return JsonResponse({"msg": "failed"})
