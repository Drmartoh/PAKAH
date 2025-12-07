"""
Test script to verify the application is working correctly
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pakahome.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from users.models import Customer
from orders.models import Order
import json

User = get_user_model()

def test_homepage():
    """Test homepage loads"""
    print("Testing homepage...")
    client = Client(HTTP_HOST='localhost')
    response = client.get('/')
    assert response.status_code == 200, f"Homepage returned {response.status_code}"
    print("✅ Homepage loads successfully")

def test_dashboard():
    """Test dashboard loads"""
    print("Testing dashboard...")
    client = Client(HTTP_HOST='localhost')
    response = client.get('/dashboard/')
    assert response.status_code == 200, f"Dashboard returned {response.status_code}"
    print("✅ Dashboard loads successfully")

def test_autocomplete_api():
    """Test autocomplete API"""
    print("Testing autocomplete API...")
    client = Client(HTTP_HOST='localhost')
    response = client.get('/api/maps/autocomplete/?query=nairobi')
    assert response.status_code == 200, f"Autocomplete API returned {response.status_code}"
    data = json.loads(response.content)
    assert 'predictions' in data, "Autocomplete response missing 'predictions'"
    print(f"✅ Autocomplete API working - found {len(data.get('predictions', []))} predictions")

def test_geocode_api():
    """Test geocode API"""
    print("Testing geocode API...")
    client = Client(HTTP_HOST='localhost')
    response = client.get('/api/maps/geocode/?address=Nairobi')
    assert response.status_code == 200, f"Geocode API returned {response.status_code}"
    data = json.loads(response.content)
    assert 'results' in data, "Geocode response missing 'results'"
    print("✅ Geocode API working")

def test_settings():
    """Test settings configuration"""
    print("Testing settings...")
    from django.conf import settings
    
    assert hasattr(settings, 'GOOGLE_MAPS_API_KEY'), "GOOGLE_MAPS_API_KEY not configured"
    assert settings.GOOGLE_MAPS_API_KEY, "GOOGLE_MAPS_API_KEY is empty"
    print(f"✅ Google Maps API key configured: {settings.GOOGLE_MAPS_API_KEY[:20]}...")
    
    assert 'pakahome.context_processors.google_maps_api_key' in settings.TEMPLATES[0]['OPTIONS']['context_processors'], \
        "Context processor not configured"
    print("✅ Context processor configured")

def test_templates():
    """Test template loading"""
    print("Testing templates...")
    from django.template.loader import get_template
    
    templates = ['landing.html', 'customer_dashboard.html', 'base.html']
    for template_name in templates:
        try:
            template = get_template(template_name)
            print(f"✅ Template {template_name} loads successfully")
        except Exception as e:
            print(f"❌ Template {template_name} failed: {e}")
            raise

def test_models():
    """Test models"""
    print("Testing models...")
    assert User.objects.count() >= 0, "User model issue"
    assert Order.objects.count() >= 0, "Order model issue"
    print("✅ Models working correctly")

def main():
    """Run all tests"""
    print("=" * 50)
    print("PAKA HOME Application Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        test_settings,
        test_templates,
        test_homepage,
        test_dashboard,
        test_autocomplete_api,
        test_geocode_api,
        test_models,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    print("=" * 50)
    
    if failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())

