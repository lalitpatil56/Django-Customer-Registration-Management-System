
from django.db.models import fields
from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory

# Create your views here.


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


def products(request):
    products = Product.objects.all()
    params = {}
    params['products'] = products
    return render(request, 'accounts/products.html', params)


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    print(orders)

    params = {'customer': customer,
              'order_count': order_count, 'orders': orders}
    return render(request, 'accounts/customer.html', params)


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


def updateOrder(request, pk):
    form = OrderForm(instance=Order.objects.get(id=pk))

    if request.method == "POST":
        form = OrderForm(request.POST, instance=Order.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('/')

    params = {'form': form}
    return render(request, 'accounts/order_form.html', params)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    params = {'order': order}
    return render(request, 'accounts/delete.html', params)
