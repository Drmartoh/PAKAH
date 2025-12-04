from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.conf import settings
from .models import Order, OrderTracking
from .serializers import OrderSerializer, OrderCreateSerializer
from .services import calculate_price, geocode_address, create_tracking_log
from users.models import Customer, Driver
from notifications.services import send_sms_notification


class OrderListCreateView(generics.ListCreateAPIView):
    """List and create orders"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            try:
                customer = user.customer_profile
                return Order.objects.filter(customer=customer).select_related('customer', 'driver').prefetch_related('tracking_logs').order_by('-created_at')
            except (Customer.DoesNotExist, AttributeError):
                return Order.objects.none()
        elif user.role == 'admin':
            return Order.objects.all().select_related('customer', 'driver').prefetch_related('tracking_logs').order_by('-created_at')
        elif user.role == 'driver':
            try:
                driver = user.driver_profile
                return Order.objects.filter(driver=driver).select_related('customer', 'driver').prefetch_related('tracking_logs').order_by('-created_at')
            except Driver.DoesNotExist:
                return Order.objects.none()
        return Order.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create to handle order creation with proper response"""
        user = request.user
        if user.role != 'customer':
            return Response(
                {'error': 'Only customers can create orders'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            customer = user.customer_profile
        except Customer.DoesNotExist:
            return Response(
                {'error': 'Customer profile not found. Please complete your registration.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Geocode addresses if coordinates not provided
        pickup_lat = serializer.validated_data.get('pickup_latitude')
        pickup_lng = serializer.validated_data.get('pickup_longitude')
        if not pickup_lat or not pickup_lng:
            lat, lng = geocode_address(serializer.validated_data['pickup_address'])
            if lat and lng:
                pickup_lat = lat
                pickup_lng = lng
                serializer.validated_data['pickup_latitude'] = lat
                serializer.validated_data['pickup_longitude'] = lng
        
        delivery_lat = serializer.validated_data.get('delivery_latitude')
        delivery_lng = serializer.validated_data.get('delivery_longitude')
        if not delivery_lat or not delivery_lng:
            lat, lng = geocode_address(serializer.validated_data['delivery_address'])
            if lat and lng:
                delivery_lat = lat
                delivery_lng = lng
                serializer.validated_data['delivery_latitude'] = lat
                serializer.validated_data['delivery_longitude'] = lng
        
        # Calculate price - use default if coordinates not available
        if pickup_lat and pickup_lng and delivery_lat and delivery_lng:
            price, is_within_nairobi = calculate_price(
                pickup_lat, pickup_lng, delivery_lat, delivery_lng
            )
        else:
            # Default to outside Nairobi pricing if geocoding fails
            price = settings.PRICING_OUTSIDE_NAIROBI
            is_within_nairobi = False
        
        serializer.validated_data['price'] = price
        serializer.validated_data['is_within_nairobi'] = is_within_nairobi
        
        order = serializer.save(
            customer=customer,
            status='pending_payment'
        )
        
        # Create initial tracking log
        create_tracking_log(order, 'pending_payment', 'Order created, awaiting payment')
        
        # Return full order details
        order_serializer = OrderSerializer(order)
        headers = self.get_success_headers(order_serializer.data)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve and update order details"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            try:
                customer = user.customer_profile
                return Order.objects.filter(customer=customer)
            except Customer.DoesNotExist:
                return Order.objects.none()
        elif user.role == 'admin':
            return Order.objects.all()
        elif user.role == 'driver':
            try:
                driver = user.driver_profile
                return Order.objects.filter(driver=driver)
            except Driver.DoesNotExist:
                return Order.objects.none()
        return Order.objects.none()


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def track_order(request, tracking_code):
    """Public endpoint to track order by tracking code"""
    try:
        order = Order.objects.get(tracking_code=tracking_code)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response(
            {'error': 'Order not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_order_status(request, order_id):
    """Update order status (admin or driver only)"""
    order = get_object_or_404(Order, id=order_id)
    user = request.user
    
    new_status = request.data.get('status')
    description = request.data.get('description', '')
    
    if not new_status:
        return Response(
            {'error': 'Status is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate status transition
    valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
    if new_status not in valid_statuses:
        return Response(
            {'error': 'Invalid status'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Permission checks
    if user.role == 'driver':
        if order.driver != user.driver_profile:
            return Response(
                {'error': 'Not authorized'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        # Drivers can only update to specific statuses
        if new_status not in ['accepted', 'picked_up', 'delivered']:
            return Response(
                {'error': 'Invalid status for driver'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    old_status = order.status
    order.status = new_status
    
    # Update timestamps
    if new_status == 'picked_up':
        from django.utils import timezone
        order.picked_up_at = timezone.now()
    elif new_status == 'delivered':
        from django.utils import timezone
        order.delivered_at = timezone.now()
    
    order.save()
    
    # Create tracking log
    create_tracking_log(order, new_status, description)
    
    # Send SMS notifications
    if new_status == 'picked_up':
        send_sms_notification(
            order.customer.phone,
            f"Your order {order.tracking_code} has been picked up and is on the way!"
        )
    elif new_status == 'delivered':
        send_sms_notification(
            order.customer.phone,
            f"Your order {order.tracking_code} has been delivered successfully. Thank you!"
        )
    
    return Response({
        'message': 'Status updated successfully',
        'order': OrderSerializer(order).data
    })

