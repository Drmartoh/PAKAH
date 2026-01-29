#!/usr/bin/env python
"""
Test admin API endpoints to verify they work.
Run: python test_admin_api.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pakahome.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
import json

User = get_user_model()

def main():
    client = Client()
    
    # Login as admin
    print("1. Logging in as admin...")
    login_response = client.post('/api/auth/login/', {
        'phone': '254700000000',
        'pin': '1234'
    }, content_type='application/json')
    
    if login_response.status_code != 200:
        print(f"   FAILED: Login returned {login_response.status_code}")
        print(f"   Response: {login_response.content.decode()}")
        return 1
    
    print("   OK: Logged in successfully")
    
    # Get current user
    print("\n2. Checking current user...")
    me_response = client.get('/api/auth/me/')
    if me_response.status_code == 200:
        me_data = json.loads(me_response.content)
        print(f"   User role: {me_data.get('user', {}).get('role')}")
        if me_data.get('user', {}).get('role') != 'admin':
            print("   WARNING: User is not admin!")
    else:
        print(f"   FAILED: /api/auth/me/ returned {me_response.status_code}")
    
    # Get orders
    print("\n3. Fetching orders...")
    orders_response = client.get('/api/orders/')
    print(f"   Status: {orders_response.status_code}")
    
    if orders_response.status_code == 200:
        orders_data = json.loads(orders_response.content)
        if isinstance(orders_data, dict) and 'results' in orders_data:
            orders = orders_data['results']
            count = orders_data.get('count', len(orders))
            print(f"   Orders (paginated): {len(orders)} of {count} total")
            print(f"   Next page: {orders_data.get('next', 'None')}")
        elif isinstance(orders_data, list):
            print(f"   Orders (list): {len(orders_data)}")
        else:
            print(f"   Unexpected format: {type(orders_data)}")
            print(f"   Data: {str(orders_data)[:200]}")
        
        if isinstance(orders_data, dict) and 'results' in orders_data:
            orders = orders_data['results']
        elif isinstance(orders_data, list):
            orders = orders_data
        else:
            orders = []
        
        if orders:
            print(f"\n   First order:")
            print(f"     Tracking: {orders[0].get('tracking_code')}")
            print(f"     Status: {orders[0].get('status')}")
            print(f"     Customer: {orders[0].get('customer', {}).get('full_name', 'N/A')}")
            print(f"     Driver: {orders[0].get('driver', {}).get('full_name', 'Not Assigned')}")
        else:
            print("   No orders found")
    else:
        print(f"   FAILED: Response content: {orders_response.content.decode()[:500]}")
    
    # Get available drivers
    print("\n4. Fetching available drivers...")
    drivers_response = client.get('/api/drivers/available/')
    print(f"   Status: {drivers_response.status_code}")
    
    if drivers_response.status_code == 200:
        drivers_data = json.loads(drivers_response.content)
        if isinstance(drivers_data, list):
            print(f"   Available drivers: {len(drivers_data)}")
            for d in drivers_data[:3]:
                print(f"     - {d.get('full_name')} ({d.get('license_number')})")
        else:
            print(f"   Unexpected format: {type(drivers_data)}")
    else:
        print(f"   FAILED: Response: {drivers_response.content.decode()[:500]}")
    
    print("\n" + "="*50)
    print("Test complete!")
    return 0

if __name__ == '__main__':
    sys.exit(main())
