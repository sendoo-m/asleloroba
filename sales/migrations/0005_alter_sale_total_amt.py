# Generated by Django 4.1.3 on 2024-08-13 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_alter_sale_expire_date_alter_sale_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='total_amt',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10),
        ),
    ]
