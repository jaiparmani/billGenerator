# Generated by Django 3.0.6 on 2020-06-13 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InvoiceGeneration', '0009_auto_20200613_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salemodel',
            name='invoiceDate',
            field=models.CharField(max_length=10),
        ),
    ]
