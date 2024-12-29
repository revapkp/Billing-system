# Generated by Django 5.1.4 on 2024-12-28 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_tax_product_tax_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitem',
            name='subtotal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='tax',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
