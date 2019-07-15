from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'panorama/home.html')

def services(request):
    return render(request,'panorama/services.html')

def contact(request):
    return render(request,'panorama/contact.html')

def about(request):
    return render(request,'panorama/about.html')