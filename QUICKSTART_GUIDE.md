# PAKA HOME - Quick Start Guide

Welcome to PAKA HOME Parcel Delivery Platform! This guide will help you get started quickly.

## 🚀 Getting Started

### For Customers

#### Step 1: Create an Account
1. Visit the landing page at http://localhost:8000
2. Click **"Get Started"** or **"Sign Up"** button
3. Fill in the registration form:
   - Username
   - Email
   - Full Name
   - Phone Number
   - Password (minimum 8 characters)
4. Click **"Sign Up as Customer"**
5. You'll be prompted to login

#### Step 2: Login
1. Click **"Sign In"** button
2. Enter your username and password
3. Click **"Sign In"**
4. You'll be redirected to your Customer Dashboard

#### Step 3: Book a Delivery
**Option A: From Landing Page**
1. Click the **"Book Now"** button on the landing page
2. Fill in the order form that appears
3. Enter pickup and delivery details
4. Review the estimated price
5. Click **"Create Order"**

**Option B: From Dashboard**
1. Go to your dashboard
2. Click **"New Order"** button
3. Fill in the order form
4. Submit the order

#### Step 4: Pay for Your Order
1. After creating an order, you'll see it in your dashboard
2. Click **"Pay Now"** button on the order
3. Enter your M-Pesa phone number (format: 254712345678)
4. Confirm the payment on your phone
5. Wait for payment confirmation

#### Step 5: Track Your Order
1. View your orders in the dashboard
2. Click **"Track"** to see real-time updates
3. You'll receive SMS notifications at key stages:
   - When driver accepts your order
   - When parcel is picked up
   - When parcel is delivered

---

### For Drivers

#### Step 1: Register as Driver
1. Visit the landing page
2. Click **"Sign Up"** button
3. Select the **"Driver"** tab
4. Fill in the registration form:
   - Username
   - Email
   - Full Name
   - Phone Number
   - License Number (required)
   - Vehicle Type (optional)
   - Vehicle Registration (optional)
   - Password
5. Click **"Sign Up as Driver"**
6. Login with your credentials

#### Step 2: Access Driver Dashboard
1. After login, you'll be redirected to the Driver Dashboard
2. Update your status to **"Available"** to receive orders

#### Step 3: Accept Orders
1. When an order is assigned to you, you'll see it in your dashboard
2. Click on the order to view details
3. Click **"Accept Order"** to confirm
4. Customer will receive SMS notification

#### Step 4: Pick Up Parcel
1. Navigate to pickup location using the map
2. Collect the parcel
3. Click **"Confirm Pickup"** in the order details
4. Customer will receive SMS notification

#### Step 5: Deliver Parcel
1. Navigate to delivery location using the map
2. Deliver the parcel
3. Click **"Confirm Delivery"** in the order details
4. Customer will receive SMS notification
5. Order is marked as completed

---

### For Administrators

#### Step 1: Access Admin Dashboard
1. Login with admin credentials
2. You'll be redirected to the Admin Dashboard
3. View all orders, drivers, and statistics

#### Step 2: Assign Drivers
1. View orders with status "Pending Assignment"
2. Click **"Assign Driver"** button
3. Select an available driver from the list
4. Driver will receive SMS notification

#### Step 3: Monitor Orders
1. View all orders in the orders table
2. Track order status and progress
3. View revenue and statistics

#### Step 4: Manage Drivers
1. View all registered drivers
2. See driver availability status
3. Monitor driver performance

---

## 📋 Order Workflow

### Complete Order Lifecycle

1. **Order Created** → Status: `Pending Payment`
   - Customer creates order
   - System calculates price automatically

2. **Payment Made** → Status: `Pending Assignment`
   - Customer pays via M-Pesa
   - Payment confirmed via callback

3. **Driver Assigned** → Status: `Assigned`
   - Admin assigns a driver
   - Driver receives notification

4. **Driver Accepts** → Status: `Accepted`
   - Driver accepts the order
   - Customer receives SMS

5. **Parcel Picked Up** → Status: `Picked Up`
   - Driver confirms pickup
   - Customer receives SMS
   - Order in transit

6. **Parcel Delivered** → Status: `Delivered`
   - Driver confirms delivery
   - Customer receives SMS
   - Order completed

---

## 💰 Pricing

- **Within Nairobi**: KES 150 (fixed rate)
- **Outside Nairobi**: KES 300 (fixed rate)

Price is automatically calculated based on pickup and delivery locations.

---

## 📱 Payment Methods

### M-Pesa Payment
1. Click **"Pay Now"** on your order
2. Enter your M-Pesa phone number
3. Confirm payment on your phone
4. Wait for confirmation (usually within 30 seconds)

**M-Pesa Till Number**: 5630946

---

## 📞 Contact Information

- **Phone**: 0792-044-622
- **M-Pesa Till**: 5630946
- **Location**: Nairobi CBD, Mfangano Street, Ndaragwa Hse, Mezanine MF22

---

## 🔍 Tracking Orders

### Public Tracking
1. Visit: http://localhost:8000/track/TRACKING_CODE/
2. Replace `TRACKING_CODE` with your order tracking code
3. View order status and location on map

### Dashboard Tracking
1. Login to your dashboard
2. View all your orders
3. Click **"Track"** on any order
4. See real-time updates and timeline

---

## 🎯 Key Features

### For Customers
- ✅ Easy order booking
- ✅ Real-time tracking
- ✅ M-Pesa payment integration
- ✅ SMS notifications
- ✅ Order history

### For Drivers
- ✅ Job assignments
- ✅ Google Maps navigation
- ✅ Status updates
- ✅ Earnings tracking

### For Admins
- ✅ Order management
- ✅ Driver assignment
- ✅ Revenue tracking
- ✅ Analytics dashboard

---

## ⚠️ Important Notes

1. **Authentication Required**: You must be logged in to place orders
2. **Phone Number Format**: Use format 254712345678 for M-Pesa payments
3. **Address Autocomplete**: Use Google Maps autocomplete for accurate addresses
4. **SMS Notifications**: Ensure your phone number is correct to receive notifications

---

## 🆘 Troubleshooting

### Can't Login?
- Check your username and password
- Make sure you've registered first
- Contact support if issues persist

### Payment Not Working?
- Check your M-Pesa phone number format
- Ensure you have sufficient M-Pesa balance
- Wait a few seconds for confirmation

### Order Not Showing?
- Refresh your dashboard
- Check your order status
- Contact support if order is missing

### Driver Not Receiving Orders?
- Ensure your status is set to "Available"
- Check that you're logged in
- Contact admin if issues persist

---

## 📚 Additional Resources

- **Full Documentation**: See `README.md`
- **Setup Guide**: See `SETUP.md`
- **API Documentation**: See API endpoints in code

---

## 🎉 You're All Set!

You now know how to use PAKA HOME. Start by creating an account and booking your first delivery!

**Happy Delivering!** 🚚📦

