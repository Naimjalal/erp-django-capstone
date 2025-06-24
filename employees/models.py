from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator

# Create your models here.
class Designation(models.Model):
    designation_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.designation_name
    
class Position(models.Model):
    position_name = models.CharField(max_length=100, unique =True )

    def __str__(self):
        return self.position_name

class Section(models.Model):
    section_no = models.CharField(max_length=10, unique=True)
    section_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.section_name

class Store(models.Model):
    store_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255,blank=True )

    def __str__(self):
        return self.store_name

class Employee(models.Model):
    employee_no = models.CharField(max_length=50, unique=True,validators=[RegexValidator(r'^\d+$', 'Only numbers are allowed.')], help_text="Employee ID number")
    employee_name = models.CharField(max_length=100)
    cpr=models.CharField(max_length=9, unique=True, validators=[RegexValidator(r'^\d{9}$', 'CPR must be exactly 9 digits.')] )
    phone1 = models.CharField(max_length=8,validators=[RegexValidator(r'^\d{8}$', 'Phone must be 8 digits.')])
    phone2 = models.CharField(max_length=8, blank=True, null=True)
    nationality = models.CharField(max_length =20)
    joining_date = models.DateField()
    last_promotion_date =models.DateField(blank=True, null=True)
    image= models.ImageField(upload_to='employee_images/', blank=True,null =True)

    position = models.ForeignKey('Position', on_delete=models.SET_NULL, null = True)
    designation = models.ForeignKey('Designation', on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True,blank=True )

    def __str__(self):
        return f"{self.employee_no} - {self.employee_name}"

