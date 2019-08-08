from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from CMLMasterProject.config.base import STATIC_ROOT
import os, json


# Create your views here.
def home(request):
    context_dict = {}
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        #special for cml researcher to get info to be used later
        context_dict.update({'username': username})


    return render(request,'MicroVis/home.html', context_dict)

def flows_fishman(request):
    context_dict = {}
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        #special for cml researcher to get info to be used later
        context_dict.update({'username': username})


    return render(request,'MicroVis/fishman.html', context_dict)

def flows_fishman2(request):
    context_dict = {}
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        #special for cml researcher to get info to be used later
        context_dict.update({'username': username})


    return render(request,'MicroVis/fishman2.html', context_dict)


def tailing(request):
    context_dict = {}
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        #special for cml researcher to get info to be used later
        context_dict.update({'username': username})


    return render(request,'MicroVis/tailing.html', context_dict)


class fishmanDefView(APIView):
    def get(self, request):
        file_ = json.load(open(os.path.join(STATIC_ROOT, 'jsonFilesFishman/US_json_abs.json')))

        return Response(file_)

class fishmanDefView2(APIView):
    def get(self, request):
        file_ = json.load(open(os.path.join(STATIC_ROOT, 'jsonFilesFishman/simple_graph.json')))

        return Response(file_)


class fishman_JP_abs(APIView):
    def get(self, request):
        file_ = json.load(open(os.path.join(STATIC_ROOT, 'jsonFilesFishman/JP_json_abs.json')))
        return Response(file_)


class fishman_US_cap(APIView):
    def get(self, request):
        file_ = json.load(open(os.path.join(STATIC_ROOT, 'jsonFilesFishman/US_json_cap.json')))
        return Response(file_)
class fishman_JP_cap(APIView):
    def get(self, request):
        file_ = json.load(open(os.path.join(STATIC_ROOT, 'jsonFilesFishman/JP_json_cap.json')))
        return Response(file_)
class fishman_US_gdp(APIView):
    def get(self, request):
        file_ = json.load(open(os.path.join(STATIC_ROOT, 'jsonFilesFishman/US_json_gdp.json')))
        return Response(file_)
class fishman_JP_gdp(APIView):
    def get(self, request):
        file_ = json.load(open(os.path.join(STATIC_ROOT, 'jsonFilesFishman/JP_json_gdp.json')))
        return Response(file_)
class fishman_US_growth(APIView):
    def get(self, request):
        file_ = json.load(open(os.path.join(STATIC_ROOT, 'jsonFilesFishman/US_json_growth.json')))
        return Response(file_)

class fishman_JP_growth(APIView):
    def get(self, request):
        file_ = json.load(open(os.path.join(STATIC_ROOT, 'jsonFilesFishman/JP_json_growth.json')))
        return Response(file_)

class fishman_US_percent(APIView):
    def get(self, request):
        file_ = json.load(open(os.path.join(STATIC_ROOT, 'jsonFilesFishman/US_json_percent.json')))
        return Response(file_)
class fishman_JP_percent(APIView):
    def get(self, request):
        file_ = json.load(open(os.path.join(STATIC_ROOT, 'jsonFilesFishman/JP_json_percent.json')))
        return Response(file_)
