from django.shortcuts import render,redirect
from .forms import InventoryCategoryForm, InventoryItemForm
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
    
    return render(request, 'inventory/add_inventory_item.html', {'form': form})
    