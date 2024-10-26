from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
import json
from . import forms
import razorpay
from django.conf import settings

@login_required(login_url='login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            Customer.objects.create(
                user=user,
                name=user.username,  
                email=user.email  

                
            )

            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('store')  
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})


def store(request):
    products=Product.objects.all()
    context={'products': products}
    return render(request, "store/store.html", context)

def cart(request):

    if request.user.is_authenticated:
        customer=request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)  
        items = order.orderitem_set.all()
    else:
        items=[]
        order={'get_cart_total': 0, 'get_cart_items':0, 'shipping':False}

    context={'items': items, 'order':order}
    return render(request, "store/cart.html", context)

def checkout(request):

   


    if request.user.is_authenticated:
        customer=request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)  
        items = order.orderitem_set.all()
    else:
        items=[]
        order={'get_cart_total': 0, 'get_cart_items':0, 'shipping':False}

    amount = order.get_cart_total
    amountt= int(amount)

    client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID, settings.KEY_SECRET))
    data = { "amount": amountt*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    order.razor_pay_order_id= payment['id']
    order.save()

    print(payment)


    context={'items':items, 'order':order, 'payment': payment}
    return render(request, "store/checkout.html", context)

def updateItem(request):
    data = json.loads(request.body)
    productId= data['productId']
    action= data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product =  Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action =='add':
        orderItem.quantity +=1
    
    elif action =='remove':
        orderItem.quantity -=1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe= False)


def processOrder(request):

    data = json.loads(request.body)

    user_data = data['form']
    shipping_data = data['shipping']

    customer = request.user.customer

    
    shipping_address = ShippingAddress.objects.create(
        customer=customer,
        order=Order.objects.get(customer = customer),
        address=shipping_data['address'],
        city=shipping_data['city'],
        state=shipping_data['state'],
        zipcode=shipping_data['zipcode'],
        country=shipping_data['country'],
    )



    print('Data:', request.body)
    return JsonResponse('Payment complete!', safe= False)




# username: xyz
#password: oneone11


def Success(request):

    order_id= request.GET.get('order_id')
    order = Order.objects.get(razor_pay_order_id = order_id)
    order.complete= True
    order.save()
    return HttpResponse('Payment Succesful, Thank you for shopping with us!')


    
    