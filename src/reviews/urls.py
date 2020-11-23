from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_request, name='login'),

    path('signup/', views.signup, name='signup'),

    path('home/', views.homepage, name='homepage'),

    path('review/<int:review_id>/', views.review_detail, name='review_detail'),

    path('categories/', views.categories, name='categories'),

    path('addproduct/', views.addproduct, name='addproduct'),

    path('category/<int:cid>/', views.products, name='products'),

    path('category/<int:cid>/<int:pid>/',
         views.product_detail, name='product_detail'),

    path('category/<int:cid>/<int:pid>/add_review/',
         views.add_review, name='add_review'),

    path('review/user/', views.user_review_list, name='user_review_list'),

    path('review/user/<username>/',
         views.user_review_list, name='user_review_list'),

    path('review/delete/<int:review_id>/',
         views.delete_review, name='delete_review'),

    path('review/Edit/<int:review_id>/',
         views.edit_review, name='edit_review'),


    path('logout/', views.logout_request, name='logout_request'),
]
