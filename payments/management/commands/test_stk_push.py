"""
Test KopoKopo M-Pesa STK Push (no auth, no order required).
Usage: python manage.py test_stk_push --phone=+254728758157 --amount=1
"""
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from payments.services import initiate_stk_push


class Command(BaseCommand):
    help = 'Initiate a test STK push to the given phone number (production or sandbox).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--phone',
            type=str,
            default='+254728758157',
            help='Subscriber phone (e.g. +254728758157)',
        )
        parser.add_argument(
            '--amount',
            type=float,
            default=1.0,
            help='Amount in KES (e.g. 1)',
        )
        parser.add_argument(
            '--reference',
            type=str,
            default='TEST-STK-001',
            help='Order/reference for metadata',
        )

    def handle(self, *args, **options):
        phone = options['phone']
        amount = options['amount']
        reference = options['reference']

        callback_url = getattr(
            settings,
            'KOPOKOPO_CALLBACK_URL',
            'https://pakaapp.pythonanywhere.com/payments/kopokopo/callback/callback/',
        )

        self.stdout.write(
            f'Initiating STK push: phone={phone}, amount={amount} KES, reference={reference}'
        )
        self.stdout.write(f'Callback URL: {callback_url}')
        self.stdout.write(f'Environment: {getattr(settings, "KOPOKOPO_ENVIRONMENT", "?")}')
        self.stdout.write(f'Till: {getattr(settings, "KOPOKOPO_TILL_NUMBER", "?")}')
        self.stdout.write('')

        result = initiate_stk_push(
            phone_number=phone,
            amount=amount,
            order_tracking_code=reference,
            callback_url=callback_url,
            customer_name='Test Customer',
            customer_email=None,
        )

        if result.get('success'):
            self.stdout.write(self.style.SUCCESS('STK push initiated successfully.'))
            self.stdout.write(f"Location: {result.get('location', 'N/A')}")
            self.stdout.write('Check the phone for the M-Pesa prompt.')
        else:
            self.stdout.write(self.style.ERROR(f"Failed: {result.get('message', 'Unknown error')}"))
            self.stdout.write(json.dumps(result.get('error_details', {}), indent=2))
