from django.urls import path
from . import views

urlpatterns = [
    path('categories/add/', views.add_inventory_category, name='add_inventory_category'),
    path('items/add/', views.add_inventory_item, name='add_inventory_item'),
    path('items/edit/<int:item_id>/', views.edit_inventory_item, name='edit_inventory_item'),
    path('items/delete/<int:item_id>/', views.delete_inventory_item, name='delete_inventory_item'),
    path('add-size-variant/', views.add_size_variant, name='add_size_variant'),
    path('size-variant/edit/<int:pk>/', views.edit_size_variant, name='edit_size_variant'),
    path('size-variant/delete/<int:pk>/', views.delete_size_variant, name='delete_size_variant'),
    path('stock-receipt/add/', views.add_stock_receipt, name='add_stock_receipt'),
    path('stock-receipts/', views.stock_receipt_list, name='stock_receipt_list'),
    path('receipts/<int:pk>/', views.receipt_detail, name='receipt_detail'),
    path('stock-receipt/<int:pk>/', views.receipt_detail, name='stock_receipt_detail'),
    path('stock-receipt/delete/<int:pk>/', views.delete_stock_receipt, name='delete_stock_receipt'),
    path('issue-items/', views.add_item_issuance, name='add_item_issuance'),
    path('issuances/', views.item_issuance_list, name='item_issuance_list'),
    path('return-items/', views.return_items, name='return_items'),
    path('confirm-return/', views.confirm_return, name='confirm_return'),
    path('returns/', views.return_list, name='return_list'),










]
