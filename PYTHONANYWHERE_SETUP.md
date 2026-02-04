# PAKA HOME – PythonAnywhere Quick Setup Guide

Deploy the current PAKAH app on PythonAnywhere from scratch.

---

## 1. Create a PythonAnywhere account and Web app

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com) and sign up (free tier is fine).
2. Open the **Web** tab.
3. Click **Add a new web app** → choose **Manual configuration** (not Flask/Django wizard).
4. Pick **Python 3.10** (or 3.11 if available).
5. Note your app URL, e.g. `pakaapp.pythonanywhere.com`.

---

## 2. Clone the repo

Open a **Bash** console (Consoles → Bash).

```bash
# Go to home (or where you want the project)
cd ~

# Clone the repo (use your GitHub URL)
git clone https://github.com/Drmartoh/PAKAH.git

# Go into the project (repo root has manage.py)
cd PAKAH
```

If the repo has an inner `PAKAH` folder and `manage.py` is inside it, use:

```bash
cd ~/PAKAH/PAKAH
```

---

## 3. Virtualenv

In the same Bash console (with `cd` in the project directory where `manage.py` is):

```bash
# Create virtualenv (use Python 3.10 to match the Web app)
python3.10 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

---

## 4. Install dependencies

Still with the virtualenv active, in the project directory:

```bash
pip install -r requirements.txt
```

If you get errors on `psycopg2-binary` or `Pillow`, you can install without them for SQLite-only:

```bash
pip install Django djangorestframework django-cors-headers python-decouple requests django-filter
```

---

## 5. Django settings (no code change)

The app already has `pakaapp.pythonanywhere.com` in `ALLOWED_HOSTS` and production defaults for KopoKopo and till **K217328**. Optional: set env vars (Web tab → your app → **Code** → **Environment variables**), for example:

- `DEBUG` = `False`
- `SECRET_KEY` = (generate a long random string for production)
- `ALLOWED_HOSTS` = `pakaapp.pythonanywhere.com` (only if you want to override)

Leaving them unset is fine; the code uses safe defaults.

---

## 6. Database and static files

In the project directory, with virtualenv active:

```bash
# Migrations (SQLite by default)
python manage.py migrate

# Create superuser (optional, for admin)
python manage.py createsuperuser

# Collect static files (required for CSS/JS)
python manage.py collectstatic --noinput
```

---

## 7. Point the Web app to your project

1. **Web** tab → your app (e.g. **pakaapp.pythonanywhere.com**).
2. **Code** section:
   - **Source code**: `/home/YOUR_USERNAME/PAKAH`  
     (or `/home/YOUR_USERNAME/PAKAH/PAKAH` if `manage.py` is inside an inner `PAKAH`).
   - **Working directory**: same path (e.g. `/home/YOUR_USERNAME/PAKAH`).
   - **Virtualenv**: `/home/YOUR_USERNAME/PAKAH/venv`  
     (or `/home/YOUR_USERNAME/PAKAH/PAKAH/venv` if you created `venv` inside the inner folder).

Replace `YOUR_USERNAME` with your PythonAnywhere username.

---

## 8. WSGI configuration

1. **Web** tab → **Code** → open the **WSGI configuration file** link (e.g. `/var/www/pakaapp_pythonanywhere_com_wsgi.py`).
2. Replace its contents with the following (adjust paths if your project is in `PAKAH/PAKAH`):

```python
import os
import sys

# Project root (directory that contains manage.py)
path = '/home/YOUR_USERNAME/PAKAH'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'pakahome.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

3. Replace `YOUR_USERNAME` with your PythonAnywhere username.
4. If your project is in `PAKAH/PAKAH`, set `path = '/home/YOUR_USERNAME/PAKAH/PAKAH'`.
5. Save the file.

---

## 9. Static files mapping (Web tab)

1. **Web** tab → scroll to **Static files**.
2. Add a mapping:
   - **URL**: `/static/`
   - **Directory**: `/home/YOUR_USERNAME/PAKAH/staticfiles`  
     (or `/home/YOUR_USERNAME/PAKAH/PAKAH/staticfiles` if you use the inner path).

This serves the files collected by `collectstatic`.

---

## 10. Reload the app

1. **Web** tab → click the green **Reload** button for your app.
2. Open `https://pakaapp.pythonanywhere.com` in the browser.

You should see the PAKA HOME landing page. Test:

- **Sign up** / **Sign in** (customer: phone + 4-digit PIN).
- **Dashboard** → **New Order** → place an order.
- **Pay Now** → M-Pesa till shown as **K217328**, STK push callback: `https://pakaapp.pythonanywhere.com/payments/kopokopo/callback/callback/`.

---

## Checklist

| Step | Action |
|------|--------|
| 1 | Create Web app (Manual, Python 3.10) |
| 2 | `git clone` → `cd PAKAH` (or `PAKAH/PAKAH`) |
| 3 | `python3.10 -m venv venv` → `source venv/bin/activate` |
| 4 | `pip install -r requirements.txt` |
| 5 | (Optional) Set `DEBUG=False`, `SECRET_KEY` in env |
| 6 | `python manage.py migrate` → `collectstatic --noinput` |
| 7 | Web app **Code**: source + working directory + virtualenv path |
| 8 | WSGI file: `path`, `DJANGO_SETTINGS_MODULE`, `get_wsgi_application()` |
| 9 | Static files: `/static/` → `.../staticfiles` |
| 10 | **Reload** and test |

---

## Troubleshooting

- **502 Bad Gateway**: Check the **Error log** on the Web tab; usually WSGI path or virtualenv wrong.
- **Static files (CSS/JS) missing**: Confirm Static files URL `/static/` and directory `.../staticfiles`, and that `collectstatic` was run.
- **Old till (5630946) still showing**: Reload the app; the code forces **K217328** in production. If you have `MPESA_TILL_NUMBER` or `KOPOKOPO_TILL_NUMBER` in env, remove or set to `K217328`.
- **Import errors**: Ensure virtualenv path in the Web app is correct and you installed dependencies in that venv.
