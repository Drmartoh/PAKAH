from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Customer, Driver


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'phone_number', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number')}),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'created_at']
    search_fields = ['full_name', 'email', 'phone']


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'license_number', 'status', 'is_active']
    list_filter = ['status', 'is_active']
    search_fields = ['full_name', 'phone', 'license_number']

