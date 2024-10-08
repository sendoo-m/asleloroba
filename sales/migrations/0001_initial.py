# Generated by Django 4.1.3 on 2024-08-13 05:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=15)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='customer/')),
                ('date', models.DateField(auto_now_add=True)),
                ('total_customers', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'verbose_name': '02 customer',
                'verbose_name_plural': '02 customers',
            },
        ),
        migrations.CreateModel(
            name='DailyOperationReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('total_income', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total_outcome', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('net_profit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('detail', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='product/')),
                ('total_purchases', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10)),
                ('total_sales', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10)),
                ('total_products', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'verbose_name': '05 Product',
                'verbose_name_plural': '05 Products',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('short_name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': '04 Unit',
                'verbose_name_plural': '04 Units',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('id_number', models.CharField(max_length=10)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='Vendor/')),
                ('phone', models.CharField(max_length=15)),
                ('status', models.BooleanField(default=False)),
                ('total_vendors', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'verbose_name': '01 Vendor',
                'verbose_name_plural': '01 Vendors',
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amt', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('sale_date', models.DateTimeField(auto_now_add=True)),
                ('expire_date', models.DateField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.product')),
            ],
            options={
                'verbose_name': '06 sale',
                'verbose_name_plural': '06 sales',
            },
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_reason', models.CharField(choices=[('Expired', 'Expired'), ('Near to Expire', 'Near to Expire')], max_length=20)),
                ('return_qty', models.DecimalField(decimal_places=2, max_digits=10)),
                ('refund_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('return_date', models.DateTimeField(auto_now_add=True)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.sale')),
            ],
            options={
                'verbose_name': '09 Return',
                'verbose_name_plural': '09 Returns',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amt', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('pur_date', models.DateTimeField(auto_now_add=True)),
                ('expire_date', models.DateField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.product')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.vendor')),
            ],
            options={
                'verbose_name': '03 purchase',
                'verbose_name_plural': '03 purchases',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.unit'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installment_number', models.IntegerField(editable=False)),
                ('paid', models.BooleanField(default=False)),
                ('receipt_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Transfer', 'Transfer'), ('Visa', 'Visa')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.customer')),
                ('vendor', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='sales.vendor')),
            ],
            options={
                'verbose_name': '08 Payment',
                'verbose_name_plural': '08 Payments',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_bal_qty', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('pur_qty', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('sale_qty', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_purchases', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sales.product')),
            ],
            options={
                'verbose_name': 'Inventory',
                'verbose_name_plural': 'Inventories',
            },
        ),
    ]
