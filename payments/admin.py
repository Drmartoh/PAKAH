from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'customer', 'amount', 'status', 'mpesa_receipt_number', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order__tracking_code', 'customer__full_name', 'mpesa_receipt_number', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

