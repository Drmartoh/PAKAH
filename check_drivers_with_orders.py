#!/usr/bin/env python
"""
Check which drivers have assigned orders
Run: python check_drivers_with_orders.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pakahome.settings')
django.setup()

from orders.models import Order
from users.models import Driver

def main():
    print("="*60)
    print("DRIVERS WITH ASSIGNED ORDERS")
    print("="*60)
    
    # Get all orders with drivers
    orders_with_drivers = Order.objects.filter(driver__isnull=False).select_related('driver').order_by('driver__id', '-created_at')
    
    if orders_with_drivers.count() == 0:
        print("\nNo orders are currently assigned to any drivers.")
        print("\nTo assign orders:")
        print("1. Log in as admin at http://127.0.0.1:8000/admin-dashboard/")
        print("2. Find orders with status 'Pending Assignment'")
        print("3. Click 'Assign Driver' and select an available driver")
    else:
        print(f"\nTotal orders with assigned drivers: {orders_with_drivers.count()}\n")
        
        # Group by driver
        drivers_dict = {}
        for order in orders_with_drivers:
            driver_id = order.driver.id
            if driver_id not in drivers_dict:
                drivers_dict[driver_id] = {
                    'driver': order.driver,
                    'orders': []
                }
            drivers_dict[driver_id]['orders'].append(order)
        
        # Display results
        for driver_id, data in drivers_dict.items():
            driver = data['driver']
            orders = data['orders']
            print(f"\n{'='*60}")
            print(f"DRIVER: {driver.full_name}")
            print(f"{'='*60}")
            print(f"  ID: {driver.id}")
            print(f"  Phone: {driver.phone}")
            print(f"  License: {driver.license_number}")
            print(f"  Status: {driver.status}")
            print(f"  Total Orders: {len(orders)}")
            print(f"\n  Orders:")
            for order in orders:
                print(f"    - {order.tracking_code}: {order.status} | From: {order.pickup_address[:50]}... | To: {order.delivery_address[:50]}...")
            
            print(f"\n  LOGIN CREDENTIALS:")
            print(f"    Phone: {driver.phone}")
            print(f"    PIN: 1234")
            print(f"    Dashboard: http://127.0.0.1:8000/driver-dashboard/")
    
    print("\n" + "="*60)
    print("ALL DRIVERS IN SYSTEM")
    print("="*60)
    all_drivers = Driver.objects.all().order_by('id')
    if all_drivers.count() == 0:
        print("\nNo drivers found in the system.")
    else:
        print(f"\nTotal drivers: {all_drivers.count()}\n")
        for driver in all_drivers:
            order_count = driver.orders.count()
            print(f"  ID: {driver.id} | {driver.full_name} | Phone: {driver.phone} | Status: {driver.status} | Orders: {order_count}")
    
    print("\n" + "="*60)
    return 0

if __name__ == '__main__':
    sys.exit(main())
