from django.urls import path
from . import views

urlpatterns = [
    path('', views.DriverListView.as_view(), name='driver_list'),
    path('available/', views.available_drivers, name='available_drivers'),
    path('<int:driver_id>/status/', views.update_driver_status, name='update_driver_status'),
    path('orders/', views.driver_orders, name='driver_orders'),
    path('orders/<int:order_id>/accept/', views.accept_order, name='accept_order'),
    path('assign/<int:order_id>/', views.assign_driver, name='assign_driver'),
]

