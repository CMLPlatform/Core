
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from CMLMasterProject.forms import SignUpForm
from CMLMasterProject.settings import AUTHENTICATION_KEY_RESEARCH, AUTHENTICATION_KEY_STUDENT
from django.contrib import messages
from django.contrib.auth.models import Group
#this is the first page of the Web-app
def homePage(request):
    context_dict = {}
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        #special for cml researcher to get info to be used later
        context_dict.update({'username': username})

    #return render_to_response('/IEMasterProject/HomePage.html', context_dict, context)
    return render(request,'CMLMasterProject/HomePage.html', context_dict)

def exploratory(request):
    context_dict = {}
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        #special for cml researcher to get info to be used later
        context_dict.update({'username': username})
    return render(request, 'CMLMasterProject/explore.html', context_dict)

def about(request):
    context_dict = {}
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        #special for cml researcher to get info to be used later
        context_dict.update({'username': username})
    return render(request, 'CMLMasterProject/about.html', context_dict)

#default signup method for decisionmakers and companies
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            #send success message
            # messages.add_message(request, level, message, extra_tags='', fail_silently=False)
            messages.add_message(request, messages.INFO, "Your signup was successful, you are now logged in.")
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'CMLMasterProject/sign-up.html', {'form': form})

def cml_signup(request):
    #sign up for CML members
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        #get the form and validate
        if form.is_valid():


            #user.profile.topics = form.cleaned_data.get('topics')
            #get the authentication key
            authenticationKey = form.cleaned_data.get('authentication_key')
            #check if authentication key is valid
            if authenticationKey == AUTHENTICATION_KEY_RESEARCH:
                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                #save the topics in the profile
                user.profile.topics = form.cleaned_data.get('topics')

                #store new user
                user.save()
                #create group if not already exist
                new_group, created = Group.objects.get_or_create(name='Editors')
                # add user to Moderator group
                user.groups.add(Group.objects.get(name='Editors'))
                #login
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                # send success message
                # messages.add_message(request, level, message, extra_tags='', fail_silently=False)
                messages.add_message(request, messages.INFO, "Your signup was successful, you are now logged in.")
                return redirect('/')


            if authenticationKey == AUTHENTICATION_KEY_STUDENT:
                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                # save the topics in the profile
                user.profile.topics = form.cleaned_data.get('topics')
                # add user to student group
                #create group if not already exist
                new_group, created = Group.objects.get_or_create(name='students')
                # add user to Moderator group
                user.groups.add(Group.objects.get(name='students'))
                # store new user
                user.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                # send success message
                # messages.add_message(request, level, message, extra_tags='', fail_silently=False)
                messages.add_message(request, messages.INFO, "Your signup was successful, you are now logged in.")
                return redirect('/')
            else:
                return render(request, 'CMLMasterProject/cml-sign-up.html',
                              {'form': form, 'status': 'Invalid authentication key supplied!'})
    else:
        form = SignUpForm()
    return render(request, 'CMLMasterProject/cml-sign-up.html', {'form': form})