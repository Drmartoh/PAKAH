from rest_framework import serializers
from .models import Order, OrderTracking
from users.serializers import CustomerSerializer, DriverSerializer


class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTracking
        fields = ['id', 'status', 'location_latitude', 'location_longitude', 
                  'description', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    tracking_logs = OrderTrackingSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'tracking_code', 'customer', 'driver', 
                  'pickup_name', 'pickup_phone', 'pickup_address',
                  'pickup_latitude', 'pickup_longitude',
                  'delivery_name', 'delivery_phone', 'delivery_address',
                  'delivery_latitude', 'delivery_longitude',
                  'parcel_description', 'parcel_weight', 'special_instructions',
                  'is_within_nairobi', 'price', 'status',
                  'created_at', 'updated_at', 'picked_up_at', 'delivered_at',
                  'tracking_logs']
        read_only_fields = ['tracking_code', 'customer', 'status', 
                           'created_at', 'updated_at', 'picked_up_at', 'delivered_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['pickup_name', 'pickup_phone', 'pickup_address',
                  'pickup_latitude', 'pickup_longitude',
                  'delivery_name', 'delivery_phone', 'delivery_address',
                  'delivery_latitude', 'delivery_longitude']
        # Removed: parcel_description, parcel_weight, special_instructions
    
    def to_internal_value(self, data):
        """Round coordinates before validation to avoid max_digits error"""
        from decimal import Decimal, ROUND_DOWN
        
        # Round coordinates if they exist
        for field in ['pickup_latitude', 'pickup_longitude', 'delivery_latitude', 'delivery_longitude']:
            if field in data and data[field] is not None and data[field] != '':
                try:
                    # Round to 6 decimal places
                    value = Decimal(str(data[field])).quantize(Decimal('0.000001'), rounding=ROUND_DOWN)
                    data[field] = str(value)
                except (ValueError, TypeError, AttributeError):
                    pass
        
        return super().to_internal_value(data)
    
    def validate(self, attrs):
        # Validate that at least one address is provided
        if not attrs.get('pickup_address') or not attrs.get('delivery_address'):
            raise serializers.ValidationError("Both pickup and delivery addresses are required")
        
        return attrs

