from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('customer/<str:pk>', customer, name='customer'),
    path('products/', products, name='products'),

    path('delete_order/<str:pk>', delete_order, name='delete_order'),
    path('create_order/<str:pk>', create_order, name='create_order'),
    path('update_order/<str:pk>', update_order, name='update_order'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),

]
