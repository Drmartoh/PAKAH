#!/usr/bin/env python
"""
Create a superuser for PAKA HOME.
Run from project root: python create_superuser.py

Login: phone number = 254700000000, PIN = admin1234
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pakahome.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

PHONE = '254700000000'
PASSWORD = '1234'  # 4-digit PIN (website login expects 4 digits)
EMAIL = 'admin@pakahome.local'

def main():
    if User.objects.filter(phone_number=PHONE).exists():
        user = User.objects.get(phone_number=PHONE)
        user.set_password(PASSWORD)
        user.is_staff = True
        user.is_superuser = True
        user.role = 'admin'
        if getattr(user, 'username', None) in (None, ''):
            user.username = PHONE
        user.save()
        print('Superuser already exists. Password updated.')
    else:
        user = User.objects.create_superuser(
            phone_number=PHONE,
            email=EMAIL,
            password=PASSWORD
        )
        if getattr(user, 'username', None) in (None, ''):
            user.username = PHONE
            user.save(update_fields=['username'])
        print('Superuser created.')
    print('')
    print('Login with:')
    print('  Phone (username):', PHONE, 'or 0700000000')
    print('  PIN (password): ', PASSWORD, '(use this on website Sign In)')
    print('')
    print('Admin panel: http://127.0.0.1:8000/admin/')
    print('Or sign in on the website and you will be redirected to Admin Dashboard.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
