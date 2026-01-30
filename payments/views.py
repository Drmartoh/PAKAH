from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Payment
from .serializers import PaymentSerializer, STKPushSerializer
from .services import initiate_stk_push, validate_webhook_signature, process_incoming_payment_result
from orders.models import Order
from users.models import Customer
from notifications.services import send_sms_notification
import uuid
import json
import logging

logger = logging.getLogger(__name__)


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
    
    # Callback URL: production uses KOPOKOPO_CALLBACK_URL (e.g. pakaapp.pythonanywhere.com), else request host
    if settings.KOPOKOPO_ENVIRONMENT == 'production':
        callback_url = getattr(
            settings, 'KOPOKOPO_CALLBACK_URL',
            'https://pakaapp.pythonanywhere.com/payments/kopokopo/callback/callback/'
        )
    else:
        # For sandbox, use the request host (works for localhost and ngrok)
        callback_url = f"{request.scheme}://{request.get_host()}/api/payments/callback/"
    
    # Get customer details
    customer_name = customer.full_name if customer.full_name else f"{customer.user.phone_number}"
    customer_email = customer.email if hasattr(customer, 'email') and customer.email else None
    
    # Initiate STK Push
    merchant_request_id = str(uuid.uuid4())
    response_data = initiate_stk_push(
        phone_number=phone_number,
        amount=order.price,
        order_tracking_code=order.tracking_code,
        callback_url=callback_url,
        customer_name=customer_name,
        customer_email=customer_email
    )
    
    # Check if we got an error response
    if not response_data.get('success'):
        payment.status = 'failed'
        error_message = response_data.get('message', 'Payment initiation failed')
        error_details = response_data.get('error_details', {})
        payment.result_description = error_message
        payment.save()
        
        return Response(
            {
                'error': error_message,
                'details': error_details,
                'message': 'Failed to initiate payment. Please try again.'
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Success - payment request initiated
    payment.merchant_request_id = merchant_request_id
    payment.checkout_request_id = response_data.get('payment_request_id', '')
    payment.status = 'processing'
    payment.save()
    
    return Response({
        'message': response_data.get('message', 'Payment request sent. Please check your phone to complete payment.'),
        'payment_request_id': response_data.get('payment_request_id'),
        'payment': PaymentSerializer(payment).data
    }, status=status.HTTP_200_OK)


@csrf_exempt
@require_http_methods(['POST'])
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def payment_callback(request):
    """KopoKopo payment callback endpoint - must be CSRF-exempt for webhook POST from KopoKopo"""
    # Get raw request body for signature validation
    request_body = request.body.decode('utf-8')
    
    # Validate webhook signature
    signature_header = request.headers.get('X-KopoKopo-Signature', '')
    if signature_header and not validate_webhook_signature(request_body, signature_header):
        logger.warning("Invalid webhook signature received")
        return Response({'error': 'Invalid signature'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Parse callback data
    try:
        callback_data = json.loads(request_body)
    except json.JSONDecodeError:
        logger.error("Invalid JSON in callback")
        return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Process the incoming payment result
    result = process_incoming_payment_result(callback_data)
    
    if not result:
        return Response({'error': 'Failed to process callback'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get metadata to find the order
    data = callback_data.get('data', {})
    attributes = data.get('attributes', {})
    metadata = attributes.get('metadata', {})
    order_tracking_code = metadata.get('order_tracking_code') or metadata.get('order_reference')
    
    if not order_tracking_code:
        logger.error("No order tracking code in callback metadata")
        return Response({'error': 'Order tracking code not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        order = Order.objects.get(tracking_code=order_tracking_code)
    except Order.DoesNotExist:
        logger.error(f"Order not found: {order_tracking_code}")
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get or create payment record
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            'customer': order.customer,
            'phone_number': result.get('sender_phone_number', ''),
            'amount': order.price,
            'status': 'pending'
        }
    )
    
    if result.get('success'):
        # Payment successful
        payment.status = 'completed'
        payment.mpesa_receipt_number = result.get('mpesa_receipt_number', '')
        payment.result_code = 0
        payment.result_description = 'Payment successful'
        
        # Parse transaction date
        transaction_date_str = result.get('transaction_date')
        if transaction_date_str:
            from datetime import datetime
            try:
                # KopoKopo uses ISO 8601 format: 2020-10-21T09:30:40+03:00
                # Handle both Z and +03:00 timezone formats
                date_str = transaction_date_str.replace('Z', '+00:00')
                # Remove microseconds if present (format: 2020-10-21T09:30:40.123+03:00)
                if '.' in date_str and '+' in date_str:
                    # Split at dot, take first part, then add timezone
                    date_part, tz_part = date_str.split('+', 1)
                    date_str = date_part.split('.')[0] + '+' + tz_part
                elif '.' in date_str:
                    date_str = date_str.split('.')[0]
                
                # Python 3.7+ supports fromisoformat
                payment.transaction_date = datetime.fromisoformat(date_str)
            except (ValueError, AttributeError) as e:
                logger.warning(f"Could not parse transaction date: {e}, value: {transaction_date_str}")
                # Try simple format without timezone
                try:
                    date_part = transaction_date_str.split('+')[0].split('Z')[0].split('.')[0]
                    payment.transaction_date = datetime.strptime(date_part, '%Y-%m-%dT%H:%M:%S')
                except:
                    logger.error(f"Failed to parse transaction date: {transaction_date_str}")
        
        payment.save()
        
        # Update order status
        order.status = 'pending_assignment'
        order.save()
        
        # Send confirmation SMS
        try:
            # Use customer phone or user phone_number
            customer_phone = getattr(payment.customer, 'phone', None) or payment.customer.user.phone_number
            if customer_phone:
                send_sms_notification(
                    customer_phone,
                    f"Payment of KES {payment.amount} for order {order.tracking_code} confirmed. Receipt: {payment.mpesa_receipt_number}"
                )
        except Exception as e:
            logger.error(f"Failed to send SMS notification: {e}")
        
        logger.info(f"Payment completed for order {order_tracking_code}")
        return Response({'message': 'Payment confirmed'}, status=status.HTTP_200_OK)
    else:
        # Payment failed
        payment.status = 'failed'
        payment.result_code = 1
        payment.result_description = result.get('error_message', 'Payment failed')
        payment.save()
        
        logger.warning(f"Payment failed for order {order_tracking_code}: {result.get('error_message')}")
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

