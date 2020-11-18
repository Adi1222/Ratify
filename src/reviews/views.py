from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import UserForm, Appuserform, AddProductForm, ReviewForm
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage

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
    allproducts = Product.objects.all()

    '''if allproducts != None:
        for product in Product.objects.all():
            if product.average_rating >= 3 and product.total_rating > 10:
                top_products.push(product)'''

    return render(request, 'reviews/homepage.html', {'latest_review_list': latest_review_list, 'top_products': top_products})


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def user_review_list(request, username=None):
    user = None
    if not username:
        user = request.user
    else:
        user = User.objects.filter(username=username)

    appuser = Appuser.objects.get(user=user)    
    latest_review_list = Review.objects.filter(rated_by=appuser).order_by('-pub_date')


    context = {
        'latest_review_list': latest_review_list,
        'username': user.username,
        'appuser': appuser

    }
    return render(request, 'reviews/user_review_list.html', context)


def categories(request):
    categories = Category.objects.all()
    return render(request, 'reviews/categories.html', {'categories': categories})


def addproduct(request):
    if request.method == 'POST':
        pform = AddProductForm(request.POST, request.FILES)
        if pform.is_valid():
            data = pform.cleaned_data
            img = data["pimg"]
            print(img)
            product = pform.save(commit=False)
            product.created_by = request.user.username
            product.save()
            return redirect('/ratify/home/')

            '''
            pname = request.POST['pname']
            company = request.POST['company']
            price = request.POST['price']
            cat = request.POST['category']
            category = Category.objects.get(catname=cat)
            website = request.POST['website']
            specification = request.POST['speci']
            data = pform.cleaned_data
            image = data["pimg"]
            print(image)
            print()

            if image != None:
                product = Product(pname=pname, company=company, price=price, category=category, website=website,
                                  specification=specification, pimg=image, created_by=request.user.username)
                # product.save()

                fs = FileSystemStorage()
                filename = fs.save(image.name, image)

                uploaded_file_url = fs.url(filename)
                print(uploaded_file_url)

            else:
                pass'''
        else:
            print('hi')
            categories = Category.objects.all()
            pform = AddProductForm()
            return render(request, 'reviews/addproduct.html', {'categories': categories, 'pform': pform})

    else:
        categories = Category.objects.all()
        pform = AddProductForm()
        return render(request, 'reviews/addproduct.html', {'categories': categories, 'pform': pform})


def products(request, cid):
    #products = Product.objects.get(category_id=cid)
    products = get_object_or_404(Product, category_id=cid)
    category = Category.objects.get(id=cid)
    return render(request, 'reviews/products.html')


def product_detail(request, cid, pid):
    product = Product.objects.filter(pk=pid, category_id=cid)
    form = ReviewForm()
    return render(request, 'reviews/product_detail.html', {'product': product, 'form': form})

def add_review(request, cid, pid):
    product = Product.objects.filter(pk=pid, category_id=cid)
    category = get_object_or_404(Category, pk=cid)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            user_name = form.cleaned_data['user_name']
            review = Review()
            review.product = product
            review.category = category
            review.rated_by = request.user
            review.rating = rating
            review.comment = comment
            review.pub_date = datetime.datetime.now()
            review.save()
            return HttpResponseRedirect(reverse('reviews:`product_detail', args=(product.id,)))

    form = ReviewForm()
    return render(request, 'reviews/product_detail.html', {'product': product, 'form': form})
            


def logout_request(request):
    logout(request)
    return redirect('/ratify/login')
