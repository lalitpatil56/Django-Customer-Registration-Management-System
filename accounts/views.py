
from django.db.models import fields
from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter


from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.

# Register Page


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)

# Login Page


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)

# logout function


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_orders = orders.count()
    total_customers = customers.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    params = {'customers': customers, 'orders': orders, 'total_orders': total_orders,
              'total_customers': total_customers, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', params)


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    params = {}
    params['products'] = products
    return render(request, 'accounts/products.html', params)


@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    params = {'customer': customer,
              'order_count': order_count, 'orders': orders, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', params)


@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    params = {'formset': formset}
    return render(request, 'accounts/order_form.html', params)


@login_required(login_url='login')
def updateOrder(request, pk):
    form = OrderForm(instance=Order.objects.get(id=pk))

    if request.method == "POST":
        form = OrderForm(request.POST, instance=Order.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('/')

    params = {'form': form}
    return render(request, 'accounts/order_form.html', params)


@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    params = {'order': order}
    return render(request, 'accounts/delete.html', params)
