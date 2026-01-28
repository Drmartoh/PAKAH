from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/drivers/', include('drivers.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/maps/', include('orders.map_urls')),

    # KopoKopo callback route
    path('payments/kopokopo/callback/', include('payments.urls')),  # <- added

    # Frontend routes
    path('', ensure_csrf_cookie(TemplateView.as_view(template_name='landing.html')), name='landing'),
    path('dashboard/', ensure_csrf_cookie(TemplateView.as_view(template_name='customer_dashboard.html')), name='customer_dashboard'),
    path('admin-dashboard/', ensure_csrf_cookie(TemplateView.as_view(template_name='admin_dashboard.html')), name='admin_dashboard'),
    path('driver-dashboard/', ensure_csrf_cookie(TemplateView.as_view(template_name='driver_dashboard.html')), name='driver_dashboard'),
    path('track/<str:tracking_code>/', ensure_csrf_cookie(TemplateView.as_view(template_name='tracking.html')), name='tracking'),
    path('terms/', ensure_csrf_cookie(TemplateView.as_view(template_name='terms.html')), name='terms'),
    path('careers/', ensure_csrf_cookie(TemplateView.as_view(template_name='careers.html')), name='careers'),
    path('track/', ensure_csrf_cookie(TemplateView.as_view(template_name='tracking.html')), name='track'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

