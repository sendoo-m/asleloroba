# Generated by Django 4.1.3 on 2024-08-13 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_alter_sale_total_amt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='total_purchases',
        ),
        migrations.RemoveField(
            model_name='product',
            name='total_sales',
        ),
    ]
