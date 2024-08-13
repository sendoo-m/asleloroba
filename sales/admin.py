from django.contrib import admin
from .models import *

# Customize admin site titles
admin.site.site_header = 'LYS Account System Administration'
admin.site.site_title = 'Asl Eloroba Admin'
admin.site.index_title = 'Welcome to Asl Eloroba Admin'

class PurchaseAdmin(admin.ModelAdmin):
    list_display=['product','qty','price','total_amt','vendor','pur_date']

class VendorAdmin(admin.ModelAdmin):
    list_display=['full_name','address','id_number','phone','status']

class CustomerAdmin(admin.ModelAdmin):
    list_display=['name','address','phone']

class SaleAdmin(admin.ModelAdmin):
    list_display=['product', 'customer', 'qty','price','total_amt','sale_date', 'expire_date']

class ProductAdmin(admin.ModelAdmin):
    list_display=['title','unit']

class UnitAdmin(admin.ModelAdmin):
    list_display=['title','short_name']

class InventoryAdmin(admin.ModelAdmin):
    list_display=['product','pur_qty','sale_qty','total_bal_qty']
    
class PaymentAdmin(admin.ModelAdmin):
    list_display=['customer','vendor','installment_number','payment_method','amount','receipt_date']

@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ('sale_info', 'return_reason', 'return_qty', 'refund_amount', 'return_date')

    def sale_info(self, obj):
        return f"{obj.sale.product.title} by {obj.sale.customer.name}"


admin.site.register(Vendor,VendorAdmin)
admin.site.register(Unit,UnitAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Product,ProductAdmin)

admin.site.register(Purchase,PurchaseAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Inventory,InventoryAdmin)
admin.site.register(Sale,SaleAdmin)
