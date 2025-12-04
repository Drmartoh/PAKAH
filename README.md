# PAKA HOME Parcel Delivery Platform

A modern, world-class parcel delivery platform built with Django and Django REST Framework, designed for Kenya's market with M-Pesa integration, SMS notifications, and real-time tracking.

## Features

- **Customer Portal**: Place orders, track deliveries, view order history
- **Admin Dashboard**: Manage orders, assign drivers, view analytics and revenue
- **Driver Interface**: Receive job assignments, navigate with Google Maps, confirm pickup/delivery
- **Real-time Tracking**: Live GPS tracking with Google Maps integration
- **M-Pesa Payments**: Secure payment processing via Safaricom Daraja API
- **SMS Notifications**: Automated SMS updates via Africa's Talking API
- **Smart Pricing**: Automatic price calculation (KES 150 within Nairobi, KES 300 outside)

## Technology Stack

### Backend
- Django 5.0
- Django REST Framework
- PostgreSQL
- Celery (optional, for async tasks)
- Redis (optional, for caching)

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap 5
- Google Maps JavaScript API
- Font Awesome Icons

### Integrations
- M-Pesa Daraja API (Payments)
- Africa's Talking SMS API (Notifications)
- Google Maps APIs (Geocoding, Directions, Places)

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   cd PAKAH
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your configuration:
   - Django SECRET_KEY
   - Database credentials
   - M-Pesa API credentials
   - Africa's Talking API credentials
   - Google Maps API key

5. **Set up database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Frontend: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## Configuration

### M-Pesa Daraja API Setup

1. Register at https://developer.safaricom.co.ke/
2. Get your Consumer Key and Consumer Secret
3. Set up your shortcode and passkey
4. Configure callback URL for payment confirmations

### Africa's Talking SMS Setup

1. Sign up at https://africastalking.com/
2. Get your API key and username
3. Configure sender ID (default: PAKAHOME)

### Google Maps API Setup

1. Create a project in Google Cloud Console
2. Enable the following APIs:
   - Maps JavaScript API
   - Geocoding API
   - Directions API
   - Places API
3. Create an API key and restrict it to your domain

## Project Structure

```
PAKAH/
├── pakahome/          # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── users/             # User authentication and profiles
├── orders/            # Order management
├── drivers/           # Driver management
├── payments/          # M-Pesa payment integration
├── notifications/     # SMS notification service
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS, images)
├── requirements.txt
└── manage.py
```

## API Endpoints

### Authentication
- `POST /api/auth/register/customer/` - Register customer
- `POST /api/auth/register/driver/` - Register driver
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/me/` - Get current user

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/` - Create order
- `GET /api/orders/{id}/` - Get order details
- `GET /api/orders/tracking/{tracking_code}/` - Track order (public)
- `POST /api/orders/{id}/status/` - Update order status

### Payments
- `POST /api/payments/stkpush/` - Initiate M-Pesa payment
- `POST /api/payments/callback/` - M-Pesa callback endpoint
- `GET /api/payments/` - List payments

### Drivers
- `GET /api/drivers/` - List drivers (admin)
- `GET /api/drivers/available/` - Get available drivers
- `POST /api/drivers/assign/{order_id}/` - Assign driver to order
- `POST /api/drivers/{id}/status/` - Update driver status
- `GET /api/drivers/orders/` - Get driver's orders
- `POST /api/drivers/orders/{id}/accept/` - Accept order

### Maps
- `GET /api/maps/autocomplete/` - Address autocomplete
- `GET /api/maps/geocode/` - Geocode address
- `GET /api/maps/directions/` - Get directions

## Order Workflow

1. Customer places order with pickup and delivery details
2. System calculates price automatically
3. Customer pays via M-Pesa STK Push
4. Order status changes to "Pending Assignment"
5. Admin assigns a driver
6. Driver accepts the order
7. Driver confirms pickup (SMS sent to customer)
8. Order status: "In Transit"
9. Driver confirms delivery (SMS sent to customer)
10. Order status: "Delivered"

## Pricing

- **Within Nairobi**: KES 150 (fixed)
- **Outside Nairobi**: KES 300 (fixed)

The system automatically determines pricing based on pickup and delivery coordinates.

## User Roles

### Customer
- Place orders
- Track orders
- View order history
- Make payments

### Admin
- View all orders
- Assign drivers
- Manage drivers
- View analytics and revenue
- Send SMS notifications

### Driver
- View assigned orders
- Accept/decline orders
- Update order status
- Navigate with Google Maps
- Update availability status

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in settings
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up SSL certificate
- [ ] Configure production database
- [ ] Set up proper logging
- [ ] Configure static file serving
- [ ] Set up Celery workers (if using async tasks)
- [ ] Configure Redis (if using caching)
- [ ] Set up backup strategy
- [ ] Configure monitoring and error tracking

### Recommended Hosting

- **Backend**: PythonAnywhere, DigitalOcean, AWS, Heroku
- **Database**: PostgreSQL on same server or managed service
- **Domain**: Configure DNS for pakahomeapp.co.ke
- **SSL**: Let's Encrypt (free SSL certificate)

## Support

For support, email support@pakahomeapp.co.ke or call +254 700 000 000

## License

Copyright © 2024 PAKA HOME. All rights reserved.

## Contributing

This is a private project. For contributions or questions, please contact the development team.

