from django import forms
from .models import Inventory_Category,Inventory_Item

class InventoryCategoryForm(forms.ModelForm):
    class Meta:
        model = Inventory_Category
        fields = ['category_name']
        labels={
            'category_name':'Category Name'
        }
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control'})
        }

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = Inventory_Item
        fields = ['item_name', 'category', 'is_returnable', 'has_expiry', 'unit', 'image']
        widgets = {
            'is_returnable': forms.CheckboxInput(),
            'has_expiry': forms.CheckboxInput(),
        }

