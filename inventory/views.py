from django.shortcuts import render,redirect,get_object_or_404
from django.forms import modelform_factory, inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import InventoryCategoryForm, InventoryItemForm, SizeVariantForm,StockReceiptForm, StockReceiptItemFormSet,ItemIssuanceForm, ItemIssuanceItemForm
from .models import Inventory_Item,SizeVariant, StockReceipt, StockReceiptItem, Supplier,Inventory_Category,ItemIssuance,ItemIssuanceItem,ItemReturn, ItemReturnItem
from django.db.models import Sum
from collections import defaultdict
from employees.models import Store,Employee
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
import json
from django.forms import modelformset_factory
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

def add_size_variant(request):
    if request.method == 'POST':
        form = SizeVariantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_size_variant')
    else:
        form = SizeVariantForm()

    grouped_variants = defaultdict(list)

    for variant in SizeVariant.objects.select_related('item'):
        
        total_received = StockReceiptItem.objects.filter(size_variant=variant).aggregate(
            total=Sum('quantity_received')
        )['total'] or 0

        
        total_issued = ItemIssuanceItem.objects.filter(size_variant=variant).aggregate(
            total=Sum('quantity')
        )['total'] or 0

        
        calculated_current = total_received - total_issued

        if (
            variant.quantity_original != total_received or
            variant.quantity_current != calculated_current
        ):
            variant.quantity_original = total_received
            variant.quantity_current = max(0, calculated_current)
            variant.save()

        
        grouped_variants[variant.item].append({
            'variant': variant,
            'original_qty': variant.quantity_original,
            'current_qty': variant.quantity_current,
        })

    context = {
        'form': form,
        'grouped_variants': grouped_variants.items(),
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
    items = Inventory_Item.objects.select_related('category').all()
    suppliers = Supplier.objects.all()
    stores = Store.objects.all()
    categories = Inventory_Category.objects.all()

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

        
        items_list = request.POST.getlist('item[]')
        sizes_list = request.POST.getlist('size_variant[]')
        qty_list = request.POST.getlist('quantity[]')
        unit_list = request.POST.getlist('unit[]')
        expiry_list = request.POST.getlist('expiry_date[]')

        for i in range(len(items_list)):
            item_id = items_list[i]
            size_id = sizes_list[i] or None  
            quantity = qty_list[i]
            unit = unit_list[i]
            expiry = expiry_list[i] or None  

            StockReceiptItem.objects.create(
                stock_receipt=stock_receipt,
                item_id=item_id,
                size_variant_id=size_id,
                quantity_received=quantity,
                unit=unit,
                expiry_date=expiry
            )

        return redirect('add_stock_receipt')  

    
    size_variant_data = defaultdict(list)
    for variant in SizeVariant.objects.select_related('item'):
        size_variant_data[variant.item.id].append({
            'id': variant.id,
            'size_label': variant.size_label
        })

   
    item_data = defaultdict(list)
    item_expiry_map = {item.id: item.has_expiry for item in items} 
    for item in items:
        item_data[item.category.id].append({
            'id': item.id,
            'name': item.item_name,
            'has_expiry': item.has_expiry,
            
            

        })

    context = {
        'items': items,
        'suppliers': suppliers,
        'stores': stores,
        'categories': categories,
        'size_variant_data': json.dumps(size_variant_data),
        'item_data': json.dumps(item_data),
        'item_expiry_map': json.dumps(item_expiry_map),
    }

    return render(request, 'inventory/add_stock_receipt.html', context)

def stock_receipt_list(request):
    receipts = StockReceipt.objects.select_related('store', 'received_by').order_by('-received_date')
    return render(request, 'inventory/stock_receipt_list.html', {'receipts': receipts})

def receipt_detail(request, pk):
    receipt = get_object_or_404(StockReceipt, pk=pk)
    items = receipt.receipt_items.all()
   

    return render(request, 'inventory/receipt_detail.html',{
        'receipt': receipt,
        'items': items

    })


def delete_stock_receipt(request, pk):
    receipt = get_object_or_404(StockReceipt, pk=pk)
    if request.method == 'POST':
        receipt.delete()
        return redirect('stock_receipt_list')  

    return render(request, 'inventory/confirm_delete_receipt.html', {'receipt': receipt})

@login_required
def add_item_issuance(request):
    categories = Inventory_Category.objects.all()
    items = Inventory_Item.objects.select_related('category')
    size_variants = SizeVariant.objects.select_related('item')
    employees = Employee.objects.all()

    if request.method == 'POST':
        issuance = ItemIssuance.objects.create(
            employee_id=request.POST.get('employee'),
            issue_date=request.POST.get('issue_date'),
            shift=request.POST.get('shift'),
            is_emergency=bool(request.POST.get('is_emergency')),
            card_verified=bool(request.POST.get('card_verified')),
            verification_time=request.POST.get('verification_time') or None,
            note=request.POST.get('note'),
            issued_by=request.user
        )

        items_list = request.POST.getlist('item[]')
        sizes_list = request.POST.getlist('size_variant[]')
        qty_list = request.POST.getlist('quantity[]')

        for i in range(len(items_list)):
            item_id = items_list[i]
            size_id = sizes_list[i] or None
            quantity = int(qty_list[i])

            ItemIssuanceItem.objects.create(
                issuance=issuance,
                item_id=item_id,
                size_variant_id=size_id,
                quantity=quantity
            )

            
            if size_id:
                size_variant = SizeVariant.objects.get(id=size_id)
                size_variant.quantity_current = max(0, size_variant.quantity_current - quantity)
                size_variant.save()

        return redirect('item_issuance_list')  # ✅ success redirect

    # GET method → prepare form
    item_data = {}
    for item in items:
        item_data.setdefault(item.category_id, []).append({
            'id': item.id,
            'name': item.item_name,
            'has_expiry': item.has_expiry
        })

    size_variant_data = {}
    for sv in size_variants:
        size_variant_data.setdefault(sv.item_id, []).append({
            'id': sv.id,
            'size_label': sv.size_label
        })

    item_expiry_map = {item.id: item.has_expiry for item in items}

    context = {
        'employees': employees,
        'categories': categories,
        'item_data': json.dumps(item_data),
        'size_variant_data': json.dumps(size_variant_data),
        'item_expiry_map': json.dumps(item_expiry_map),
    }

    return render(request, 'inventory/add_item_issuance.html', context)




def item_issuance_list(request):
    issuances = ItemIssuance.objects.all().order_by('-issue_date')
    return render(request, 'inventory/item_issuance_list.html', {
        'issuances': issuances
    })


@login_required
def return_items(request):
    employees = Employee.objects.all()
    issued_items = []

    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        if employee_id:
            
            returned_issuance_ids = ItemReturn.objects.values_list('issuance_id', flat=True)

            issuances = ItemIssuance.objects.filter(
            employee_id=employee_id
            ).exclude(id__in=returned_issuance_ids).order_by('-issue_date')

            for issuance in issuances:
                for item in issuance.items.filter(item__is_returnable=True):
                    issued_items.append({
                        'issuance_id': issuance.id,
                        'item_id': item.item.id,
                        'size_variant_id': item.size_variant.id if item.size_variant else '',
                        'item_name': item.item.item_name,
                        'size': item.size_variant.size_label if item.size_variant else '',
                        'quantity': item.quantity
                    })

    return render(request, 'inventory/return_items.html', {
        'employees': employees,
        'issued_items': issued_items
    })

@login_required
def confirm_return(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        return_item_ids = request.POST.getlist('return_item_ids[]')

        if not return_item_ids:
            messages.error(request, "No items selected for return.")
            return redirect('return_items')

      
        first_issuance_id = request.POST.get(f'issuance_id_{return_item_ids[0]}')
        issuance = get_object_or_404(ItemIssuance, id=first_issuance_id)

        item_return = ItemReturn.objects.create(
            issuance=issuance,
            returned_by=request.user,
            card_verified=False,
            verification_time=None
        )

        for i in return_item_ids:
            item_id = request.POST.get(f'item_id_{i}')
            size_variant_id = request.POST.get(f'size_variant_id_{i}') or None
            quantity = int(request.POST.get(f'quantity_{i}'))

            ItemReturnItem.objects.create(
                return_record=item_return,
                item_id=item_id,
                size_variant_id=size_variant_id,
                quantity=quantity
            )

            if size_variant_id:
                size_variant = SizeVariant.objects.get(id=size_variant_id)
                size_variant.quantity_current += quantity
                size_variant.save()

        messages.success(request, "Items returned successfully.")
        return redirect('item_issuance_list')