#!/usr/bin/env python
"""
Test payment (STK push & callback) endpoints.
Run from project root: python test_payment_endpoints.py
Uses Django test client - no running server needed.
"""

import os
import sys
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pakahome.settings')
django.setup()

from django.test import Client
from django.conf import settings


def test_callback_endpoint():
    """Callback must accept POST without CSRF and return 400 for invalid JSON (not 403)."""
    client = Client(enforce_csrf_checks=True)  # Simulate production CSRF
    url = '/api/payments/callback/'

    # Empty body -> invalid JSON -> 400
    response = client.post(url, data='', content_type='application/json')
    if response.status_code == 403:
        print("[FAIL] Callback endpoint: Got 403 (CSRF or auth). Callback must be CSRF-exempt for KopoKopo.")
        return False
    if response.status_code in (400, 404):
        # 400 = invalid JSON (expected); 404 = wrong URL
        if response.status_code == 404:
            print("[FAIL] Callback endpoint: 404 Not Found. Check URL routing.")
            return False
        print("[OK] Callback endpoint: POST accepted without CSRF, returned %s for invalid body" % response.status_code)
        return True
    print("[OK] Callback endpoint: POST accepted, status %s" % response.status_code)
    return True


def test_callback_with_invalid_json():
    """Callback with invalid JSON returns 400."""
    client = Client()
    url = '/api/payments/callback/'
    response = client.post(url, data='{ invalid }', content_type='application/json')
    if response.status_code == 400:
        print("[OK] Callback invalid JSON: 400 as expected")
        return True
    print("[FAIL] Callback invalid JSON: Expected 400, got %s" % response.status_code)
    return False


def test_callback_with_valid_structure_no_order():
    """Callback with valid KopoKopo-like structure but no order returns 400."""
    client = Client()
    url = '/api/payments/callback/'
    body = {
        "data": {
            "type": "incoming_payment",
            "attributes": {
                "status": "Success",
                "event": {"resource": {}},
                "metadata": {}
            }
        }
    }
    response = client.post(
        url,
        data=json.dumps(body),
        content_type='application/json'
    )
    # We expect 400 (order tracking code not found) or 404 (order not found)
    if response.status_code in (400, 404):
        print("[OK] Callback valid structure: returns %s when order missing" % response.status_code)
        return True
    print("[FAIL] Callback valid structure: Expected 400/404, got %s" % response.status_code)
    return False


def test_stkpush_without_auth():
    """STK push without authentication must return 403 or 401 (auth required). 400 = endpoint exists, validation/auth."""
    client = Client()
    url = '/api/payments/stkpush/'
    response = client.post(
        url,
        data=json.dumps({"order_id": 1, "phone_number": "254700000000"}),
        content_type='application/json'
    )
    if response.status_code == 404:
        print("[FAIL] STK push: 404 Not Found. Check URL: %s" % url)
        return False
    if response.status_code in (401, 403):
        print("[OK] STK push (no auth): %s Forbidden/Unauthorized as expected" % response.status_code)
        return True
    if response.status_code == 400:
        # Endpoint exists; 400 = validation or "customer only" etc.
        print("[OK] STK push (no auth): endpoint reachable, returned 400 (auth or validation)")
        return True
    print("[FAIL] STK push (no auth): Expected 401/403/400, got %s" % response.status_code)
    return False


def test_callback_url_setting():
    """Production callback URL should be pakahomeparceldelivery.website."""
    callback_url = getattr(settings, 'KOPOKOPO_CALLBACK_URL', None)
    if not callback_url:
        print("[FAIL] KOPOKOPO_CALLBACK_URL: Not set in settings")
        return False
    if 'pakahomeparceldelivery.website' not in callback_url:
        print("[WARN] KOPOKOPO_CALLBACK_URL: Expected pakahomeparceldelivery.website, got: %s" % callback_url)
        return False
    if not callback_url.rstrip('/').endswith('/api/payments/callback'):
        print("[WARN] KOPOKOPO_CALLBACK_URL: Expected path /api/payments/callback/, got: %s" % callback_url)
    print("[OK] KOPOKOPO_CALLBACK_URL: %s" % callback_url)
    return True


def main():
    print("PAKA HOME – Payment endpoints test")
    print("=" * 50)
    results = []
    results.append(("Callback URL setting", test_callback_url_setting()))
    results.append(("Callback POST (no CSRF)", test_callback_endpoint()))
    results.append(("Callback invalid JSON", test_callback_with_invalid_json()))
    results.append(("Callback valid structure", test_callback_with_valid_structure_no_order()))
    results.append(("STK push no auth → 403", test_stkpush_without_auth()))
    print("=" * 50)
    all_ok = all(r[1] for r in results)
    if all_ok:
        print("\n[OK] All payment endpoint checks passed.")
        return 0
    print("\n[FAIL] Some checks failed.")
    return 1


if __name__ == '__main__':
    sys.exit(main())
