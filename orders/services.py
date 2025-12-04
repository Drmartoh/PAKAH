"""Order service utilities"""
from django.conf import settings
from .models import Order, OrderTracking
import requests


def calculate_price(pickup_lat, pickup_lng, delivery_lat, delivery_lng):
    """
    Calculate order price based on location
    Within Nairobi: KES 150
    Outside Nairobi: KES 300
    """
    # Simple check: if coordinates are within Nairobi bounds
    # Nairobi approximate bounds: -1.5 to -1.1 lat, 36.6 to 37.0 lng
    nairobi_bounds = {
        'min_lat': -1.5,
        'max_lat': -1.1,
        'min_lng': 36.6,
        'max_lng': 37.0
    }
    
    # Check if both pickup and delivery are within Nairobi
    pickup_lat_f = float(pickup_lat)
    pickup_lng_f = float(pickup_lng)
    delivery_lat_f = float(delivery_lat)
    delivery_lng_f = float(delivery_lng)
    
    pickup_in_nairobi = (
        nairobi_bounds['min_lat'] <= pickup_lat_f <= nairobi_bounds['max_lat'] and
        nairobi_bounds['min_lng'] <= pickup_lng_f <= nairobi_bounds['max_lng']
    )
    
    delivery_in_nairobi = (
        nairobi_bounds['min_lat'] <= delivery_lat_f <= nairobi_bounds['max_lat'] and
        nairobi_bounds['min_lng'] <= delivery_lng_f <= nairobi_bounds['max_lng']
    )
    
    is_within_nairobi = pickup_in_nairobi and delivery_in_nairobi
    
    if is_within_nairobi:
        return settings.PRICING_NAIROBI, True
    else:
        return settings.PRICING_OUTSIDE_NAIROBI, False


def geocode_address(address):
    """
    Geocode an address using Google Maps Geocoding API
    Returns (latitude, longitude) or (None, None) if failed
    """
    api_key = settings.GOOGLE_MAPS_API_KEY
    if not api_key:
        return None, None
    
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    except Exception as e:
        print(f"Geocoding error: {e}")
    
    return None, None


def create_tracking_log(order, status, description="", lat=None, lng=None):
    """Create a tracking log entry for an order"""
    OrderTracking.objects.create(
        order=order,
        status=status,
        location_latitude=lat,
        location_longitude=lng,
        description=description
    )

