#!/usr/bin/env python
"""
System Test Script for PAKA HOME
Tests the system configuration and identifies issues
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pakahome.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)

from django.conf import settings
from django.db import connection
from django.core.management import call_command
from django.urls import get_resolver

def test_imports():
    """Test if all required modules can be imported"""
    print("\n📦 Testing Imports...")
    issues = []
    
    try:
        from users.models import User, Customer, Driver
        print("  ✓ User models imported")
    except Exception as e:
        issues.append(f"User models: {e}")
        print(f"  ✗ User models: {e}")
    
    try:
        from orders.models import Order, OrderTracking
        print("  ✓ Order models imported")
    except Exception as e:
        issues.append(f"Order models: {e}")
        print(f"  ✗ Order models: {e}")
    
    try:
        from payments.models import Payment
        print("  ✓ Payment models imported")
    except Exception as e:
        issues.append(f"Payment models: {e}")
        print(f"  ✗ Payment models: {e}")
    
    try:
        from notifications.services import send_sms_notification
        print("  ✓ Notification services imported")
    except Exception as e:
        issues.append(f"Notification services: {e}")
        print(f"  ✗ Notification services: {e}")
    
    try:
        from payments.services import initiate_stk_push
        print("  ✓ Payment services imported")
    except Exception as e:
        issues.append(f"Payment services: {e}")
        print(f"  ✗ Payment services: {e}")
    
    return len(issues) == 0

def test_database():
    """Test database connection"""
    print("\n🗄️  Testing Database...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("  ✓ Database connection successful")
        return True
    except Exception as e:
        print(f"  ✗ Database connection failed: {e}")
        print("  ⚠ Make sure PostgreSQL is running and credentials are correct")
        return False

def test_settings():
    """Test critical settings"""
    print("\n⚙️  Testing Settings...")
    issues = []
    
    if not settings.SECRET_KEY or settings.SECRET_KEY == 'django-insecure-change-this-in-production':
        issues.append("SECRET_KEY is using default value")
        print("  ⚠ SECRET_KEY is using default value")
    else:
        print("  ✓ SECRET_KEY configured")
    
    if not settings.MPESA_CONSUMER_KEY:
        issues.append("M-Pesa Consumer Key not configured")
        print("  ✗ M-Pesa Consumer Key not configured")
    else:
        print("  ✓ M-Pesa Consumer Key configured")
    
    if not settings.MPESA_CONSUMER_SECRET:
        issues.append("M-Pesa Consumer Secret not configured")
        print("  ✗ M-Pesa Consumer Secret not configured")
    else:
        print("  ✓ M-Pesa Consumer Secret configured")
    
    if not settings.GOOGLE_MAPS_API_KEY:
        issues.append("Google Maps API Key not configured")
        print("  ✗ Google Maps API Key not configured")
    else:
        print("  ✓ Google Maps API Key configured")
    
    return len(issues) == 0

def test_urls():
    """Test URL configuration"""
    print("\n🔗 Testing URLs...")
    try:
        resolver = get_resolver()
        url_count = len([p for p in resolver.url_patterns])
        print(f"  ✓ URL configuration loaded ({url_count} patterns)")
        return True
    except Exception as e:
        print(f"  ✗ URL configuration error: {e}")
        return False

def test_templates():
    """Test template configuration"""
    print("\n📄 Testing Templates...")
    from django.template.loader import get_template
    
    templates_to_test = [
        'landing.html',
        'customer_dashboard.html',
        'admin_dashboard.html',
        'driver_dashboard.html',
        'tracking.html',
        'base.html'
    ]
    
    issues = []
    for template_name in templates_to_test:
        try:
            get_template(template_name)
            print(f"  ✓ {template_name} found")
        except Exception as e:
            issues.append(f"{template_name}: {e}")
            print(f"  ✗ {template_name}: {e}")
    
    return len(issues) == 0

def test_apps():
    """Test installed apps"""
    print("\n📱 Testing Apps...")
    required_apps = ['users', 'orders', 'drivers', 'payments', 'notifications']
    missing_apps = []
    
    for app in required_apps:
        if app in settings.INSTALLED_APPS:
            print(f"  ✓ {app} installed")
        else:
            missing_apps.append(app)
            print(f"  ✗ {app} not installed")
    
    return len(missing_apps) == 0

def main():
    print("=" * 60)
    print("PAKA HOME System Test")
    print("=" * 60)
    
    results = {
        'imports': test_imports(),
        'database': test_database(),
        'settings': test_settings(),
        'urls': test_urls(),
        'templates': test_templates(),
        'apps': test_apps()
    }
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name.upper():15} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! System is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run migrations: python manage.py migrate")
        print("3. Check your .env file for API credentials")
        return 1

if __name__ == '__main__':
    sys.exit(main())

