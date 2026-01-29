from django.urls import path
from . import views

urlpatterns = [
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/driver/', views.register_driver, name='register_driver'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('me/', views.current_user, name='current_user'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('customers/', views.list_customers, name='list_customers'),
    path('drivers/', views.list_drivers, name='list_drivers'),
]

