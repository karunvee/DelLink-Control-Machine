
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
        id = int(id)
        headers = {'Content-Type': 'application/json', 'Authorization': 'Basic XXXXXXXXXX='}
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
                'mLName' : mLName,
                'mDName' : mDName,
                'mID' : mID,
                'mIP' : mIP,
                'mType' : mType,
                'mModel' : mModel,
                'mStatus' : mStatus,
                'tag_data': tag_data,
            }
            return render(request, 'item_view.html', context)
            # return render(request, 'OldHTML/_item_view.html', context)

        else:
            error_context = {
                'test_error' : "At tag information process",
                'status_code' : t_response.status_code,
            }
            return render(request, 'Error/ErrorAPI.html', error_context)

def writeData(request, id, pk):
    recent_path = '/machine_view/id' + id

    
    return HttpResponseRedirect(recent_path)