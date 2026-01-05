# 🚀 Quick Command Reference

## Essential Commands

### 1️⃣ Setup (Run Once)
```bash
# Create groups and permissions
python manage.py setup_groups

# Create demo users (manager/staff)
python manage.py create_demo_users

# Add 10 sample medicines
python manage.py populate_sample_data
```

### 2️⃣ Run Server
```bash
python manage.py runserver
```

### 3️⃣ Access Application
```
http://127.0.0.1:8000/
```

---

## 🔑 Login Credentials

**Manager:** `manager` / `manager123` (Full Access)  
**Staff:** `staff` / `staff123` (No Delete)  
**Admin:** `admin` / (your password)

---

## 🌐 Quick URL Reference

| Page | URL |
|------|-----|
| Login | http://127.0.0.1:8000/login/ |
| Dashboard | http://127.0.0.1:8000/ |
| Medicine List | http://127.0.0.1:8000/medicines/ |
| Search | http://127.0.0.1:8000/search/ |
| Add Medicine | http://127.0.0.1:8000/add/ |
| Admin Panel | http://127.0.0.1:8000/admin/ |

---

## 📊 Sample Data Summary

✅ **10 medicines** in database  
⚠️ **3 low stock** (≤10 units)  
⚠️ **1 expiring soon** (within 30 days)  
🔴 **1 expired** medicine

---

## 🛠️ Useful Django Commands

```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Check for issues
python manage.py check

# Django shell
python manage.py shell
```

---

## ✅ Everything Ready!

**Start testing now:**
1. Run: `python manage.py runserver`
2. Visit: http://127.0.0.1:8000/
3. Login as: manager / manager123
4. Explore all features!
