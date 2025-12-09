from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager where phone_number is the unique identifier"""
    
    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        """Create and save a regular user with phone_number"""
        if not phone_number:
            raise ValueError('The phone_number field must be set')
        
        # Normalize phone number
        phone_number = self.normalize_phone(phone_number)
        email = self.normalize_email(email) if email else None
        
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        """Create and save a superuser with phone_number"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(phone_number, email, password, **extra_fields)
    
    @staticmethod
    def normalize_phone(phone):
        """Normalize phone number to 254XXXXXXXXX format"""
        if not phone:
            return phone
        # Remove common separators
        phone = phone.replace(' ', '').replace('-', '').replace('+', '')
        # Ensure it starts with country code
        if not phone.startswith('254'):
            if phone.startswith('0'):
                phone = '254' + phone[1:]
            else:
                phone = '254' + phone
        return phone


class User(AbstractUser):
    """Custom User model with role-based access - uses phone number as username"""
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('driver', 'Driver'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)  # Temporarily allow null for migration
    terms_accepted = models.BooleanField(default=False)
    terms_accepted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Make username use phone_number
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []  # No required fields beyond phone_number
    
    # Use custom manager
    objects = UserManager()
    
    def __str__(self):
        return f"{self.phone_number} ({self.role})"


class Customer(models.Model):
    """Customer profile extending User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)  # Email is optional
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name


class Driver(models.Model):
    """Driver profile extending User"""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    license_number = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(max_length=50, blank=True)
    vehicle_registration = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline')
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.license_number}"

