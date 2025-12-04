from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
import requests


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def autocomplete(request):
    """Google Maps Places Autocomplete"""
    api_key = settings.GOOGLE_MAPS_API_KEY
    query = request.GET.get('query', '')
    
    if not api_key:
        return Response(
            {'error': 'Google Maps API key not configured'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if not query:
        return Response(
            {'error': 'Query parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
    params = {
        'input': query,
        'key': api_key,
        'components': 'country:ke',  # Restrict to Kenya
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        return Response(data)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def geocode(request):
    """Geocode an address"""
    api_key = settings.GOOGLE_MAPS_API_KEY
    address = request.GET.get('address', '')
    
    if not api_key:
        return Response(
            {'error': 'Google Maps API key not configured'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if not address:
        return Response(
            {'error': 'Address parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': api_key,
        'region': 'ke',  # Bias results to Kenya
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        return Response(data)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def directions(request):
    """Get directions between two points with route optimization"""
    api_key = settings.GOOGLE_MAPS_API_KEY
    origin = request.GET.get('origin', '')
    destination = request.GET.get('destination', '')
    waypoints = request.GET.get('waypoints', '')  # Optional waypoints for optimization
    optimize = request.GET.get('optimize', 'false').lower() == 'true'
    
    if not api_key:
        return Response(
            {'error': 'Google Maps API key not configured'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if not origin or not destination:
        return Response(
            {'error': 'Origin and destination parameters are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        'origin': origin,
        'destination': destination,
        'key': api_key,
        'region': 'ke',  # Bias to Kenya
        'alternatives': 'false',  # Get single best route
    }
    
    # Add waypoints if provided (for route optimization)
    if waypoints:
        if optimize:
            params['waypoints'] = f'optimize:true|{waypoints}'
        else:
            params['waypoints'] = waypoints
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('status') == 'OK' and data.get('routes'):
            route = data['routes'][0]
            # Add route summary
            route_summary = {
                'distance': route['legs'][0]['distance']['text'],
                'duration': route['legs'][0]['duration']['text'],
                'start_address': route['legs'][0]['start_address'],
                'end_address': route['legs'][0]['end_address'],
            }
            data['route_summary'] = route_summary
        
        return Response(data)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def validate_address(request):
    """Validate and geocode an address"""
    api_key = settings.GOOGLE_MAPS_API_KEY
    address = request.data.get('address', '')
    
    if not api_key:
        return Response(
            {'error': 'Google Maps API key not configured'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if not address:
        return Response(
            {'error': 'Address is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Use Places API for better address validation
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        'input': address,
        'inputtype': 'textquery',
        'fields': 'formatted_address,geometry,place_id,address_components',
        'key': api_key,
        'locationbias': 'circle:50000@-1.2921,36.8219',  # Bias to Nairobi
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        if data.get('status') == 'OK' and data.get('candidates'):
            candidate = data['candidates'][0]
            result = {
                'valid': True,
                'formatted_address': candidate.get('formatted_address'),
                'latitude': candidate['geometry']['location']['lat'],
                'longitude': candidate['geometry']['location']['lng'],
                'place_id': candidate.get('place_id'),
                'address_components': candidate.get('address_components', [])
            }
            return Response(result)
        else:
            return Response({
                'valid': False,
                'error': 'Address not found'
            }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(
            {'error': str(e), 'valid': False}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def route_optimization(request):
    """Optimize route with multiple waypoints"""
    api_key = settings.GOOGLE_MAPS_API_KEY
    origin = request.GET.get('origin', '')
    destination = request.GET.get('destination', '')
    waypoints = request.GET.get('waypoints', '')  # Comma-separated waypoints
    
    if not api_key:
        return Response(
            {'error': 'Google Maps API key not configured'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if not origin or not destination or not waypoints:
        return Response(
            {'error': 'Origin, destination, and waypoints are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        'origin': origin,
        'destination': destination,
        'waypoints': f'optimize:true|{waypoints}',
        'key': api_key,
        'region': 'ke',
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('status') == 'OK' and data.get('routes'):
            route = data['routes'][0]
            # Extract optimized waypoint order
            waypoint_order = route.get('waypoint_order', [])
            optimized_route = {
                'waypoint_order': waypoint_order,
                'distance': sum(leg['distance']['value'] for leg in route['legs']) / 1000,  # km
                'duration': sum(leg['duration']['value'] for leg in route['legs']) / 60,  # minutes
                'route': route
            }
            return Response(optimized_route)
        else:
            return Response(
                {'error': data.get('error_message', 'Route optimization failed')}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
