
from django.shortcuts import render
from django.http import HttpResponse
from .models import *

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
