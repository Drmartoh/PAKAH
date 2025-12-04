from django.urls import path
from . import map_views

urlpatterns = [
    path('autocomplete/', map_views.autocomplete, name='map_autocomplete'),
    path('geocode/', map_views.geocode, name='map_geocode'),
    path('directions/', map_views.directions, name='map_directions'),
    path('validate-address/', map_views.validate_address, name='validate_address'),
    path('route-optimization/', map_views.route_optimization, name='route_optimization'),
]

