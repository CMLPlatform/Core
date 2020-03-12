from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'panorama/home.html')


def services(request):
    return render(request, 'panorama/services.html')


def contact(request):
    return render(request, 'panorama/contact.html')


def about(request):
    return render(request, 'panorama/about.html')


def methods(request):
    return render(request, 'panorama/methods.html')


def mfa(request):
    return render(request, 'panorama/mfa.html')


def school(request):
    return render(request, 'panorama/summerschool.html')
