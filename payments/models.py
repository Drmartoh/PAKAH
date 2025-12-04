from django.db import models
from orders.models import Order
from users.models import Customer


class Payment(models.Model):
    """Payment model for M-Pesa transactions"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    
    # M-Pesa details
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_receipt_number = models.CharField(max_length=50, blank=True, null=True)
    transaction_date = models.DateTimeField(null=True, blank=True)
    
    # Transaction details
    merchant_request_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    checkout_request_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    result_code = models.IntegerField(null=True, blank=True)
    result_description = models.TextField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment for Order {self.order.tracking_code} - {self.status}"

