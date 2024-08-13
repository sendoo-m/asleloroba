from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from decimal import Decimal
from datetime import date, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
import json


from django.shortcuts import render, get_object_or_404
from .models import CompanyInformation

def company_info(request):
    company = get_object_or_404(CompanyInformation, pk=1)  # Assuming there is only one company info record
    return render(request, 'company_info.html', {'company': company})

def update_company_info(request):
    company = get_object_or_404(CompanyInformation, pk=1)
    if request.method == 'POST':
        company.name = request.POST.get('name', company.name)
        company.address_line_1 = request.POST.get('address_line_1', company.address_line_1)
        company.address_line_2 = request.POST.get('address_line_2', company.address_line_2)
        company.phone = request.POST.get('phone', company.phone)
        company.email = request.POST.get('email', company.email)
        company.save()
        return render(request, 'company_info.html', {'company': company, 'success': 'Company info updated successfully'})
    return render(request, 'update_company_info.html', {'company': company})


# Vendor List View
@login_required
def home(request):
    customer = Customer.objects.first()  # Modified to handle if no customers exist
    payments = Payment.objects.filter(customer=customer)
    sales = Sale.objects.filter(customer=customer)
    context = {
        'customer': customer,
        'payments': payments,
        'sales': sales,
    }
    return render(request, 'sales/home.html', context)

# Vendor Registration View
@login_required
def register_vendor(request):
    if request.method == "POST":
        form = VendorForm(request.POST, request.FILES)  # Added request.FILES for handling image uploads
        if form.is_valid():
            form.save()
            return redirect('vendor_list')
    else:
        form = VendorForm()
    
    return render(request, 'sales/register_vendor.html', {'form': form})


# Vendor List View
@login_required
def vendor_list(request):
    vendors = Vendor.objects.all()
    search_form = vendorsearchForm(request.GET)

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        if search_query:
            vendors = vendors.filter(
                Q(full_name__iexact=search_query) | Q(phone__iexact=search_query)
            )

    paginator = Paginator(vendors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'vendors': vendors,
        'page_obj': page_obj,
        'search_form': search_form,
    }
    return render(request, 'sales/vendor_list.html', context)


# Customer Registration View
@login_required
def register_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)  # Added request.FILES for handling image uploads
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'sales/register_customer.html', {'form': form})

# Customer List View
@login_required
def customer_list(request):
    customers = Customer.objects.all()
    search_form = customersearchForm(request.GET)

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        if search_query:
            customers = customers.filter(
                Q(name__iexact=search_query) | Q(phone__iexact=search_query)
            )

    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'customers': customers,
        'page_obj': page_obj,
        'search_form': search_form,
    }
    return render(request, 'sales/customer_list.html', context)

# Sale Management View
@login_required
def sale(request):
    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            try:
                sale = form.save(commit=False)
                sale.save()  # The save method now handles inventory deduction and validation
                messages.success(request, 'Sale was successfully completed.')
                return redirect('sale_list')
            except ValidationError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'There was an error processing the sale. Please check the details.')
    else:
        form = SaleForm()

    return render(request, 'sales/sale.html', {'form': form})



@login_required
def sale_list(request):
    search_query = request.GET.get('search', '')  # Get the search query from the request

    # Filter sales based on the search query
    sales = Sale.objects.filter(
        Q(customer__name__icontains=search_query) |
        Q(product__title__icontains=search_query)
    ).order_by('-sale_date')  # Add order_by to order by sale_date descending

    # Paginate the sales list
    paginator = Paginator(sales, 10)  # Show 10 sales per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sales': page_obj,  # Use page_obj for the sales
        'search_query': search_query,  # Pass the search query back to the template
        'page_obj': page_obj,  # Include page_obj for pagination
    }
    return render(request, 'sales/sale_list.html', context)


# Payment Management View
@login_required
def payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()

    return render(request, 'sales/payment.html', {'form': form})

# Inventory Management View
@login_required
def manage_inventory(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()

    return render(request, 'sales/manage_inventory.html', {'form': form})

# Inventory List View
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from .models import Inventory
from .forms import InventorysearchForm

@login_required
def inventory_list(request):
    inventories = Inventory.objects.all()
    search_form = InventorysearchForm(request.GET)

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        if search_query:
            inventories = inventories.filter(
                Q(product__title__icontains=search_query)
            )

    # Ensure you're paginating and displaying only the current inventory status
    paginator = Paginator(inventories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'inventories': page_obj,  # Update to reflect correct pagination
        'page_obj': page_obj,
        'search_form': search_form,
    }
    return render(request, 'sales/inventory_list.html', context)


# Unit views

class UnitListView(ListView):
    model = Unit
    context_object_name = 'unit_list'
    template_name = 'sales/unit_list.html'


class UnitCreateView(CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'sales/unit_form.html'
    success_url = reverse_lazy('unit_list')


class UnitUpdateView(UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = 'sales/update_unit.html'
    success_url = reverse_lazy('unit_list')


class UnitDeleteView(DeleteView):
    model = Unit
    context_object_name = 'unit_delete'
    template_name = 'sales/unit_delete.html'
    success_url = reverse_lazy('unit_list')


# Product views

class ProductListView(ListView):
    model = Product
    template_name = 'sales/product_list.html'
    context_object_name = 'products'  # Use 'products' in your template
    paginate_by = 10  # Number of payments per page


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'sales/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'sales/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'sales/product_delete.html'
    success_url = reverse_lazy('product_list')



# Purchase views

class PurchaseListView(ListView):
    model = Purchase
    template_name = 'sales/purchase_list.html'
    context_object_name = 'purchases'  # Use 'purchases' in your template


class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'sales/purchase_form.html'
    success_url = reverse_lazy('purchase_list')


class PurchaseUpdateView(UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'sales/purchase_form.html'
    success_url = reverse_lazy('purchase_list')


class PurchaseDeleteView(DeleteView):
    model = Purchase
    template_name = 'sales/purchase_delete.html'
    success_url = reverse_lazy('purchase_list')


# Payment views

class PaymentListView(ListView):
    model = Payment
    context_object_name = "payments"
    template_name = 'sales/payment_list.html'
    paginate_by = 10  # Number of payments per page

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')

        if search_query:
            queryset = queryset.filter(
                Q(customer__name__icontains=search_query) |
                Q(vendor__full_name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'sales/payment_form.html'
    success_url = reverse_lazy('payment_list')


class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'sales/payment_form.html'
    success_url = reverse_lazy('payment_list')


class PaymentDeleteView(DeleteView):
    model = Payment
    template_name = 'sales/payment_delete.html'
    success_url = reverse_lazy('payment_list')


# Customer Account View

class CustomerAccountView(View):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        payments = Payment.objects.filter(customer=customer)
        total_amount_owed = 0
        amount_paid = 0

        for payment in payments:
            if payment.paid:
                amount_paid += payment.amount
            else:
                total_amount_owed += payment.amount

        balance = total_amount_owed - amount_paid

        return render(request, 'sales/customer_account.html', {
            'customer': customer,
            'payments': payments,
            'total_amount_owed': total_amount_owed,
            'amount_paid': amount_paid,
            'balance': balance
        })


# Customer Purchase History View

class CustomerPurchaseHistoryView(View):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        sales = Sale.objects.filter(customer=customer)
        payments = Payment.objects.filter(customer=customer)

        total_purchases = sum(sale.total_amt for sale in sales)
        total_paid = sum(payment.amount for payment in payments)
        balance = total_purchases - float(total_paid)

        return render(request, 'sales/customer_purchase_history.html', {
            'customer': customer,
            'sales': sales,
            'payments': payments,
            'total_purchases': total_purchases,
            'total_paid': total_paid,
            'balance': balance
        })


# Payment Receipt View
class PaymentReceiptView(View):
    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id)
        customer = payment.customer

        # Retrieve all sales and payments for the customer
        sales = Sale.objects.filter(customer=customer)
        payments = Payment.objects.filter(customer=customer)

        # Calculate Total Purchases (sum of all sales)
        total_purchases = sum(Decimal(sale.total_amt) for sale in sales)

        # Calculate Total Paid (sum of all payments)
        total_paid = sum(Decimal(payment.amount) for payment in payments)

        # Calculate Balance (Total Purchases - Total Paid)
        balance = total_purchases - total_paid

        return render(request, 'sales/payment_receipt.html', {
            'payment': payment,
            'customer': customer,
            'sales': sales,
            'total_purchases': total_purchases,
            'balance': balance
        })

# vendor_details
@login_required
def vendor_details(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)

    # Converting the float fields to Decimal for accurate financial calculation
    total_purchases = Decimal(vendor.purchase_set.aggregate(Sum('total_amt'))['total_amt__sum'] or 0)
    
    
    # Get all purchases and paginate them
    purchases_list = vendor.purchase_set.all()
    
    paginator = Paginator(purchases_list, 10)  # Show 10 purchases per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'vendor': vendor,
        'total_purchases': total_purchases,
        'page_obj': page_obj,
    }
    
    return render(request, 'sales/vendor_details.html', context)
 
# Customer Details View
@login_required
def customer_details(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    payments = Payment.objects.filter(customer=customer)
    sales = Sale.objects.filter(customer=customer)

    total_purchases = sum(sale.total_amt for sale in sales)
    total_paid = sum(payment.amount for payment in payments)
    balance = total_purchases - Decimal(total_paid)

    paginator = Paginator(payments, 10)  # Show 10 purchases per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'sales/customer_details.html', {
        'customer': customer,
        'total_purchases': total_purchases,
        'total_paid': total_paid,
        'balance': balance,
        'payments': payments,
        'sales': sales,
        'page_obj': page_obj,
    })

# invoice Details View
@login_required
def invoice_details(request, pk):
    # Retrieve the Sale object based on the pk
    sale = get_object_or_404(Sale, pk=pk)
    customer = sale.customer  # Assuming Sale has a ForeignKey to Customer
    payments = Payment.objects.filter(customer=customer)
    sales = Sale.objects.filter(customer=customer)

    total_purchases = sum(sale.total_amt for sale in sales)
    total_paid = sum(payment.amount for payment in payments)
    balance = total_purchases - Decimal(total_paid)

    # Fetch company information
    company = get_object_or_404(CompanyInformation, pk=1)  # Assuming you only have one record

    paginator = Paginator(payments, 10)  # Show 10 purchases per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sales/invoice_details.html', {
        'sale': sale,
        'customer': customer,
        'total_purchases': total_purchases,
        'total_paid': total_paid,
        'balance': balance,
        'payments': payments,
        'sales': sales,
        'page_obj': page_obj,
        'company': company,  # Add company info to the context
    })


# Update Customer View
@login_required
def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_details', pk=pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'sales/update_customer.html', {'form': form})

# delete Customer View
class CustomerDeleteView(DeleteView):
    model = Customer
    context_object_name = 'customer_delete'
    template_name = 'sales/customer_delete.html'
    success_url = reverse_lazy('customer_list')

# delete vendor View
class VendorDeleteView(DeleteView):
    model = Vendor
    context_object_name = 'vendor_delete'
    template_name = 'sales/vendor_delete.html'
    success_url = reverse_lazy('vendor_list')

##==================== register_return ====================##
def register_return(request):
    if request.method == "POST":
        form = ReturnForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Return successfully registered.')
            return redirect('return_list')  # Replace with the actual URL or view for listing returns
        else:
            messages.error(request, 'There was an error registering the return.')
    else:
        form = ReturnForm()
    
    return render(request, 'sales/register_return.html', {'form': form})

class ReturnListView(ListView):
    model = Return
    template_name = 'sales/return_list.html'  # Specify your template
    context_object_name = 'returns'

# Update Vendor View
@login_required
def update_vendor(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        form = VendorForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendor_details', vendor_id=pk)  # Change 'pk' to 'vendor_id'
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'sales/update_vendor.html', {'form': form})

############################################
############################################
############################################

import json
from django.shortcuts import render
from django.db.models import Sum, F
from decimal import Decimal

def report_view(request):
    # Calculate total sales, purchases, and inventory
    sales = Sale.objects.annotate(
        annotated_qty=F('qty'), 
        annotated_total_amt=F('total_amt')
    ).values('annotated_qty', 'annotated_total_amt')

    purchases = Purchase.objects.annotate(
        annotated_qty=F('qty'), 
        annotated_total_amt=F('total_amt')
    ).values('annotated_qty', 'annotated_total_amt')

    payments = Payment.objects.annotate(
        annotated_amount=F('amount')
    ).values('annotated_amount')
    
    # Inventory: Sum the purchase quantities and subtract the sales quantities to get the remaining balance
    inventory = Inventory.objects.values('product__title').annotate(
        total_bal_qty=Sum('pur_qty') - Sum('sale_qty')
    ).order_by('product__title')

    # Convert Decimal fields to float for JSON serialization
    sales_data = [
        {'qty': float(sale['annotated_qty']), 'total_amt': float(sale['annotated_total_amt'])}
        for sale in sales
    ]
    purchases_data = [
        {'qty': float(purchase['annotated_qty']), 'total_amt': float(purchase['annotated_total_amt'])}
        for purchase in purchases
    ]
    payments_data = [
        {'amount': float(payment['annotated_amount'])}
        for payment in payments
    ]
    inventory_data = [
        {'product__title': inv['product__title'], 'total_bal_qty': float(inv['total_bal_qty'] or 0)}
        for inv in inventory
    ]

    context = {
        'sales': json.dumps(sales_data),
        'purchases': json.dumps(purchases_data),
        'payments': json.dumps(payments_data),
        'inventory': json.dumps(inventory_data),
    }

    return render(request, 'report/report.html', context)



############################################
############################################
############################################

##=============== generate daily report ================ ##
def generate_daily_report(request):
    report_date = date.today()
    start_date = report_date - timedelta(days=30)  # Change the number of days as needed
    
    daily_payments = Payment.objects.filter(paid=True, receipt_date__date__range=[start_date, report_date]).values('receipt_date__date').annotate(total_amount=Sum('amount')).order_by('-receipt_date__date')

    paginator = Paginator(daily_payments, 10)  # Show 10 payments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'report_date': report_date,
        'daily_payments': page_obj
    }
    return render(request, 'report/daily_report.html', context)

def customer_employee_report(request):
    total_customers = Customer.objects.count()
    total_employees = Vendor.objects.count()

    context = {
        'total_customers': total_customers,
        'total_employees': total_employees,
    }

    return render(request, 'report/customer_employee_report.html', context)


def financial_report(request):
    # Recalculate totals after any deletions
    total_sales = Sale.objects.aggregate(total_sales=Sum('total_amt'))['total_sales'] or Decimal('0')
    total_payments = Payment.objects.aggregate(total_payments=Sum('amount'))['total_payments'] or Decimal('0')
    total_purchases = Purchase.objects.aggregate(total_purchases=Sum('total_amt'))['total_purchases'] or Decimal('0')

    total_income = total_payments
    net_profit = total_income - total_purchases

    context = {
        'total_sales': total_sales,
        'total_purchases': total_purchases,
        'total_income': total_income,
        'net_profit': net_profit,
    }

    return render(request, 'report/financial_report.html', context)



#     return render(request, 'report/product_report.html', context)
def product_report(request):
    product_stats = []
    products = Product.objects.all()

    for product in products:
        # Get the latest inventory record for the product
        latest_inventory = Inventory.objects.filter(product=product).order_by('-id').first()

        if latest_inventory:
            total_inventory = latest_inventory.total_bal_qty or 0
        else:
            total_inventory = 0
        
        # Calculate total purchase quantity from Inventory
        total_purchase_qty = Inventory.objects.filter(product=product).aggregate(total_qty=Sum('pur_qty'))['total_qty'] or 0
        
        # Calculate total sales quantity from Inventory
        total_sales_qty_for_product = Inventory.objects.filter(product=product).aggregate(total_qty=Sum('sale_qty'))['total_qty'] or 0
        
        # Calculate total revenue from Sale records
        total_revenue = Sale.objects.filter(product=product).aggregate(total_revenue=Sum('total_amt'))['total_revenue'] or 0
        
        # Calculate total cost from Purchase records
        total_cost = Purchase.objects.filter(product=product).aggregate(total_cost=Sum('total_amt'))['total_cost'] or 0
        
        # Calculate product profit
        product_profit = total_revenue - total_cost

        product_stat = {
            'product': product,
            'total_purchase_qty': total_purchase_qty,  # Total quantity purchased
            'total_sales_qty': total_sales_qty_for_product,  # Total quantity sold
            'total_inventory': total_inventory,  # Remaining inventory
            'total_revenue': total_revenue,
            'total_cost': total_cost,
            'product_profit': product_profit,
        }
        product_stats.append(product_stat)

    context = {
        'product_stats': product_stats,
    }

    return render(request, 'report/product_report.html', context)

