from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee , Section
from .forms import EmployeeForm
# Create your views here.

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_employee')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Add Employee'})

def employee_list(request):
    # employees = Employee.objects.filter(is_active=True)
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees':employees})

def edit_employee(request, pk):
    employee = get_object_or_404(Employee,pk=pk)
    if request.method =='POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('list_employee')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html',{'form': form, 'title': 'Edit Employee',
    'edit': True})

# def delete_employee(request,pk):
#     employee = get_object_or_404(Employee,pk=pk)
#     if request.method == 'POST':
#         employee.delete()
#         return redirect('list_employee')
#     return render(request, 'employees/confirm_delete.html')
def deactivate_employee(request,pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.is_active =False
    employee.save()
    return redirect('list_employee')

def inactive_employees(request):
    employees = Employee.objects.filter(is_active=False)
    return render(request, 'employees/inactive_list.html',{'employees': employees})

def reactivate_employee(request, pk):
    employee = get_object_or_404(Employee,pk=pk, is_active=False)
    employee.is_active = True
    employee.save()
    return redirect('inactive_employees')

def employee_search(request):
    searched = False
    result = None
    query = request.GET.get('emp_num')
    if query:
        searched = True
        try:
            result = Employee.objects.get(employee_no__icontains=query)
        except Employee.DoesNotExist:
            result = None
    return render(request, 'employees/employee_search.html', {'result': result, 'searched': searched})


def employee_list(request):
    section_id = request.GET.get('section')
    employees = Employee.objects.all()

    if section_id:
        employees = employees.filter(section_id = section_id )
    
    sections = Section.objects.all()
    return render(request,'employees/employee_list.html',{
        'employees': employees,
        'sections': sections,
        'selected_section': section_id,
    })




