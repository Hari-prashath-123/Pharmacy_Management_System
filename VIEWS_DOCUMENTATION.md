# Pharmacy Management System - Views Documentation

## Overview
The inventory app includes multiple views for managing pharmacy medicines efficiently using Django's Class-Based Views (CBV) and function-based views.

---

## Views Implemented

### 1. Medicine Dashboard (Class-Based View - ListView)
**URL:** `/` (root)  
**View:** `MedicineDashboardView`  
**Template:** `inventory/dashboard.html`

**Features:**
- Lists all medicines in the inventory with pagination (20 items per page)
- Displays key statistics:
  - Total medicines count
  - Low stock items (≤10 units)
  - Expired medicines count
- Shows medicine details: ID, name, category, price, stock, dates, and status
- Color-coded stock indicators:
  - 🔴 Red: Out of stock (0 units)
  - 🟡 Yellow: Low stock (≤10 units)
  - 🟢 Green: Good stock (>10 units)
- Status badges for expired/active medicines

---

### 2. Search Medicine (Function-Based View)
**URL:** `/search/`  
**View:** `search_medicine`  
**Template:** `inventory/search_medicine.html`

**Features:**
- Search medicines by exact name (case-insensitive)
- Displays comprehensive medicine details:
  - **Rate (Price):** Current selling price
  - **Expiry Date:** With expired/valid status badge
  - **Stock Status:** Out of Stock / Low Stock / In Stock
- Provides summary with:
  - Price per unit
  - Availability status
  - Expiration warnings
- Handles medicine not found scenarios
- Suggests adding new medicine if not found

**Usage:**
```
GET /search/?q=Aspirin
```

---

### 3. Add Medicine (Class-Based View - CreateView)
**URL:** `/add/`  
**View:** `AddMedicineView`  
**Template:** `inventory/add_medicine.html`

**Features:**
- Form to add new medicine stock
- Fields:
  - Name (required)
  - Category (required)
  - Price (required, decimal)
  - Stock Quantity (required, integer)
  - Manufacture Date (required, date picker)
  - Expiry Date (required, date picker)
- Form validation:
  - Ensures expiry date is after manufacture date
  - Validates all required fields
- Success message on successful addition
- Redirects to dashboard after adding

---

### 4. Delete Expired Medicines (Function-Based View)
**URL:** `/delete-expired/`  
**View:** `delete_all_expired`  
**Template:** `inventory/confirm_delete_expired.html`

**Features:**
- Lists all medicines that have expired (expiry_date < today)
- Shows detailed table with:
  - Medicine ID, name, category, price
  - Current stock quantity
  - Expiry date
  - Days since expiration
- Confirmation prompt before deletion
- Bulk delete functionality (removes all expired medicines at once)
- Success/info messages after operation
- Shows success message if no expired medicines exist

---

## Technical Implementation

### Class-Based Views Used:
1. **ListView** - `MedicineDashboardView`
   - Automatic pagination
   - Query optimization
   - Context data enrichment

2. **CreateView** - `AddMedicineView`
   - Form handling
   - Validation
   - Automatic model saving

### Form Implementation:
**File:** `inventory/forms.py`  
**Class:** `MedicineForm`

- Bootstrap 5 styling
- Custom widgets for all fields
- Date pickers for date fields
- Form-level validation
- Clean, user-friendly labels

---

## URL Configuration

**Main URLs** (`pharmacy_pro/urls.py`):
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),
]
```

**Inventory URLs** (`inventory/urls.py`):
```python
urlpatterns = [
    path('', views.MedicineDashboardView.as_view(), name='medicine_dashboard'),
    path('search/', views.search_medicine, name='search_medicine'),
    path('add/', views.AddMedicineView.as_view(), name='add_medicine'),
    path('delete-expired/', views.delete_all_expired, name='delete_expired'),
]
```

---

## Templates

All templates extend `inventory/base.html` which includes:
- Bootstrap 5 styling
- Responsive navigation bar
- Message display system
- Footer
- Consistent layout

### Template Files:
1. `base.html` - Base template with navigation
2. `dashboard.html` - Medicine listing dashboard
3. `search_medicine.html` - Medicine search interface
4. `add_medicine.html` - Add medicine form
5. `confirm_delete_expired.html` - Delete expired medicines confirmation

---

## Admin Panel Integration

**File:** `inventory/admin.py`

Registered models with custom admin interfaces:

### MedicineAdmin:
- List display with all key fields
- Status indicator (Expired/Out of Stock/Low Stock/Active)
- Search by name and category
- Filter by category and expiry date
- Pagination (25 items per page)

### PharmacistAdmin:
- Employee ID, full name, contact details
- Search by employee ID, name, phone
- Ordered by employee ID

---

## Usage Instructions

### Starting the Server:
```bash
# Activate virtual environment first
.venv\Scripts\Activate.ps1

# Run server
python manage.py runserver
```

### Accessing Views:
- **Dashboard:** http://127.0.0.1:8000/
- **Search:** http://127.0.0.1:8000/search/
- **Add Medicine:** http://127.0.0.1:8000/add/
- **Delete Expired:** http://127.0.0.1:8000/delete-expired/
- **Admin Panel:** http://127.0.0.1:8000/admin/

---

## Features Summary

✅ **Class-Based Views** for efficiency  
✅ **Search functionality** with detailed medicine info  
✅ **Dashboard** with statistics and pagination  
✅ **Add medicine** form with validation  
✅ **Delete expired** medicines with bulk operation  
✅ **Responsive design** using Bootstrap 5  
✅ **Color-coded indicators** for stock status  
✅ **Admin panel integration**  
✅ **Message system** for user feedback  

---

## Next Steps

Consider implementing:
- User authentication and permissions
- Edit medicine functionality
- Medicine sales tracking
- Inventory reports and analytics
- Email alerts for low stock/expiring medicines
- Barcode scanning integration
- PDF invoice generation
