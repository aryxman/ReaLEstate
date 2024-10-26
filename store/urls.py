from django.urls import path, include
from . import views

urlpatterns=[
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name='process_order'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('success/', views.Success, name='success')
]