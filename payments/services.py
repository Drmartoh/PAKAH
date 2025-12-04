"""M-Pesa Daraja API integration service"""
from django.conf import settings
import requests
import base64
from datetime import datetime
import json


def get_access_token():
    """Get M-Pesa OAuth access token"""
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    
    if not consumer_key or not consumer_secret:
        return None
    
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    if settings.MPESA_ENVIRONMENT == 'production':
        url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    auth_string = f"{consumer_key}:{consumer_secret}"
    auth_bytes = auth_string.encode('ascii')
    auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
    
    headers = {
        'Authorization': f'Basic {auth_base64}'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('access_token')
    except Exception as e:
        print(f"M-Pesa access token error: {e}")
    
    return None


def generate_password():
    """Generate M-Pesa API password"""
    shortcode = settings.MPESA_SHORTCODE
    passkey = settings.MPESA_PASSKEY
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = f"{shortcode}{passkey}{timestamp}"
    
    password = base64.b64encode(data_to_encode.encode()).decode('ascii')
    return password, timestamp


def initiate_stk_push(phone_number, amount, order_tracking_code, callback_url):
    """
    Initiate M-Pesa STK Push payment
    Returns response data or None if failed
    """
    access_token = get_access_token()
    if not access_token:
        return None
    
    shortcode = settings.MPESA_SHORTCODE
    password, timestamp = generate_password()
    
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
    if settings.MPESA_ENVIRONMENT == 'production':
        url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Format phone number (remove + and ensure it starts with 254)
    phone = phone_number.replace('+', '').replace(' ', '')
    if not phone.startswith('254'):
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        else:
            phone = '254' + phone
    
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": order_tracking_code,
        "TransactionDesc": f"PAKA HOME Order {order_tracking_code}"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"M-Pesa STK Push error: {e}")
    
    return None

