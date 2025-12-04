from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import Driver
from users.serializers import DriverSerializer
from orders.models import Order
from orders.serializers import OrderSerializer


class DriverListView(generics.ListAPIView):
    """List all drivers (admin only)"""
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role != 'admin':
            return Driver.objects.none()
        return Driver.objects.filter(is_active=True)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def available_drivers(request):
    """Get list of available drivers"""
    if request.user.role != 'admin':
        return Response(
            {'error': 'Only admins can view available drivers'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    drivers = Driver.objects.filter(status='available', is_active=True)
    serializer = DriverSerializer(drivers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def assign_driver(request, order_id):
    """Assign driver to order (admin only)"""
    if request.user.role != 'admin':
        return Response(
            {'error': 'Only admins can assign drivers'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    order = get_object_or_404(Order, id=order_id)
    driver_id = request.data.get('driver_id')
    
    if not driver_id:
        return Response(
            {'error': 'driver_id is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    driver = get_object_or_404(Driver, id=driver_id, is_active=True)
    
    if driver.status != 'available':
        return Response(
            {'error': 'Driver is not available'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    order.driver = driver
    order.status = 'assigned'
    order.save()
    
    # Update driver status
    driver.status = 'busy'
    driver.save()
    
    # Create tracking log
    from orders.services import create_tracking_log
    create_tracking_log(order, 'assigned', f'Order assigned to driver {driver.full_name}')
    
    # Send SMS to driver
    from notifications.services import send_sms_notification
    send_sms_notification(
        driver.phone,
        f"New order {order.tracking_code} assigned to you. Pickup: {order.pickup_address}"
    )
    
    return Response({
        'message': 'Driver assigned successfully',
        'order': OrderSerializer(order).data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_driver_status(request, driver_id):
    """Update driver status (driver only)"""
    user = request.user
    if user.role != 'driver':
        return Response(
            {'error': 'Only drivers can update their status'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        driver = user.driver_profile
        if driver.id != driver_id:
            return Response(
                {'error': 'Not authorized'}, 
                status=status.HTTP_403_FORBIDDEN
            )
    except Driver.DoesNotExist:
        return Response(
            {'error': 'Driver profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    new_status = request.data.get('status')
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')
    
    if new_status:
        if new_status not in ['available', 'busy', 'offline']:
            return Response(
                {'error': 'Invalid status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        driver.status = new_status
    
    if latitude and longitude:
        driver.current_latitude = latitude
        driver.current_longitude = longitude
    
    driver.save()
    
    return Response({
        'message': 'Status updated successfully',
        'driver': DriverSerializer(driver).data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_order(request, order_id):
    """Driver accepts an assigned order"""
    user = request.user
    if user.role != 'driver':
        return Response(
            {'error': 'Only drivers can accept orders'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        driver = user.driver_profile
    except Driver.DoesNotExist:
        return Response(
            {'error': 'Driver profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    order = get_object_or_404(Order, id=order_id, driver=driver)
    
    if order.status != 'assigned':
        return Response(
            {'error': 'Order is not in assigned status'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    order.status = 'accepted'
    order.save()
    
    # Create tracking log
    from orders.services import create_tracking_log
    create_tracking_log(order, 'accepted', f'Order accepted by driver {driver.full_name}')
    
    # Send SMS to customer
    from notifications.services import send_sms_notification
    send_sms_notification(
        order.customer.phone,
        f"Driver {driver.full_name} has accepted your order {order.tracking_code}. They will pick up soon!"
    )
    
    return Response({
        'message': 'Order accepted successfully',
        'order': OrderSerializer(order).data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def driver_orders(request):
    """Get orders assigned to current driver"""
    user = request.user
    if user.role != 'driver':
        return Response(
            {'error': 'Only drivers can view their orders'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        driver = user.driver_profile
        orders = Order.objects.filter(driver=driver).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    except Driver.DoesNotExist:
        return Response(
            {'error': 'Driver profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

