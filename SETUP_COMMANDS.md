# Django Pharmacy Management System - Setup Commands

## Project Setup Complete! ✅

Your Django project 'pharmacy_pro' with the 'inventory' app has been successfully created.

---

## Commands Reference (for future setup on new machines)

### 1. Create Virtual Environment
```bash
python -m venv .venv
```

### 2. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Install Django
```bash
pip install django
```

### 4. Create Django Project
```bash
django-admin startproject pharmacy_pro .
```

### 5. Create Django App
```bash
python manage.py startapp inventory
```

### 6. Add App to settings.py
Add `'inventory'` to the `INSTALLED_APPS` list in `pharmacy_pro/settings.py`

---

## Next Steps

### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Development Server
```bash
python manage.py runserver
```

Then visit: http://127.0.0.1:8000/

---

## Project Structure

```
Pharmacy_Management_System/
├── .venv/                  # Virtual environment
├── pharmacy_pro/          # Main project directory
│   ├── __init__.py
│   ├── settings.py        # Project settings (inventory app configured)
│   ├── urls.py           # URL routing
│   ├── asgi.py           # ASGI configuration
│   └── wsgi.py           # WSGI configuration
├── inventory/             # Inventory app
│   ├── __init__.py
│   ├── admin.py          # Admin panel configuration
│   ├── apps.py           # App configuration
│   ├── models.py         # Database models
│   ├── tests.py          # Tests
│   ├── views.py          # Views/Controllers
│   └── migrations/       # Database migrations
└── manage.py             # Django management script
```

---

## Configuration Summary

- **Project Name:** pharmacy_pro
- **App Name:** inventory
- **Python Version:** 3.10.0
- **Django Version:** 5.2.9
- **Virtual Environment:** .venv (already configured and activated)
- **Database:** SQLite (default)

The 'inventory' app has been added to INSTALLED_APPS in settings.py.
