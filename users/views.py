from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .serializers import (
    UserSerializer, CustomerRegistrationSerializer, DriverRegistrationSerializer,
    LoginSerializer, CustomerSerializer, DriverSerializer
)
from .models import User, Customer, Driver
from orders.models import Order
from payments.models import Payment


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_customer(request):
    """Register a new customer"""
    serializer = CustomerRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()
        return Response({
            'message': 'Customer registered successfully',
            'customer': CustomerSerializer(customer).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_driver(request):
    """Register a new driver"""
    serializer = DriverRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        driver = serializer.save()
        return Response({
            'message': 'Driver registered successfully',
            'driver': DriverSerializer(driver).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Login user"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        # Get profile data based on role
        profile_data = {}
        if user.role == 'customer':
            try:
                customer = user.customer_profile
                profile_data = CustomerSerializer(customer).data
            except Customer.DoesNotExist:
                pass
        elif user.role == 'driver':
            try:
                driver = user.driver_profile
                profile_data = DriverSerializer(driver).data
            except Driver.DoesNotExist:
                pass
        
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'profile': profile_data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Logout user"""
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """Get current authenticated user"""
    user = request.user
    profile_data = {}
    
    if user.role == 'customer':
        try:
            customer = user.customer_profile
            profile_data = CustomerSerializer(customer).data
        except Customer.DoesNotExist:
            pass
    elif user.role == 'driver':
        try:
            driver = user.driver_profile
            profile_data = DriverSerializer(driver).data
        except Driver.DoesNotExist:
            pass
    
    return Response({
        'user': UserSerializer(user).data,
        'profile': profile_data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def delete_account(request):
    """Permanently delete user account"""
    user = request.user
    
    if user.role != 'customer':
        return Response(
            {'error': 'Only customers can delete their accounts through this endpoint'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Verify PIN
    pin = request.data.get('pin')
    if not pin:
        return Response(
            {'error': 'PIN is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Authenticate with phone and PIN
    authenticated_user = authenticate(request, username=user.phone_number, password=pin)
    if not authenticated_user or authenticated_user != user:
        return Response(
            {'error': 'Invalid PIN. Please enter your correct 4-digit PIN.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Delete associated data
        customer = user.customer_profile
        orders = Order.objects.filter(customer=customer)
        
        # Delete payments associated with orders
        for order in orders:
            if hasattr(order, 'payment'):
                order.payment.delete()
        
        # Delete orders
        orders.delete()
        
        # Delete customer profile
        customer.delete()
        
        # Delete user account
        user.delete()
        
        # Logout the user
        logout(request)
        
        return Response(
            {'message': 'Account deleted successfully'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': f'Error deleting account: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

