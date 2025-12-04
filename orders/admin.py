from django.contrib import admin
from .models import Order, OrderTracking


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['tracking_code', 'customer', 'driver', 'status', 'price', 'created_at']
    list_filter = ['status', 'is_within_nairobi', 'created_at']
    search_fields = ['tracking_code', 'customer__full_name', 'pickup_address', 'delivery_address']
    readonly_fields = ['tracking_code', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

