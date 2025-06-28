from django.urls import path
from . import views

urlpatterns = [
    path('categories/add/', views.add_inventory_category, name='add_inventory_category'),
    path('items/add/', views.add_inventory_item, name='add_inventory_item'),
    path('items/edit/<int:item_id>/', views.edit_inventory_item, name='edit_inventory_item'),
    path('items/delete/<int:item_id>/', views.delete_inventory_item, name='delete_inventory_item'),
]
