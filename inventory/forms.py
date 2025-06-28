from django import forms
from .models import Inventory_Category,Inventory_Item, SizeVariant, StockReceipt, StockReceiptItem
from django.forms import inlineformset_factory

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

class SizeVariantForm(forms.ModelForm):
    class Meta:
        model = SizeVariant
        fields = ['item', 'size_label']


class StockReceiptForm(forms.ModelForm):
    class Meta:
        model = StockReceipt
        fields = ['receipt_no', 'supplier', 'received_by', 'store', 'received_date', 'attachment']

class StockReceiptItemForm(forms.ModelForm):
    class Meta:
        model = StockReceiptItem
        fields = ['item', 'size_variant', 'quantity_received', 'unit', 'expiry_date']

# Create inline formset
StockReceiptItemFormSet = inlineformset_factory(
    StockReceipt, StockReceiptItem,
    form=StockReceiptItemForm,
    extra=1,
    can_delete=True
)