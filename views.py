from django.shortcuts import render
from myapp.models import Action, Mode, Motion, Door
from rest_framework import viewsets
from django.template import RequestContext, loader
from myapp.serializers import ModeSerializer, ActionSerializer
import requests
import json
from django.http import HttpResponse

IP = '3B'   # By hostname

# IP = '127.0.0.1' #IP at localhost
# IP = '192.168.1.21' #IP at Home
# IP = '155.246.169.177' #IP at Stevens

#Username and Password of django user
username = 'hello'
password = 'nishil123'


# Create your views here.
class ModeViewSet(viewsets.ModelViewSet):
    queryset = Mode.objects.all()
    serializer_class = ModeSerializer

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

def index(request):
    template = loader.get_template('myapp/history.html')
    return HttpResponse(template.render(request))

def m(request):
    latest_motion_log = Motion.objects.order_by('-motion_date')[:100]
    context = {'latest_motion_log' : latest_motion_log}
    return render(request, 'myapp/motion.html', context)

def d(request):
    latest_door_log = Door.objects.order_by('-door_date')[:100]
    context = {'latest_door_log' : latest_door_log}
    return render(request, 'myapp/door.html', context)

def m_detail(request, motion_id):
    return HttpResponse("You are looking at motion %s." % motion_id)

def d_detail(request, door_id):
    return HttpResponse("You are looking at door %s." % door_id)

def home(request):
    out = ''
    currentmode = 'manual'
    currentaction = 'off'

    if 'snap' in request.POST:
        values = {"name": "snap"}
        r = requests.put('http://'+IP+':8000/action/1/',
                        data=values, auth=(username, password))
        result = r.text
        output = json.loads(result)
        out = output['name']

    if 'vid' in request.POST:
        values = {"name": "vid"}
        r = requests.put('http://'+IP+':8000/action/1/',
                        data=values, auth=(username, password))
        result = r.text
        output = json.loads(result)
        out = output['name']

    if 'stream' in request.POST:
        values = {"name": "stream"}
        r = requests.put('http://'+IP+':8000/action/1/',
                        data=values, auth=(username, password))
        result = r.text
        output = json.loads(result)
        out = output['name']
        
    if 'off' in request.POST:
        values = {"name": "off"}
        r = requests.put('http://'+IP+':8000/action/1/',
                        data=values, auth=(username, password))
        result = r.text
        output = json.loads(result)
        out = output['name']
        
    if 'auto' in request.POST:
        values = {"name": "auto"}
        r = requests.put('http://'+IP+':8000/mode/1/',
                        data=values, auth=(username, password))
        result = r.text
        output = json.loads(result)
        out = output['name']
        
    if 'manual' in request.POST:
        values = {"name": "manual"}
        r = requests.put('http://'+IP+':8000/mode/1/',
                        data=values, auth=(username, password))
        result = r.text
        output = json.loads(result)
        out = output['name']

    r = requests.get('http://'+IP+':8000/mode/1/',
                    auth=(username, password))
    result = r.text
    output = json.loads(result)
    currentmode = output['name']

    r = requests.get('http://'+IP+':8000/action/1/',
                    auth=(username, password))
    result = r.text
    output = json.loads(result)
    currentaction = output['name']

    return render(request, 'myapp/index.html', {'name':out,
    'currentmode':currentmode, 'currentaction':currentaction})
