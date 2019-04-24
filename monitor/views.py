from django.shortcuts import render
from monitor.tasks import get_camera_list

from labMonitoring.settings import BASE_DIR
from monitor.models import *
from monitor.tasks import photo_capture_by_id
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

