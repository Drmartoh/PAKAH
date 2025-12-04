# Quick Start Guide - PAKA HOME

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows CMD:
venv\Scripts\activate.bat

# Linux/Mac:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Test System Configuration

```bash
python test_system.py
```

This will check:
- ✅ All modules can be imported
- ✅ Database connection
- ✅ Settings configuration
- ✅ URL routing
- ✅ Templates

### Step 3: Set Up Database

**Option A: Quick Testing (SQLite - Automatic)**
- No configuration needed!
- System will automatically use SQLite if PostgreSQL is not configured
- Database file will be created at: `db.sqlite3`

**Option B: Production (PostgreSQL)**
- Install PostgreSQL
- Create database: `CREATE DATABASE pakahome_db;`
- Create `.env` file with database credentials

### Step 4: Run Migrations

```bash
python manage.py migrate
```

This creates all database tables.

### Step 5: Create Admin User

```bash
python manage.py createsuperuser
```

Enter:
- Username
- Email (optional)
- Password

### Step 6: Start Server

```bash
python manage.py runserver
```

### Step 7: Access Application

Open your browser:
- **Landing Page**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## 🎯 Quick Test Flow

1. **Visit Landing Page**: http://localhost:8000
2. **Sign Up** as Customer (click "Sign Up" button)
3. **Login** with your credentials
4. **Create Order** (click "New Order" button)
5. **Test Payment** (click "Pay Now" on pending order)

## 📝 API Credentials Status

All credentials are pre-configured in `settings.py`:
- ✅ M-Pesa credentials: Configured
- ✅ Google Maps API: Configured
- ✅ Africa's Talking: Needs configuration (optional)

## ⚠️ Troubleshooting

### "ModuleNotFoundError: No module named 'django'"
**Fix**: Install dependencies
```bash
pip install -r requirements.txt
```

### "Database connection failed"
**Fix**: Use SQLite for testing (automatic) or configure PostgreSQL

### "Template not found"
**Fix**: Ensure you're in the project root directory

### "Port 8000 already in use"
**Fix**: Use a different port
```bash
python manage.py runserver 8080
```

## 📚 Next Steps

1. Read `README.md` for full documentation
2. Read `SETUP.md` for detailed setup instructions
3. Read `ISSUES_FIXED.md` for known issues and fixes
4. Test the complete order workflow

## 🎉 You're Ready!

The system is configured and ready to use. All API credentials are set, and the database will automatically use SQLite for quick testing.

Happy testing! 🚀

