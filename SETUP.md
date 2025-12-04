# PAKA HOME Setup Guide

## Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create PostgreSQL database (run in PostgreSQL)
CREATE DATABASE pakahome_db;
CREATE USER pakahome_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE pakahome_db TO pakahome_user;
```

### 3. Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-generate-with-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=pakahome_db
DB_USER=pakahome_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# M-Pesa Daraja API (Sandbox)
MPESA_CONSUMER_KEY=your-consumer-key
MPESA_CONSUMER_SECRET=your-consumer-secret
MPESA_SHORTCODE=your-shortcode
MPESA_PASSKEY=your-passkey
MPESA_TILL_NUMBER=5630946
MPESA_ENVIRONMENT=sandbox

# Africa's Talking SMS
AFRICASTALKING_API_KEY=your-api-key
AFRICASTALKING_USERNAME=your-username
AFRICASTALKING_SENDER_ID=PAKAHOME

# Google Maps API
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

**Generate Django Secret Key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin User

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Access the application at http://localhost:8000

## API Credentials Setup

### M-Pesa Daraja API

1. Register at https://developer.safaricom.co.ke/
2. Create an app to get Consumer Key and Secret
3. For sandbox testing, use test credentials
4. Configure callback URL: `http://your-domain.com/api/payments/callback/`

### Africa's Talking SMS

1. Sign up at https://africastalking.com/
2. Create an account and get API credentials
3. Configure sender ID (must be approved)

### Google Maps API

1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable APIs:
   - Maps JavaScript API
   - Geocoding API
   - Directions API
   - Places API
4. Create API key and restrict it

## Testing the Application

### Create Test Users

1. **Customer**: Sign up via the landing page
2. **Driver**: Sign up as driver via the landing page
3. **Admin**: Use the superuser created with `createsuperuser`

### Test Order Flow

1. Login as customer
2. Create a new order
3. Make payment (M-Pesa sandbox)
4. Login as admin
5. Assign driver to order
6. Login as driver
7. Accept order and update status

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists

### API Integration Issues
- Check API keys in `.env`
- Verify API credentials are correct
- Check API quotas/limits

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Migration Issues
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

## Production Deployment

1. Set `DEBUG = False` in settings
2. Configure `ALLOWED_HOSTS` with your domain
3. Set up SSL certificate
4. Use production database
5. Configure static file serving (nginx/Apache)
6. Set up proper logging
7. Configure backup strategy

