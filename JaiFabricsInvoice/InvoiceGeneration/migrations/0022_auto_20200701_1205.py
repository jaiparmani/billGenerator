# Generated by Django 3.0.6 on 2020-07-01 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceGeneration', '0021_auto_20200628_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salemodel',
            name='invoiceDate',
            field=models.DateTimeField(blank=True, max_length=40, null=True),
        ),
    ]