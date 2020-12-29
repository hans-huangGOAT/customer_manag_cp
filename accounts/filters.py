from django_filters import FilterSet
from .models import *


class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']
