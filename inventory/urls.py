from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Medicine Management
    path('', views.MedicineDashboardView.as_view(), name='medicine_dashboard'),
    path('medicines/', views.MedicineListView.as_view(), name='medicine_list'),
    path('search/', views.search_medicine, name='search_medicine'),
    path('add/', views.AddMedicineView.as_view(), name='add_medicine'),
    path('edit/<int:pk>/', views.EditMedicineView.as_view(), name='edit_medicine'),
    path('delete-expired/', views.delete_all_expired, name='delete_expired'),
    path('update-stock/<int:pk>/', views.update_stock, name='update_stock'),
    
    # Employee Management
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/edit/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('employees/delete/<int:pk>/', views.delete_employee, name='delete_employee'),
]
