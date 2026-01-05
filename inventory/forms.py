from django import forms
from django.contrib.auth.models import User, Group
from .models import Medicine


class MedicineForm(forms.ModelForm):
    """Form for adding/editing medicine"""
    
    class Meta:
        model = Medicine
        fields = ['name', 'category', 'price', 'stock_quantity', 'manufacture_date', 'expiry_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter medicine name'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Antibiotic, Painkiller'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': '0'}),
            'manufacture_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'name': 'Medicine Name',
            'category': 'Category',
            'price': 'Price (₹)',
            'stock_quantity': 'Stock Quantity',
            'manufacture_date': 'Manufacture Date',
            'expiry_date': 'Expiry Date',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        manufacture_date = cleaned_data.get('manufacture_date')
        expiry_date = cleaned_data.get('expiry_date')
        
        if manufacture_date and expiry_date:
            if expiry_date <= manufacture_date:
                raise forms.ValidationError('Expiry date must be after manufacture date.')
        
        return cleaned_data


class EmployeeForm(forms.ModelForm):
    """Form for adding new employee"""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=['Manager', 'Staff']),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Role'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'employee@pharmacy.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2


class EmployeeEditForm(forms.ModelForm):
    """Form for editing existing employee"""
    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=['Manager', 'Staff']),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Role'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'employee@pharmacy.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

