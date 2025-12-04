from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_sms, name='send_sms'),
    path('logs/', views.SMSLogListView.as_view(), name='sms_logs'),
]

