from django.contrib import admin
from django.contrib import admin
from .models import (
    Inventory_Category,
    Supplier,
    Inventory_Item,
    ItemStoreStock,
    SizeVariant,
    StockReceipt,
    StockReceiptItem,
    ItemIssuance,           
    ItemIssuanceItem 
    

)

# Register your models here.
admin.site.register(Inventory_Category)
admin.site.register(Supplier)
admin.site.register(Inventory_Item)
admin.site.register(ItemStoreStock)
admin.site.register(SizeVariant)
admin.site.register(StockReceipt)
admin.site.register(StockReceiptItem)
admin.site.register(ItemIssuance)         
admin.site.register(ItemIssuanceItem) 
