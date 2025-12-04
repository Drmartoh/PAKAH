from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Customer, Driver


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number']


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField()
    
    class Meta:
        model = Customer
        fields = ['username', 'password', 'email', 'full_name', 'phone', 'address']
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='customer',
            phone_number=validated_data.get('phone')
        )
        
        customer = Customer.objects.create(
            user=user,
            email=email,
            **validated_data
        )
        return customer


class DriverRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField()
    
    class Meta:
        model = Driver
        fields = ['username', 'password', 'email', 'full_name', 'phone', 
                  'license_number', 'vehicle_type', 'vehicle_registration']
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='driver',
            phone_number=validated_data.get('phone')
        )
        
        driver = Driver.objects.create(
            user=user,
            **validated_data
        )
        return driver


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        
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

