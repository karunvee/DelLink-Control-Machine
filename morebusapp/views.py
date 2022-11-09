
from .models import  Indicator
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.bit_read_message import ReadCoilsResponse, ReadCoilsRequest
import json
import requests
import socket
import datetime

API_URL = 'http://127.0.0.1:5000/api/v1' 
SERVER_IP = '10.234.232.101'

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def connectionIP(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        result = sock.connect((ip, port))
        return True
    except Exception as e: 
        return False
    finally:
        sock.close()

# Create your views here.     
def home_view(request):
    ip = get_client_ip(request)

    error_context = {'test_error' : "IP isn't connect",}
    chk = connectionIP('127.0.0.1',5000)
    if chk == False:
        return render(request, 'Error/ErrorAPI.html', error_context)


    headers = {'Content-Type': 'application/json'}
    body = {  }
    d_response = requests.get(API_URL + '/devices')
    if d_response.status_code == requests.codes.ok:
        device_data = d_response.json()
        context = {
            'user_ip': ip ,
            'response': device_data,
        }
        return render(request, 'home_view.html', context)
    else:
        error_context = {
            'test_error' : "At device information process",
            'status_code' : d_response.status_code,
        }
        return render(request, 'Error/ErrorAPI.html', error_context)

def setting_view(request):

    template = loader.get_template('setting_view.html')
    return HttpResponse(template.render({}, request))

def item_view(request, id="0"):
        ip = get_client_ip(request)

        id = int(id)
        d_response = requests.get(API_URL+'/devices')

        if d_response.status_code == requests.codes.ok:
            device_data = d_response.json()
            for val in device_data:
                if val['deviceId'] == id:
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

        url_tag = API_URL + '/devices/' + str(id) + '/tags'
        t_response = requests.get(url_tag)

        if t_response.status_code == requests.codes.ok or t_response.status_code == requests.codes.no_content:
            tag_data = t_response.json()
            context = {
                'user_ip': ip ,
                'mLName' : mLName,
                'mDName' : mDName,
                'mID' : mID,
                'mIP' : mIP,
                'mType' : mType,
                'mModel' : mModel,
                'mStatus' : mStatus,
                'tag_data': tag_data,
            }
            if ip == SERVER_IP:
                return render(request, 'ServerHTML/_item_view.html', context)
            else:
                return render(request, 'item_view.html', context)

        else:
            error_context = {
                'test_error' : "At tag information process",
                'status_code' : t_response.status_code,
            }
            return render(request, 'Error/ErrorAPI.html', error_context)

def writeData(request, id, tg):
    value = request.POST['TagValue']

    url_writeData = API_URL + "/devices/" + str(id) + "/tags/" + str(tg) + "/value/" + str(value)
    headers = {
        'Content-Length': '0',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyb290IiwianRpIjoiMDIwNDI4MjMzMWFmNDhkNThiMTMxNGUxZTk1YjI4YmIiLCJpYXQiOjE2Njc5ODQwNDEsIm5iZiI6MTY2Nzk4NDA0MCwiZXhwIjoxNjY4MDI3MjQwLCJpc3MiOiJBUEkuRElBTGluay5ERUxUQSIsImF1ZCI6IkRJQUxpbmsgQVBJIFVzZXIifQ.CyCAO2a09_U_p2Dj6vZRyX7o3XuSIduLaUU-ePjgf5U',
        }
    2
    w_response = requests.put(url_writeData, headers=headers)

    if w_response.status_code == requests.codes.ok or w_response.status_code == requests.codes.no_content:
        recent_path = '/machine_view/id' + id
        return redirect(recent_path)
        # return redirect(reverse('item_view', kwargs={'id':id}))
    else:
        html = "<html><body>%s</body></html>" % w_response.status_code
        return HttpResponse(html)
    