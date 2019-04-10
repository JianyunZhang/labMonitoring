from django.shortcuts import render
from monitor.tasks import get_camera_list
from monitor.tasks import photo_capture
from monitor.models import *
import json
# Create your views here.
# monitor/views.py


def control(request):
    # 获取相机列表
    camera_list = list(Camera.objects.all())
    # print(camera_list)
    # 将相机列表中的数据转换为字典
    for num in range(0, len(camera_list)):
        camera_list[num] = json.loads(json.dumps(camera_list[num], default=lambda obj: obj.__dict__))
    # print(camera_list)
    return render(request, 'monitor/control.html', {'camera_data': camera_list})


def photo(request):
    # photo_capture.delay()
    return render(request, 'monitor/photo.html')


def detection(request):
    return render(request, 'monitor/detection.html')


# 修改相机属性页面
def camera_edit(request):
    # 先获取传入的相机id
    camera_id = request.GET.get('id')
    # 从数据库中查询该相机的数据
    camera = Camera.objects.get(id=camera_id)
    # 将相机类转换为字典
    camera_dict = json.loads(json.dumps(camera, default=lambda obj: obj.__dict__))

    # 如果form通过POST方法发送数据
    if request.method == 'POST':
        # 接收request.POST参数构造form类的实例
        camera_name = request.POST.get('name')
        camera_location = request.POST.get('location')
        if request.POST.get('is_working') == '开启':
            camera_is_working = True
        elif request.POST.get('is_working') == '关闭':
            camera_is_working = False

        # 修改数据库中数据
        Camera.objects.filter(id=camera_id).update(name=camera_name, location=camera_location, is_working=camera_is_working)

    return render(request, 'monitor/camera-edit.html', {'camera_dict': camera_dict})

