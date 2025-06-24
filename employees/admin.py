from django.contrib import admin
from .models import Designation,Position, Section,Store,  Employee
# Register your models here.
admin.site.register(Designation)
admin.site.register(Position)
admin.site.register(Section)
admin.site.register(Store)
admin.site.register(Employee)