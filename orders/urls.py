from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListCreateView.as_view(), name='order_list_create'),
    path('<int:id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('tracking/<str:tracking_code>/', views.track_order, name='track_order'),
    path('<int:order_id>/status/', views.update_order_status, name='update_order_status'),
]

