from django.shortcuts import render

# Create your views here.
def home(request):
    context_dict = {}
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        #special for cml researcher to get info to be used later
        context_dict.update({'username': username})


    return render(request,'MicroVis/home.html', context_dict)

def flows_fishman(request):
    context_dict = {}
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        #special for cml researcher to get info to be used later
        context_dict.update({'username': username})


    return render(request,'MicroVis/fishman.html', context_dict)

def us_stocks(request):
    context_dict = {}
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        #special for cml researcher to get info to be used later
        context_dict.update({'username': username})


    return render(request,'MicroVis/us_stock.html', context_dict)


def us_flows(request):
    context_dict = {}
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        #special for cml researcher to get info to be used later
        context_dict.update({'username': username})


    return render(request,'MicroVis/us_flows.html', context_dict)

def tailing(request):
    context_dict = {}
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        #special for cml researcher to get info to be used later
        context_dict.update({'username': username})


    return render(request,'MicroVis/tailing.html', context_dict)