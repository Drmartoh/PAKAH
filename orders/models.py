from django.db import models
from django.conf import settings
from users.models import Customer, Driver
import uuid


class Order(models.Model):
    """Order model for parcel delivery"""
    STATUS_CHOICES = [
        ('pending_payment', 'Pending Payment'),
        ('pending_assignment', 'Pending Assignment'),
        ('assigned', 'Assigned'),
        ('accepted', 'Accepted by Driver'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    tracking_code = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # Pickup details
    pickup_name = models.CharField(max_length=255)
    pickup_phone = models.CharField(max_length=15)
    pickup_address = models.TextField()
    pickup_latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    pickup_longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    
    # Delivery details
    delivery_name = models.CharField(max_length=255)
    delivery_phone = models.CharField(max_length=15)
    delivery_address = models.TextField()
    delivery_latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    delivery_longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    
    # Order details
    parcel_description = models.TextField(blank=True)
    parcel_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    special_instructions = models.TextField(blank=True)
    
    # Pricing
    is_within_nairobi = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = self.generate_tracking_code()
        super().save(*args, **kwargs)
    
    def generate_tracking_code(self):
        """Generate unique tracking code"""
        return f"PAKA{str(uuid.uuid4())[:8].upper()}"
    
    def __str__(self):
        return f"Order {self.tracking_code} - {self.status}"


class OrderTracking(models.Model):
    """Track order status changes and location updates"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tracking_logs')
    status = models.CharField(max_length=20)
    location_latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    location_longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order.tracking_code} - {self.status} at {self.created_at}"

