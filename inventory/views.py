from django.shortcuts import render,redirect,get_object_or_404
from .forms import InventoryCategoryForm, InventoryItemForm, SizeVariantForm,StockReceiptForm, StockReceiptItemFormSet
from .models import Inventory_Item,SizeVariant, StockReceipt, StockReceiptItem, Supplier
from collections import defaultdict
from employees.models import Store
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
import json
# Create your views here.

def add_inventory_category(request):
    if request.method == 'POST':
        form = InventoryCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_inventory_category')
    else:
        form = InventoryCategoryForm()

    return render(request,'inventory/add_inventory_category.html',{'form':form} )

def add_inventory_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_inventory_item')
    else:
        form = InventoryItemForm()
    
    items = Inventory_Item.objects.select_related('category').all()
    return render(request, 'inventory/add_inventory_item.html', {'form': form,'items':items
    })



def edit_inventory_item(request, item_id):
    item = get_object_or_404(Inventory_Item, pk=item_id)

    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('add_inventory_item')
    else:
        form = InventoryItemForm(instance=item)

    items = Inventory_Item.objects.all()
    return render(request, 'inventory/add_inventory_item.html', {'form': form, 'items': items})

def delete_inventory_item(request, item_id):
    item = get_object_or_404(Inventory_Item, pk=item_id)
    item.delete()
    return redirect('add_inventory_item')



# def add_size_variant(request):
#     form = SizeVariantForm()
#     variants = SizeVariant.objects.select_related('item')  # For item.item_name access

#     if request.method == 'POST':
#         form = SizeVariantForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('add_size_variant')  # Redirect back to the same form or change if needed

#     return render(request, 'inventory/add_size_variant.html', {'form': form,'variants': variants })
def add_size_variant(request):
    from .forms import SizeVariantForm

    if request.method == 'POST':
        form = SizeVariantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_size_variant')  # Refresh the view after saving
    else:
        form = SizeVariantForm()

    # Grouping SizeVariants by item
    grouped_variants = defaultdict(list)
    for variant in SizeVariant.objects.select_related('item'):
        grouped_variants[variant.item].append(variant)

    context = {
        'form': form,
        'grouped_variants': grouped_variants.items(),  # gives (item, [variants])
    }
    return render(request, 'inventory/add_size_variant.html', context)


def edit_size_variant(request, pk):
    size_variant = get_object_or_404(SizeVariant, pk=pk)
    if request.method == 'POST':
        form = SizeVariantForm(request.POST, instance=size_variant)
        if form.is_valid():
            form.save()
            return redirect('add_size_variant')  # Or to a list page
    else:
        form = SizeVariantForm(instance=size_variant)
    return render(request, 'inventory/edit_size_variant.html', {'form': form})

def delete_size_variant(request, pk):
    size_variant = get_object_or_404(SizeVariant, pk=pk)
    if request.method == 'POST':
        size_variant.delete()
        return redirect('add_size_variant')
    return render(request, 'inventory/confirm_delete.html', {'object': size_variant})

def add_stock_receipt(request):
    items = Inventory_Item.objects.all()
    suppliers = Supplier.objects.all()
    stores = Store.objects.all()

    if request.method == 'POST':
        receipt_no = request.POST.get('receipt_no')
        store_id = request.POST.get('store')
        received_date = request.POST.get('received_date')
        attachment = request.FILES.get('attachment')

        # Save StockReceipt
        stock_receipt = StockReceipt.objects.create(
            receipt_no=receipt_no,
            store_id=store_id,
            received_date=received_date,
            attachment=attachment,
            received_by=request.user if request.user.is_authenticated else None
        )

        # Save StockReceiptItems (loop through multiple rows)
        items_list = request.POST.getlist('item[]')
        sizes_list = request.POST.getlist('size_variant[]')
        qty_list = request.POST.getlist('quantity[]')
        unit_list = request.POST.getlist('unit[]')
        expiry_list = request.POST.getlist('expiry_date[]')

        for i in range(len(items_list)):
            item_id = items_list[i]
            size_id = sizes_list[i] or None  # Optional
            quantity = qty_list[i]
            unit = unit_list[i]
            expiry = expiry_list[i] or None  # Optional

            StockReceiptItem.objects.create(
                stock_receipt=stock_receipt,
                item_id=item_id,
                size_variant_id=size_id,
                quantity_received=quantity,
                unit=unit,
                expiry_date=expiry
            )

        return redirect('add_stock_receipt')  # Success

    # GET request: prepare context and show form
    size_variant_data = defaultdict(list)
    for variant in SizeVariant.objects.select_related('item'):
        size_variant_data[variant.item.id].append({
            'id': variant.id,
            'size_label': variant.size_label
        })

    context = {
        'items': items,
        'suppliers': suppliers,
        'stores': stores,
        'size_variant_data': json.dumps(size_variant_data),
    }

    return render(request, 'inventory/add_stock_receipt.html', context)
