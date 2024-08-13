from django import forms
from .models import *



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'address']

class customersearchForm(forms.Form):
    search_query = forms.CharField(
        label='Search', 
        required=False, 
        max_length=100, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by Name, Phone',
            'class': 'form-control',
        })
    )
    phone = forms.ModelChoiceField(
        queryset=Customer.objects.all(), 
        label='Phone', 
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'

class vendorsearchForm(forms.Form):
    search_query = forms.CharField(
        label='Search', 
        required=False, 
        max_length=100, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by Name, Phone',
            'class': 'form-control',
        })
    )
    phone = forms.ModelChoiceField(
        queryset=Vendor.objects.all(), 
        label='Phone', 
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

class InventorysearchForm(forms.Form):
    search_query = forms.CharField(
        label='Search', 
        required=False, 
        max_length=100, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Search product',
            'class': 'form-control',
        })
    )
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(), 
        label='product', 
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

# class SaleForm(forms.ModelForm):
#     class Meta:
#         model = Sale
#         fields = ('product', 'customer', 'qty','price', 'expire_date')


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'customer', 'qty', 'price', 'expire_date']
    
    def clean_qty(self):
        qty = self.cleaned_data['qty']
        if qty <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return qty
    
    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('payment_method', 'amount', 'customer')

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('total_bal_qty', 'sale_qty')

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('title', 'short_name')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'detail', 'unit', 'photo')

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('product', 'vendor', 'qty', 'price', 'expire_date')

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('product', 'pur_qty', 'sale_qty', 'total_bal_qty')

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('customer', 'vendor', 'paid', 'payment_method', 'amount')


class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ['sale', 'return_reason', 'return_qty']
    
    def clean_return_qty(self):
        return_qty = self.cleaned_data.get('return_qty')
        sale = self.cleaned_data.get('sale')
        
        # Ensure the return quantity does not exceed the original sale quantity
        if return_qty > sale.qty:
            raise forms.ValidationError(f"Cannot return more than the originally sold quantity ({sale.qty} items).")
        
        return return_qty


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'address', 'phone', 'photo')

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ('full_name', 'address', 'id_number', 'photo', 'phone', 'status')

