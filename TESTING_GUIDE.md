# PAKA HOME - Testing Guide

## 🚀 Server Status

**Development server is running at:** http://127.0.0.1:8000/

---

## 👤 Test Accounts

### Admin Account (Already Created)
- **Phone:** `254700000000` or `0700000000`
- **PIN:** `1234`
- **Dashboard:** http://127.0.0.1:8000/admin-dashboard/
- **Admin Panel:** http://127.0.0.1:8000/admin/

### Customer Account
**Create via website:**
1. Go to http://127.0.0.1:8000/
2. Click **Sign Up** (or use the modal)
3. Fill in: Phone, PIN (4 digits), Full Name, Email (optional), Address (optional)
4. After signup, you'll be redirected to login → then to Customer Dashboard

**Or create via Django admin:**
- Go to http://127.0.0.1:8000/admin/ → Users → Users → Add user
- Set role = `customer`, phone_number, password (PIN)
- Then create Customer profile

### Driver Account
**Create via website:**
1. Go to http://127.0.0.1:8000/register/driver/
2. Fill in: Phone, PIN (4 digits), Full Name, License Number (required), Vehicle Type/Registration (optional)
3. After signup, you'll be auto-logged in and redirected to Driver Dashboard

**Or create via Django admin:**
- Go to http://127.0.0.1:8000/admin/ → Users → Users → Add user
- Set role = `driver`, phone_number, password (PIN)
- Then create Driver profile (license_number required)

---

## 🧪 Testing Checklist

### 1. Customer Dashboard
**URL:** http://127.0.0.1:8000/dashboard/

**Test:**
- [ ] Sign in as customer
- [ ] Create a new order (pickup + delivery addresses)
- [ ] View order list
- [ ] Track an order
- [ ] Pay for an order (STK push - will need real M-Pesa for production)

### 2. Driver Dashboard
**URL:** http://127.0.0.1:8000/driver-dashboard/

**Test:**
- [ ] Sign up as driver (or create via admin)
- [ ] Sign in → should redirect to `/driver-dashboard/`
- [ ] View assigned orders (empty initially)
- [ ] Update driver status (Available/Busy/Offline)
- [ ] Accept an assigned order
- [ ] Confirm pickup
- [ ] Confirm delivery
- [ ] View map with pickup/delivery locations

**Protection Test:**
- [ ] Logout, try to access `/driver-dashboard/` → should redirect to `/register/driver/`
- [ ] Sign in as customer, try `/driver-dashboard/` → should redirect to `/`

### 3. Admin Dashboard
**URL:** http://127.0.0.1:8000/admin-dashboard/

**Test:**
- [ ] Sign in as admin (phone: `254700000000`, PIN: `1234`)
- [ ] View all orders (should load all pages if > 20 orders)
- [ ] View stats: Total Orders, Pending Assignment, In Transit, Total Revenue
- [ ] Assign driver to a pending order
- [ ] View orders table with customer/driver/status/price
- [ ] Click "Assign Driver" → select driver → assign

**Protection Test:**
- [ ] Logout, try `/admin-dashboard/` → should redirect to `/?login=1` (login modal opens)
- [ ] Sign in as customer, try `/admin-dashboard/` → should redirect to `/`

---

## 🔄 Complete Order Flow Test

1. **Customer creates order:**
   - Sign in as customer
   - Create order with pickup/delivery addresses
   - Order status: `pending_payment`

2. **Customer pays:**
   - Click "Pay Now" on order
   - Enter phone number for M-Pesa STK push
   - (In production: complete payment on phone)
   - Order status: `pending_assignment`

3. **Admin assigns driver:**
   - Sign in as admin
   - Go to Admin Dashboard
   - Find order with status "Pending Assignment"
   - Click "Assign Driver"
   - Select an available driver
   - Order status: `assigned`, Driver status: `busy`

4. **Driver accepts:**
   - Sign in as driver
   - View assigned orders
   - Click order → "Accept Order"
   - Order status: `accepted`

5. **Driver confirms pickup:**
   - Click "Confirm Pickup"
   - Order status: `picked_up`
   - Customer receives SMS (if Africa's Talking configured)

6. **Driver confirms delivery:**
   - Click "Confirm Delivery"
   - Order status: `delivered`
   - Customer receives SMS

---

## 🔗 Quick Links

- **Landing Page:** http://127.0.0.1:8000/
- **Customer Dashboard:** http://127.0.0.1:8000/dashboard/
- **Driver Sign Up:** http://127.0.0.1:8000/register/driver/
- **Driver Dashboard:** http://127.0.0.1:8000/driver-dashboard/
- **Admin Dashboard:** http://127.0.0.1:8000/admin-dashboard/
- **Django Admin:** http://127.0.0.1:8000/admin/
- **Track Order:** http://127.0.0.1:8000/track/

---

## 🐛 Troubleshooting

### "An error occurred" on driver signup
- Check browser console (F12) for detailed error
- Check Django server console for traceback
- Ensure phone number is unique
- Ensure license_number is unique

### Dashboard shows "Loading..." forever
- Check browser console (F12) for JavaScript errors
- Check Network tab → see if API calls return 401/403
- Ensure you're signed in (check cookies)

### Can't access driver/admin dashboard
- Ensure you're signed in
- Ensure user role is correct (driver/admin)
- Check URL: `/driver-dashboard/` (not `/driver-dashboard`)

---

## 📝 Notes

- **M-Pesa STK Push:** Requires production KopoKopo credentials and callback URL configured
- **SMS Notifications:** Requires Africa's Talking API credentials (optional)
- **Google Maps:** Requires valid API key (already configured in settings)
- **Database:** Using SQLite (db.sqlite3) for development

---

*Last updated: January 2025*
