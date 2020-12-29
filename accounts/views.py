from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth import login, logout, authenticate


# Create your views here.

def login(request):
    form = CreateUserForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all().order_by('-date_created')[:5]

    total_orders = orders.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    delivered_orders = Order.objects.filter(status='Delivered').count()
    context = {
        'customers': customers,
        'orders': orders,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
    }
    return render(request, 'accounts/dashboard.html', context)


def customer(request, pk):
    customer = Customer.objects.get(pk=pk)

    orders = customer.order_set.all().order_by('-date_created')
    total_orders = customer.order_set.all().count()

    filter = OrderFilter(request.GET, queryset=orders)
    orders = filter.qs
    context = {
        'customer': customer,
        'orders': orders,
        'filter': filter,
        'total_orders': total_orders,
    }
    return render(request, 'accounts/customer.html', context)


def create_order(request, pk):
    customer = Customer.objects.get(pk=pk)
    OrdersForm = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    formset = OrdersForm(queryset=customer.order_set.none(), instance=customer)
    if request.method == 'POST':
        formset = OrdersForm(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {
        'forms': formset,
    }
    return render(request, 'accounts/create_orders.html', context)


def products(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'accounts/products.html', context)


def delete_order(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {
        'item': order,
    }
    return render(request, 'accounts/delete_order.html', context)


def update_order(request, pk):
    order = Order.objects.get(pk=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {
        'form': form,
    }
    return render(request, 'accounts/update_order.html', context)
