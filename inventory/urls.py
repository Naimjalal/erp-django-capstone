from django.urls import path
from . import views

urlpatterns = [
    path('categories/add/', views.add_inventory_category, name='add_inventory_category'),
    path('items/add/', views.add_inventory_item, name='add_inventory_item'),
]
