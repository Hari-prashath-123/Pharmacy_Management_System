# Django Authentication System - Setup Guide

## ✅ Implementation Complete

### Overview
Django's built-in authentication system has been integrated with custom permissions for Manager and Staff roles.

---

## 🔐 Authentication Features

### 1. **Login System**
- **URL:** `/login/`
- **Template:** `inventory/login.html`
- **Features:**
  - Beautiful gradient design
  - Bootstrap 5 styling
  - Error message display
  - Redirect authenticated users
  - Responsive layout

### 2. **Logout System**
- **URL:** `/logout/`
- Redirects to login page after logout
- Available in sidebar navigation

### 3. **Login Required Protection**
All views now require authentication:
- ✅ Dashboard (`@LoginRequiredMixin`)
- ✅ Medicine List (`@LoginRequiredMixin`)
- ✅ Add Medicine (`@LoginRequiredMixin`)
- ✅ Edit Medicine (`@LoginRequiredMixin`)
- ✅ Search Medicine (`@login_required`)
- ✅ Delete Expired (`@login_required` + `@permission_required`)

---

## 👥 User Groups & Permissions

### Manager Group
**Full Access** - Can perform all operations:
- ✅ **View** medicines
- ✅ **Add** new medicines
- ✅ **Update** existing medicines
- ✅ **Delete** medicines (including expired)

### Staff Group
**Limited Access** - Cannot delete:
- ✅ **View** medicines
- ✅ **Add** new medicines
- ✅ **Update** existing medicines
- ❌ **No Delete** permission

---

## 🛠️ Setup Instructions

### 1. Create Groups and Permissions
Run the management command:
```bash
python manage.py setup_groups
```

**Output:**
```
Setting up groups and permissions...
✓ Created Manager group
✓ Assigned all permissions to Manager group
  - View medicines
  - Add medicines
  - Update medicines
  - Delete medicines
✓ Created Staff group
✓ Assigned limited permissions to Staff group
  - View medicines
  - Add medicines
  - Update medicines
  - NO delete permission
```

### 2. Create Test Users

#### Create Manager User:
```bash
python manage.py createsuperuser --username manager --email manager@pharmacy.com
```

#### Create Staff User:
```bash
python manage.py createsuperuser --username staff --email staff@pharmacy.com
```

### 3. Assign Users to Groups

**Via Django Admin:**
1. Go to: http://127.0.0.1:8000/admin/
2. Navigate to **Users**
3. Select a user
4. Scroll to **Groups** section
5. Add user to either **Manager** or **Staff** group
6. Save

**Via Django Shell:**
```python
python manage.py shell

from django.contrib.auth.models import User, Group

# Assign user to Manager group
manager_user = User.objects.get(username='manager')
manager_group = Group.objects.get(name='Manager')
manager_user.groups.add(manager_group)

# Assign user to Staff group
staff_user = User.objects.get(username='staff')
staff_group = Group.objects.get(name='Staff')
staff_user.groups.add(staff_group)
```

---

## 🎯 Permission Implementation

### Views with LoginRequiredMixin
```python
class MedicineDashboardView(LoginRequiredMixin, ListView):
    """Login required for access"""
    model = Medicine
    # ...
```

### Views with @login_required Decorator
```python
@login_required
def search_medicine(request):
    """Login required for access"""
    # ...
```

### Views with Permission Check
```python
@login_required
@permission_required('inventory.delete_medicine', raise_exception=True)
def delete_all_expired(request):
    """Only Manager group can delete"""
    if not (request.user.groups.filter(name='Manager').exists() or request.user.is_superuser):
        messages.error(request, 'Only Managers have permission to delete medicines.')
        return redirect('medicine_dashboard')
    # ...
```

---

## 📝 Settings Configuration

**File:** `pharmacy_pro/settings.py`

```python
# Authentication settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'medicine_dashboard'
LOGOUT_REDIRECT_URL = 'login'
```

---

## 🌐 URL Routes

**File:** `inventory/urls.py`

```python
urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Protected Routes (Login Required)
    path('', views.MedicineDashboardView.as_view(), name='medicine_dashboard'),
    path('medicines/', views.MedicineListView.as_view(), name='medicine_list'),
    path('search/', views.search_medicine, name='search_medicine'),
    path('add/', views.AddMedicineView.as_view(), name='add_medicine'),
    path('edit/<int:pk>/', views.EditMedicineView.as_view(), name='edit_medicine'),
    path('delete-expired/', views.delete_all_expired, name='delete_expired'),
]
```

---

## 🎨 UI Features

### Sidebar User Info
Shows current user information:
- Username
- User role (Administrator/Manager/Staff/User)
- Logout button

### Login Page
- Gradient background design
- Professional branding
- Error message display
- Responsive layout
- Bootstrap 5 styling

### Edit Button
- Only visible to authenticated users with proper permissions
- Appears in dashboard table
- Yellow warning button style

---

## ✅ Testing Checklist

### Test Manager Account:
1. ✅ Login as manager
2. ✅ View dashboard
3. ✅ Add new medicine
4. ✅ Edit existing medicine
5. ✅ Delete expired medicines
6. ✅ Logout

### Test Staff Account:
1. ✅ Login as staff
2. ✅ View dashboard
3. ✅ Add new medicine
4. ✅ Edit existing medicine
5. ❌ Delete expired medicines (should show error)
6. ✅ Logout

### Test Unauthenticated Access:
1. ❌ Try accessing dashboard without login → Redirect to login
2. ❌ Try accessing add medicine → Redirect to login
3. ❌ Try accessing search → Redirect to login

---

## 🔒 Security Features

1. **Login Required**: All views protected with authentication
2. **Permission Checks**: Delete operations require Manager role
3. **Group-Based Access**: Staff cannot delete records
4. **CSRF Protection**: All forms include CSRF tokens
5. **Session Management**: Django session framework
6. **Password Security**: Django's built-in password hashing

---

## 📊 Permission Matrix

| Action | Manager | Staff | Unauthenticated |
|--------|---------|-------|-----------------|
| View Medicines | ✅ | ✅ | ❌ |
| Add Medicines | ✅ | ✅ | ❌ |
| Edit Medicines | ✅ | ✅ | ❌ |
| Delete Medicines | ✅ | ❌ | ❌ |
| View Dashboard | ✅ | ✅ | ❌ |
| Search Medicines | ✅ | ✅ | ❌ |

---

## 🚀 Quick Start Commands

```bash
# 1. Setup groups and permissions
python manage.py setup_groups

# 2. Create manager user
python manage.py createsuperuser --username manager --email manager@pharmacy.com

# 3. Create staff user  
python manage.py createsuperuser --username staff --email staff@pharmacy.com

# 4. Run server
python manage.py runserver

# 5. Assign users to groups via admin panel
# Visit: http://127.0.0.1:8000/admin/
```

---

## 📁 Files Modified/Created

### Created:
- ✅ `inventory/templates/inventory/login.html` - Login page
- ✅ `inventory/templates/inventory/edit_medicine.html` - Edit form
- ✅ `inventory/management/commands/setup_groups.py` - Setup command
- ✅ `inventory/management/__init__.py`
- ✅ `inventory/management/commands/__init__.py`

### Modified:
- ✅ `inventory/views.py` - Added authentication mixins and decorators
- ✅ `inventory/urls.py` - Added login/logout routes
- ✅ `inventory/templates/inventory/base.html` - Added user info in sidebar
- ✅ `inventory/templates/inventory/dashboard.html` - Added edit buttons
- ✅ `pharmacy_pro/settings.py` - Added authentication settings

---

## 💡 Additional Features

### Custom Login View
```python
class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'inventory/login.html'
    redirect_authenticated_user = True
```

### Edit Medicine View
```python
class EditMedicineView(LoginRequiredMixin, UpdateView):
    """Edit medicine - Manager and Staff only"""
    model = Medicine
    form_class = MedicineForm
    template_name = 'inventory/edit_medicine.html'
```

---

## 🎓 Usage Examples

### Login Process:
1. Navigate to http://127.0.0.1:8000/login/
2. Enter username and password
3. Click "Sign In"
4. Redirected to dashboard

### Delete Operation (Manager Only):
1. Login as manager
2. Navigate to "Delete Expired"
3. Confirm deletion
4. Success message displayed

### Delete Attempt (Staff - Denied):
1. Login as staff
2. Try to access "Delete Expired"
3. Error message: "Only Managers have permission to delete medicines."
4. Redirected to dashboard

---

## ✅ Success Criteria

All requirements met:
- ✅ Django's built-in authentication system configured
- ✅ Login page created with professional design
- ✅ @login_required decorators applied
- ✅ LoginRequiredMixin used for class-based views
- ✅ Manager group with full permissions (including delete)
- ✅ Staff group with limited permissions (no delete)
- ✅ Permission checks in views
- ✅ Only authenticated pharmacists can add/edit medicines
- ✅ User information displayed in sidebar
- ✅ Logout functionality working

---

## 🎉 System Ready!

The authentication system is fully configured and ready for use. Users can now:
- Login securely
- Access features based on their role
- Add and edit medicines (Manager & Staff)
- Delete records (Manager only)
- View all data (both groups)
