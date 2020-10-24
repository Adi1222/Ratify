from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import UserForm, Appuserform

# Create your views here.


def login_request(request):
    if request.method == 'POST':
        _username = request.POST.get('username')
        _password = request.POST.get('password')
        user = authenticate(username=_username, password=_password)
        if user is not None:
            login(request, user)
            return HttpResponse("You have successfully signed in !!")
        else:
            messages.error(request, 'The form is invalid.')

    return render(request, "reviews/login.html")


def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        appuserform = Appuserform(request.POST)

        if user_form.is_valid() and appuserform.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            app_user = appuserform.save(commit=False)
            app_user.user = user
            app_user.save()
            login(request, user)
            return redirect('/ratify/home/')
        else:
            print(user_form.errors)
            print(appuserform.errors)
            messages.error(request, user_form.errors)
            messages.error(request, appuserform.errors)
            return redirect('/ratify/signup')

    else:
        userform = UserForm()
        userform1 = Appuserform()
        return render(request, 'reviews/signup.html', {'userform': userform, 'userform1': userform1})


def homepage(request):
    return HttpResponse('Working')
