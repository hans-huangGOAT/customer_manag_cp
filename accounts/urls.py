from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('customer/', customer, name='customer'),
    path('products/', products, name='products'),
]
