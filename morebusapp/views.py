
from .models import  *
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from django.template import loader
from django.urls import reverse
# from pymodbus.client.sync import ModbusTcpClient
# from pymodbus.bit_read_message import ReadCoilsResponse, ReadCoilsRequest
import requests
import urllib.request
import cv2
from django.views.decorators import gzip
import threading

# DIA_IP = '10.195.220.7'
# DIA_PORT = '9000'
API_URL = 'http://10.195.220.7:9000/api/v1' 
SERVER_IP = '10.234.232.101'

def ReturnHttpDIA(ip, port, method):
    http_name = 'http://' + ip + ':' + port + '/api/v1/' + method
    return http_name

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def internet_on(http):
    try:
        urllib.request.urlopen(http, timeout=2)
        return True
    except:
        return False

# Create your views here.     

def home_view(request):
    line_members = LineInfo.objects.all()
    context = {
        'line_members': line_members,
    }
    return render(request, 'home_view.html', context)

def line_view(request, ln):
    ip = get_client_ip(request)
    line_members = LineInfo.objects.all()
    line_ = LineInfo.objects.get(id = ln)
    status_members = Indicator.objects.filter(data_type__exact = 'STATUS')

    httpurl = 'http://' + line_.ip + ':'+ line_.port
    error_context = {'test_error' : httpurl + " didn’t send any data, please check the IP or port and try again.",}
    chk = internet_on(httpurl)
    if chk == False:
        return render(request, 'Error/ErrorAPI.html', error_context)

    headers = {'Content-Type': 'application/json'}
    body = {  }
    d_response = requests.get( ReturnHttpDIA(line_.ip, line_.port, 'devices') )
    if d_response.status_code == requests.codes.ok:
        device_data = d_response.json()

        context = {
            'status_members': status_members,
            'httpLine': httpurl,
            'line_id' : ln,
            'line_members': line_members,
            'user_ip': ip ,
            'response': device_data,
        }
        return render(request, 'line_view.html', context)
    else:
        error_context = {
            'test_error' : "At device information process",
            'status_code' : d_response.status_code,
        }
        return render(request, 'Error/ErrorAPI.html', error_context)
def notice_view(request):
    errorMsg = ErrorNotification.objects.all()
    context = {
        'errorMsg' : errorMsg,
    }
    return render(request, 'notice_view.html', context)

def setting_view(request):

    template = loader.get_template('setting_view.html')
    return HttpResponse(template.render({}, request))

def item_view(request, ln ,id="0"):
        line_ = LineInfo.objects.get(id = ln)
        DIA_http = 'http://' + line_.ip + ':' + line_.port
        ip = get_client_ip(request)
        displayType_list = Indicator.DISPLAY_TYPE

        #Tag Indicator
        indicator_list = Indicator.objects.filter(machineID__exact = id, lineID__exact = str(ln))
        status_member = Indicator.objects.filter(machineID__exact = id, lineID__exact = str(ln), data_type__exact = 'STATUS')
        
        #Notification error
        notification_error = ErrorNotification.objects.filter(tag_member__machineID = id, tag_member__lineID = str(ln))

        if request.method == 'POST':
            machineID = id
            lineID = ln
            name = request.POST['tagName']
            tag_id = request.POST['tagID']
            register = request.POST['register']
            data_type = request.POST['data_type']
            display = request.POST['display_type']
            color = request.POST['color']
            indicator_member = Indicator(machineID = machineID, lineID = lineID, name = name, tag_id = tag_id, register = register, data_type = data_type, display = display, color = color)
            indicator_member.save()
            return redirect('/machine_view/ln' + ln + 'id' +id +'/')

        id = int(id)

        d_response = requests.get(ReturnHttpDIA(line_.ip, line_.port, 'devices'))

        if d_response.status_code == requests.codes.ok:
            device_data = d_response.json()
            for val in device_data:
                if val['deviceId'] == id:
                    mGuid = val['guid']
                    mLName = val['comment']
                    mDName = val['name']
                    mID = val['deviceId']
                    mIP = val['ip']
                    mType = val['type']
                    mModel = val['model']
                    mStatus = val['status']
        else:
            error_context = {
                'test_error' : "At device information process",
                'status_code' : d_response.status_code,
            }
            return render(request, 'Error/ErrorAPI.html', error_context)

        url_tag = ReturnHttpDIA(line_.ip, line_.port, 'devices/' + str(id) + '/tags' )
        t_response = requests.get(url_tag)


        if t_response.status_code == requests.codes.ok or t_response.status_code == requests.codes.no_content:
            tag_data = t_response.json()
            context = {
                'notification_error' : notification_error,
                'status_member' : status_member,
                'indicator_list' : indicator_list,
                'displayType_list' : displayType_list,
                'DIA_http': DIA_http,
                'user_ip': ip ,
                'mGuid': mGuid,
                'mLName' : mLName,
                'mDName' : mDName,
                'lineID' : ln,
                'mID' : mID,
                'mIP' : mIP,
                'mType' : mType,
                'mModel' : mModel,
                'mStatus' : mStatus,
                'tag_data': tag_data,
            }
            return render(request, 'item_view.html', context)
        else:
            error_context = {
                'test_error' : "At tag information process",
                'status_code' : t_response.status_code,
            }
            return render(request, 'Error/ErrorAPI.html', error_context)

def delete_indicator(request, ln ,id="0", tid="0"):
    indicator = Indicator.objects.get(tag_id = tid)
    indicator.delete()
    return redirect('/machine_view/ln' + ln + 'id' +id +'/')

@gzip.gzip_page
def camera_view(request, id):
    try:
        rtsp = "rtsp://admin:@Admin12345@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0"
        cam = VideoCamera(rtsp)
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'camera_view.html')
#to capture video class
class VideoCamera(object):
    def __init__(self, rtsp):
        self.video = cv2.VideoCapture(rtsp)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')