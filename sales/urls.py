from django.urls import path
from . import views
from .views import *
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('', views.home, name='home'),
    
    path('register_customer/', views.register_customer, name='register_customer'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('customer/<pk>/update/', views.update_customer, name='update_customer'),
    path('customer/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='delete_customer'),
    path('customer/<pk>/', views.customer_details, name='customer_details'),

    path('register_vendor/', views.register_vendor, name='register_vendor'),
    path('vendor_list/', views.vendor_list, name='vendor_list'),
    path('vendor/<pk>/update/', views.update_vendor, name='update_vendor'),
    path('vendor/<int:vendor_id>/', vendor_details, name='vendor_details'),
    path('vendor/<int:pk>/delete/', views.VendorDeleteView.as_view(), name='delete_vendor'),

    path('sale_list/', views.sale_list, name='sale_list'),
    path('sale/', views.sale, name='sale'),
    path('payment/', views.payment, name='payment'),

    path('inventory_list/', views.inventory_list, name='inventory_list'),

    path('register_return/', register_return, name='register_return'),
    path('returns/', ReturnListView.as_view(), name='return_list'),
    
    path('unit/', views.UnitListView.as_view(), name='unit_list'),
    path('units/create/', views.UnitCreateView.as_view(), name='unit_create'),
    path('units/<int:pk>/update/', views.UnitUpdateView.as_view(), name='unit_update'),
    path('units/<int:pk>/delete/', views.UnitDeleteView.as_view(), name='unit_delete'),

    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    path('purchases/', views.PurchaseListView.as_view(), name='purchase_list'),
    path('purchases/create/', views.PurchaseCreateView.as_view(), name='purchase_create'),
    path('purchases/<int:pk>/update/', views.PurchaseUpdateView.as_view(), name='purchase_update'),
    path('purchases/<int:pk>/delete/', views.PurchaseDeleteView.as_view(), name='purchase_delete'),

    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('payments/create/', views.PaymentCreateView.as_view(), name='payment_create'),
    path('payments/<int:pk>/update/', views.PaymentUpdateView.as_view(), name='payment_update'),
    path('payments/<int:pk>/delete/', views.PaymentDeleteView.as_view(), name='payment_delete'),

    path('customer/account/<int:customer_id>/', views.CustomerAccountView.as_view(), name='customer_account'),
    path('customer/purchase_history/<int:customer_id>/', views.CustomerPurchaseHistoryView.as_view(), name='customer_purchase_history'),
    path('payment/receipt/<int:payment_id>/', views.PaymentReceiptView.as_view(), name='payment_receipt'),

    path('report/customers_employees/', customer_employee_report, name='customer_employee_report'),
    path('report/financial/', financial_report, name='financial_report'),
    path('report/products/', product_report, name='product_report'),    
    path('daily-report/', generate_daily_report, name='daily_report'),
    path('report/', report_view, name='report'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)