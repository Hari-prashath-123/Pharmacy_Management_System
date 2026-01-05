# URL Configuration Guide - Pharmacy Management System

## ✅ Complete URL Configuration

### Project URLs (`pharmacy_pro/urls.py`)
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),  # Include inventory app URLs
]
```

**Explanation:**
- `admin/` - Django admin panel
- `''` (root) - All other URLs handled by inventory app

---

### App URLs (`inventory/urls.py`)
```python
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Medicine Management URLs
    path('', views.MedicineDashboardView.as_view(), name='medicine_dashboard'),
    path('medicines/', views.MedicineListView.as_view(), name='medicine_list'),
    path('search/', views.search_medicine, name='search_medicine'),
    path('add/', views.AddMedicineView.as_view(), name='add_medicine'),
    path('edit/<int:pk>/', views.EditMedicineView.as_view(), name='edit_medicine'),
    path('delete-expired/', views.delete_all_expired, name='delete_expired'),
]
```

---

## 🌐 Complete URL Map

| URL Pattern | View | Name | Description | Auth Required |
|-------------|------|------|-------------|---------------|
| `/` | MedicineDashboardView | medicine_dashboard | Main dashboard | ✅ Yes |
| `/login/` | CustomLoginView | login | Login page | ❌ No |
| `/logout/` | LogoutView | logout | Logout action | ✅ Yes |
| `/medicines/` | MedicineListView | medicine_list | Detailed table view | ✅ Yes |
| `/search/` | search_medicine | search_medicine | Search medicines | ✅ Yes |
| `/add/` | AddMedicineView | add_medicine | Add new medicine | ✅ Yes |
| `/edit/<id>/` | EditMedicineView | edit_medicine | Edit medicine | ✅ Yes |
| `/delete-expired/` | delete_all_expired | delete_expired | Delete expired | ✅ Yes (Manager) |
| `/admin/` | Django Admin | admin:index | Admin panel | ✅ Yes (Admin) |

---

## 📋 URL Examples

### Authentication
- **Login:** `http://127.0.0.1:8000/login/`
- **Logout:** `http://127.0.0.1:8000/logout/`

### Medicine Management
- **Dashboard:** `http://127.0.0.1:8000/`
- **Medicine List:** `http://127.0.0.1:8000/medicines/`
- **Search:** `http://127.0.0.1:8000/search/`
- **Add Medicine:** `http://127.0.0.1:8000/add/`
- **Edit Medicine:** `http://127.0.0.1:8000/edit/1/` (where 1 is medicine ID)
- **Delete Expired:** `http://127.0.0.1:8000/delete-expired/`

### Admin
- **Admin Panel:** `http://127.0.0.1:8000/admin/`

---

## 🔗 Template URL References

### Using URL Names in Templates
```django
<!-- Link to dashboard -->
<a href="{% url 'medicine_dashboard' %}">Dashboard</a>

<!-- Link to add medicine -->
<a href="{% url 'add_medicine' %}">Add Medicine</a>

<!-- Link to edit medicine (with parameter) -->
<a href="{% url 'edit_medicine' medicine.pk %}">Edit</a>

<!-- Link to login -->
<a href="{% url 'login' %}">Login</a>

<!-- Link to logout -->
<a href="{% url 'logout' %}">Logout</a>
```

---

## 🔄 View to URL Mapping

### Class-Based Views (CBV)
```python
# Dashboard View
class MedicineDashboardView(LoginRequiredMixin, ListView):
    # URL: /
    # Name: medicine_dashboard
    
# Add Medicine View
class AddMedicineView(LoginRequiredMixin, CreateView):
    # URL: /add/
    # Name: add_medicine
    
# Edit Medicine View
class EditMedicineView(LoginRequiredMixin, UpdateView):
    # URL: /edit/<pk>/
    # Name: edit_medicine
    
# Medicine List View
class MedicineListView(LoginRequiredMixin, ListView):
    # URL: /medicines/
    # Name: medicine_list
```

### Function-Based Views (FBV)
```python
# Search Medicine
@login_required
def search_medicine(request):
    # URL: /search/
    # Name: search_medicine

# Delete Expired
@login_required
@permission_required('inventory.delete_medicine')
def delete_all_expired(request):
    # URL: /delete-expired/
    # Name: delete_expired
```

---

## 🎯 Redirect Configuration

### Settings (`pharmacy_pro/settings.py`)
```python
LOGIN_URL = 'login'                    # Redirect to login if not authenticated
LOGIN_REDIRECT_URL = 'medicine_dashboard'  # After successful login
LOGOUT_REDIRECT_URL = 'login'         # After logout
```

---

## ✅ URL Testing Checklist

Test all URLs to ensure they're working:

```bash
# Start the server
python manage.py runserver

# Test each URL in browser:
```

1. ✅ **http://127.0.0.1:8000/** - Dashboard (should redirect to login if not authenticated)
2. ✅ **http://127.0.0.1:8000/login/** - Login page
3. ✅ **http://127.0.0.1:8000/medicines/** - Medicine list table
4. ✅ **http://127.0.0.1:8000/search/** - Search page
5. ✅ **http://127.0.0.1:8000/add/** - Add medicine form
6. ✅ **http://127.0.0.1:8000/edit/1/** - Edit first medicine
7. ✅ **http://127.0.0.1:8000/delete-expired/** - Delete expired page
8. ✅ **http://127.0.0.1:8000/logout/** - Logout
9. ✅ **http://127.0.0.1:8000/admin/** - Admin panel

---

## 🚀 Complete Setup Commands

```bash
# 1. Setup groups and permissions
python manage.py setup_groups

# 2. Create demo users
python manage.py create_demo_users

# 3. Populate sample medicine data
python manage.py populate_sample_data

# 4. Run the server
python manage.py runserver

# 5. Access the application
# Open browser: http://127.0.0.1:8000/login/
```

---

## 📊 Sample Data Created

The `populate_sample_data` command creates 10 medicines:

| Medicine | Category | Stock | Status |
|----------|----------|-------|--------|
| Aspirin | Painkiller | 150 | ✅ Active |
| Amoxicillin | Antibiotic | 80 | ✅ Active |
| Ibuprofen | Painkiller | 200 | ✅ Active |
| Paracetamol | Fever Reducer | 5 | ⚠️ Low Stock |
| Metformin | Diabetes | 120 | ✅ Active |
| Lisinopril | Blood Pressure | 95 | ✅ Active |
| Omeprazole | Antacid | 3 | ⚠️ Low + Expiring Soon |
| Ciprofloxacin | Antibiotic | 60 | ✅ Active |
| Vitamin D3 | Vitamin | 180 | ✅ Active |
| Expired Medicine Sample | Test | 0 | 🔴 Expired |

---

## 🔧 URL Pattern Details

### Dynamic URL Parameters

**Edit Medicine URL:**
```python
path('edit/<int:pk>/', views.EditMedicineView.as_view(), name='edit_medicine')
```
- `<int:pk>` - Captures integer ID as primary key
- Example: `/edit/5/` captures pk=5

**Usage in view:**
```python
class EditMedicineView(LoginRequiredMixin, UpdateView):
    pk_url_kwarg = 'pk'  # Uses pk from URL
```

**Usage in template:**
```django
<a href="{% url 'edit_medicine' medicine.id %}">Edit</a>
<!-- or -->
<a href="{% url 'edit_medicine' pk=medicine.pk %}">Edit</a>
```

---

## 🎨 Navigation Implementation

### Sidebar Navigation (base.html)
```django
<ul class="sidebar-menu">
    <li>
        <a href="{% url 'medicine_dashboard' %}" 
           class="{% if request.resolver_match.url_name == 'medicine_dashboard' %}active{% endif %}">
            Dashboard
        </a>
    </li>
    <!-- More menu items... -->
</ul>
```

---

## ✅ Everything is Connected!

Your URL configuration is complete and ready:

1. ✅ **Project URLs** - Configured in `pharmacy_pro/urls.py`
2. ✅ **App URLs** - Configured in `inventory/urls.py`
3. ✅ **Views** - All linked to URL patterns
4. ✅ **Templates** - Using URL names for navigation
5. ✅ **Authentication** - Login/logout URLs configured
6. ✅ **Sample Data** - 10 medicines populated in database

**Start Testing:**
```bash
python manage.py runserver
# Visit: http://127.0.0.1:8000/login/
# Login with: manager / manager123
```
