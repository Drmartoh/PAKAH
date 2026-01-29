#!/usr/bin/env python
"""
Create test data: orders and drivers for testing admin dashboard.
Run: python create_test_data.py
"""
import os
import sys
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pakahome.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import Customer, Driver
from orders.models import Order
from payments.models import Payment

User = get_user_model()

def make_phone(n):
    return f"254700000{n:03d}"

def main():
    print("Creating test data...")
    
    # Create test customer
    try:
        customer_user = User.objects.get(phone_number=make_phone(1))
        print(f"Customer user already exists: {make_phone(1)}")
    except User.DoesNotExist:
        customer_user = User.objects.create_user(
            phone_number=make_phone(1),
            email='customer@test.pakahome.local',
            password='1234',
            role='customer'
        )
        customer_user.username = make_phone(1)
        customer_user.save(update_fields=['username'])
        print(f"Created customer user: {make_phone(1)}")
    
    customer, created = Customer.objects.get_or_create(
        user=customer_user,
        defaults={
            'full_name': 'Test Customer',
            'phone': make_phone(1),
            'address': 'Nairobi, Kenya'
        }
    )
    if created:
        print(f"Created customer profile: {customer.full_name}")
    
    # Create test drivers
    drivers_data = [
        {'name': 'John Driver', 'phone': make_phone(2), 'license': 'DL001'},
        {'name': 'Jane Driver', 'phone': make_phone(3), 'license': 'DL002'},
        {'name': 'Mike Driver', 'phone': make_phone(4), 'license': 'DL003'},
    ]
    
    drivers_created = []
    for d in drivers_data:
        try:
            driver_user = User.objects.get(phone_number=d['phone'])
            print(f"Driver user already exists: {d['phone']}")
        except User.DoesNotExist:
            driver_user = User.objects.create_user(
                phone_number=d['phone'],
                email=f"{d['phone']}@test.pakahome.local",
                password='1234',
                role='driver'
            )
            driver_user.username = d['phone']
            driver_user.save(update_fields=['username'])
            print(f"Created driver user: {d['phone']}")
        
        driver, created = Driver.objects.get_or_create(
            user=driver_user,
            defaults={
                'full_name': d['name'],
                'phone': d['phone'],
                'license_number': d['license'],
                'status': 'available',
                'is_active': True
            }
        )
        if created:
            print(f"Created driver: {driver.full_name} (License: {driver.license_number})")
        drivers_created.append(driver)
    
    # Create test orders
    orders_data = [
        {
            'pickup': 'Nairobi CBD, Mfangano Street',
            'delivery': 'Westlands, Nairobi',
            'price': 150,
            'status': 'pending_assignment',
            'paid': False
        },
        {
            'pickup': 'Kasarani, Nairobi',
            'delivery': 'Runda, Nairobi',
            'price': 150,
            'status': 'pending_assignment',
            'paid': True
        },
        {
            'pickup': 'Nairobi CBD',
            'delivery': 'Mombasa',
            'price': 300,
            'status': 'assigned',
            'paid': True,
            'driver': drivers_created[0] if drivers_created else None
        },
        {
            'pickup': 'Nairobi',
            'delivery': 'Nairobi',
            'price': 150,
            'status': 'picked_up',
            'paid': True,
            'driver': drivers_created[1] if len(drivers_created) > 1 else None
        },
    ]
    
    orders_created = []
    for i, o in enumerate(orders_data):
        order, created = Order.objects.get_or_create(
            customer=customer,
            tracking_code=f'PAKATEST{i+1:02d}',
            defaults={
                'pickup_name': 'Test Sender',
                'pickup_phone': make_phone(1),
                'pickup_address': o['pickup'],
                'pickup_latitude': Decimal('-1.29'),
                'pickup_longitude': Decimal('36.82'),
                'delivery_name': 'Test Receiver',
                'delivery_phone': make_phone(1),
                'delivery_address': o['delivery'],
                'delivery_latitude': Decimal('-1.30'),
                'delivery_longitude': Decimal('36.83'),
                'price': Decimal(str(o['price'])),
                'status': o['status'],
                'is_within_nairobi': o['price'] == 150,
                'driver': o.get('driver')
            }
        )
        if created:
            print(f"Created order: {order.tracking_code} - Status: {order.status}")
            orders_created.append(order)
            
            # Create payment if paid
            if o.get('paid'):
                payment, _ = Payment.objects.get_or_create(
                    order=order,
                    defaults={
                        'customer': customer,
                        'phone_number': make_phone(1),
                        'amount': order.price,
                        'status': 'completed',
                        'mpesa_receipt_number': f'MPESA{order.tracking_code}'
                    }
                )
                if _:
                    print(f"  Created payment for {order.tracking_code}")
    
    print("\n" + "="*50)
    print("Test data created successfully!")
    print("="*50)
    print(f"\nAdmin login:")
    print(f"  Phone: 254700000000")
    print(f"  PIN: 1234")
    print(f"\nTest drivers created: {len(drivers_created)}")
    print(f"Test orders created: {len(orders_created)}")
    print(f"\nOrders status breakdown:")
    for status in ['pending_assignment', 'assigned', 'picked_up', 'delivered']:
        count = Order.objects.filter(status=status).count()
        if count > 0:
            print(f"  {status}: {count}")
    print("\nGo to http://127.0.0.1:8000/admin-dashboard/ to test!")
    return 0

if __name__ == '__main__':
    sys.exit(main())
