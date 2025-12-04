#!/usr/bin/env python
"""
Quick setup verification script for PAKA HOME
Run this after initial setup to verify everything is configured correctly
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pakahome.settings')
django.setup()

from django.conf import settings
from django.db import connection

def check_database():
    """Check database connection"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✓ Database connection: OK")
        return True
    except Exception as e:
        print(f"✗ Database connection: FAILED - {e}")
        return False

def check_settings():
    """Check critical settings"""
    issues = []
    
    if settings.SECRET_KEY == 'django-insecure-change-this-in-production':
        issues.append("SECRET_KEY is using default value")
    
    if not settings.MPESA_CONSUMER_KEY:
        issues.append("M-Pesa Consumer Key not configured")
    
    if not settings.AFRICASTALKING_API_KEY:
        issues.append("Africa's Talking API Key not configured")
    
    if not settings.GOOGLE_MAPS_API_KEY:
        issues.append("Google Maps API Key not configured")
    
    if issues:
        print("⚠ Configuration warnings:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✓ Settings: OK")
    
    return len(issues) == 0

def check_migrations():
    """Check if migrations are applied"""
    try:
        from django.core.management import call_command
        from io import StringIO
        
        out = StringIO()
        call_command('showmigrations', '--list', stdout=out)
        output = out.getvalue()
        
        if '[X]' in output:
            print("✓ Migrations: Applied")
            return True
        else:
            print("⚠ Migrations: Some migrations may not be applied")
            return False
    except Exception as e:
        print(f"✗ Migrations check: FAILED - {e}")
        return False

def main():
    print("PAKA HOME Setup Verification")
    print("=" * 40)
    
    results = []
    results.append(("Database", check_database()))
    results.append(("Settings", check_settings()))
    results.append(("Migrations", check_migrations()))
    
    print("=" * 40)
    all_ok = all(result[1] for result in results)
    
    if all_ok:
        print("\n✓ All checks passed! You're ready to go.")
        return 0
    else:
        print("\n⚠ Some checks failed. Please review the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

