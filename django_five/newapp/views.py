from django.shortcuts import render
from newapp.forms import UserForm, UserProfileInfoform
from newapp.models import UserProfileInfo
from . import forms
from django.contrib.auth.models import User




from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    return render(request, 'newapp/index.html')

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileInfoform(request.POST)

        if user_form.is_valid() and userprofile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = userprofile_form.save(commit = False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors, userprofile_form.errors)
    else:
        user_form = UserForm()
        userprofile_form = UserProfileInfoform()

    mydict = {'userform': user_form, 'profileform': userprofile_form, 'registered': registered }
    return render (request, 'newapp/registration.html',context = mydict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account Not Active')
        else:
            print('Someone tried to login and failed')
            print('Username:{}, password{}'.format(username,password))
            return HttpResponse('invalid login details supplied')
    else:
        return render(request,'newapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponse('index')

@login_required
def special(request):
    return HttpResponse('You are logged in')
