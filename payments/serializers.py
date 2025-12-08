from rest_framework import serializers
from .models import Payment
from orders.serializers import OrderSerializer
from users.serializers import CustomerSerializer


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'order', 'customer', 'phone_number', 'amount',
                  'mpesa_receipt_number', 'transaction_date',
                  'merchant_request_id', 'checkout_request_id',
                  'result_code', 'result_description', 'status',
                  'created_at', 'updated_at']
        read_only_fields = ['mpesa_receipt_number', 'transaction_date',
                           'merchant_request_id', 'checkout_request_id',
                           'result_code', 'result_description',
                           'created_at', 'updated_at']


class STKPushSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
    phone_number = serializers.CharField(max_length=20, required=True)
    
    def validate_phone_number(self, value):
        """Normalize and validate phone number"""
        if not value:
            raise serializers.ValidationError('Phone number is required')
        
        # Remove common separators
        phone = value.replace(' ', '').replace('-', '').replace('+', '').strip()
        
        # Ensure it starts with country code
        if not phone.startswith('254'):
            if phone.startswith('0'):
                phone = '254' + phone[1:]
            else:
                phone = '254' + phone
        
        # Validate length (254 + 9 digits = 12 characters)
        if len(phone) < 12 or len(phone) > 15:
            raise serializers.ValidationError('Invalid phone number format. Use format: 254712345678 or 0712345678')
        
        # Validate it's numeric
        if not phone.isdigit():
            raise serializers.ValidationError('Phone number must contain only digits')
        
        return phone

