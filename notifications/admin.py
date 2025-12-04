from django.contrib import admin
from .models import SMSLog


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['phone_number', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

