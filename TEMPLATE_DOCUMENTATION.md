# Template Documentation - Pharmacy Management System

## Base Template with Sidebar Navigation

### File: `inventory/templates/inventory/base.html`

#### Features:
✅ **Sidebar Navigation** - Fixed left sidebar with gradient blue background
✅ **Bootstrap 5 Styling** - Modern, responsive design
✅ **Active Page Highlighting** - Current page highlighted in sidebar
✅ **Icon Integration** - Bootstrap Icons throughout

#### Navigation Menu:
- **Dashboard** - Overview with statistics
- **Medicine List** - Detailed table view with expiry highlighting
- **Add Medicine** - Form to add new medicines
- **Search** - Search for specific medicines
- **Employees** - Link to admin panel for employee management
- **Delete Expired** - Remove expired medicines
- **Admin Panel** - Full Django admin access

#### Styling Features:
- Gradient sidebar: Blue (#0d6efd to #0a58ca)
- Hover effects on menu items
- Active page indicator with yellow border
- Fixed sidebar (250px width)
- Responsive main content area
- Professional shadows and rounded corners

---

## Medicine List Template

### File: `inventory/templates/inventory/medicine_list.html`

#### Features:
✅ **Complete Medicine Table** - All inventory records displayed
✅ **Expiry Date Highlighting** - Color-coded rows based on expiry status
✅ **Statistics Dashboard** - Quick overview cards
✅ **Pagination** - 50 items per page
✅ **Sorting** - Ordered by expiry date (expiring items first)

#### Color-Coded Row Highlighting:

1. **Red Background (Expired)**
   - Condition: `expiry_date < today`
   - CSS Class: `expired-row`
   - Background: `#f8d7da` (light red)
   - Left Border: 4px solid red (#dc3545)
   - Status Badge: Red "EXPIRED"

2. **Yellow Background (Expiring Soon)**
   - Condition: `expiry_date within next 30 days`
   - CSS Class: `expiring-soon`
   - Background: `#fff3cd` (light yellow)
   - Left Border: 4px solid yellow (#ffc107)
   - Status Badge: Yellow "Expiring Soon"

3. **White Background (Active)**
   - Condition: `expiry_date > 30 days from now`
   - No special class
   - Normal table styling
   - Status Badge: Green "Active"

#### Table Columns:
1. ID
2. Medicine Name
3. Category
4. Price ($)
5. Stock (with color badges)
6. Manufacture Date
7. Expiry Date
8. Days Until Expiry
9. Status

#### Django Template Logic:

```django
{% if medicine.expiry_date < today %}
    {# Red - Expired #}
    <tr class="expired-row">
        ...
    </tr>
{% else %}
    {% if medicine.days_until_expiry <= 30 %}
        {# Yellow - Expiring within 30 days #}
        <tr class="expiring-soon">
            ...
        </tr>
    {% else %}
        {# White - Active #}
        <tr>
            ...
        </tr>
    {% endif %}
{% endif %}
```

#### Statistics Cards:
- **Total Medicines** - Count of all medicines
- **Expiring Soon** - Medicines expiring within 30 days
- **Expired** - Already expired medicines
- **Low Stock** - Items with ≤10 units

#### Legend Display:
Visual legend at top of page showing:
- 🔴 Red Badge = Expired
- 🟡 Yellow Badge = Expiring within 30 days  
- 🟢 Green Badge = Active & Valid

---

## View Implementation

### File: `inventory/views.py`

```python
class MedicineListView(ListView):
    """Display all medicines in a detailed table with expiry highlighting"""
    model = Medicine
    template_name = 'inventory/medicine_list.html'
    context_object_name = 'medicines'
    paginate_by = 50
    ordering = ['expiry_date']  # Show expiring items first
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Calculate days until expiry for each medicine
        for medicine in queryset:
            delta = medicine.expiry_date - date.today()
            medicine.days_until_expiry = delta.days
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        thirty_days_later = today + timedelta(days=30)
        
        context['total_medicines'] = Medicine.objects.count()
        context['expired'] = Medicine.objects.filter(expiry_date__lt=today).count()
        context['expiring_soon'] = Medicine.objects.filter(
            expiry_date__gte=today,
            expiry_date__lte=thirty_days_later
        ).count()
        context['low_stock'] = Medicine.objects.filter(stock_quantity__lte=10).count()
        context['today'] = today
        return context
```

---

## URL Configuration

### File: `inventory/urls.py`

```python
urlpatterns = [
    path('', views.MedicineDashboardView.as_view(), name='medicine_dashboard'),
    path('medicines/', views.MedicineListView.as_view(), name='medicine_list'),
    path('search/', views.search_medicine, name='search_medicine'),
    path('add/', views.AddMedicineView.as_view(), name='add_medicine'),
    path('delete-expired/', views.delete_all_expired, name='delete_expired'),
]
```

---

## Usage

### Accessing the Medicine List:
```
http://127.0.0.1:8000/medicines/
```

### Features in Action:

1. **Expired Medicines** appear at the top (sorted by expiry date)
   - Red background highlights them immediately
   - "EXPIRED" badge clearly visible
   - Warning icon next to name

2. **Medicines Expiring Soon** (within 30 days)
   - Yellow background for visual warning
   - "Expiring Soon" label under name
   - Days remaining shown in badge

3. **Active Medicines** (>30 days until expiry)
   - Normal white background
   - Green "Active" status badge
   - Days until expiry shown in gray badge

4. **Stock Indicators**
   - Red badge: Out of stock (0 units)
   - Yellow badge: Low stock (≤10 units)
   - Green badge: Good stock (>10 units)

---

## CSS Customization

All styles are embedded in `base.html`:

```css
/* Expired row styling */
.expired-row {
    background-color: #f8d7da !important;
    border-left: 4px solid #dc3545;
}

/* Expiring soon row styling */
.expiring-soon {
    background-color: #fff3cd !important;
    border-left: 4px solid #ffc107;
}

/* Sidebar styling */
.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 250px;
    background: linear-gradient(180deg, #0d6efd 0%, #0a58ca 100%);
}
```

---

## Benefits

✅ **Visual Priority System** - Critical items (expired/expiring) stand out
✅ **Quick Scanning** - Color coding allows fast inventory assessment
✅ **Professional Design** - Clean, modern Bootstrap 5 interface
✅ **User-Friendly Navigation** - Intuitive sidebar with icons
✅ **Responsive Layout** - Works on different screen sizes
✅ **Consistent Branding** - Unified color scheme throughout
✅ **Accessibility** - Clear labels, badges, and visual indicators

---

## Template Hierarchy

```
base.html (Sidebar + Layout)
├── dashboard.html (Statistics overview)
├── medicine_list.html (Detailed table with highlighting)
├── add_medicine.html (Form)
├── search_medicine.html (Search interface)
└── confirm_delete_expired.html (Delete confirmation)
```

All templates extend `base.html` to maintain consistent navigation and styling.
