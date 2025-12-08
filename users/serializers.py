from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Customer, Driver


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number']


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True, min_length=10, max_length=15)
    pin = serializers.CharField(write_only=True, min_length=4, max_length=4)
    email = serializers.EmailField(required=False, allow_blank=True)
    
    class Meta:
        model = Customer
        fields = ['phone', 'pin', 'email', 'full_name', 'address']
    
    def validate_phone(self, value):
        """Normalize phone number (remove spaces, dashes, etc.)"""
        # Remove common separators
        phone = value.replace(' ', '').replace('-', '').replace('+', '')
        # Ensure it starts with country code if not present
        if not phone.startswith('254'):
            if phone.startswith('0'):
                phone = '254' + phone[1:]
            else:
                phone = '254' + phone
        return phone
    
    def validate_pin(self, value):
        """Validate PIN is exactly 4 digits"""
        if not value.isdigit():
            raise serializers.ValidationError('PIN must contain only numbers')
        if len(value) != 4:
            raise serializers.ValidationError('PIN must be exactly 4 digits')
        return value
    
    def create(self, validated_data):
        phone = validated_data.pop('phone')
        pin = validated_data.pop('pin')
        email = validated_data.pop('email', '')
        
        # Check if phone number already exists
        if User.objects.filter(phone_number=phone).exists():
            raise serializers.ValidationError({'phone': 'This phone number is already registered'})
        
        # Create user with phone number as username
        user = User.objects.create_user(
            phone_number=phone,
            email=email or f"{phone}@pakahome.local",  # Use phone-based email if not provided
            password=pin,
            role='customer'
        )
        
        # Use phone-based email if not provided, or None if empty
        customer_email = email if email and email.strip() else None
        
        customer = Customer.objects.create(
            user=user,
            email=customer_email,
            **validated_data
        )
        return customer


class DriverRegistrationSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True, min_length=10, max_length=15)
    pin = serializers.CharField(write_only=True, min_length=4, max_length=4)
    email = serializers.EmailField(required=False, allow_blank=True)
    
    class Meta:
        model = Driver
        fields = ['phone', 'pin', 'email', 'full_name', 
                  'license_number', 'vehicle_type', 'vehicle_registration']
    
    def validate_phone(self, value):
        """Normalize phone number (remove spaces, dashes, etc.)"""
        # Remove common separators
        phone = value.replace(' ', '').replace('-', '').replace('+', '')
        # Ensure it starts with country code if not present
        if not phone.startswith('254'):
            if phone.startswith('0'):
                phone = '254' + phone[1:]
            else:
                phone = '254' + phone
        return phone
    
    def validate_pin(self, value):
        """Validate PIN is exactly 4 digits"""
        if not value.isdigit():
            raise serializers.ValidationError('PIN must contain only numbers')
        if len(value) != 4:
            raise serializers.ValidationError('PIN must be exactly 4 digits')
        return value
    
    def create(self, validated_data):
        phone = validated_data.pop('phone')
        pin = validated_data.pop('pin')
        email = validated_data.pop('email', '')
        
        # Check if phone number already exists
        if User.objects.filter(phone_number=phone).exists():
            raise serializers.ValidationError({'phone': 'This phone number is already registered'})
        
        # Create user with phone number as username
        user = User.objects.create_user(
            phone_number=phone,
            email=email or f"{phone}@pakahome.local",  # Use phone-based email if not provided
            password=pin,
            role='driver'
        )
        
        driver = Driver.objects.create(
            user=user,
            phone=phone,
            **validated_data
        )
        return driver


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    pin = serializers.CharField()
    
    def validate_phone(self, value):
        """Normalize phone number"""
        phone = value.replace(' ', '').replace('-', '').replace('+', '')
        if not phone.startswith('254'):
            if phone.startswith('0'):
                phone = '254' + phone[1:]
            else:
                phone = '254' + phone
        return phone
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        pin = attrs.get('pin')
        
        if phone and pin:
            # Authenticate using phone_number as username
            user = authenticate(username=phone, password=pin)
            if not user:
                raise serializers.ValidationError('Invalid phone number or PIN')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include phone number and PIN')
        
        return attrs


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'user', 'full_name', 'email', 'phone', 'address', 'created_at']


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Driver
        fields = ['id', 'user', 'full_name', 'phone', 'license_number', 
                  'vehicle_type', 'vehicle_registration', 'status', 
                  'current_latitude', 'current_longitude', 'is_active', 'created_at']

