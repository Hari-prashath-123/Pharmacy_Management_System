from django.db import models
from django.contrib.auth.models import User


class Medicine(models.Model):
    """Model representing a medicine in the pharmacy inventory"""
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Medicines"


class CashBox(models.Model):
    """Model representing the cash box in the pharmacy"""
    current_cash = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CashBox: ₹{self.current_cash}"

    class Meta:
        verbose_name_plural = "Cash Box"

class Pharmacist(models.Model):
    """Model extending User to manage pharmacist/employee details"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_joining = models.DateField()
    qualification = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"
    
    class Meta:
        verbose_name_plural = "Pharmacists"
