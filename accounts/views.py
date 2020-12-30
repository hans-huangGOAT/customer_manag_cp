from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *


# Create your views here.

def logout_page(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect.')
    context = {

    }
    return render(request, 'accounts/login.html', context)


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Accoutn was created for ' + username)
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


@admin_only
@login_required(login_url='login')
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


@login_required(login_url='login')
def user(request):
    context = {

    }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
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


@allowed_user(allowed_roles=['admin'])
@login_required(login_url='login')
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


@allowed_user(allowed_roles=['admin'])
@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'accounts/products.html', context)


@allowed_user(allowed_roles=['admin'])
@login_required(login_url='login')
def delete_order(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {
        'item': order,
    }
    return render(request, 'accounts/delete_order.html', context)


@allowed_user(allowed_roles=['admin'])
@login_required(login_url='login')
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
