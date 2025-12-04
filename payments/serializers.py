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
    order_id = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=15)

