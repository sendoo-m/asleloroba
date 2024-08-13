from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Vendor)
@receiver(post_delete, sender=Vendor)
def update_vendor_count(sender, **kwargs):
    total_vendors = Vendor.objects.count()
    Vendor.objects.update(total_vendors=total_vendors)

@receiver(post_save, sender=Customer)
@receiver(post_delete, sender=Customer)
def update_customer_count(sender, **kwargs):
    total_customers = Customer.objects.count()
    Customer.objects.update(total_customers=total_customers)

@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def update_product_count(sender, **kwargs):
    total_products = Product.objects.count()
    Product.objects.update(total_products=total_products)


@receiver(post_save, sender=Sale)
def update_inventory_on_save(sender, instance, **kwargs):
    # Update inventory after a sale is saved
    try:
        inventory = Inventory.objects.get(product=instance.product)
        inventory.sale_qty = Sale.objects.filter(product=instance.product).aggregate(Sum('qty'))['qty__sum'] or 0
        inventory.save()
    except Inventory.DoesNotExist:
        # Handle the case where Inventory does not exist for the product
        pass

@receiver(post_delete, sender=Sale)
def update_inventory_on_delete(sender, instance, **kwargs):
    # Update inventory after a sale is deleted
    try:
        inventory = Inventory.objects.get(product=instance.product)
        inventory.sale_qty = Sale.objects.filter(product=instance.product).aggregate(Sum('qty'))['qty__sum'] or 0
        inventory.save()
    except Inventory.DoesNotExist:
        # Handle the case where Inventory does not exist for the product
        pass

# @receiver(post_save, sender=Purchase)
# @receiver(post_delete, sender=Purchase)
# def update_purchase_total(sender, **kwargs):
#     total_purchases = Purchase.objects.aggregate(total=models.Sum('total_amt'))['total'] or 0
#     Product.objects.update(total_purchases=total_purchases)

# @receiver(post_save, sender=Sale)
# @receiver(post_delete, sender=Sale)
# def update_sale_total(sender, **kwargs):
#     total_sales = Sale.objects.aggregate(total=models.Sum('total_amt'))['total'] or 0
#     Product.objects.update(total_sales=total_sales)

# @receiver(post_save, sender=Purchase)
# def update_product_purchase(sender, instance, **kwargs):
#     product = instance.product
#     product.total_purchases += instance.total_amt
#     product.total_products += instance.qty
#     product.save()

# @receiver(post_save, sender=Sale)
# def update_product_sale(sender, instance, **kwargs):
#     product = instance.product
#     product.total_sales += instance.total_amt
#     product.total_products -= instance.qty
#     product.save()