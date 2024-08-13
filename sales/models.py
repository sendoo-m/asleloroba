from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.db.models import Sum
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Count
from django.db.models import Sum, F
import datetime  # Make sure this import is at the top of your file


# Vendor
class Vendor(models.Model):
    full_name   = models.CharField(max_length=100)
    address     = models.TextField()
    id_number   = models.CharField(max_length=10)
    photo       = models.ImageField(upload_to="Vendor/", blank=True, null=True)
    phone       = models.CharField(max_length=15)
    status      = models.BooleanField(default=False)
    total_vendors = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = '01 Vendor'
        verbose_name_plural = '01 Vendors'

    def __str__(self):
        return self.full_name

# customer
class Customer(models.Model):
    name        = models.CharField(max_length=100)
    address     = models.TextField()
    phone       = models.CharField(max_length=15)
    photo       = models.ImageField(upload_to="customer/", blank=True, null=True)
    date        = models.DateField(auto_now_add=True)
    total_customers = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = '02 customer'
        verbose_name_plural = '02 customers'

    def __str__(self):
        return self.name


# Unit
class Unit(models.Model):
    title       = models.CharField(max_length=50)
    short_name  = models.CharField(max_length=50)

    class Meta:
        verbose_name = '04 Unit'
        verbose_name_plural = '04 Units'

    def __str__(self):
        return self.title

# Product
## ======================== start Product ======================== ##
    # total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    # total_purchases = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)

class Product(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="product/", blank=True, null=True)
    total_products = models.PositiveIntegerField(default=0, editable=False)    # Track current stock

    class Meta:
        verbose_name = '05 Product'
        verbose_name_plural = '05 Products'

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Ensure that all related inventory records are deleted
        Inventory.objects.filter(product=self).delete()
        super(Product, self).delete(*args, **kwargs)
## ======================== end Product ======================== ##


## ======================== start Purchase ======================== ##
class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amt = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    pur_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateField()

    class Meta:
        verbose_name = '03 purchase'
        verbose_name_plural = '03 purchases'

    def save(self, *args, **kwargs):
        self.total_amt = self.qty * self.price
        super(Purchase, self).save(*args, **kwargs)

        inventory, created = Inventory.objects.get_or_create(
            product=self.product,
            defaults={'total_bal_qty': self.qty}
        )

        if not created:
            inventory.total_bal_qty += self.qty
            inventory.pur_qty += self.qty
        else:
            inventory.pur_qty = self.qty

        inventory.save()

        # Update total_purchases
        total_purchases = Purchase.objects.filter(product=self.product).aggregate(total=models.Sum('total_amt'))['total'] or 0
        self.product.total_purchases = total_purchases
        self.product.save()

    def delete(self, *args, **kwargs):
        inventory = Inventory.objects.filter(product=self.product).order_by('-id').first()

        if inventory:
            inventory.total_bal_qty -= self.qty
            inventory.pur_qty -= self.qty
            inventory.save()

        super(Purchase, self).delete(*args, **kwargs)

        # Update total_purchases
        total_purchases = Purchase.objects.filter(product=self.product).aggregate(total=models.Sum('total_amt'))['total'] or 0
        self.product.total_purchases = total_purchases
        self.product.save()


## ======================== end Purchase ======================== ##
## ======================== end Purchase ======================== ##
## ======================== end Purchase ======================== ##
## ======================== end Purchase ======================== ##
## ======================== end Purchase ======================== ##
## ======================== end Purchase ======================== ##



## ======================== start sale ======================== ##
# class Sale(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     qty = models.FloatField()
#     price = models.FloatField()
#     total_amt = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
#     sale_date = models.DateTimeField(auto_now_add=True)
#     expire_date = models.DateField()

#     class Meta:
#         verbose_name = '06 sale'
#         verbose_name_plural = '06 sales'

#     def save(self, *args, **kwargs):
#         self.total_amt = Decimal(self.qty) * Decimal(self.price)
#         super(Sale, self).save(*args, **kwargs)

#         inventory = Inventory.objects.filter(product=self.product).order_by('-id').first()
#         if inventory:
#             if Decimal(inventory.total_bal_qty) < Decimal(self.qty):
#                 raise ValidationError(f"Not enough inventory available. Only {inventory.total_bal_qty} items left.")

#             inventory.total_bal_qty = Decimal(inventory.total_bal_qty) - Decimal(self.qty)
#             inventory.sale_qty = Decimal(inventory.sale_qty) + Decimal(self.qty)
#             inventory.save()

#     def delete(self, *args, **kwargs):
#         inventory = Inventory.objects.filter(product=self.product).order_by('-id').first()
#         if inventory:
#             inventory.total_bal_qty = Decimal(inventory.total_bal_qty) + Decimal(self.qty)
#             inventory.sale_qty = Decimal(inventory.sale_qty) - Decimal(self.qty)
#             inventory.save()

#         super(Sale, self).delete(*args, **kwargs)

# sale
from decimal import Decimal

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    qty = models.FloatField()
    price = models.FloatField()
    total_amt = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    sale_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateField()

    class Meta:
        verbose_name = '06 sale'
        verbose_name_plural = '06 sales'

    def save(self, *args, **kwargs):
        # Convert qty and price to Decimal before multiplying
        self.total_amt = Decimal(self.qty) * Decimal(self.price)

        # Check if the inventory is available
        inventory = Inventory.objects.filter(product=self.product).order_by('-id').first()

        if inventory is None:
            raise ValidationError(f"No inventory record found for the product '{self.product.title}'.")

        print(f"Before Sale: Total Balance Qty: {inventory.total_bal_qty}, Sale Qty: {inventory.sale_qty}")

        if Decimal(inventory.total_bal_qty) < Decimal(self.qty):
            raise ValidationError(f"Not enough inventory available. Only {inventory.total_bal_qty} items left.")

        # Deduct the sold quantity from the inventory
        inventory.total_bal_qty = Decimal(inventory.total_bal_qty) - Decimal(self.qty)
        inventory.sale_qty = Decimal(inventory.sale_qty) + Decimal(self.qty)
        inventory.save()

        print(f"After Sale: Total Balance Qty: {inventory.total_bal_qty}, Sale Qty: {inventory.sale_qty}")

        super(Sale, self).save(*args, **kwargs)

## ======================== end sale ======================== ##
## ======================== end sale ======================== ##
## ======================== end sale ======================== ##
## ======================== end sale ======================== ##
## ======================== end sale ======================== ##
## ======================== end sale ======================== ##
## ======================== end sale ======================== ##

# class Inventory(models.Model):
#     product = models.OneToOneField(Product, on_delete=models.CASCADE)
#     purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True, blank=True)
#     sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True, blank=True)
#     pur_qty = models.FloatField(default=0, null=True)
#     sale_qty = models.FloatField(default=0, null=True)
#     total_bal_qty = models.FloatField()

#     class Meta:
#         verbose_name = '07 Inventory'
#         verbose_name_plural = '07 Inventories'
#         constraints = [
#             models.UniqueConstraint(fields=['product'], name='unique_product_inventory')
#         ]

#     def __str__(self):
#         return f"{self.product.title} - {self.total_bal_qty} items"

class Inventory(models.Model):
    product         = models.OneToOneField(Product, on_delete=models.CASCADE)
    total_bal_qty   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pur_qty         = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sale_qty        = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_purchases = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Check for this field

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return str(self.product)


################## get inventory report ################



# Payment
## ======================== start Payment ======================== ##

# class Payment(models.Model):

#     PAYMENT_METHOD_CHOICES = (
#         ('Cash', 'Cash'),
#         ('Transfer', 'Transfer'),
#         ('Visa', 'Visa'),
#     )
#     customer            = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     vendor              = models.ForeignKey(Vendor, on_delete=models.CASCADE, default=0)
#     installment_number  = models.IntegerField(editable=False)
#     paid                = models.BooleanField(default=False)
#     receipt_date        = models.DateTimeField(default=timezone.now, editable=False)
#     payment_method      = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
#     amount              = models.DecimalField(max_digits=10, decimal_places=2)

#     class Meta:
#         verbose_name = '08 Payment'
#         verbose_name_plural = '08 Payment'

#     def __str__(self):
#         return f"{self.customer.name} - {self.amount} via {self.payment_method}"

#     def save(self, *args, **kwargs):
#         if not self.installment_number:
#             last_payment = Payment.objects.filter(customer=self.customer).order_by('-installment_number').first()
#             if last_payment:
#                 self.installment_number = last_payment.installment_number + 1
#             else:
#                 self.installment_number = 1
#         super(Payment, self).save(*args, **kwargs)

from django.db.models import Sum

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('Cash', 'Cash'),
        ('Transfer', 'Transfer'),
        ('Visa', 'Visa'),
    )
    customer            = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor              = models.ForeignKey(Vendor, on_delete=models.CASCADE, default=0)
    installment_number  = models.IntegerField(editable=False)
    paid                = models.BooleanField(default=False)
    receipt_date        = models.DateTimeField(default=timezone.now, editable=False)
    payment_method      = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    amount              = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = '08 Payment'
        verbose_name_plural = '08 Payments'

    def __str__(self):
        return f"{self.customer.name} - {self.amount} via {self.payment_method}"

    def save(self, *args, **kwargs):
        if not self.installment_number:
            last_payment = Payment.objects.filter(customer=self.customer).order_by('-installment_number').first()
            if last_payment:
                self.installment_number = last_payment.installment_number + 1
            else:
                self.installment_number = 1
        super(Payment, self).save(*args, **kwargs)

    @property
    def total_payments(self):
        return Payment.objects.filter(customer=self.customer).aggregate(total=Sum('amount'))['total'] or 0

## ======================== end Payment ======================== ##

## ======================== Start Return ======================== ##
# class Return(models.Model):
#     RETURN_REASON_CHOICES = (
#         ('Expired', 'Expired'),
#         ('Near to Expire', 'Near to Expire'),
#     )

#     sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
#     return_date = models.DateTimeField(default=timezone.now)
#     return_reason = models.CharField(max_length=20, choices=RETURN_REASON_CHOICES)
#     return_qty = models.FloatField()
#     return_amt = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

#     class Meta:
#         verbose_name = '09 Return'
#         verbose_name_plural = '09 Returns'

#     def __str__(self):
#         return f"Return of {self.return_qty} {self.sale.product.title} by {self.sale.customer.name}"

#     def save(self, *args, **kwargs):
#         # Calculate the return amount based on the sale price
#         self.return_amt = Decimal(self.return_qty) * Decimal(self.sale.price)
        
#         # Update inventory by adding the returned quantity back
#         inventory = Inventory.objects.filter(product=self.sale.product).order_by('-id').first()

#         if inventory:
#             inventory.total_bal_qty = Decimal(inventory.total_bal_qty) + Decimal(self.return_qty)
#             inventory.sale_qty = Decimal(inventory.sale_qty) - Decimal(self.return_qty)
#             inventory.save()

#         super(Return, self).save(*args, **kwargs)
class Return(models.Model):
    RETURN_REASON_CHOICES = (
        ('Expired', 'Expired'),
        ('Near to Expire', 'Near to Expire'),
    )
    sale            = models.ForeignKey(Sale, on_delete=models.CASCADE)
    return_reason = models.CharField(max_length=20, choices=RETURN_REASON_CHOICES)
    return_qty      = models.DecimalField(max_digits=10, decimal_places=2)
    refund_amount   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    return_date     = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = '09 Return'
        verbose_name_plural = '09 Returns'

    def __str__(self):
        return f"Return for {self.sale.product.title} - {self.return_qty} units"

    def save(self, *args, **kwargs):
        super(Return, self).save(*args, **kwargs)

        # Deduct the refund amount from the total payments of the customer
        payment = Payment.objects.filter(customer=self.sale.customer).order_by('-receipt_date').first()
        if payment and not payment.paid:
            payment.amount -= self.refund_amount
            if payment.amount < 0:
                payment.amount = 0
            payment.save()

## ======================== end Return ======================== ##

class DailyOperationReport(models.Model):
    date = models.DateField(unique=True)
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_outcome = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Daily Operation Report for {self.date}"
