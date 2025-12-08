from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Payment
from .serializers import PaymentSerializer, STKPushSerializer
from .services import initiate_stk_push
from orders.models import Order
from users.models import Customer
from notifications.services import send_sms_notification
import uuid


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def initiate_payment(request):
    """Initiate M-Pesa STK Push payment"""
    serializer = STKPushSerializer(data=request.data)
    if not serializer.is_valid():
        # Return detailed error messages
        error_messages = []
        for field, errors in serializer.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")
        return Response(
            {'error': 'Validation failed', 'details': serializer.errors, 'messages': error_messages}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = request.user
    if user.role != 'customer':
        return Response(
            {'error': 'Only customers can initiate payments'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    order_id = serializer.validated_data['order_id']
    phone_number = serializer.validated_data['phone_number']
    
    try:
        customer = user.customer_profile
    except Customer.DoesNotExist:
        return Response(
            {'error': 'Customer profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        order = Order.objects.get(id=order_id, customer=customer)
    except Order.DoesNotExist:
        return Response(
            {'error': 'Order not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if payment already exists
    if hasattr(order, 'payment'):
        payment = order.payment
        if payment.status == 'completed':
            return Response(
                {'error': 'Order already paid'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        # Create payment record
        payment = Payment.objects.create(
            order=order,
            customer=customer,
            phone_number=phone_number,
            amount=order.price,
            status='pending'
        )
    
    # Generate callback URL
    callback_url = f"{request.scheme}://{request.get_host()}/api/payments/callback/"
    
    # Initiate STK Push
    merchant_request_id = str(uuid.uuid4())
    response_data = initiate_stk_push(
        phone_number=phone_number,
        amount=order.price,
        order_tracking_code=order.tracking_code,
        callback_url=callback_url
    )
    
    # Check if we got an error response
    if response_data and response_data.get('error'):
        payment.status = 'failed'
        error_message = response_data.get('CustomerMessage') or response_data.get('errorMessage') or 'Payment initiation failed'
        payment.result_description = error_message
        payment.save()
        
        return Response(
            {
                'error': error_message,
                'details': {
                    'errorCode': response_data.get('errorCode'),
                    'errorMessage': response_data.get('errorMessage'),
                    'ResponseCode': response_data.get('ResponseCode'),
                    'ResponseDescription': response_data.get('ResponseDescription'),
                },
                'message': 'Failed to initiate payment. Please check your M-Pesa credentials and try again.'
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if response_data and response_data.get('ResponseCode') == '0':
        payment.merchant_request_id = merchant_request_id
        payment.checkout_request_id = response_data.get('CheckoutRequestID')
        payment.status = 'processing'
        payment.save()
        
        # Update order status
        order.status = 'pending_assignment'
        order.save()
        
        return Response({
            'message': 'Payment request sent. Please check your phone to complete payment.',
            'checkout_request_id': payment.checkout_request_id,
            'payment': PaymentSerializer(payment).data
        }, status=status.HTTP_200_OK)
    else:
        payment.status = 'failed'
        error_message = 'Payment initiation failed'
        error_details = {}
        
        if response_data:
            error_message = response_data.get('CustomerMessage') or response_data.get('errorDescription') or response_data.get('errorMessage') or 'Payment failed'
            error_details = {
                'ResponseCode': response_data.get('ResponseCode'),
                'ResponseDescription': response_data.get('ResponseDescription'),
                'CustomerMessage': response_data.get('CustomerMessage'),
                'errorCode': response_data.get('errorCode'),
                'errorMessage': response_data.get('errorMessage'),
            }
        else:
            error_message = 'No response from M-Pesa API. Please check your API credentials and network connection.'
            error_details = {
                'error': 'M-Pesa API did not respond. This could be due to:',
                'possible_causes': [
                    'Invalid M-Pesa API credentials',
                    'Network connectivity issues',
                    'M-Pesa API service unavailable',
                    'Access token could not be retrieved'
                ]
            }
        
        payment.result_description = error_message
        payment.save()
        
        return Response(
            {
                'error': error_message,
                'details': error_details,
                'message': 'Failed to initiate payment. Please check your M-Pesa credentials and try again.'
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def payment_callback(request):
    """M-Pesa payment callback endpoint"""
    # M-Pesa sends callback data in request body
    data = request.data
    
    body = data.get('Body', {})
    stk_callback = body.get('stkCallback', {})
    
    checkout_request_id = stk_callback.get('CheckoutRequestID')
    result_code = stk_callback.get('ResultCode')
    result_description = stk_callback.get('ResultDesc')
    
    if not checkout_request_id:
        return Response({'error': 'Invalid callback'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        payment = Payment.objects.get(checkout_request_id=checkout_request_id)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if result_code == 0:
        # Payment successful
        callback_metadata = stk_callback.get('CallbackMetadata', {})
        items = callback_metadata.get('Item', [])
        
        receipt_number = None
        transaction_date = None
        
        for item in items:
            if item.get('Name') == 'MpesaReceiptNumber':
                receipt_number = item.get('Value')
            elif item.get('Name') == 'TransactionDate':
                transaction_date = item.get('Value')
        
        payment.status = 'completed'
        payment.mpesa_receipt_number = receipt_number
        payment.result_code = result_code
        payment.result_description = result_description
        
        if transaction_date:
            from datetime import datetime
            try:
                # M-Pesa date format: YYYYMMDDHHMMSS
                payment.transaction_date = datetime.strptime(str(transaction_date), '%Y%m%d%H%M%S')
            except:
                pass
        
        payment.save()
        
        # Update order status
        order = payment.order
        order.status = 'pending_assignment'
        order.save()
        
        # Send confirmation SMS
        send_sms_notification(
            payment.customer.phone,
            f"Payment of KES {payment.amount} for order {order.tracking_code} confirmed. Receipt: {receipt_number}"
        )
        
        return Response({'message': 'Payment confirmed'}, status=status.HTTP_200_OK)
    else:
        # Payment failed
        payment.status = 'failed'
        payment.result_code = result_code
        payment.result_description = result_description
        payment.save()
        
        return Response({'message': 'Payment failed'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def payment_list(request):
    """Get list of payments"""
    user = request.user
    
    if user.role == 'customer':
        try:
            customer = user.customer_profile
            payments = Payment.objects.filter(customer=customer).order_by('-created_at')
        except Customer.DoesNotExist:
            payments = Payment.objects.none()
    elif user.role == 'admin':
        payments = Payment.objects.all().order_by('-created_at')
    else:
        payments = Payment.objects.none()
    
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

