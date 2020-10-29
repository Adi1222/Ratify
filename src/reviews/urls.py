from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_request, name='login'),

    path('signup/', views.signup, name='signup'),

    path('home/', views.homepage, name='homepage'),

    path('review/<int:review_id>/', views.review_detail, name='review_detail'),

    path('review/username>/', views.user_review_list, name='user_review_list'),

    path('categories/', views.categories, name='categories'),

    path('logout/', views.logout_request, name='logout_request'),
]
