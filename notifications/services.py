"""Africa's Talking SMS service"""
from django.conf import settings
import requests
from .models import SMSLog


def send_sms_notification(phone_number, message):
    """
    Send SMS via Africa's Talking API
    Returns True if successful, False otherwise
    """
    api_key = settings.AFRICASTALKING_API_KEY
    username = settings.AFRICASTALKING_USERNAME
    sender_id = settings.AFRICASTALKING_SENDER_ID
    
    if not api_key or not username:
        # Log but don't fail if API not configured
        SMSLog.objects.create(
            phone_number=phone_number,
            message=message,
            status='failed',
            response='API not configured'
        )
        return False
    
    url = "https://api.africastalking.com/version1/messaging"
    
    headers = {
        'ApiKey': api_key,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    # Format phone number
    phone = phone_number.replace('+', '').replace(' ', '')
    if not phone.startswith('254'):
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        else:
            phone = '254' + phone
    
    data = {
        'username': username,
        'to': phone,
        'message': message,
        'from': sender_id
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        
        # Log the SMS
        sms_log = SMSLog.objects.create(
            phone_number=phone_number,
            message=message,
            status='sent' if response.status_code == 201 else 'failed',
            response=response.text
        )
        
        if response.status_code == 201:
            return True
        else:
            return False
    except Exception as e:
        SMSLog.objects.create(
            phone_number=phone_number,
            message=message,
            status='failed',
            response=str(e)
        )
        return False

