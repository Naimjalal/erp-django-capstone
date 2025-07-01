from django.db import models 
from employees.models import Store,Employee
from users.models import User
from django.conf import settings




# Create your models here.
class Inventory_Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.category_name 
    
class Supplier(models.Model):

    supplier_name = models.CharField(max_length=100, unique=True)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.supplier_name
    
class Inventory_Item(models.Model):
    item_name = models.CharField(max_length=100)
    category = models.ForeignKey(Inventory_Category, on_delete=models.CASCADE)
    is_returnable = models.BooleanField(default=True, help_text="True = item must be returned")
    has_expiry = models.BooleanField(default=False, help_text="True = item has expiry date")
    unit = models.CharField(max_length=50, help_text="e.g. pcs, box, liters")
    image = models.ImageField(upload_to='item_photos/', blank=True, null=True)
    # created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.item_name
    
class ItemStoreStock(models.Model):
    item = models.ForeignKey(Inventory_Item, on_delete=models.CASCADE, help_text="Reference to the inventory item")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, help_text="Reference to the store")
    size = models.CharField(max_length=50, blank=True, null=True, help_text="Size label (e.g., S, M, L, XL)")
    quantity_original = models.PositiveIntegerField(help_text="Original received quantity")
    quantity_current = models.PositiveIntegerField(help_text="Current available quantity")

    def __str__(self):
        return f"{self.item.item_name} @ {self.store.store_name}"
    
class SizeVariant (models.Model):
    item = models.ForeignKey(Inventory_Item, on_delete=models.CASCADE,help_text="Reference to the inventory item")
    size_label = models.CharField(max_length=50, help_text="e.g., S, M, L, 42, XL")
    quantity_original = models.PositiveIntegerField(default=0, help_text="Original quantity received")
    quantity_current = models.PositiveIntegerField(default=0, help_text="Current available quantity")

    def __str__(self):
        return f"{self.item.item_name} - {self.size_label}"

class StockReceipt(models.Model):
    receipt_no = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    # received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    received_date = models.DateTimeField()
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)

    def __str__(self):
        return f"Receipt {self.receipt_no} - {self.store}"

class StockReceiptItem(models.Model):
        
    stock_receipt = models.ForeignKey(StockReceipt, on_delete=models.CASCADE, related_name='receipt_items')
    item = models.ForeignKey(Inventory_Item, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity_received = models.PositiveIntegerField()
    unit = models.CharField(max_length=20, help_text="Unit for this batch (e.g., pcs, box, liters)")
    expiry_date = models.DateField(null=True, blank=True)
        
    def __str__(self):
        return f"{self.item.item_name} - Qty: {self.quantity_received}"
    
class ItemIssuance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='issued_items')
    issue_date = models.DateField()
    shift = models.CharField(max_length=20)
    is_emergency = models.BooleanField(default=False)
    card_verified = models.BooleanField(default=False)
    verification_time = models.DateTimeField(null=True, blank=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Issuance to {self.employee} on {self.issue_date}"


class ItemIssuanceItem(models.Model):
    issuance = models.ForeignKey(ItemIssuance, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Inventory_Item, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.item} for Issuance #{self.issuance.id}"

class ItemReturn(models.Model):
    issuance = models.OneToOneField(ItemIssuance, on_delete=models.CASCADE)
    returned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    return_date = models.DateTimeField(auto_now_add=True)
    card_verified = models.BooleanField(default=False)
    verification_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Return for Issuance #{self.issuance.id}"

class ItemReturnItem(models.Model):
    return_record = models.ForeignKey(ItemReturn, on_delete=models.CASCADE)
    item = models.ForeignKey(Inventory_Item, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    is_damaged = models.BooleanField(default=False)
    damage_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        size = f" - {self.size_variant.size_label}" if self.size_variant else ""
        return f"Return: {self.quantity} x {self.item.item_name}{size}"


















