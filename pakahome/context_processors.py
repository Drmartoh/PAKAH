from django.conf import settings


def google_maps_api_key(request):
    """Context processor to make Google Maps API key, office location, and M-Pesa info available in templates"""
    return {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'OFFICE_LATITUDE': getattr(settings, 'OFFICE_LATITUDE', -1.2921),
        'OFFICE_LONGITUDE': getattr(settings, 'OFFICE_LONGITUDE', 36.8219),
        'OFFICE_ADDRESS': getattr(settings, 'OFFICE_ADDRESS', 'Nairobi CBD, Mfangano Street, Ndaragwa Hse, Mezanine MF22'),
        'MPESA_TILL_NUMBER': getattr(settings, 'MPESA_TILL_NUMBER', 'K217328'),
    }

