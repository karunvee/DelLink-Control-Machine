
from .models import  LineInfo, Indicator
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

DIA_IP = '10.195.220.7'
DIA_PORT = '9000'
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
    line_members = LineInfo.objects.all()
    ip = get_client_ip(request)

    error_context = {'test_error' : "IP isn't connect",}
    chk = connectionIP(DIA_IP, int(DIA_PORT))
    if chk == False:
        return render(request, 'Error/ErrorAPI.html', error_context)


    headers = {'Content-Type': 'application/json'}
    body = {  }
    d_response = requests.get( ReturnHttpDIA(DIA_IP, DIA_PORT, 'devices') )
    if d_response.status_code == requests.codes.ok:
        device_data = d_response.json()
        context = {
            'line_members': line_members,
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
        d_response = requests.get(ReturnHttpDIA(DIA_IP, DIA_PORT, 'devices'))

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

        url_tag = ReturnHttpDIA(DIA_IP, DIA_PORT, 'devices/' + str(id) + '/tags' )
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
            return render(request, 'ServerHTML/_item_view.html', context)
        else:
            error_context = {
                'test_error' : "At tag information process",
                'status_code' : t_response.status_code,
            }
            return render(request, 'Error/ErrorAPI.html', error_context)

    