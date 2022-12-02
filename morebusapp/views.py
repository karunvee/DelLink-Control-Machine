from django.views import View
from .models import  *
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from django.template import loader, Context, Template 
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
# from pymodbus.client.sync import ModbusTcpClient
# from pymodbus.bit_read_message import ReadCoilsResponse, ReadCoilsRequest
import requests, time, json
import urllib.request
import cv2
from django.views.decorators import gzip
import threading
import logging

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


def event_stream():
    machine_members = dict()
    ini_data = ""

    line_ = LineInfo.objects.all()

    for m_ip in line_:           #loop for get ip and port of each lines.
        m_response = requests.get(ReturnHttpDIA(m_ip.ip, m_ip.port, 'devices'))
        if m_response.status_code == requests.codes.ok or m_response.status_code == requests.codes.no_content:
            response_data = m_response.json()
            deviceList = []               #array for container all deviceId. and clear array to be empty
            for val in response_data:     #loop for insert each deviceId to array
                deviceList.append(val['deviceId'])      #insert to array
            key_ = m_ip.ip + ':' + m_ip.port
            if key_ not in machine_members:          #make sure these array is not duplicate inserting
                machine_members[key_] = deviceList  #insert key and data(array) to dictionary
    while True: 
        for key in machine_members.keys():  #find those key from dictionary
            ip = key.split(':')[0]
            port = key.split(':')[1]
            for id in machine_members[key]:
                print(ip + ':' + port + '>>' + str(id))
                t_response = requests.get(ReturnHttpDIA(ip, port, 'devices/' + str(id) + '/tags'))
                if t_response.status_code == requests.codes.ok or t_response.status_code == requests.code.no_content:
                    data_tag = t_response.json()
                    for val in data_tag:
                        if val['name'] == 'statusCode':     #filter find only statusCode
                            print(str(val['deviceId']) + "/" + str(val['tid']))
                            # data = json.dumps(list(), cls=DjangoJSONEncoder)
                            # # data = json.dumps(list(ErrorNotification.objects.order_by("-id").values("error_code", 
                            # #         "error_message", )),
                            # #         cls=DjangoJSONEncoder
                            # #     )
                            # if not ini_data == data:
                            #     yield "\ndata: {}\n\n".format(data)
                            #     ini_data = data
                            time.sleep(2)

class ErrorStreamView(View):
    def get(self, request):
        response = StreamingHttpResponse(event_stream())
        response['Content-Type'] = 'text/event-stream'
        return response
        

def notice_view(request):    
    errorMsg = ErrorNotification.objects.all()
    context = {
        'errorMsg' : errorMsg,
    }
    return render(request, 'notice_view.html', context)












# def hello():
#     yield 'Hello,'
#     yield 'there!'

# def stream_response_generator():
#     yield "<html><body>\n"
#     x = 0
#     while True:
#         x = x + 1
#         yield "<h1>Hi , i'm here</h1><div>%s</div>\n" % x
#         yield " " * 1024  # Encourage browser to render incrementally
#         time.sleep(1)
#     yield "</body></html>\n"

# def gen_error_msg():
#     # t = loader.get_template('notice_msg.html')
#     t = Template('{{ tag_data }} <br />\n')
#     while True:
#         t_response = requests.get('http://10.195.220.21:5000/api/v1/devices')
#         if t_response.status_code == requests.codes.ok or t_response.status_code == requests.codes.no_content:
#             tag_data = t_response.json()
#         else:
#             tag_data = 'error to get data'

#         context = Context({'tag_data': tag_data,})
#         time.sleep(1)
#         yield t.render(context)