"""
Django settings for pakahome project.
"""

from pathlib import Path
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)

# allow local dev and your PythonAnywhere subdomain by default
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='pakahomeparceldelivery.website,www.pakahomeparceldelivery.website,pakahomedeliveries.co.ke,www.pakahomedeliveries.co.ke,pakaapp.pythonanywhere.com,localhost,127.0.0.1,testserver'
).split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'users',
    'orders',
    'drivers',
    'payments',
    'notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pakahome.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pakahome.context_processors.google_maps_api_key',
            ],
        },
    },
]

WSGI_APPLICATION = 'pakahome.wsgi.application'

# Database selection (unchanged) ...
DB_ENGINE = config('DB_ENGINE', default='postgresql')
if DB_ENGINE == 'sqlite' or (DB_ENGINE == 'postgresql' and not config('DB_PASSWORD', default='')):
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': BASE_DIR / 'db.sqlite3',}}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='pakahome_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 4,}}
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
CORS_ALLOW_CREDENTIALS = True

# KopoKopo M-Pesa STK Push – use env vars in production to override these defaults.
# Set environment: 'production' or 'sandbox'
KOPOKOPO_ENVIRONMENT = config('KOPOKOPO_ENVIRONMENT', default='production')

if KOPOKOPO_ENVIRONMENT == 'production':
    # Production live credentials (override with env vars: KOPOKOPO_CLIENT_ID, etc.)
    KOPOKOPO_CLIENT_ID = config(
        'KOPOKOPO_CLIENT_ID',
        default='u0dUZOdtIMX9wv3cpGcaA5KatlVYXdGbGlRL1Ig8rqg'
    )
    KOPOKOPO_CLIENT_SECRET = config(
        'KOPOKOPO_CLIENT_SECRET',
        default='Ds9RXtvwGUBbwCCOThIzEbZ25Emy1vC4hjeDBzCD8B0'
    )
    KOPOKOPO_API_KEY = config(
        'KOPOKOPO_API_KEY',
        default='f09c5e6a1658b952652dca36684dc02951d60c8a'
    )
    KOPOKOPO_TILL_NUMBER = config('KOPOKOPO_TILL_NUMBER', default='K217328')
    KOPOKOPO_BASE_URL = config('KOPOKOPO_BASE_URL', default='https://api.kopokopo.com')
else:
    KOPOKOPO_CLIENT_ID = config('KOPOKOPO_CLIENT_ID', default='')
    KOPOKOPO_CLIENT_SECRET = config('KOPOKOPO_CLIENT_SECRET', default='')
    KOPOKOPO_API_KEY = config('KOPOKOPO_API_KEY', default='')
    KOPOKOPO_TILL_NUMBER = config('KOPOKOPO_TILL_NUMBER', default='')
    KOPOKOPO_BASE_URL = config('KOPOKOPO_BASE_URL', default='https://sandbox.kopokopo.com')

# M-Pesa till for display (customer dashboard, landing). Live till: K217328.
MPESA_TILL_NUMBER = config('MPESA_TILL_NUMBER', default='K217328')

# KopoKopo webhook callback URL – must be HTTPS and the exact path that receives POST.
# Production: pakaapp.pythonanywhere.com
KOPOKOPO_CALLBACK_URL = config(
    'KOPOKOPO_CALLBACK_URL',
    default='https://pakaapp.pythonanywhere.com/payments/kopokopo/callback/callback/'
)

AFRICASTALKING_API_KEY = config('AFRICASTALKING_API_KEY', default='')
AFRICASTALKING_USERNAME = config('AFRICASTALKING_USERNAME', default='')
AFRICASTALKING_SENDER_ID = config('AFRICASTALKING_SENDER_ID', default='PAKAHOME')

GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY', default='AIzaSyBUE5XLUc3mCaGZRlJYDJ2TcE2ItTOQR3g')

OFFICE_LATITUDE = -1.2921
OFFICE_LONGITUDE = 36.8219
OFFICE_ADDRESS = "Nairobi CBD, Mfangano Street, Ndaragwa Hse, Mezanine MF22"

PRICING_NAIROBI = 150
PRICING_OUTSIDE_NAIROBI = 300

CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
