from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('hr','HR'),
        ('Scheduler', 'Scheduler'),
        ('supervisor', 'Supervisor'),
        ('viewer', 'Viewer'),
    )
    role = models.CharField(max_length=20, choices =ROLE_CHOICES)