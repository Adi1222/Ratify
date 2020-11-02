from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import UserForm, Appuserform
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def login_request(request):
    if request.method == 'POST':
        _username = request.POST.get('username')
        _password = request.POST.get('password')
        print(_username)
        print(_password)

        try:
            u = User.objects.get(username=_username)
            login(request, u)
            if u is not None:
                # return HttpResponse("You have successfully signed in !!")
                # messages.success(
                #    request, f"You are now logged in as {request.user.username}")
                return redirect('/ratify/home')
            else:
                messages.error(request, 'The form is invalid.')
        except User.DoesNotExist:
            messages.error(request, 'The form is invalid.')

        # uu = authenticate(username=_username, password=_password)
        # print(uu)

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
    latest_review_list = Review.objects.order_by('-pub_date')[:10]
    top_products = []
    for product in Product.objects.all():
        if product.average_rating >= 3 and product.total_rating > 10:
            top_products.push(product)

    return render(request, 'reviews/homepage.html', {'latest_review_list': latest_review_list, 'top_products': top_products})


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def user_review_list(request, username=None):
    user = None

    if not username:
        user = request.user

    user = User.objects.get(username=username)

    latest_review_list = Review.objects.filter(
        rated_by=user).order_by('-pub_date')
    context = {
        'latest_review_list': latest_review_list,
        'username': username,
    }
    return render(request, 'reviews/user_review_list.html', context)


def categories(request):
    categories = Category.objects.all()
    return render(request, 'reviews/categories.html', {'categories': categories})


def logout_request(request):
    logout(request)
    return redirect('/ratify/login')
