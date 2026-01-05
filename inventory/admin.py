from django.contrib import admin
from .models import Medicine, Pharmacist, CashBox
@admin.register(CashBox)
class CashBoxAdmin(admin.ModelAdmin):
    list_display = ['id', 'current_cash', 'last_updated']
    readonly_fields = ['last_updated']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'stock_quantity', 'expiry_date', 'get_status']
    list_filter = ['category', 'expiry_date']
    search_fields = ['name', 'category']
    ordering = ['-id']
    list_per_page = 25
    
    def get_status(self, obj):
        from datetime import date
        if obj.expiry_date < date.today():
            return "Expired"
        elif obj.stock_quantity == 0:
            return "Out of Stock"
        elif obj.stock_quantity <= 10:
            return "Low Stock"
        return "Active"
    get_status.short_description = 'Status'


@admin.register(Pharmacist)
class PharmacistAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'get_full_name', 'phone_number', 'date_of_joining', 'qualification']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'phone_number']
    ordering = ['employee_id']
    list_per_page = 25
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Full Name'
