"""
URL configuration for pakahome project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/drivers/', include('drivers.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/maps/', include('orders.map_urls')),
    
    # Frontend routes
    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),
    path('dashboard/', TemplateView.as_view(template_name='customer_dashboard.html'), name='customer_dashboard'),
    path('admin-dashboard/', TemplateView.as_view(template_name='admin_dashboard.html'), name='admin_dashboard'),
    path('driver-dashboard/', TemplateView.as_view(template_name='driver_dashboard.html'), name='driver_dashboard'),
    path('track/<str:tracking_code>/', TemplateView.as_view(template_name='tracking.html'), name='tracking'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

