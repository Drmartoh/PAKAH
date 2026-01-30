# Production Setup Guide

## ✅ Completed Changes

### 1. **Secured Credentials**
- All KopoKopo production credentials are now required via environment variables
- No credentials are hardcoded in the codebase
- Set these in PythonAnywhere's environment variables or `.env` file:
  ```
  KOPOKOPO_CLIENT_ID=u0dUZOdtIMX9wv3cpGcaA5KatlVYXdGbGlRL1Ig8rqg
  KOPOKOPO_CLIENT_SECRET=Ds9RXtvwGUBbwCCOThIzEbZ25Emy1vC4hjeDBzCD8B0
  KOPOKOPO_API_KEY=f09c5e6a1658b952652dca36684dc02951d60c8a
  KOPOKOPO_BASE_URL=https://api.kopokopo.com
  KOPOKOPO_TILL_NUMBER=K217328
  KOPOKOPO_ENVIRONMENT=production
  MPESA_TILL_NUMBER=K217328
  ```

### 2. **Removed Driver from Frontend**
- Driver signup/login removed from frontend UI
- Only Customer signup is available
- Drivers are created by Admin and credentials sent to them
- Driver dashboard still accessible via direct URL for admin-created drivers

### 3. **Assets Folder Created**
- Created `static/assets/images/` folder
- **ACTION REQUIRED**: Add your logo and favicon images:
  - `static/assets/images/logo.png` - Main logo (recommended: 200x60px)
  - `static/assets/images/favicon.ico` - Browser favicon (32x32px or 180x180px)

### 4. **Updated Navbar Colors**
- Navbar now uses gradient matching logo colors (black to dark blue)
- Orange accent color (#FCA311) for highlights
- Customer service number displayed in navbar: **0792-044-622**

### 5. **Updated Footer**
- Customer service number: **0792-044-622**
- Added Careers section
- Added Terms of Use link
- Updated contact information

### 6. **Careers Page**
- Created `/careers/` page
- Shows "Currently no open positions"
- Admin can manage job postings from Admin Dashboard (future feature)

### 7. **Terms of Use**
- Created comprehensive Terms of Use page at `/terms/`
- Checkbox required during customer signup
- Terms acceptance automatically recorded with timestamp

### 8. **Account Deletion**
- Added Settings modal in customer dashboard
- "Delete My Account" option with red danger zone
- Requires PIN verification
- Permanently deletes account and all associated data
- Endpoint: `POST /api/auth/delete-account/`

### 9. **Changed "Delivery" to "Drop-off"**
- Updated all booking forms
- Changed labels: "Delivery Details" → "Drop-off Details"
- Changed field labels: "Delivery Name/Phone/Address" → "Drop-off Name/Phone/Address"

## 📋 Pre-Deployment Checklist

### Required Actions:

1. **Add Images to Assets Folder**
   - Copy your logo to: `static/assets/images/logo.png`
   - Copy your favicon to: `static/assets/images/favicon.ico`
   - Run: `python manage.py collectstatic` after adding images

2. **Set Environment Variables on PythonAnywhere**
   - Go to your PythonAnywhere dashboard
   - Navigate to "Web" tab → "Environment variables"
   - Add all KopoKopo credentials listed above

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **Verify Webhook Subscription**
   - Ensure webhook is configured in KopoKopo dashboard
   - URL: `https://pakaapp.pythonanywhere.com/api/payments/callback/`
   - Event: `buygoods_transaction_received`

## 🔒 Security Notes

- All sensitive credentials are now environment variables
- Never commit `.env` file to version control
- Use PythonAnywhere's environment variables for production
- Terms acceptance is tracked in database
- Account deletion requires PIN verification

## 📝 Database Changes

New migration created:
- `users/migrations/0003_user_terms_accepted_user_terms_accepted_at.py`
- Adds `terms_accepted` and `terms_accepted_at` fields to User model

Run migration before deploying:
```bash
python manage.py migrate
```

## 🎨 UI/UX Updates

- Navbar: Gradient background (black to dark blue) matching logo
- Customer service number prominently displayed
- Settings button in customer dashboard
- Danger zone styling for account deletion
- Terms checkbox in signup form
- Careers link in footer

## 📞 Contact Information

- Customer Service: **0792-044-622**
- Email: support@pakahomeapp.co.ke
- Address: Nairobi CBD, Mfangano Street, Ndaragwa Hse, Mezanine MF22

