from django.urls import path
from . import views

urlpatterns = [
    path('stkpush/', views.initiate_payment, name='initiate_payment'),
    path('callback/', views.payment_callback, name='payment_callback'),
    path('', views.payment_list, name='payment_list'),
]

