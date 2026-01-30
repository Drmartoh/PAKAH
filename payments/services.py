"""KopoKopo M-Pesa API integration service"""
from django.conf import settings
import requests
import json
import hashlib
import hmac
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def get_access_token():
    """Get KopoKopo OAuth access token using client credentials flow"""
    client_id = settings.KOPOKOPO_CLIENT_ID
    client_secret = settings.KOPOKOPO_CLIENT_SECRET
    base_url = settings.KOPOKOPO_BASE_URL
    
    if not client_id or not client_secret:
        logger.error("KopoKopo credentials not configured")
        return None
    
    url = f"{base_url}/oauth/token"
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'PAKA-HOME/1.0'
    }
    
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        logger.info(f"KopoKopo Access Token Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access_token')
            if access_token:
                logger.info("KopoKopo access token retrieved successfully")
                return access_token
            else:
                logger.error(f"KopoKopo access token response: {data}")
        else:
            logger.error(f"KopoKopo access token error - Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logger.error(f"KopoKopo access token error: {e}")
    
    return None


def initiate_stk_push(phone_number, amount, order_tracking_code, callback_url, customer_name=None, customer_email=None):
    """
    Initiate KopoKopo M-Pesa STK Push payment
    Returns dict with success status and message/error_details
    """
    access_token = get_access_token()
    if not access_token:
        return {
            'success': False,
            'message': 'Failed to authenticate with KopoKopo. Please check your API credentials.',
            'error_details': 'Could not retrieve access token'
        }
    
    base_url = settings.KOPOKOPO_BASE_URL
    url = f"{base_url}/api/v1/incoming_payments"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'PAKA-HOME/1.0'
    }
    
    # Format phone number (ensure it starts with +254)
    phone = phone_number.replace(' ', '').replace('-', '')
    if not phone.startswith('+254'):
        if phone.startswith('254'):
            phone = '+' + phone
        elif phone.startswith('0'):
            phone = '+254' + phone[1:]
        else:
            phone = '+254' + phone
    
    # Split customer name if provided
    first_name = 'Customer'
    last_name = ''
    if customer_name:
        name_parts = customer_name.strip().split(' ', 1)
        first_name = name_parts[0]
        if len(name_parts) > 1:
            last_name = name_parts[1]
    
    # Prepare subscriber data
    subscriber = {
        'phone_number': phone,
        'first_name': first_name,
        'last_name': last_name
    }
    if customer_email:
        subscriber['email'] = customer_email
    
    # Prepare amount data
    # Convert to float first to handle Decimal types, then format as string
    # Remove unnecessary .0 for whole numbers (e.g., 150.0 -> 150, 150.5 -> 150.5)
    amount_float = float(amount)
    if amount_float.is_integer():
        amount_value = str(int(amount_float))
    else:
        amount_value = str(amount_float)
    
    amount_data = {
        'currency': 'KES',
        'value': amount_value
    }
    
    # Prepare metadata
    metadata = {
        'order_tracking_code': order_tracking_code,
        'order_reference': order_tracking_code
    }
    
    # Prepare links
    links = {
        'callback_url': callback_url
    }
    
    payload = {
        'payment_channel': 'M-PESA STK Push',
        'till_number': settings.KOPOKOPO_TILL_NUMBER,
        'subscriber': subscriber,
        'amount': amount_data,
        'metadata': metadata,
        '_links': links
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response_data = response.json() if response.content else {}
        
        logger.info(f"KopoKopo STK Push Response Status: {response.status_code}")
        logger.info(f"KopoKopo STK Push Response: {response_data}")
        
        if response.status_code == 201:
            # Success - Location header contains the payment request URL
            location = response.headers.get('Location', '')
            return {
                'success': True,
                'message': 'Payment request sent successfully. Please check your phone to complete payment.',
                'location': location,
                'payment_request_id': location.split('/')[-1] if location else None
            }
        else:
            # Error response
            error_message = response_data.get('error_message', 'Unknown error')
            error_code = response_data.get('error_code', response.status_code)
            
            return {
                'success': False,
                'message': f'Failed to initiate payment: {error_message}',
                'error_details': {
                    'error_code': error_code,
                    'error_message': error_message,
                    'status_code': response.status_code,
                    'full_response': response_data
                }
            }
    except requests.exceptions.RequestException as e:
        logger.error(f"KopoKopo STK Push network error: {e}")
        return {
            'success': False,
            'message': f'Network error: {str(e)}',
            'error_details': {
                'error_type': 'NETWORK_ERROR',
                'error_message': str(e)
            }
        }
    except Exception as e:
        logger.error(f"KopoKopo STK Push error: {e}")
        return {
            'success': False,
            'message': f'An unexpected error occurred: {str(e)}',
            'error_details': {
                'error_type': 'UNKNOWN_ERROR',
                'error_message': str(e)
            }
        }


def validate_webhook_signature(request_body, signature_header):
    """
    Validate KopoKopo webhook signature.
    KopoKopo signs webhooks with SHA256 HMAC of the request body using client_secret as key.
    See: https://developers.kopokopo.com/guides/webhooks/validating-webhooks.html
    """
    client_secret = settings.KOPOKOPO_CLIENT_SECRET
    if not client_secret:
        logger.warning("KopoKopo client secret not configured, skipping signature validation")
        return False
    
    try:
        expected_signature = hmac.new(
            client_secret.encode('utf-8'),
            request_body.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature_header)
    except Exception as e:
        logger.error(f"Error validating webhook signature: {e}")
        return False


def process_incoming_payment_result(callback_data):
    """
    Process KopoKopo incoming payment result callback
    Returns dict with payment status and details
    """
    try:
        data = callback_data.get('data', {})
        attributes = data.get('attributes', {})
        event = attributes.get('event', {})
        
        status = attributes.get('status', 'Unknown')
        resource = event.get('resource')
        errors = event.get('errors')
        
        if status == 'Success' and resource:
            # Payment successful
            return {
                'success': True,
                'status': 'completed',
                'mpesa_receipt_number': resource.get('reference'),
                'amount': resource.get('amount'),
                'currency': resource.get('currency'),
                'sender_phone_number': resource.get('sender_phone_number'),
                'transaction_date': resource.get('origination_time'),
                'till_number': resource.get('till_number'),
                'sender_first_name': resource.get('sender_first_name'),
                'sender_last_name': resource.get('sender_last_name'),
                'metadata': attributes.get('metadata', {}),
                'full_resource': resource
            }
        else:
            # Payment failed
            error_message = errors if errors else 'Payment request failed'
            return {
                'success': False,
                'status': 'failed',
                'error_message': error_message,
                'errors': errors
            }
    except Exception as e:
        logger.error(f"Error processing incoming payment result: {e}")
        return {
            'success': False,
            'status': 'error',
            'error_message': f'Error processing callback: {str(e)}'
        }
