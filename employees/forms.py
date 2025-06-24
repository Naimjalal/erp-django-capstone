from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        labels = {
            'employee_no': 'Employee Number',
            'employee_name': 'Employee Name',
            'cpr':'CPR Number',
            'phone1': 'Primary Phone',
            'phone2': 'Secondary Phone (Optional)',
            }
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),'last_promotion_date':forms.DateInput(attrs={'type':'date'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            }
        help_texts = {
            'employee_no':'Enter the employee’s unique ID number.','cpr': 'Enter the 9-digit CPR number.',
            'phone1': 'Enter 8-digit phone number.',
            }

