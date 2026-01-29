"""
Driver app tests: API and flows.
Run: python manage.py test drivers
"""
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import Customer, Driver
from orders.models import Order

User = get_user_model()


def make_phone(n):
    return f"2547000000{n:02d}"


class DriverAPITestCase(TestCase):
    """Driver API and flow tests."""

    def setUp(self):
        self.client = APIClient()
        # Admin
        self.admin_user = User.objects.create_user(
            phone_number=make_phone(1),
            email='admin@test.pakahome.local',
            password='1234',
            role='admin',
            is_staff=True,
            is_superuser=True
        )
        self.admin_user.username = make_phone(1)
        self.admin_user.save(update_fields=['username'])
        # Customer + profile
        self.customer_user = User.objects.create_user(
            phone_number=make_phone(2),
            email='customer@test.pakahome.local',
            password='1234',
            role='customer'
        )
        self.customer_user.username = make_phone(2)
        self.customer_user.save(update_fields=['username'])
        self.customer = Customer.objects.create(
            user=self.customer_user,
            full_name='Test Customer',
            phone=make_phone(2),
            address='Nairobi'
        )
        # Driver + profile
        self.driver_user = User.objects.create_user(
            phone_number=make_phone(3),
            email='driver@test.pakahome.local',
            password='1234',
            role='driver'
        )
        self.driver_user.username = make_phone(3)
        self.driver_user.save(update_fields=['username'])
        self.driver = Driver.objects.create(
            user=self.driver_user,
            full_name='Test Driver',
            phone=make_phone(3),
            license_number='DL001',
            status='available',
            is_active=True
        )
        # Order (pending_assignment) for customer
        self.order = Order.objects.create(
            customer=self.customer,
            tracking_code='PAKATEST01',
            pickup_name='A',
            pickup_phone=make_phone(2),
            pickup_address='Nairobi A',
            pickup_latitude=Decimal('-1.29'),
            pickup_longitude=Decimal('36.82'),
            delivery_name='B',
            delivery_phone=make_phone(2),
            delivery_address='Nairobi B',
            delivery_latitude=Decimal('-1.30'),
            delivery_longitude=Decimal('36.83'),
            price=Decimal('150'),
            status='pending_assignment',
            is_within_nairobi=True
        )

    # --- Admin-only: list drivers (returns paginated {results: [...]}) ---
    def test_driver_list_admin_ok(self):
        self.client.force_authenticate(user=self.admin_user)
        r = self.client.get('/api/drivers/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        results = data.get('results', data) if isinstance(data, dict) else data
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 1)

    def test_driver_list_customer_empty(self):
        """Customer gets 200 with empty results (queryset is none for non-admin)."""
        self.client.force_authenticate(user=self.customer_user)
        r = self.client.get('/api/drivers/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        results = data.get('results', data) if isinstance(data, dict) else data
        self.assertEqual(len(results), 0)

    def test_driver_list_unauthenticated_forbidden(self):
        r = self.client.get('/api/drivers/')
        self.assertIn(r.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    # --- Admin-only: available drivers ---
    def test_available_drivers_admin_ok(self):
        self.client.force_authenticate(user=self.admin_user)
        r = self.client.get('/api/drivers/available/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'available')

    def test_available_drivers_driver_forbidden(self):
        self.client.force_authenticate(user=self.driver_user)
        r = self.client.get('/api/drivers/available/')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    # --- Admin: assign driver ---
    def test_assign_driver_admin_ok(self):
        self.client.force_authenticate(user=self.admin_user)
        r = self.client.post(
            f'/api/drivers/assign/{self.order.id}/',
            {'driver_id': self.driver.id},
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.driver_id, self.driver.id)
        self.assertEqual(self.order.status, 'assigned')
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.status, 'busy')

    def test_assign_driver_missing_driver_id(self):
        self.client.force_authenticate(user=self.admin_user)
        r = self.client.post(
            f'/api/drivers/assign/{self.order.id}/',
            {},
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_assign_driver_driver_forbidden(self):
        self.client.force_authenticate(user=self.driver_user)
        r = self.client.post(
            f'/api/drivers/assign/{self.order.id}/',
            {'driver_id': self.driver.id},
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    # --- Driver: my orders ---
    def test_driver_orders_driver_ok(self):
        self.order.driver = self.driver
        self.order.status = 'assigned'
        self.order.save()
        self.client.force_authenticate(user=self.driver_user)
        r = self.client.get('/api/drivers/orders/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]['tracking_code'], self.order.tracking_code)

    def test_driver_orders_admin_forbidden(self):
        self.client.force_authenticate(user=self.admin_user)
        r = self.client.get('/api/drivers/orders/')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    # --- Driver: accept order ---
    def test_accept_order_driver_ok(self):
        self.order.driver = self.driver
        self.order.status = 'assigned'
        self.order.save()
        self.client.force_authenticate(user=self.driver_user)
        r = self.client.post(f'/api/drivers/orders/{self.order.id}/accept/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'accepted')

    def test_accept_order_wrong_status(self):
        self.order.driver = self.driver
        self.order.status = 'accepted'
        self.order.save()
        self.client.force_authenticate(user=self.driver_user)
        r = self.client.post(f'/api/drivers/orders/{self.order.id}/accept/')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_accept_order_customer_forbidden(self):
        self.order.driver = self.driver
        self.order.status = 'assigned'
        self.order.save()
        self.client.force_authenticate(user=self.customer_user)
        r = self.client.post(f'/api/drivers/orders/{self.order.id}/accept/')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    # --- Driver: update order status (picked_up, delivered) ---
    def test_update_order_status_picked_up_driver_ok(self):
        self.order.driver = self.driver
        self.order.status = 'accepted'
        self.order.save()
        self.client.force_authenticate(user=self.driver_user)
        r = self.client.post(
            f'/api/orders/{self.order.id}/status/',
            {'status': 'picked_up', 'description': 'Picked up'},
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'picked_up')
        self.assertIsNotNone(self.order.picked_up_at)

    def test_update_order_status_delivered_driver_ok(self):
        self.order.driver = self.driver
        self.order.status = 'picked_up'
        self.order.save()
        self.client.force_authenticate(user=self.driver_user)
        r = self.client.post(
            f'/api/orders/{self.order.id}/status/',
            {'status': 'delivered', 'description': 'Delivered'},
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'delivered')
        self.assertIsNotNone(self.order.delivered_at)

    def test_update_order_status_driver_wrong_order_forbidden(self):
        other_driver_user = User.objects.create_user(
            phone_number=make_phone(4),
            email='driver2@test.pakahome.local',
            password='1234',
            role='driver'
        )
        other_driver_user.username = make_phone(4)
        other_driver_user.save(update_fields=['username'])
        other_driver = Driver.objects.create(
            user=other_driver_user,
            full_name='Other Driver',
            phone=make_phone(4),
            license_number='DL002',
            is_active=True
        )
        self.order.driver = self.driver
        self.order.status = 'accepted'
        self.order.save()
        self.client.force_authenticate(user=other_driver_user)
        r = self.client.post(
            f'/api/orders/{self.order.id}/status/',
            {'status': 'picked_up'},
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    # --- Driver: update own status ---
    def test_update_driver_status_driver_ok(self):
        self.client.force_authenticate(user=self.driver_user)
        r = self.client.post(
            f'/api/drivers/{self.driver.id}/status/',
            {'status': 'offline'},
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.status, 'offline')

    def test_update_driver_status_with_location(self):
        self.client.force_authenticate(user=self.driver_user)
        r = self.client.post(
            f'/api/drivers/{self.driver.id}/status/',
            {'status': 'available', 'latitude': -1.29, 'longitude': 36.82},
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.status, 'available')
        self.assertIsNotNone(self.driver.current_latitude)
        self.assertIsNotNone(self.driver.current_longitude)

    def test_update_driver_status_wrong_driver_forbidden(self):
        other_driver_user = User.objects.create_user(
            phone_number=make_phone(5),
            email='driver3@test.pakahome.local',
            password='1234',
            role='driver'
        )
        other_driver_user.username = make_phone(5)
        other_driver_user.save(update_fields=['username'])
        other_driver = Driver.objects.create(
            user=other_driver_user,
            full_name='Other Driver 2',
            phone=make_phone(5),
            license_number='DL003',
            is_active=True
        )
        self.client.force_authenticate(user=other_driver_user)
        r = self.client.post(
            f'/api/drivers/{self.driver.id}/status/',
            {'status': 'offline'},
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_driver_status_invalid_value(self):
        self.client.force_authenticate(user=self.driver_user)
        r = self.client.post(
            f'/api/drivers/{self.driver.id}/status/',
            {'status': 'invalid'},
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Full flow: assign -> accept -> picked_up -> delivered ---
    def test_full_driver_flow(self):
        # 1. Admin assigns driver
        self.client.force_authenticate(user=self.admin_user)
        r = self.client.post(
            f'/api/drivers/assign/{self.order.id}/',
            {'driver_id': self.driver.id},
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'assigned')

        # 2. Driver gets orders and accepts
        self.client.force_authenticate(user=self.driver_user)
        r = self.client.get('/api/drivers/orders/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(r.json()), 1)

        r = self.client.post(f'/api/drivers/orders/{self.order.id}/accept/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'accepted')

        # 3. Driver confirms pickup
        r = self.client.post(
            f'/api/orders/{self.order.id}/status/',
            {'status': 'picked_up'},
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'picked_up')

        # 4. Driver confirms delivery
        r = self.client.post(
            f'/api/orders/{self.order.id}/status/',
            {'status': 'delivered'},
            format='json'
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'delivered')
