from django.shortcuts import render,redirect,get_object_or_404
from .forms import InventoryCategoryForm, InventoryItemForm
from .models import Inventory_Item
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

from django.shortcuts import get_object_or_404

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
 