from django.shortcuts import render, redirect
from PUMA.forms import WeatherStation
from PUMA.forms import Area, Lines,  CommentForm
from PUMA.models import Comment
from datetime import datetime, timedelta
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import authenticate, login,logout

# Create your views here.
def test(request):

    book = WeatherStation.objects.all()
    area = Area.objects.all()
    line= Lines.objects.all()
    print(Lines.objects.all().values_list('color'))

    latest_device_list = [[]]

    return render(request,'PUMA/test.html', {'latest_device_list': latest_device_list,'book':book, 'area':area, 'line':line})


def home(request):
    #comments = Comment.objects.filter.order_by('created_date')
    #comments = Comment.objects.latest()#>=datetime.now()-timedelta(days=7))
    #last_ten = Comment.objects.filter.order_by('created_date')[:10]
    #retrieve last 10 comments from database
    comments = Comment.objects.order_by('created_date')[:10]
    # do a force logout
    logout(request)
    return render(request,'PUMA/Home.html', {"comments":comments})

@login_required(redirect_field_name='my_redirect_field', login_url='/puma/register/')
def add_comment_to_post(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)

                comment.save()
                return redirect('../../puma/')
        else:
            form = CommentForm()
        return render(request, 'PUMA/add_comment_to_post.html', {'form': form})

    else:
         return HttpResponse("You are not logged in.")


def transport(request):
    return render(request,'PUMA/transport.html')

def infrastructure(request):
    return render(request,'PUMA/infrastructure.html')

def commercial(request):
    return render(request,'PUMA/commercial.html')

def industrial(request):
    return render(request,'PUMA/industrial.html')

def public(request):
    return render(request,'PUMA/public.html')

def appliances(request):
    return render(request,'PUMA/appliances.html')

def oost(request):
    return render(request,'PUMA/oost.html')

def info(request):
    return render(request,'PUMA/mapInfo.html')

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:

                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('../',context)
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('PUMA/nLogin.html', {}, context)




# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('../',request)