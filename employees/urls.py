from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_employee, name='add_employee'),
    path('list/', views.employee_list, name='list_employee'),
    path('edit/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('deactivate/<int:pk>/', views.deactivate_employee, name='deactivate_employee'),
    path('inactive/', views.inactive_employees, name='inactive_employees'),
    path('reactivate/<int:pk>/', views.reactivate_employee, name='reactivate_employee'),
    path('search/', views.employee_search, name='employee_search'),





]