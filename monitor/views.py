from django.shortcuts import render
from monitor.tasks import get_camera_list
from monitor.tasks import photo_capture
# Create your views here.
# monitor/views.py


def control(request):
    get_camera_list.delay()

    return render(request, 'monitor/control.html')


def photo(request):
    photo_capture.delay()
    return render(request, 'monitor/photo.html')


def detection(request):
    return render(request, 'monitor/detection.html')
