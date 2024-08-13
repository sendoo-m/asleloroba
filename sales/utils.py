from datetime import datetime, timedelta
from .models import *


def generate_daily_report(date):
    daily_report, created = DailyReport.objects.get_or_create(date=date)
    daily_report.total_revenue = Sale.objects.filter(date=date).aggregate(models.Sum('total_amt'))['total_amt__sum'] or 0
    daily_report.total_expenses = Purchase.objects.filter(date=date).aggregate(models.Sum('total_amt'))['total_amt__sum'] or 0
    daily_report.profit = daily_report.total_revenue - daily_report.total_expenses
    daily_report.save()
    return daily_report

def generate_monthly_report(month):
    monthly_report, created = MonthlyReport.objects.get_or_create(month=month)
    sales = Sale.objects.filter(date__month=month)
    purchases = Purchase.objects.filter(date__month=month)
    monthly_report.total_revenue = sales.aggregate(models.Sum('total_amt'))['total_amt__sum'] or 0
    monthly_report.total_expenses = purchases.aggregate(models.Sum('total_amt'))['total_amt__sum'] or 0
    monthly_report.profit = monthly_report.total_revenue - monthly_report.total_expenses
    monthly_report.save()
    return monthly_report

def generate_warehouse_report(date):
    warehouse_report, created = WarehouseReport.objects.get_or_create(date=date)
    warehouse_report.total_items = Inventory.objects.filter(date=date).aggregate(models.Sum('total_bal_qty'))['total_bal_qty__sum'] or 0
    warehouse_report.total_value = Inventory.objects.filter(date=date).aggregate(models.Sum(models.F('total_bal_qty') * models.F('product__price')))['total_bal_qty__product__price__sum'] or 0
    warehouse_report.save()
    return warehouse_report

def generate_customer_report(date):
    customer_report, created = CustomerReport.objects.get_or_create(date=date)
    customer_report.total_customers = Sale.objects.filter(date=date).values('customer').distinct().count()
    customer_report.total_revenue = Sale.objects.filter(date=date).aggregate(models.Sum('total_amt'))['total_amt__sum'] or 0
    customer_report.save()
    return customer_report

# def generate_vendor_report(date):
#     vendor_report, created = VendorReport.objects.get_or_create(date=date)
#     vendor_report.total_vendors = Payment.objects.filter(date=date).values('vendor').distinct().count()
#     vendor_report.total_salary = Payment.objects.filter(date=date).aggregate(models.Sum('amount'))['amount__sum'] or 0
#     vendor_report.save()
#     return vendor_report

def generate_vendor_report(date):
    vendor_report, created = VendorReport.objects.get_or_create(date=date)
    vendor_report.total_vendors = Payment.objects.filter(receipt_date=date).values('vendor').distinct().count()
    vendor_report.total_salary = Payment.objects.filter(receipt_date=date).aggregate(models.Sum('amount'))['amount__sum'] or 0
    vendor_report.save()
    return vendor_report