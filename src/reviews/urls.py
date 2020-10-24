from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_request, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.homepage, name='homepage')
]
