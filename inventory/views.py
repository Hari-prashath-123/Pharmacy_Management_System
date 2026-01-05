from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import date
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User, Group
from django.http import HttpResponseForbidden
from .models import Medicine
from .forms import MedicineForm


class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'inventory/login.html'
    redirect_authenticated_user = True


class MedicineDashboardView(LoginRequiredMixin, ListView):
    """Display all medicines in the inventory - Login Required"""
    model = Medicine
    template_name = 'inventory/dashboard.html'
    context_object_name = 'medicines'
    paginate_by = 20
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_medicines'] = Medicine.objects.count()
        context['low_stock'] = Medicine.objects.filter(stock_quantity__lte=10).count()
        context['expired'] = Medicine.objects.filter(expiry_date__lt=date.today()).count()
        context['today'] = date.today()
        from .models import CashBox
        cash_box = CashBox.objects.first()
        context['cash_box'] = cash_box
        return context


class AddMedicineView(LoginRequiredMixin, CreateView):
    """Form view to add new medicine stock - Manager Only"""
    model = Medicine
    form_class = MedicineForm
    template_name = 'inventory/add_medicine.html'
    success_url = reverse_lazy('medicine_dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, f'Medicine "{form.instance.name}" added successfully!')
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        # Check if user has permission to add medicines - MANAGER ONLY
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not (request.user.groups.filter(name='Manager').exists() or request.user.is_superuser):
            messages.error(request, 'Only Managers have permission to add medicines.')
            return redirect('medicine_dashboard')
        return super().dispatch(request, *args, **kwargs)


class EditMedicineView(LoginRequiredMixin, UpdateView):
    """Form view to edit existing medicine - Manager Only"""
    model = Medicine
    form_class = MedicineForm
    template_name = 'inventory/edit_medicine.html'
    success_url = reverse_lazy('medicine_dashboard')
    pk_url_kwarg = 'pk'
    
    def form_valid(self, form):
        messages.success(self.request, f'Medicine "{form.instance.name}" updated successfully!')
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        # Check if user has permission to change medicines - MANAGER ONLY
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not (request.user.groups.filter(name='Manager').exists() or request.user.is_superuser):
            messages.error(request, 'Only Managers have permission to edit medicines.')
            return redirect('medicine_dashboard')
        return super().dispatch(request, *args, **kwargs)


@login_required
def search_medicine(request):
    """Search for medicines by name and display details - Login Required"""
    context = {
        'searched': False,
        'medicine': None,
        'query': ''
    }
    
    if request.method == 'GET' and 'q' in request.GET:
        query = request.GET.get('q', '').strip()
        context['query'] = query
        context['searched'] = True
        
        if query:
            # Search for medicine (case-insensitive)
            try:
                medicine = Medicine.objects.get(name__iexact=query)
                context['medicine'] = medicine
                
                # Determine stock status
                if medicine.stock_quantity == 0:
                    context['stock_status'] = 'Out of Stock'
                    context['stock_class'] = 'danger'
                elif medicine.stock_quantity <= 10:
                    context['stock_status'] = 'Low Stock'
                    context['stock_class'] = 'warning'
                else:
                    context['stock_status'] = 'In Stock'
                    context['stock_class'] = 'success'
                
                # Check if expired
                context['is_expired'] = medicine.expiry_date < date.today()
                
            except Medicine.DoesNotExist:
                messages.warning(request, f'Medicine "{query}" not found in inventory.')
            except Medicine.MultipleObjectsReturned:
                # If multiple medicines with same name, get the first one
                medicine = Medicine.objects.filter(name__iexact=query).first()
                context['medicine'] = medicine
                messages.info(request, 'Multiple medicines found with this name. Showing the first match.')
    
    return render(request, 'inventory/search_medicine.html', context)


class DeleteExpiredMedicinesView(DeleteView):
    """View to delete expired medicines"""
    model = Medicine
    template_name = 'inventory/delete_expired.html'
    success_url = reverse_lazy('medicine_dashboard')
    
    def get_queryset(self):
        """Only show expired medicines"""
        return Medicine.objects.filter(expiry_date__lt=date.today())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expired_medicines'] = self.get_queryset()
        return context


@login_required
@permission_required('inventory.delete_medicine', raise_exception=True)
def delete_all_expired(request):
    """Delete all expired medicines at once - Manager Only"""
    # Check if user is in Manager group
    if not (request.user.groups.filter(name='Manager').exists() or request.user.is_superuser):
        messages.error(request, 'Only Managers have permission to delete medicines.')
        return redirect('medicine_dashboard')
    
    if request.method == 'POST':
        expired_medicines = Medicine.objects.filter(expiry_date__lt=date.today())
        count = expired_medicines.count()
        
        if count > 0:
            expired_medicines.delete()
            messages.success(request, f'Successfully deleted {count} expired medicine(s).')
        else:
            messages.info(request, 'No expired medicines found.')
        
        return redirect('medicine_dashboard')
    
    # If GET request, show confirmation page
    expired_medicines = Medicine.objects.filter(expiry_date__lt=date.today())
    context = {
        'expired_medicines': expired_medicines,
        'count': expired_medicines.count()
    }
    return render(request, 'inventory/confirm_delete_expired.html', context)


class MedicineListView(LoginRequiredMixin, ListView):
    """Display all medicines in a detailed table with expiry highlighting - Login Required"""
    model = Medicine
    template_name = 'inventory/medicine_list.html'
    context_object_name = 'medicines'
    paginate_by = 50
    ordering = ['expiry_date']  # Order by expiry date to show expiring items first
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Annotate each medicine with days until expiry
        from datetime import timedelta
        for medicine in queryset:
            delta = medicine.expiry_date - date.today()
            medicine.days_until_expiry = delta.days
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        from datetime import timedelta
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


@login_required
def employee_list(request):
    """Display all employees - Manager Only"""
    if not (request.user.groups.filter(name='Manager').exists() or request.user.is_superuser):
        messages.error(request, 'Only Managers have permission to view employees.')
        return redirect('medicine_dashboard')
    
    employees = User.objects.all().order_by('-date_joined')
    return render(request, 'inventory/employee_list.html', {'employees': employees})


@login_required
def add_employee(request):
    """Add new employee - Manager Only"""
    if not (request.user.groups.filter(name='Manager').exists() or request.user.is_superuser):
        messages.error(request, 'Only Managers have permission to add employees.')
        return redirect('medicine_dashboard')
    
    if request.method == 'POST':
        from .forms import EmployeeForm
        form = EmployeeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            # Add to group
            group = form.cleaned_data['group']
            user.groups.add(group)
            
            messages.success(request, f'Employee "{user.username}" created successfully!')
            return redirect('employee_list')
    else:
        from .forms import EmployeeForm
        form = EmployeeForm()
    
    return render(request, 'inventory/add_employee.html', {'form': form})


@login_required
def edit_employee(request, pk):
    """Edit existing employee - Manager Only"""
    if not (request.user.groups.filter(name='Manager').exists() or request.user.is_superuser):
        messages.error(request, 'Only Managers have permission to edit employees.')
        return redirect('medicine_dashboard')
    
    employee = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        from .forms import EmployeeEditForm
        form = EmployeeEditForm(request.POST, instance=employee)
        if form.is_valid():
            user = form.save()
            
            # Update group
            if 'group' in form.cleaned_data:
                user.groups.clear()
                group = form.cleaned_data['group']
                user.groups.add(group)
            
            messages.success(request, f'Employee "{user.username}" updated successfully!')
            return redirect('employee_list')
    else:
        from .forms import EmployeeEditForm
        initial_group = employee.groups.first()
        form = EmployeeEditForm(instance=employee, initial={'group': initial_group})
    
    return render(request, 'inventory/edit_employee.html', {'form': form, 'employee': employee})


@login_required
def delete_employee(request, pk):
    """Delete employee - Manager Only"""
    if not (request.user.groups.filter(name='Manager').exists() or request.user.is_superuser):
        messages.error(request, 'Only Managers have permission to delete employees.')
        return redirect('medicine_dashboard')
    
    employee = get_object_or_404(User, pk=pk)
    
    if employee.is_superuser:
        messages.error(request, 'Cannot delete superuser account.')
        return redirect('employee_list')
    
    username = employee.username
    employee.delete()
    messages.success(request, f'Employee "{username}" deleted successfully!')
    return redirect('employee_list')


@login_required
def update_stock(request, pk):
    """Update medicine stock after sale - Staff can use this"""
    from .models import CashBox
    medicine = get_object_or_404(Medicine, pk=pk)
    cash_box = CashBox.objects.first()
    if not cash_box:
        # Create a cash box if not exists
        cash_box = CashBox.objects.create(current_cash=0)
    
    if request.method == 'POST':
        sold_quantity = int(request.POST.get('sold_quantity', 0))
        
        if sold_quantity <= 0:
            messages.error(request, 'Sold quantity must be greater than 0.')
        elif sold_quantity > medicine.stock_quantity:
            messages.error(request, f'Cannot sell {sold_quantity} units. Only {medicine.stock_quantity} units available.')
        else:
            medicine.stock_quantity -= sold_quantity
            medicine.save()
            # Add cash to cash box
            total_sale = sold_quantity * medicine.price
            cash_box.current_cash += total_sale
            cash_box.save()
            messages.success(request, f'Stock updated! Sold {sold_quantity} units of "{medicine.name}". Remaining: {medicine.stock_quantity}. Cash in box: ₹{cash_box.current_cash}')
        
        return redirect('medicine_dashboard')
    
    return render(request, 'inventory/update_stock.html', {'medicine': medicine, 'cash_box': cash_box})


